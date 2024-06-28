# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom app command tests"""

import unittest
import os
import json

try:
    from urllib import parse
except ImportError:
    import urlparse as parse
from mock import patch, MagicMock
import requests
import vcr
import sfctl.custom_app as sf_c
from sfctl.tests.mock_server import (find_localhost_free_port, start_mock_server)
from sfctl.custom_exceptions import SFCTLInternalException
from sfctl.tests.helpers import (MOCK_CONFIG, get_mock_endpoint, set_mock_endpoint)


class AppTests(unittest.TestCase):
    """App tests"""

    @classmethod
    def setUpClass(cls):
        """A class method called before tests in an individual class are run"""
        cls.port = find_localhost_free_port()
        cls.old_endpoint = get_mock_endpoint()

        # Start mock server
        start_mock_server(cls.port)

    @classmethod
    def tearDownClass(cls):
        """A class method called after tests in an individual class have run"""

        set_mock_endpoint(cls.old_endpoint)

    def test_app_path_absolute(self):
        """App path returns absolute path always"""
        import tempfile
        import shutil

        test_dir = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(test_dir))

        res = sf_c.validate_app_path(test_dir)
        self.assertEqual(os.path.abspath(res), res)

    def test_app_path_file_error(self):
        """App path raise ValueError on non directory arguments"""
        import tempfile

        (test_fd, test_path) = tempfile.mkstemp()

        def cleanup():
            """Cleanup test files created"""
            os.close(test_fd)
            os.remove(test_path)

        self.addCleanup(cleanup)

        with self.assertRaises(ValueError):
            sf_c.validate_app_path(test_path)

    def test_parse_app_params_none(self):
        """Parse app params returns None with None args"""
        self.assertIs(sf_c.parse_app_params(None), None)

    def test_parse_app_params_empty(self):
        """Parse app params returns empty list with empty args"""
        self.assertEqual(sf_c.parse_app_params(""), [])

    def test_parse_single_app_param(self):
        """Parse app params returns a single parameter successfully"""
        from azure.servicefabric.models import ApplicationParameter

        res = sf_c.parse_app_params({'test': 'test2'})
        self.assertEqual(len(res), 1)
        res = res[0]
        self.assertIsInstance(res, ApplicationParameter)
        self.assertEqual(res.key, 'test')
        self.assertEqual(res.value, 'test2')

    def test_parse_app_metrics_none(self):
        """Parse app metrics returns None with None args"""
        self.assertIs(sf_c.parse_app_metrics(None), None)

    def test_parse_app_metrics_empty(self):
        """Parse app metrics returns empty list with empty args"""
        self.assertEqual(sf_c.parse_app_metrics(''), [])

    def test_parse_app_metrics_single(self):
        """Parse app metrics returns a single metric successfully"""
        from azure.servicefabric.models import ApplicationMetricDescription

        res = sf_c.parse_app_metrics([{'name': 'test',
                                       'maximum_capacity': '3',
                                       'reservation_capacity': '2',
                                       'total_application_capacity': '2'}])

        self.assertEqual(len(res), 1)
        res = res[0]
        self.assertIsInstance(res, ApplicationMetricDescription)
        self.assertEqual(res.name, 'test')
        self.assertEqual(res.maximum_capacity, '3')
        self.assertEqual(res.reservation_capacity, '2')
        self.assertEqual(res.total_application_capacity, '2')

    def test_parse_fileshare_path(self):
        """Parse fileshare path from the image store connection string"""
        test_string = r'file:C:\test_store'
        expected_string = r'C:\test_store'
        self.assertEqual(sf_c.path_from_imagestore_string(test_string),
                         expected_string)

    def test_upload_to_fileshare(self):  # pylint: disable=no-self-use
        """Upload copies files to non-native store correctly with no
        progress"""
        import shutil
        import tempfile

        temp_file = tempfile.NamedTemporaryFile(dir=tempfile.mkdtemp())
        temp_src_dir = os.path.dirname(temp_file.name)
        temp_dst_dir = tempfile.mkdtemp()
        shutil_mock = MagicMock()
        shutil_mock.copyfile.return_value = None
        with patch('sfctl.custom_app.shutil', new=shutil_mock):
            sf_c.upload_to_fileshare(temp_src_dir, temp_dst_dir, False)
            shutil_mock.copyfile.assert_called_once()
        temp_file.close()
        shutil.rmtree(os.path.dirname(temp_file.name))
        shutil.rmtree(temp_dst_dir)


    def test_upload_image_store_timeout_overall(self):  #pylint: disable=invalid-name
        """
        Test to make sure that we end the overall upload process when it times out.

        Things we check for:
        - Where the timeout is not sufficient - too small for one file
            - Should get SFCTLInternalException
            - Manually make sure there is only one outgoing request with the correct timeout
              since it's hard to record the http request from another process.
        """

        # Doing patch here because patching outside of the function does not work
        with patch('sfctl.config.CLIConfig', new=MOCK_CONFIG):

            current_directory = os.path.dirname(os.path.realpath(__file__))
            # 4 files total in sample_nested_folders
            path_to_upload_file = os.path.join(current_directory, 'sample_nested_folders')
            endpoint = 'http://localhost:' + str(self.port)
            set_mock_endpoint(endpoint)

            # Mock server will take 3 seconds to respond to each request, simulating
            # a large file.

            exception_triggered = False
            try:
                timeout = 2
                sf_c.upload(path_to_upload_file, timeout=timeout)
            except SFCTLInternalException as ex:
                self.assertIn(
                    'Upload has timed out. Consider passing a longer timeout duration.',
                    ex.message,
                    msg='Application upload to image store returned the incorrect timeout message')
                exception_triggered = True
            # ConnectionResetError will be returned when the process cuts off, but we expect
            # upload to swallow that and return SFCTLInternalException

            self.assertTrue(exception_triggered, msg='A timeout exception is expected during '
                                                     'application upload timeout test with '
                                                     'response time 2 on the server side. '
                                                     'And timeout 2 overall.')

    def test_upload_image_store_timeout_long(self):  #pylint: disable=too-many-locals,invalid-name
        """Test function upload_to_native_imagestore to check that is it sending each
        file upload with the appropriate timeout. Does not look at overall timeout

        Things we check for:
        - Where the timeout is sufficient to completing the task.
            - Make sure the # of requests is correct -> # of files + # of dirs
            - Make sure that each URL shows a decreasing amount of time left"""

        current_directory = os.path.dirname(os.path.realpath(__file__))
        # 4 files total in sample_nested_folders
        path_to_upload_file = os.path.join(current_directory, 'sample_nested_folders')
        endpoint = 'http://localhost:' + str(self.port)
        basename = os.path.basename(path_to_upload_file)

        generated_file_path = 'native_image_store_upload_test.json'

        with requests.Session() as sesh:
            # Session does not need any security

            # Testing long timeout - expect upload completion

            # In case this file was created and not deleted by a previous test,
            # delete it here
            try:
                os.remove(generated_file_path)
            except OSError:
                # if the file doesn't exist, then there's nothing for us to do here
                pass

            timeout = 65  # upload should complete
            with vcr.use_cassette(generated_file_path, record_mode='all',
                                  serializer='json'), \
                    patch('sfctl.custom_app.get_job_count') as get_job_count_mock:

                try:
                    get_job_count_mock.return_value = 1
                    sf_c.upload_to_native_imagestore(sesh, endpoint, path_to_upload_file, basename,
                                                 show_progress=False, timeout=timeout)
                except:
                    pass
        # Read in the json file to make sure that each file waited ~3 seconds, and not much more
        # or less.

        with open(generated_file_path, 'r') as http_recording_file:
            json_str = http_recording_file.read()
            vcr_recording = json.loads(json_str)

            requests_list = vcr_recording['interactions']
            self.assertEqual(len(requests_list), 8, msg='Application upload test: '
                                                        'An incorrect number of requests '
                                                        'was generated.')

            iteration = 0
            for request in requests_list:
                uri = request['request']['uri']
                parsed_url = parse.urlparse(uri)
                query = parse.parse_qs(parsed_url.query)
                query_timeout = query['timeout']

                # Here 3 is the response time in seconds from the mock server
                # however, the mock server can be a bit slow, taking an extra second from receiving
                # the request to start processing it. Linux does not seem to have this problem.
                # Issue seen on Windows only. If testing on windows, change the 3 seconds to 4.
                self.assertAlmostEqual(int(query_timeout[0]), timeout-iteration*3, delta=2)

                iteration += 1

