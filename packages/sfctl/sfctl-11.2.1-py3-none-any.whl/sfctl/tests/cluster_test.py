# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom cluster command tests"""

import unittest
from datetime import datetime
from knack.util import CLIError
from knack.testsdk import ScenarioTest
from mock import patch
import sfctl.custom_cluster as sf_c
from sfctl.tests.helpers import (MOCK_CONFIG, get_mock_endpoint, set_mock_endpoint)
from sfctl.entry import cli
from sfctl.custom_cluster import check_cluster_version, sfctl_cluster_version_matches
from sfctl.custom_exceptions import SFCTLInternalException
from sfctl import state as sfctl_state


class ClusterTests(unittest.TestCase):
    """Cluster tests"""

    def test_select_bad_ca_args(self):
        """Select with CA certs but not client certs returns error"""
        with self.assertRaises(CLIError):
            sf_c.select_arg_verify('http://test.com:190800', None, None, None,
                                   'ca_bundle', False, False)

    def test_select_missing_key_args(self):
        """Select with only cert file but not key returns error"""
        with self.assertRaises(CLIError):
            sf_c.select_arg_verify('http://test.com:190800', 'test.crt', None,
                                   None, None, False, False)

    def test_select_verify_missing_cert(self):
        """Select with no-verify but no cert returns error"""
        with self.assertRaises(CLIError):
            sf_c.select_arg_verify('http://test.com:190800', None, None, None,
                                   None, False, True)

    def test_select_two_cert_args(self):
        """Select with both cert and pem returns error"""
        with self.assertRaises(CLIError):
            sf_c.select_arg_verify('http://test.com:190800', 'test.crt',
                                   'test.key', 'test.pem', None, False, False)

    def test_select_cert_and_aad(self):
        """Select with both cert and aad returns error"""
        with self.assertRaises(CLIError):
            sf_c.select_arg_verify('http://test.com:190800', 'test.crt',
                                   'test.key', None, None, True, False)

    def test_sfctl_cluster_version_matches(self):  # pylint: disable=invalid-name
        """
        Test that the latest version of sfctl has a corresponding service fabric cluster
        version that it matches with.
        """
        current_sfctl_version = sfctl_state.get_sfctl_version()

        # An exception will be raised if the current cluster version doesn't exist in the function
        try:
            self.assertTrue(sfctl_cluster_version_matches('8.0', current_sfctl_version),
                            msg='You are most likely getting this error because we need to '
                                'update the method sfctl_cluster_version_matches in '
                                'custom_cluster so that it works with the '
                                'current version of sfctl, or we need to update this test.')
        except SFCTLInternalException as ex:
            # Give a more test appropriate error message
            self.fail(ex.message + ' You are most likely getting this error because we need to '
                                   'update the method sfctl_cluster_version_matches in '
                                   'custom_cluster so that it works with the '
                                   'current version of sfctl, or we need to update this test.')

    def test_version_check_older_cluster(self):  # pylint: disable=invalid-name
        """
        Test that when hitting an older cluster without a cluster version, the time is updated and
        we mark the cluster check as passed/not done.

        We don't actually hit a live cluster, so we will enter a dummy value of None to the
        function call, which is what the result will be http gateway returns error.
        """

        state_file_path = sfctl_state.get_state_path()

        # empty the file
        open(state_file_path, 'w').close()

        current_utc_time = datetime.utcnow()

        # Check cluster version. This should update the last updated time (in state)
        checks_passed_or_not_done = check_cluster_version(
            False, dummy_cluster_version='NoResult')

        self.assertTrue(checks_passed_or_not_done, 'check_cluster_version should return True '
                                                   'because checks should not be performed, '
                                                   'since we are simulating that we are a newer '
                                                   'sfctl hitting a cluster without the '
                                                   'get cluster version API.')

        self.assertGreater(sfctl_state.get_cluster_version_check_time(), current_utc_time,
                           'check_cluster_version command should have modified the '
                           'last checked time such that the time in state is greater than our '
                           'time.')


    def test_version_check_triggered(self):
        """Test that under the following circumstances, a cluster version & sfctl version
        compatibility check is triggered and verify that the last check time was left
        in a good state after the call:
            - The last check time (in state) doesn't exist yet
            - An error has occurred during function call
            - On connection to a new cluster even
                if time since last check is less than SF_CLI_VERSION_CHECK_INTERVAL
            - The last check time (in state) was greater than
                config.py's SF_CLI_VERSION_CHECK_INTERVAL

        NOTE: this is a unit test only, which relies on the
        custom_cluster.py - check_cluster_version
        function being called with the correct parameters, and being called at all.
        """

        # Start session state with condition last check time does not exist:
        state_file_path = sfctl_state.get_state_path()
        # If anything other than one line with our state exists in the file
        # (2 lines total - one to specify the section)
        # then throw an error. This may happen if sfctl uses the state file for something else.
        # If the state file ends up being used for anything else
        # other than last checked API version time, then modify this test then to remove
        # only that one line.
        with open(state_file_path) as state_file:
            content = state_file.readlines()

        content_trimmed = []
        for line in content:
            if line.strip():
                content_trimmed.append(line)

        self.assertLess(len(content_trimmed), 3,
                        'sfctl state file should not have more than 2 lines. '
                        'Content: ' + str(content_trimmed))

        # empty the file
        open(state_file_path, 'w').close()

        # Create cluster version object.
        cluster_version = 'invalid_version'

        current_utc_time = datetime.utcnow()

        # Check cluster version. This should update the last updated time (in state)
        checks_passed_or_not_done = check_cluster_version(
            False, dummy_cluster_version=cluster_version)

        self.assertFalse(checks_passed_or_not_done, 'check_cluster_version should return False '
                                                    'because checks were performed and the '
                                                    'versions do not match')
        self.assertGreater(sfctl_state.get_cluster_version_check_time(),
                           current_utc_time,
                           'check_cluster_version command should have modified the '
                           'last checked time such that the time in state is greater than our '
                           'time.')

        # Set the last checked time in state to something recent, and set calling on failure
        # to True
        sfctl_state.set_cluster_version_check_time(current_utc_time)

        checks_passed_or_not_done = check_cluster_version(
            on_failure_or_connection=True, dummy_cluster_version=cluster_version)

        self.assertFalse(checks_passed_or_not_done, 'check_cluster_version should return False '
                                                    'because checks were performed and the '
                                                    'versions do not match')
        self.assertGreater(sfctl_state.get_cluster_version_check_time(), current_utc_time,
                           'check_cluster_version command should have modified the '
                           'last checked time such that the time in state is greater than our '
                           'time.')

        # Last check time is in the past (well past SF_CLI_VERSION_CHECK_INTERVAL),
        # so should trigger an update and a check
        utc_time_past = datetime(
            year=current_utc_time.year - 1,
            month=12,
            day=20,
            hour=0,
            minute=0,
            second=0
        )

        sfctl_state.set_cluster_version_check_time(utc_time_past)

        checks_passed_or_not_done = check_cluster_version(
            on_failure_or_connection=False, dummy_cluster_version=cluster_version)

        self.assertFalse(checks_passed_or_not_done, 'check_cluster_version should return False '
                                                    'because checks were performed and the '
                                                    'versions do not match')
        self.assertGreater(sfctl_state.get_cluster_version_check_time(), utc_time_past,
                           'check_cluster_version command should have modified the '
                           'last checked time such that the time in state is greater than our '
                           'time.')

    def test_version_check_not_triggered(self):  # pylint: disable=invalid-name
        """Test that under the following circumstances, a cluster version & sfctl version
        compatibility check is NOT triggered and if the last check time was left in a good state
        after the call:
            - The last check time was less than config.py - SF_CLI_VERSION_CHECK_INTERVAL

        NOTE: this is a unit test only, which relies on the
        custom_cluster.py - check_cluster_version
        function being called with the correct parameters, and being called at all.

        This test assumes SF_CLI_VERSION_CHECK_INTERVAL = 24 hours
        """

        current_utc_time = datetime.utcnow()

        adjusted_hour = current_utc_time.hour
        adjusted_minute = current_utc_time.minute
        adjusted_day = current_utc_time.day
        if adjusted_minute >= 5:
            adjusted_minute = adjusted_minute - 5
        elif adjusted_hour >= 1:
            adjusted_hour = adjusted_hour - 1
        else:
            adjusted_day = adjusted_day- 1
            adjusted_hour = 23

        utc_time_past = datetime(
            year=current_utc_time.year,
            month=current_utc_time.month,
            day=adjusted_day,
            hour=adjusted_hour,
            minute=adjusted_minute
        )

        cluster_version = 'invalid_version'

        # Configure last checked time to current time minus some amount of time less than 24 hours
        # Run check_cluster_version
        # Check that the values in the state file of the last checked time is correct
        # Test may fail if SF_CLI_VERSION_CHECK_INTERVAL value is too low.

        sfctl_state.set_cluster_version_check_time(utc_time_past)
        checks_passed_or_not_done = check_cluster_version(
            on_failure_or_connection=False, dummy_cluster_version=cluster_version)

        self.assertTrue(checks_passed_or_not_done, 'check_cluster_version should return True '
                                                   'because no checks were performed')
        self.assertEqual(utc_time_past, sfctl_state.get_cluster_version_check_time(),
                         'check_cluster_version command should not have modified the '
                         'last checked time values since it should have returned True, having '
                         'done no work.')

        # Configure last checked time to current time
        # Run check_cluster_version
        # Check that the values in the state file of the last checked time is correct

        current_utc_time = datetime.utcnow()
        sfctl_state.set_cluster_version_check_time(current_utc_time)

        checks_passed_or_not_done = check_cluster_version(
            on_failure_or_connection=False, dummy_cluster_version=cluster_version)

        self.assertTrue(checks_passed_or_not_done, 'check_cluster_version should return True '
                                                   'because no checks were performed')
        self.assertEqual(current_utc_time, sfctl_state.get_cluster_version_check_time(),
                         'check_cluster_version command should not have modified the '
                         'last checked time values since it should have returned True, having '
                         'done no work.')