# SIG # Begin Windows Authenticode signature block
# MIIoLQYJKoZIhvcNAQcCoIIoHjCCKBoCAQExDzANBglghkgBZQMEAgEFADB5Bgor
# BgEEAYI3AgEEoGswaTA0BgorBgEEAYI3AgEeMCYCAwEAAAQQse8BENmB6EqSR2hd
# JGAGggIBAAIBAAIBAAIBAAIBADAxMA0GCWCGSAFlAwQCAQUABCCXOwMtV3nXFWB8
# mikTdk8VS7LTlMdsElwjhNtgoJNLW6CCDXYwggX0MIID3KADAgECAhMzAAADrzBA
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
# /Xmfwb1tbWrJUnMTDXpQzTGCGg0wghoJAgEBMIGVMH4xCzAJBgNVBAYTAlVTMRMw
# EQYDVQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVN
# aWNyb3NvZnQgQ29ycG9yYXRpb24xKDAmBgNVBAMTH01pY3Jvc29mdCBDb2RlIFNp
# Z25pbmcgUENBIDIwMTECEzMAAAOvMEAOTKNNBUEAAAAAA68wDQYJYIZIAWUDBAIB
# BQCgga4wGQYJKoZIhvcNAQkDMQwGCisGAQQBgjcCAQQwHAYKKwYBBAGCNwIBCzEO
# MAwGCisGAQQBgjcCARUwLwYJKoZIhvcNAQkEMSIEIPGMkgQB22bh9ZpN6RXtdfcZ
# M2mq5XuS8psKhdj/vJpSMEIGCisGAQQBgjcCAQwxNDAyoBSAEgBNAGkAYwByAG8A
# cwBvAGYAdKEagBhodHRwOi8vd3d3Lm1pY3Jvc29mdC5jb20wDQYJKoZIhvcNAQEB
# BQAEggEAnlQa+6IGnSybgmKVsGSyCqAHEouBwDY4TBoz3pFcrX+6AN+37gEnKdiU
# G6uyMwL68S25xAZsFCSG29u6q1/UBSRCPzOWboNclXGu5dDy/vlZczTbQ/RgIfjP
# 5UtobI3/OaB9tPmuw6GNU3QRnvWrKmpT2pFwgexI3+o0vMJcYJuMXkYEI5KN15gg
# JKtG84wKVl5yVgWfzWPEgvSzzlnFIk5GO+WW69XbdoQf1lplz2xdzneC6pDZcdgD
# WXc3QzD+/yX8+QgC53SLza0jNwBBKYVGC+4QUi0omsMKfAcDW2qMef6z/YHtVudX
# 8nfndbUHa35AJKPxwCXy6RwJ7sbNgKGCF5cwgheTBgorBgEEAYI3AwMBMYIXgzCC
# F38GCSqGSIb3DQEHAqCCF3AwghdsAgEDMQ8wDQYJYIZIAWUDBAIBBQAwggFSBgsq
# hkiG9w0BCRABBKCCAUEEggE9MIIBOQIBAQYKKwYBBAGEWQoDATAxMA0GCWCGSAFl
# AwQCAQUABCCXMck8/kyvwceZqvJ8tE5yPdDgswsd1iFBvPklvrdLmgIGZmsMWHwV
# GBMyMDI0MDYyMDE1MDAwMi40ODJaMASAAgH0oIHRpIHOMIHLMQswCQYDVQQGEwJV
# UzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwGA1UE
# ChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSUwIwYDVQQLExxNaWNyb3NvZnQgQW1l
# cmljYSBPcGVyYXRpb25zMScwJQYDVQQLEx5uU2hpZWxkIFRTUyBFU046N0YwMC0w
# NUUwLUQ5NDcxJTAjBgNVBAMTHE1pY3Jvc29mdCBUaW1lLVN0YW1wIFNlcnZpY2Wg
# ghHtMIIHIDCCBQigAwIBAgITMwAAAfAqfB1ZO+YfrQABAAAB8DANBgkqhkiG9w0B
# AQsFADB8MQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UE
# BxMHUmVkbW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSYwJAYD
# VQQDEx1NaWNyb3NvZnQgVGltZS1TdGFtcCBQQ0EgMjAxMDAeFw0yMzEyMDYxODQ1
# NTFaFw0yNTAzMDUxODQ1NTFaMIHLMQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2Fz
# aGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENv
# cnBvcmF0aW9uMSUwIwYDVQQLExxNaWNyb3NvZnQgQW1lcmljYSBPcGVyYXRpb25z
# MScwJQYDVQQLEx5uU2hpZWxkIFRTUyBFU046N0YwMC0wNUUwLUQ5NDcxJTAjBgNV
# BAMTHE1pY3Jvc29mdCBUaW1lLVN0YW1wIFNlcnZpY2UwggIiMA0GCSqGSIb3DQEB
# AQUAA4ICDwAwggIKAoICAQC1Hi1Tozh3O0czE8xfRnrymlJNCaGWommPy0eINf+4
# EJr7rf8tSzlgE8Il4Zj48T5fTTOAh6nITRf2lK7+upcnZ/xg0AKoDYpBQOWrL9Ob
# FShylIHfr/DQ4PsRX8GRtInuJsMkwSg63bfB4Q2UikMEP/CtZHi8xW5XtAKp95cs
# 3mvUCMvIAA83Jr/UyADACJXVU4maYisczUz7J111eD1KrG9mQ+ITgnRR/X2xTDMC
# z+io8ZZFHGwEZg+c3vmPp87m4OqOKWyhcqMUupPveO/gQC9Rv4szLNGDaoePeK6I
# U0JqcGjXqxbcEoS/s1hCgPd7Ux6YWeWrUXaxbb+JosgOazUgUGs1aqpnLjz0YKfU
# qn8i5TbmR1dqElR4QA+OZfeVhpTonrM4sE/MlJ1JLpR2FwAIHUeMfotXNQiytYfR
# BUOJHFeJYEflZgVk0Xx/4kZBdzgFQPOWfVd2NozXlC2epGtUjaluA2osOvQHZzGO
# oKTvWUPX99MssGObO0xJHd0DygP/JAVp+bRGJqa2u7AqLm2+tAT26yI5veccDmNZ
# sg3vDh1HcpCJa9QpRW/MD3a+AF2ygV1sRnGVUVG3VODX3BhGT8TMU/GiUy3h7ClX
# OxmZ+weCuIOzCkTDbK5OlAS8qSPpgp+XGlOLEPaM31Mgf6YTppAaeP0ophx345oh
# twIDAQABo4IBSTCCAUUwHQYDVR0OBBYEFNCCsqdXRy/MmjZGVTAvx7YFWpslMB8G
# A1UdIwQYMBaAFJ+nFV0AXmJdg/Tl0mWnG1M1GelyMF8GA1UdHwRYMFYwVKBSoFCG
# Tmh0dHA6Ly93d3cubWljcm9zb2Z0LmNvbS9wa2lvcHMvY3JsL01pY3Jvc29mdCUy
# MFRpbWUtU3RhbXAlMjBQQ0ElMjAyMDEwKDEpLmNybDBsBggrBgEFBQcBAQRgMF4w
# XAYIKwYBBQUHMAKGUGh0dHA6Ly93d3cubWljcm9zb2Z0LmNvbS9wa2lvcHMvY2Vy
# dHMvTWljcm9zb2Z0JTIwVGltZS1TdGFtcCUyMFBDQSUyMDIwMTAoMSkuY3J0MAwG
# A1UdEwEB/wQCMAAwFgYDVR0lAQH/BAwwCgYIKwYBBQUHAwgwDgYDVR0PAQH/BAQD
# AgeAMA0GCSqGSIb3DQEBCwUAA4ICAQA4IvSbnr4jEPgo5W4xj3/+0dCGwsz863QG
# Z2mB9Z4SwtGGLMvwfsRUs3NIlPD/LsWAxdVYHklAzwLTwQ5M+PRdy92DGftyEOGM
# Hfut7Gq8L3RUcvrvr0AL/NNtfEpbAEkCFzseextY5s3hzj3rX2wvoBZm2ythwcLe
# ZmMgHQCmjZp/20fHWJgrjPYjse6RDJtUTlvUsjr+878/t+vrQEIqlmebCeEi+VQV
# xc7wF0LuMTw/gCWdcqHoqL52JotxKzY8jZSQ7ccNHhC4eHGFRpaKeiSQ0GXtlbGI
# bP4kW1O3JzlKjfwG62NCSvfmM1iPD90XYiFm7/8mgR16AmqefDsfjBCWwf3qheIM
# fgZzWqeEz8laFmM8DdkXjuOCQE/2L0TxhrjUtdMkATfXdZjYRlscBDyr8zGMlprF
# C7LcxqCXlhxhtd2CM+mpcTc8RB2D3Eor0UdoP36Q9r4XWCVV/2Kn0AXtvWxvIfyO
# Fm5aLl0eEzkhfv/XmUlBeOCElS7jdddWpBlQjJuHHUHjOVGXlrJT7X4hicF1o23x
# 5U+j7qPKBceryP2/1oxfmHc6uBXlXBKukV/QCZBVAiBMYJhnktakWHpo9uIeSnYT
# 6Qx7wf2RauYHIER8SLRmblMzPOs+JHQzrvh7xStx310LOp+0DaOXs8xjZvhpn+Wu
# Zij5RmZijDCCB3EwggVZoAMCAQICEzMAAAAVxedrngKbSZkAAAAAABUwDQYJKoZI
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
# 6Xu/OHBE0ZDxyKs6ijoIYn/ZcGNTTY3ugm2lBRDBcQZqELQdVTNYs6FwZvKhggNQ
# MIICOAIBATCB+aGB0aSBzjCByzELMAkGA1UEBhMCVVMxEzARBgNVBAgTCldhc2hp
# bmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29mdCBDb3Jw
# b3JhdGlvbjElMCMGA1UECxMcTWljcm9zb2Z0IEFtZXJpY2EgT3BlcmF0aW9uczEn
# MCUGA1UECxMeblNoaWVsZCBUU1MgRVNOOjdGMDAtMDVFMC1EOTQ3MSUwIwYDVQQD
# ExxNaWNyb3NvZnQgVGltZS1TdGFtcCBTZXJ2aWNloiMKAQEwBwYFKw4DAhoDFQDC
# KAZKKv5lsdC2yoMGKYiQy79p/6CBgzCBgKR+MHwxCzAJBgNVBAYTAlVTMRMwEQYD
# VQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVNaWNy
# b3NvZnQgQ29ycG9yYXRpb24xJjAkBgNVBAMTHU1pY3Jvc29mdCBUaW1lLVN0YW1w
# IFBDQSAyMDEwMA0GCSqGSIb3DQEBCwUAAgUA6h4b+jAiGA8yMDI0MDYyMDAzMDk0
# NloYDzIwMjQwNjIxMDMwOTQ2WjB3MD0GCisGAQQBhFkKBAExLzAtMAoCBQDqHhv6
# AgEAMAoCAQACAgSEAgH/MAcCAQACAhM1MAoCBQDqH216AgEAMDYGCisGAQQBhFkK
# BAIxKDAmMAwGCisGAQQBhFkKAwKgCjAIAgEAAgMHoSChCjAIAgEAAgMBhqAwDQYJ
# KoZIhvcNAQELBQADggEBAELnGa0HR7KbllbMe4P0ZJGV6hxx6xF+GN0EIve5pWW8
# NhF/U4vgSXNzX3et9h4sksGRUABEyaGvpzTEMbhzgV3jfrlFepzNlz/EXhlZs64G
# fNtTS54GhRDE5y/vme+21wk51lxzk7QKOPkYj2qxmbMw7Ue0c/8/jmbZv0wFKIqL
# nyHuib0QtowqTgWoKdcSwfKdBkgWKGaycD3bZf24/nV1rL2tHbXQNCs/KmOR0xuL
# Xk++Hf1BuLFNrCz+GChfsiM0ujayALk2UfqqB48RR38w1CD2meI9NbMEA4b3rTwk
# VmTqkYY+Ekf02mW+E8dxIaCubZnvgQWUP4UY8GiyQhwxggQNMIIECQIBATCBkzB8
# MQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVk
# bW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSYwJAYDVQQDEx1N
# aWNyb3NvZnQgVGltZS1TdGFtcCBQQ0EgMjAxMAITMwAAAfAqfB1ZO+YfrQABAAAB
# 8DANBglghkgBZQMEAgEFAKCCAUowGgYJKoZIhvcNAQkDMQ0GCyqGSIb3DQEJEAEE
# MC8GCSqGSIb3DQEJBDEiBCAg7u1ygCNlQLmD8jr7YUBhrzBQnbaLekkncSNwTI/I
# 5TCB+gYLKoZIhvcNAQkQAi8xgeowgecwgeQwgb0EIFwBmqOlcv3kU7mAB5sWR74Q
# FAiS6mb+CM6asnFAZUuLMIGYMIGApH4wfDELMAkGA1UEBhMCVVMxEzARBgNVBAgT
# Cldhc2hpbmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29m
# dCBDb3Jwb3JhdGlvbjEmMCQGA1UEAxMdTWljcm9zb2Z0IFRpbWUtU3RhbXAgUENB
# IDIwMTACEzMAAAHwKnwdWTvmH60AAQAAAfAwIgQgaYxIKx9X24hBOUyL6HtAPARU
# i9NjcuTYVFGYdruEk3EwDQYJKoZIhvcNAQELBQAEggIAMKZA8SaxqClzBf9z29xR
# de2C5xrHjhLNulDX07QlZ3VbiqT4Alb2ATZukOdgvnI+nmMGJrFU9BuXKFc/PJ6t
# ZWfWDtrEV8cMCAVRSe/lKms7yt3G8j8ZuccpWcSTyx7inVVGA86EF9dw4zhQ0h1c
# 5/ln2dQwCL01qHNlnQ3UEpwt3PXb79kA8u2xJuHQQL3V4tpeK/bY/NZp6/Dv7RBB
# uByWNT5CNnqWYQ/x0sKmLGbu8cimlj7zqM5d0oy8RYN7kVKqvcXeOhR0PGxZf15J
# xAdaT/denJAPP7cC5mNyXq5pW/mYKZlxnnQcrpswqEfrNve3baK8u4p/8RUBip1b
# xHC4/wnMmXZEfMn2bx/wrIJkzRLwyk9lfEnMFpnB4XzzaTOYddj0TMaatUUwr4JZ
# WTWL9HRXOeMvc8KlOGqCknEHMWEeYr8XKNVSjg4WIXgX3mvEEusBxnuI4DzMlxNc
# IgvNiUeP5fy+rBLLQIguA/UCPFN4G+3dy5SsZFM16uEBkRjShvYzq2YVXb1PfI8X
# JoYeZoVqNWXpt8ydQnbT6l1pwaoiDV6CA+96+zi0ch1lETZKVdEH1LvZ1965zVnS
# VQ/uR+e/i49wNKJo/YSzmlUvWPYoW5WLXiqA+bBd6nBtj7pFXPf7hioc4Bszyqcs
# W4fttA0TjUr4IPEi5DK6BnY=
# SIG # End Windows Authenticode signature block