class ClusterScenarioTests(ScenarioTest):
    """Cluster scenario tests"""

    def __init__(self, method_name):
        cli_env = cli()
        super(ClusterScenarioTests, self).__init__(cli_env, method_name)

    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def test_show_cluster(self):
        """Ensure that the correct message is returned when a cluster is set"""
        old_endpoint = get_mock_endpoint()

        set_mock_endpoint('https://testUrl.com')

        self.assertEqual('https://testUrl.com', sf_c.show_connection())

        set_mock_endpoint(str(old_endpoint))

    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def test_show_cluster_no_endpoint(self):
        """Ensure that the correct message is returned when a cluster is not set"""
        old_endpoint = get_mock_endpoint()

        set_mock_endpoint('')

        self.assertEqual(None, sf_c.show_connection())

        set_mock_endpoint(str(old_endpoint))

# SIG # Begin Windows Authenticode signature block
# MIIoKgYJKoZIhvcNAQcCoIIoGzCCKBcCAQExDzANBglghkgBZQMEAgEFADB5Bgor
# BgEEAYI3AgEEoGswaTA0BgorBgEEAYI3AgEeMCYCAwEAAAQQse8BENmB6EqSR2hd
# JGAGggIBAAIBAAIBAAIBAAIBADAxMA0GCWCGSAFlAwQCAQUABCB0dmcBXpg8q8Xu
# lxV6hwNlm4vWETi96eYun7DHJHje8aCCDXYwggX0MIID3KADAgECAhMzAAADrzBA
# DkyjTQVBAAAAAAOvMA0GCSqGSIb3DQEBCwUAMH4xCzAJBgNVBAYTAlVTMRMwEQYD
# VQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVNaWNy
# b3NvZnQgQ29ycG9yYXRpb24xKDAmBgNVBAMTH01pY3Jvc29mdCBDb2RlIFNpZ25p
# bmcgUENBIDIwMTEwHhcNMjMxMTE2MTkwOTAwWhcNMjQxMTE0MTkwOTAwWjB0MQsw
# CQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9u
# ZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMR4wHAYDVQQDExVNaWNy
# b3NvZnQgQ29ycG9yYXRpb24wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIB
# AQDOS8s1ra6f0YGtg0OhEaQa/t3Q+q1MEHhWJhqQVuO5amYXQpy8MDPNoJYk+FWA
# hePP5LxwcSge5aen+f5Q6WNPd6EDxGzotvVpNi5ve0H97S3F7C/axDfKxyNh21MG
# 0W8Sb0vxi/vorcLHOL9i+t2D6yvvDzLlEefUCbQV/zGCBjXGlYJcUj6RAzXyeNAN
# xSpKXAGd7Fh+ocGHPPphcD9LQTOJgG7Y7aYztHqBLJiQQ4eAgZNU4ac6+8LnEGAL
# go1ydC5BJEuJQjYKbNTy959HrKSu7LO3Ws0w8jw6pYdC1IMpdTkk2puTgY2PDNzB
# tLM4evG7FYer3WX+8t1UMYNTAgMBAAGjggFzMIIBbzAfBgNVHSUEGDAWBgorBgEE
# AYI3TAgBBggrBgEFBQcDAzAdBgNVHQ4EFgQURxxxNPIEPGSO8kqz+bgCAQWGXsEw
# RQYDVR0RBD4wPKQ6MDgxHjAcBgNVBAsTFU1pY3Jvc29mdCBDb3Jwb3JhdGlvbjEW
# MBQGA1UEBRMNMjMwMDEyKzUwMTgyNjAfBgNVHSMEGDAWgBRIbmTlUAXTgqoXNzci
# tW2oynUClTBUBgNVHR8ETTBLMEmgR6BFhkNodHRwOi8vd3d3Lm1pY3Jvc29mdC5j
# b20vcGtpb3BzL2NybC9NaWNDb2RTaWdQQ0EyMDExXzIwMTEtMDctMDguY3JsMGEG
# CCsGAQUFBwEBBFUwUzBRBggrBgEFBQcwAoZFaHR0cDovL3d3dy5taWNyb3NvZnQu
# Y29tL3BraW9wcy9jZXJ0cy9NaWNDb2RTaWdQQ0EyMDExXzIwMTEtMDctMDguY3J0
# MAwGA1UdEwEB/wQCMAAwDQYJKoZIhvcNAQELBQADggIBAISxFt/zR2frTFPB45Yd
# mhZpB2nNJoOoi+qlgcTlnO4QwlYN1w/vYwbDy/oFJolD5r6FMJd0RGcgEM8q9TgQ
# 2OC7gQEmhweVJ7yuKJlQBH7P7Pg5RiqgV3cSonJ+OM4kFHbP3gPLiyzssSQdRuPY
# 1mIWoGg9i7Y4ZC8ST7WhpSyc0pns2XsUe1XsIjaUcGu7zd7gg97eCUiLRdVklPmp
# XobH9CEAWakRUGNICYN2AgjhRTC4j3KJfqMkU04R6Toyh4/Toswm1uoDcGr5laYn
# TfcX3u5WnJqJLhuPe8Uj9kGAOcyo0O1mNwDa+LhFEzB6CB32+wfJMumfr6degvLT
# e8x55urQLeTjimBQgS49BSUkhFN7ois3cZyNpnrMca5AZaC7pLI72vuqSsSlLalG
# OcZmPHZGYJqZ0BacN274OZ80Q8B11iNokns9Od348bMb5Z4fihxaBWebl8kWEi2O
# PvQImOAeq3nt7UWJBzJYLAGEpfasaA3ZQgIcEXdD+uwo6ymMzDY6UamFOfYqYWXk
# ntxDGu7ngD2ugKUuccYKJJRiiz+LAUcj90BVcSHRLQop9N8zoALr/1sJuwPrVAtx
# HNEgSW+AKBqIxYWM4Ev32l6agSUAezLMbq5f3d8x9qzT031jMDT+sUAoCw0M5wVt
# CUQcqINPuYjbS1WgJyZIiEkBMIIHejCCBWKgAwIBAgIKYQ6Q0gAAAAAAAzANBgkq
# hkiG9w0BAQsFADCBiDELMAkGA1UEBhMCVVMxEzARBgNVBAgTCldhc2hpbmd0b24x
# EDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29mdCBDb3Jwb3JhdGlv
# bjEyMDAGA1UEAxMpTWljcm9zb2Z0IFJvb3QgQ2VydGlmaWNhdGUgQXV0aG9yaXR5
# IDIwMTEwHhcNMTEwNzA4MjA1OTA5WhcNMjYwNzA4MjEwOTA5WjB+MQswCQYDVQQG
# EwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwG
# A1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSgwJgYDVQQDEx9NaWNyb3NvZnQg
# Q29kZSBTaWduaW5nIFBDQSAyMDExMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIIC
# CgKCAgEAq/D6chAcLq3YbqqCEE00uvK2WCGfQhsqa+laUKq4BjgaBEm6f8MMHt03
# a8YS2AvwOMKZBrDIOdUBFDFC04kNeWSHfpRgJGyvnkmc6Whe0t+bU7IKLMOv2akr
# rnoJr9eWWcpgGgXpZnboMlImEi/nqwhQz7NEt13YxC4Ddato88tt8zpcoRb0Rrrg
# OGSsbmQ1eKagYw8t00CT+OPeBw3VXHmlSSnnDb6gE3e+lD3v++MrWhAfTVYoonpy
# 4BI6t0le2O3tQ5GD2Xuye4Yb2T6xjF3oiU+EGvKhL1nkkDstrjNYxbc+/jLTswM9
# sbKvkjh+0p2ALPVOVpEhNSXDOW5kf1O6nA+tGSOEy/S6A4aN91/w0FK/jJSHvMAh
# dCVfGCi2zCcoOCWYOUo2z3yxkq4cI6epZuxhH2rhKEmdX4jiJV3TIUs+UsS1Vz8k
# A/DRelsv1SPjcF0PUUZ3s/gA4bysAoJf28AVs70b1FVL5zmhD+kjSbwYuER8ReTB
# w3J64HLnJN+/RpnF78IcV9uDjexNSTCnq47f7Fufr/zdsGbiwZeBe+3W7UvnSSmn
# Eyimp31ngOaKYnhfsi+E11ecXL93KCjx7W3DKI8sj0A3T8HhhUSJxAlMxdSlQy90
# lfdu+HggWCwTXWCVmj5PM4TasIgX3p5O9JawvEagbJjS4NaIjAsCAwEAAaOCAe0w
# ggHpMBAGCSsGAQQBgjcVAQQDAgEAMB0GA1UdDgQWBBRIbmTlUAXTgqoXNzcitW2o
# ynUClTAZBgkrBgEEAYI3FAIEDB4KAFMAdQBiAEMAQTALBgNVHQ8EBAMCAYYwDwYD
# VR0TAQH/BAUwAwEB/zAfBgNVHSMEGDAWgBRyLToCMZBDuRQFTuHqp8cx0SOJNDBa
# BgNVHR8EUzBRME+gTaBLhklodHRwOi8vY3JsLm1pY3Jvc29mdC5jb20vcGtpL2Ny
# bC9wcm9kdWN0cy9NaWNSb29DZXJBdXQyMDExXzIwMTFfMDNfMjIuY3JsMF4GCCsG
# AQUFBwEBBFIwUDBOBggrBgEFBQcwAoZCaHR0cDovL3d3dy5taWNyb3NvZnQuY29t
# L3BraS9jZXJ0cy9NaWNSb29DZXJBdXQyMDExXzIwMTFfMDNfMjIuY3J0MIGfBgNV
# HSAEgZcwgZQwgZEGCSsGAQQBgjcuAzCBgzA/BggrBgEFBQcCARYzaHR0cDovL3d3
# dy5taWNyb3NvZnQuY29tL3BraW9wcy9kb2NzL3ByaW1hcnljcHMuaHRtMEAGCCsG
# AQUFBwICMDQeMiAdAEwAZQBnAGEAbABfAHAAbwBsAGkAYwB5AF8AcwB0AGEAdABl
# AG0AZQBuAHQALiAdMA0GCSqGSIb3DQEBCwUAA4ICAQBn8oalmOBUeRou09h0ZyKb
# C5YR4WOSmUKWfdJ5DJDBZV8uLD74w3LRbYP+vj/oCso7v0epo/Np22O/IjWll11l
# hJB9i0ZQVdgMknzSGksc8zxCi1LQsP1r4z4HLimb5j0bpdS1HXeUOeLpZMlEPXh6
# I/MTfaaQdION9MsmAkYqwooQu6SpBQyb7Wj6aC6VoCo/KmtYSWMfCWluWpiW5IP0
# wI/zRive/DvQvTXvbiWu5a8n7dDd8w6vmSiXmE0OPQvyCInWH8MyGOLwxS3OW560
# STkKxgrCxq2u5bLZ2xWIUUVYODJxJxp/sfQn+N4sOiBpmLJZiWhub6e3dMNABQam
# ASooPoI/E01mC8CzTfXhj38cbxV9Rad25UAqZaPDXVJihsMdYzaXht/a8/jyFqGa
# J+HNpZfQ7l1jQeNbB5yHPgZ3BtEGsXUfFL5hYbXw3MYbBL7fQccOKO7eZS/sl/ah
# XJbYANahRr1Z85elCUtIEJmAH9AAKcWxm6U/RXceNcbSoqKfenoi+kiVH6v7RyOA
# 9Z74v2u3S5fi63V4GuzqN5l5GEv/1rMjaHXmr/r8i+sLgOppO6/8MO0ETI7f33Vt
# Y5E90Z1WTk+/gFcioXgRMiF670EKsT/7qMykXcGhiJtXcVZOSEXAQsmbdlsKgEhr
# /Xmfwb1tbWrJUnMTDXpQzTGCGgowghoGAgEBMIGVMH4xCzAJBgNVBAYTAlVTMRMw
# EQYDVQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVN
# aWNyb3NvZnQgQ29ycG9yYXRpb24xKDAmBgNVBAMTH01pY3Jvc29mdCBDb2RlIFNp
# Z25pbmcgUENBIDIwMTECEzMAAAOvMEAOTKNNBUEAAAAAA68wDQYJYIZIAWUDBAIB
# BQCgga4wGQYJKoZIhvcNAQkDMQwGCisGAQQBgjcCAQQwHAYKKwYBBAGCNwIBCzEO
# MAwGCisGAQQBgjcCARUwLwYJKoZIhvcNAQkEMSIEIEKo1kHOadIuYwFMsaD3sfks
# oO/da0ASgjsaiZJUcemJMEIGCisGAQQBgjcCAQwxNDAyoBSAEgBNAGkAYwByAG8A
# cwBvAGYAdKEagBhodHRwOi8vd3d3Lm1pY3Jvc29mdC5jb20wDQYJKoZIhvcNAQEB
# BQAEggEANksp6ml86jt+a1q2Z0K2lVscKmlbtcIkNy6xC1vYZYCx1pl1PoSOSy7v
# nvwh0Vtv0114D+Z7LDcW/vvgHHFivVFdeUtTjiHTaQfvHSoaMnu0SOsfibg7Qwg1
# iUtDZ6+yvFkJFr/kZpnVFeQ1l8IqC8YV3E8M+/J2EFbG4Tnx2d0ooIyar0wwW8s3
# 0HqvvZsAxmQIikwyLmL9hMkp2614uMwejgsviPl+YFYMHUKO4qc+oqp52lVSvmII
# h/IsFeSQqq6om9dHXiPRM0K+lZQQGcqKHcjww6VTqidDbC8PcpJK6GPGjxg2FXd6
# 8tdNVoBlm+DyLSc/UdbMb+Amui67Y6GCF5QwgheQBgorBgEEAYI3AwMBMYIXgDCC
# F3wGCSqGSIb3DQEHAqCCF20wghdpAgEDMQ8wDQYJYIZIAWUDBAIBBQAwggFSBgsq
# hkiG9w0BCRABBKCCAUEEggE9MIIBOQIBAQYKKwYBBAGEWQoDATAxMA0GCWCGSAFl
# AwQCAQUABCAI0Xuh/I0ehzKxlDBdB4v+7QhQVncH/9aWnQhHDWSI8gIGZmrjAXM9
# GBMyMDI0MDYyMDE1MDAwNC4wNzdaMASAAgH0oIHRpIHOMIHLMQswCQYDVQQGEwJV
# UzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwGA1UE
# ChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSUwIwYDVQQLExxNaWNyb3NvZnQgQW1l
# cmljYSBPcGVyYXRpb25zMScwJQYDVQQLEx5uU2hpZWxkIFRTUyBFU046OTIwMC0w
# NUUwLUQ5NDcxJTAjBgNVBAMTHE1pY3Jvc29mdCBUaW1lLVN0YW1wIFNlcnZpY2Wg
# ghHqMIIHIDCCBQigAwIBAgITMwAAAecujy+TC08b6QABAAAB5zANBgkqhkiG9w0B
# AQsFADB8MQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UE
# BxMHUmVkbW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSYwJAYD
# VQQDEx1NaWNyb3NvZnQgVGltZS1TdGFtcCBQQ0EgMjAxMDAeFw0yMzEyMDYxODQ1
# MTlaFw0yNTAzMDUxODQ1MTlaMIHLMQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2Fz
# aGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENv
# cnBvcmF0aW9uMSUwIwYDVQQLExxNaWNyb3NvZnQgQW1lcmljYSBPcGVyYXRpb25z
# MScwJQYDVQQLEx5uU2hpZWxkIFRTUyBFU046OTIwMC0wNUUwLUQ5NDcxJTAjBgNV
# BAMTHE1pY3Jvc29mdCBUaW1lLVN0YW1wIFNlcnZpY2UwggIiMA0GCSqGSIb3DQEB
# AQUAA4ICDwAwggIKAoICAQDCV58v4IuQ659XPM1DtaWMv9/HRUC5kdiEF89YBP6/
# Rn7kjqMkZ5ESemf5Eli4CLtQVSefRpF1j7S5LLKisMWOGRaLcaVbGTfcmI1vMRJ1
# tzMwCNIoCq/vy8WH8QdV1B/Ab5sK+Q9yIvzGw47TfXPE8RlrauwK/e+nWnwMt060
# akEZiJJz1Vh1LhSYKaiP9Z23EZmGETCWigkKbcuAnhvh3yrMa89uBfaeHQZEHGQq
# dskM48EBcWSWdpiSSBiAxyhHUkbknl9PPztB/SUxzRZjUzWHg9bf1mqZ0cIiAWC0
# EjK7ONhlQfKSRHVLKLNPpl3/+UL4Xjc0Yvdqc88gOLUr/84T9/xK5r82ulvRp2A8
# /ar9cG4W7650uKaAxRAmgL4hKgIX5/0aIAsbyqJOa6OIGSF9a+DfXl1LpQPNKR79
# 2scF7tjD5WqwIuifS9YUiHMvRLjjKk0SSCV/mpXC0BoPkk5asfxrrJbCsJePHSOE
# blpJzRmzaP6OMXwRcrb7TXFQOsTkKuqkWvvYIPvVzC68UM+MskLPld1eqdOOMK7S
# bbf2tGSZf3+iOwWQMcWXB9gw5gK3AIYK08WkJJuyzPqfitgubdRCmYr9CVsNOuW+
# wHDYGhciJDF2LkrjkFUjUcXSIJd9f2ssYitZ9CurGV74BQcfrxjvk1L8jvtN7mul
# IwIDAQABo4IBSTCCAUUwHQYDVR0OBBYEFM/+4JiAnzY4dpEf/Zlrh1K73o9YMB8G
# A1UdIwQYMBaAFJ+nFV0AXmJdg/Tl0mWnG1M1GelyMF8GA1UdHwRYMFYwVKBSoFCG
# Tmh0dHA6Ly93d3cubWljcm9zb2Z0LmNvbS9wa2lvcHMvY3JsL01pY3Jvc29mdCUy
# MFRpbWUtU3RhbXAlMjBQQ0ElMjAyMDEwKDEpLmNybDBsBggrBgEFBQcBAQRgMF4w
# XAYIKwYBBQUHMAKGUGh0dHA6Ly93d3cubWljcm9zb2Z0LmNvbS9wa2lvcHMvY2Vy
# dHMvTWljcm9zb2Z0JTIwVGltZS1TdGFtcCUyMFBDQSUyMDIwMTAoMSkuY3J0MAwG
# A1UdEwEB/wQCMAAwFgYDVR0lAQH/BAwwCgYIKwYBBQUHAwgwDgYDVR0PAQH/BAQD
# AgeAMA0GCSqGSIb3DQEBCwUAA4ICAQB0ofDbk+llWi1cC6nsfie5Jtp09o6b6ARC
# pvtDPq2KFP+hi+UNNP7LGciKuckqXCmBTFIhfBeGSxvk6ycokdQr3815pEOaYWTn
# HvQ0+8hKy86r1F4rfBu4oHB5cTy08T4ohrG/OYG/B/gNnz0Ol6v7u/qEjz48zXZ6
# ZlxKGyZwKmKZWaBd2DYEwzKpdLkBxs6A6enWZR0jY+q5FdbV45ghGTKgSr5ECAOn
# LD4njJwfjIq0mRZWwDZQoXtJSaVHSu2lHQL3YHEFikunbUTJfNfBDLL7Gv+sTmRi
# DZky5OAxoLG2gaTfuiFbfpmSfPcgl5COUzfMQnzpKfX6+FkI0QQNvuPpWsDU8sR+
# uni2VmDo7rmqJrom4ihgVNdLaMfNUqvBL5ZiSK1zmaELBJ9a+YOjE5pmSarW5sGb
# n7iVkF2W9JQIOH6tGWLFJS5Hs36zahkoHh8iD963LeGjZqkFusKaUW72yMj/yxTe
# GEDOoIr35kwXxr1Uu+zkur2y+FuNY0oZjppzp95AW1lehP0xaO+oBV1XfvaCur/B
# 5PVAp2xzrosMEUcAwpJpio+VYfIufGj7meXcGQYWA8Umr8K6Auo+Jlj8IeFS6lSv
# KhqQpmdBzAMGqPOQKt1Ow3ZXxehK7vAiim3ZiALlM0K546k0sZrxdZPgpmz7O8w9
# gHLuyZAQezCCB3EwggVZoAMCAQICEzMAAAAVxedrngKbSZkAAAAAABUwDQYJKoZI
# hvcNAQELBQAwgYgxCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpXYXNoaW5ndG9uMRAw
# DgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVNaWNyb3NvZnQgQ29ycG9yYXRpb24x
# MjAwBgNVBAMTKU1pY3Jvc29mdCBSb290IENlcnRpZmljYXRlIEF1dGhvcml0eSAy
# MDEwMB4XDTIxMDkzMDE4MjIyNVoXDTMwMDkzMDE4MzIyNVowfDELMAkGA1UEBhMC
# VVMxEzARBgNVBAgTCldhc2hpbmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNV
# BAoTFU1pY3Jvc29mdCBDb3Jwb3JhdGlvbjEmMCQGA1UEAxMdTWljcm9zb2Z0IFRp
# bWUtU3RhbXAgUENBIDIwMTAwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoIC
# AQDk4aZM57RyIQt5osvXJHm9DtWC0/3unAcH0qlsTnXIyjVX9gF/bErg4r25Phdg
# M/9cT8dm95VTcVrifkpa/rg2Z4VGIwy1jRPPdzLAEBjoYH1qUoNEt6aORmsHFPPF
# dvWGUNzBRMhxXFExN6AKOG6N7dcP2CZTfDlhAnrEqv1yaa8dq6z2Nr41JmTamDu6
# GnszrYBbfowQHJ1S/rboYiXcag/PXfT+jlPP1uyFVk3v3byNpOORj7I5LFGc6XBp
# Dco2LXCOMcg1KL3jtIckw+DJj361VI/c+gVVmG1oO5pGve2krnopN6zL64NF50Zu
# yjLVwIYwXE8s4mKyzbnijYjklqwBSru+cakXW2dg3viSkR4dPf0gz3N9QZpGdc3E
# XzTdEonW/aUgfX782Z5F37ZyL9t9X4C626p+Nuw2TPYrbqgSUei/BQOj0XOmTTd0
# lBw0gg/wEPK3Rxjtp+iZfD9M269ewvPV2HM9Q07BMzlMjgK8QmguEOqEUUbi0b1q
# GFphAXPKZ6Je1yh2AuIzGHLXpyDwwvoSCtdjbwzJNmSLW6CmgyFdXzB0kZSU2LlQ
# +QuJYfM2BjUYhEfb3BvR/bLUHMVr9lxSUV0S2yW6r1AFemzFER1y7435UsSFF5PA
# PBXbGjfHCBUYP3irRbb1Hode2o+eFnJpxq57t7c+auIurQIDAQABo4IB3TCCAdkw
# EgYJKwYBBAGCNxUBBAUCAwEAATAjBgkrBgEEAYI3FQIEFgQUKqdS/mTEmr6CkTxG
# NSnPEP8vBO4wHQYDVR0OBBYEFJ+nFV0AXmJdg/Tl0mWnG1M1GelyMFwGA1UdIARV
# MFMwUQYMKwYBBAGCN0yDfQEBMEEwPwYIKwYBBQUHAgEWM2h0dHA6Ly93d3cubWlj
# cm9zb2Z0LmNvbS9wa2lvcHMvRG9jcy9SZXBvc2l0b3J5Lmh0bTATBgNVHSUEDDAK
# BggrBgEFBQcDCDAZBgkrBgEEAYI3FAIEDB4KAFMAdQBiAEMAQTALBgNVHQ8EBAMC
# AYYwDwYDVR0TAQH/BAUwAwEB/zAfBgNVHSMEGDAWgBTV9lbLj+iiXGJo0T2UkFvX
# zpoYxDBWBgNVHR8ETzBNMEugSaBHhkVodHRwOi8vY3JsLm1pY3Jvc29mdC5jb20v
# cGtpL2NybC9wcm9kdWN0cy9NaWNSb29DZXJBdXRfMjAxMC0wNi0yMy5jcmwwWgYI
# KwYBBQUHAQEETjBMMEoGCCsGAQUFBzAChj5odHRwOi8vd3d3Lm1pY3Jvc29mdC5j
# b20vcGtpL2NlcnRzL01pY1Jvb0NlckF1dF8yMDEwLTA2LTIzLmNydDANBgkqhkiG
# 9w0BAQsFAAOCAgEAnVV9/Cqt4SwfZwExJFvhnnJL/Klv6lwUtj5OR2R4sQaTlz0x
# M7U518JxNj/aZGx80HU5bbsPMeTCj/ts0aGUGCLu6WZnOlNN3Zi6th542DYunKmC
# VgADsAW+iehp4LoJ7nvfam++Kctu2D9IdQHZGN5tggz1bSNU5HhTdSRXud2f8449
# xvNo32X2pFaq95W2KFUn0CS9QKC/GbYSEhFdPSfgQJY4rPf5KYnDvBewVIVCs/wM
# nosZiefwC2qBwoEZQhlSdYo2wh3DYXMuLGt7bj8sCXgU6ZGyqVvfSaN0DLzskYDS
# PeZKPmY7T7uG+jIa2Zb0j/aRAfbOxnT99kxybxCrdTDFNLB62FD+CljdQDzHVG2d
# Y3RILLFORy3BFARxv2T5JL5zbcqOCb2zAVdJVGTZc9d/HltEAY5aGZFrDZ+kKNxn
# GSgkujhLmm77IVRrakURR6nxt67I6IleT53S0Ex2tVdUCbFpAUR+fKFhbHP+Crvs
# QWY9af3LwUFJfn6Tvsv4O+S3Fb+0zj6lMVGEvL8CwYKiexcdFYmNcP7ntdAoGokL
# jzbaukz5m/8K6TT4JDVnK+ANuOaMmdbhIurwJ0I9JZTmdHRbatGePu1+oDEzfbzL
# 6Xu/OHBE0ZDxyKs6ijoIYn/ZcGNTTY3ugm2lBRDBcQZqELQdVTNYs6FwZvKhggNN
# MIICNQIBATCB+aGB0aSBzjCByzELMAkGA1UEBhMCVVMxEzARBgNVBAgTCldhc2hp
# bmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29mdCBDb3Jw
# b3JhdGlvbjElMCMGA1UECxMcTWljcm9zb2Z0IEFtZXJpY2EgT3BlcmF0aW9uczEn
# MCUGA1UECxMeblNoaWVsZCBUU1MgRVNOOjkyMDAtMDVFMC1EOTQ3MSUwIwYDVQQD
# ExxNaWNyb3NvZnQgVGltZS1TdGFtcCBTZXJ2aWNloiMKAQEwBwYFKw4DAhoDFQCz
# cgTnGasSwe/dru+cPe1NF/vwQ6CBgzCBgKR+MHwxCzAJBgNVBAYTAlVTMRMwEQYD
# VQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVNaWNy
# b3NvZnQgQ29ycG9yYXRpb24xJjAkBgNVBAMTHU1pY3Jvc29mdCBUaW1lLVN0YW1w
# IFBDQSAyMDEwMA0GCSqGSIb3DQEBCwUAAgUA6h6bYDAiGA8yMDI0MDYyMDEyMTMy
# MFoYDzIwMjQwNjIxMTIxMzIwWjB0MDoGCisGAQQBhFkKBAExLDAqMAoCBQDqHptg
# AgEAMAcCAQACAgXbMAcCAQACAhMjMAoCBQDqH+zgAgEAMDYGCisGAQQBhFkKBAIx
# KDAmMAwGCisGAQQBhFkKAwKgCjAIAgEAAgMHoSChCjAIAgEAAgMBhqAwDQYJKoZI
# hvcNAQELBQADggEBAB3f3oKg5c6evIOqKt4To9T5kmXka4no5Xcw27V1LX7Q+vfk
# SssPJ75eA7xT4PLDGcp7GicdAZ7vgUvZeI/OiJgCNlTVHW5DCFMQvoU+Pgp0USlK
# 30hVXoK451cpFv48q/UoXn1Q28L+6XX9+fBQl1dI95vg/vgEjjE3Cxh0teBVPwMo
# qlRbTRaFM+9zx8bVb3rHWrY+DWpchax2AP6jNeN/BrQadcKRUp5LLaX+F8ZAMNNF
# TuyT+YKgYYpG9p9hDENozXxtYr1J3LLxS7AzdyX1Eg8OoQ7cSuBr1rFMva/FaX3r
# Vpuz6Rj72/5vyXypMBFBH9YpSJRYkYex+h3nINsxggQNMIIECQIBATCBkzB8MQsw
# CQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9u
# ZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSYwJAYDVQQDEx1NaWNy
# b3NvZnQgVGltZS1TdGFtcCBQQ0EgMjAxMAITMwAAAecujy+TC08b6QABAAAB5zAN
# BglghkgBZQMEAgEFAKCCAUowGgYJKoZIhvcNAQkDMQ0GCyqGSIb3DQEJEAEEMC8G
# CSqGSIb3DQEJBDEiBCCb1caOu95eOPzqoFkAyC9AUgAzsCxeAw57VldAG5QBVTCB
# +gYLKoZIhvcNAQkQAi8xgeowgecwgeQwgb0EIOU2XQ12aob9DeDFXM9UFHeEX74F
# v0ABvQMG7qC51nOtMIGYMIGApH4wfDELMAkGA1UEBhMCVVMxEzARBgNVBAgTCldh
# c2hpbmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29mdCBD
# b3Jwb3JhdGlvbjEmMCQGA1UEAxMdTWljcm9zb2Z0IFRpbWUtU3RhbXAgUENBIDIw
# MTACEzMAAAHnLo8vkwtPG+kAAQAAAecwIgQgN1+uKqI05LQtKK15mqEJMf9oQCBH
# 0T8zLp5xlfLGOocwDQYJKoZIhvcNAQELBQAEggIAXiTmkN+6WMZbgNOYT9WACXgm
# RmlbGbxJ3zrMlTjeZZJdXl25ca7r48RI13e401o/uS2ksODwrtm49wj30pnWmQJ5
# 72jtUybMjsshCLDSAbXMndz5aaFgkOQnFBMTYsZyEKqtG+9x+0rUh66HmNpgscm3
# 6saAXQgeKgQ2osibzFifCvy2W9MtBMzTeEc5soXpOIS1qtw9I83ST6G6Dhc+fiAr
# wDhjB/kjHVRjgFBaUpKtLD+tSlwfbNCkJ0j9zWmQTMvq2oVghROktSp8rq6tqO2k
# KRW1wLUqPrV16BDcltC7J55FW9g9qsLrIBmLIHaRIDp7Za9BrfybrISe1oevdRG2
# P+rZ0OtrhH8HOoDr/uVEolwrZa1hg7mLfzxuruWe/s+MoVWqFGIw4zY+x3WC0m1K
# KwgwKptmWNfbxPb9f5PT2lBA9WTHeF5+eKu9odiEC3yNO56Ong509Vs9Nb5IzX2D
# 8iUtNhdYt09JkIOy/LftY13lFn+32Y/ZP1jKUe7oQzLu481Gt2rGCHH63BwstNRI
# 0Wpt2F0DGsmYGnHGo+ZyLB/abufOvBBCD96PFRfQ4nQo2I3zE2KO53CNYJ+P06Oe
# 90JI2MVrDSEJ42v12PaULc+CzL9uiH/puQfGbkcZ6dtDM8rzNtZTOXXiHOLZcQTr
# ot2RD4Xb1shw2NHZ6tc=
# SIG # End Windows Authenticode signature block