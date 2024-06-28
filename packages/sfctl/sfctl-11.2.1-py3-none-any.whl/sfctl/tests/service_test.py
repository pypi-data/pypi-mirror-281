# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom service command tests"""

import unittest
from knack.util import CLIError
import sfctl.custom_service as sf_c


# pylint: disable=invalid-name

class ServiceTests(unittest.TestCase):  # pylint: disable=too-many-public-methods
    """Service tests"""

    def test_parse_none_correlation_desc(self):
        """Parse None correlation description returns None"""
        self.assertIs(sf_c.correlation_desc(None, None), None)

    def test_parse_partial_correlation_desc(self):
        """Parse partial correlation description raises error"""
        with self.assertRaises(CLIError):
            sf_c.correlation_desc('test_svc', None)

    def test_parse_complete_correlation_desc(self):
        """Parse a single correlation description"""
        res = sf_c.correlation_desc('test', 'Affinity')
        self.assertEqual(res.service_name, 'test')
        self.assertEqual(res.scheme, 'Affinity')

    def test_parse_empty_load_metrics(self):
        """Parse empty load metrics returns None"""
        self.assertIsNone(sf_c.parse_load_metrics(''))

    def test_parse_none_load_metrics(self):
        """Parse none load metrics returns None"""
        self.assertIsNone(sf_c.parse_load_metrics(None))

    def test_parse_scaling_policy_test(self):
        """Parse scaling policies"""
        res = sf_c.parse_scaling_policy([{
            'mechanism':{'kind':'PartitionInstanceCount', 'min_instance_count':2, 'max_instance_count':4, 'scale_increment':2}, #pylint: disable=line-too-long
            'trigger':{'kind':'AveragePartitionLoad', 'metric_name':'MetricA', 'upper_load_threshold':20.0, 'lower_load_threshold':10.0, 'scale_interval_in_seconds':1000} #pylint: disable=line-too-long
        }, {
            'mechanism':{'kind':'AddRemoveIncrementalNamedPartition', 'min_partition_count':3, 'max_partition_count':6, 'scale_increment':2}, #pylint: disable=line-too-long
            'trigger':{'kind':'AverageServiceLoad', 'metric_name':'MetricB', 'upper_load_threshold':30.0, 'lower_load_threshold':10.0, 'scale_interval_in_seconds':1000} #pylint: disable=line-too-long
        }])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].scaling_trigger.metric_name, 'MetricA')
        self.assertEqual(res[0].scaling_trigger.upper_load_threshold, 20.0)
        self.assertEqual(res[0].scaling_trigger.lower_load_threshold, 10.0)
        self.assertEqual(res[0].scaling_mechanism.max_instance_count, 4)
        self.assertEqual(res[1].scaling_trigger.scale_interval_in_seconds, 1000)
        self.assertEqual(res[1].scaling_trigger.upper_load_threshold, 30.0)
        self.assertEqual(res[1].scaling_trigger.lower_load_threshold, 10.0)
        self.assertEqual(res[1].scaling_mechanism.scale_increment, 2)

    def test_parse_service_tags(self):
        """Parse service tags"""
        service_tags = ["tagX", "tagY", "tagZ"]
        res = sf_c.parse_service_tags(service_tags)
        self.assertEqual(len(service_tags), res.count)
        self.assertEqual(res.tags[0], service_tags[0])
        self.assertEqual(res.tags[1], service_tags[1])
        self.assertEqual(res.tags[2], service_tags[2])

    def test_parse_incomplete_load_metrics(self):
        """Parse single incomplete load metrics definition"""

        res = sf_c.parse_load_metrics([{'name': 'test_metric',
                                        'default_load': 10}])

        self.assertEqual(len(res), 1)
        res = res[0]
        self.assertEqual(res.name, 'test_metric')
        self.assertIsNone(res.weight)
        self.assertIsNone(res.primary_default_load)
        self.assertIsNone(res.secondary_default_load)
        self.assertEqual(res.default_load, 10)

    def test_parse_invalid_placement_policy_type(self):
        """Parsing invalid placement policy type raises error"""
        with self.assertRaises(CLIError):
            sf_c.parse_placement_policies([{'type': 'test',
                                            'domain_name': 'test'}])

    def test_parse_missing_placement_policy_domain_name(self):
        """Parsing missing domain name in placement policy raises error"""
        with self.assertRaises(CLIError):
            sf_c.parse_placement_policies([{'type': 'PreferPrimaryDomain'}])

    def test_parse_all_placement_policy_types(self):
        """Parse all placement policy types"""

        from azure.servicefabric.models import (ServicePlacementNonPartiallyPlaceServicePolicyDescription,  # pylint: disable=line-too-long
                                                ServicePlacementPreferPrimaryDomainPolicyDescription, # pylint: disable=line-too-long
                                                ServicePlacementRequiredDomainPolicyDescription,  # pylint: disable=line-too-long
                                                ServicePlacementRequireDomainDistributionPolicyDescription)  # pylint: disable=line-too-long

        res = sf_c.parse_placement_policies([{
            'type': 'NonPartiallyPlaceService'
        }, {
            'type': 'PreferPrimaryDomain',
            'domain_name': 'test_1'
        }, {
            'type': 'RequireDomain',
            'domain_name': 'test-22'
        }, {
            'type': 'RequireDomainDistribution',
            'domain_name': 'test_3'
        }])
        self.assertIsInstance(
            res[0],
            ServicePlacementNonPartiallyPlaceServicePolicyDescription
        )
        self.assertIsInstance(
            res[1],
            ServicePlacementPreferPrimaryDomainPolicyDescription
        )
        self.assertEqual(res[1].domain_name, 'test_1')
        self.assertIsInstance(
            res[2],
            ServicePlacementRequiredDomainPolicyDescription
        )
        self.assertEqual(res[2].domain_name, 'test-22')
        self.assertIsInstance(
            res[3],
            ServicePlacementRequireDomainDistributionPolicyDescription
        )
        self.assertEqual(res[3].domain_name, 'test_3')

    def test_invalid_move_cost(self):
        """Invalid move cost raises error"""
        with self.assertRaises(CLIError):
            sf_c.validate_move_cost('test')

    def test_empty_stateful_flags(self):
        """Empty stateful flags returns zero"""
        self.assertEqual(sf_c.stateful_flags(), 0)

    def test_all_stateful_flags(self):
        """All stateful flags sum up to correct value"""
        self.assertEqual(sf_c.stateful_flags(10, 10, 10), 7)

    def test_empty_service_update_flags(self):
        """Empty service update flags returns zero"""
        self.assertEqual(sf_c.service_update_flags(), 0)

    def test_all_service_update_flags(self):
        """All service update flags sum up to correct value"""
        self.assertEqual(sf_c.service_update_flags(target_rep_size=1,
                                                   rep_restart_wait=10,
                                                   quorum_loss_wait=10,
                                                   standby_rep_keep=10,
                                                   min_rep_size=5,
                                                   placement_constraints='',
                                                   placement_policy='',
                                                   correlation='',
                                                   metrics='',
                                                   move_cost='high',
                                                   service_placement_time=10,
                                                   tags_required_to_place=['tagA', 'tagB'],
                                                   tags_required_to_run=['tagX', 'tagY']), 3148799)

    def test_service_create_missing_service_state(self):
        """Service create must specify exactly stateful or stateless"""
        with self.assertRaises(CLIError):
            sf_c.validate_service_create_params(False, False, None, None,
                                                None, None, None, None)
        with self.assertRaises(CLIError):
            sf_c.validate_service_create_params(True, True, None, None, None,
                                                None, None, None)

    def test_service_create_target_size_matches_state(self):
        """Service create target replica set and instance count match
        stateful or stateless"""
        with self.assertRaises(CLIError):
            sf_c.validate_service_create_params(True, False, True, False,
                                                False, 10, None, None)
        with self.assertRaises(CLIError):
            sf_c.validate_service_create_params(False, True, True, False,
                                                False, None, 10, None)

    def test_service_create_missing_stateful_replica_set_sizes(self):
        """Service create without target or min replica set sizes raises
        error"""
        with self.assertRaises(CLIError):
            sf_c.validate_service_create_params(True, False, True, False,
                                                False, None, 10, None)

    def test_parse_incomplete_partition_policy_named_scheme(self):
        """Parsing named partition policy with unspecified names raises
        error"""
        with self.assertRaises(CLIError):
            sf_c.parse_partition_policy(True, None, None, None, None, None,
                                        None)

    def test_parse_incomplete_partition_policy_int(self):
        """Parsing int partition policy with incomplete args raises error"""
        with self.assertRaises(CLIError):
            sf_c.parse_partition_policy(False, None, True, 0, 5, None, False)

    def test_parse_multiple_partition_policy(self):
        """Parsing multiple different partition polices raises error"""
        with self.assertRaises(CLIError):
            sf_c.parse_partition_policy(True, ['test'], True, 0, 5, 3, True)

    def test_parse_valid_partition_policy(self):
        """Parsing valid partition polices returns correct policies"""
        from azure.servicefabric.models import (NamedPartitionSchemeDescription,  # pylint: disable=line-too-long
                                                SingletonPartitionSchemeDescription,  # pylint:disable=line-too-long
                                                UniformInt64RangePartitionSchemeDescription)  # pylint:disable=line-too-long

        res = sf_c.parse_partition_policy(True, ['test'], False, None, None,
                                          None, False)
        self.assertIsInstance(res, NamedPartitionSchemeDescription)
        self.assertEqual(res.count, 1)
        self.assertEqual(res.names, ['test'])

        res = sf_c.parse_partition_policy(False, None, True, 1, 5, 3, False)
        self.assertIsInstance(res, UniformInt64RangePartitionSchemeDescription)
        self.assertEqual(res.high_key, 5)
        self.assertEqual(res.low_key, 1)
        self.assertEqual(res.count, 3)

        res = sf_c.parse_partition_policy(False, None, False, None, None, None,
                                          True)
        self.assertIsInstance(res, SingletonPartitionSchemeDescription)

    def test_activation_mode_invalid(self):
        """Invalid activation mode specified raises error"""
        with self.assertRaises(CLIError):
            sf_c.validate_activation_mode('test')

    def test_activation_mode_none(self):  # pylint: disable=no-self-use
        """None activation mode is considered valid"""
        sf_c.validate_activation_mode(None)

    def test_service_update_specify_state(self):
        """Service update incorrectly specifying service state raises error"""
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(False, False, 10, 0, 10,
                                                10, 10, False, 10)

    def test_service_update_stateful_invalid_params(self):
        """Stateful service update with invalid args raises error"""
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(False, True, 5, 3, 10,
                                                10, 10, 1, 10)

    def test_service_update_stateless_invalid_params(self):
        """Stateless service update with invalid args raises error"""
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(True, False, 5, None, None,
                                                None, None, 10, None)
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(True, False, None, 1, None,
                                                None, None, 10, None)
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(True, False, None, None, 10,
                                                None, None, 10, None)
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(True, False, None, None, None,
                                                10, None, 10, None)
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(True, False, None, None, None,
                                                None, 5, 10, None)
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(True, False, None, None, None,
                                                None, None, 10, 5)

# SIG # Begin Windows Authenticode signature block
# MIIoLQYJKoZIhvcNAQcCoIIoHjCCKBoCAQExDzANBglghkgBZQMEAgEFADB5Bgor
# BgEEAYI3AgEEoGswaTA0BgorBgEEAYI3AgEeMCYCAwEAAAQQse8BENmB6EqSR2hd
# JGAGggIBAAIBAAIBAAIBAAIBADAxMA0GCWCGSAFlAwQCAQUABCAYrvSiI2NNedtN
# 8/tdjOCQ3Fk46eqBKSHcN2Wbpjdu7aCCDXYwggX0MIID3KADAgECAhMzAAADrzBA
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
# MAwGCisGAQQBgjcCARUwLwYJKoZIhvcNAQkEMSIEIEQbf2h2rK5TuxaMlxlxyaWa
# 3Aav1WUdHJ4S9X8/WMXVMEIGCisGAQQBgjcCAQwxNDAyoBSAEgBNAGkAYwByAG8A
# cwBvAGYAdKEagBhodHRwOi8vd3d3Lm1pY3Jvc29mdC5jb20wDQYJKoZIhvcNAQEB
# BQAEggEAoQLxdlvuJAqHVlCdUvNqU6NoZmm5Or8BA9jq/1eZbItqcOuc5JhCNEEc
# 5H7VCz2xMkTedZES0Fravd0gVdZMxaZ/iXyPAykMsYHeq2giK+SF1LoGVXH1eT9P
# 0KmJVykGWHBoCLfvk68s/vE9Db8yo14T0Ad2gyrrx+vTZZsKK17d8mb8Og++mBqH
# 6m9gONEKJn098IIIVZCCNg1V1R6w131b852pPPPpvP+nNdRQmjoX9gB54m0Uxvtj
# LFUWAxWlt5M8sC6T6RzlNJ8SL7jzJnWiZkXGO/DuCrg+ptk+8yEF4tot0+hIsCi7
# kgQpYGfB3SAnzih+qaIPyKeL2HbR/qGCF5cwgheTBgorBgEEAYI3AwMBMYIXgzCC
# F38GCSqGSIb3DQEHAqCCF3AwghdsAgEDMQ8wDQYJYIZIAWUDBAIBBQAwggFSBgsq
# hkiG9w0BCRABBKCCAUEEggE9MIIBOQIBAQYKKwYBBAGEWQoDATAxMA0GCWCGSAFl
# AwQCAQUABCBdehAsXh5DEqo2BbQ9Oh+02Pqe2DprRABuUkTz5vh94QIGZmsMWHvz
# GBMyMDI0MDYyMDE1MDAwMS4zMjlaMASAAgH0oIHRpIHOMIHLMQswCQYDVQQGEwJV
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
# MC8GCSqGSIb3DQEJBDEiBCBQQyALXkcfS1uOnC1PnjfzA1kjvSkYCLSzmIzvDOr/
# IjCB+gYLKoZIhvcNAQkQAi8xgeowgecwgeQwgb0EIFwBmqOlcv3kU7mAB5sWR74Q
# FAiS6mb+CM6asnFAZUuLMIGYMIGApH4wfDELMAkGA1UEBhMCVVMxEzARBgNVBAgT
# Cldhc2hpbmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29m
# dCBDb3Jwb3JhdGlvbjEmMCQGA1UEAxMdTWljcm9zb2Z0IFRpbWUtU3RhbXAgUENB
# IDIwMTACEzMAAAHwKnwdWTvmH60AAQAAAfAwIgQgaYxIKx9X24hBOUyL6HtAPARU
# i9NjcuTYVFGYdruEk3EwDQYJKoZIhvcNAQELBQAEggIAP8P5zxafksrsn4JTPLyO
# 3jjAb6mxYPugNoWidk3Xlc5hPpQMk+2Khv265JCEwo/wh+ODY/mZl8BN/wivnG1P
# 86ev4xHUyrcsr3SdOg5RMl4KzMuBwsPeCeW4WqY7wZiKk+F2qMnWjCbCgTzJSYkV
# Z7p3RsplwqUzMIxAwvTNkiMVf2Uc84udT/NtQhspSInsKwj5EUYuIOnnWyeFk5dJ
# 8P2CziCp3X9TXkqETqk/qQ5rkNNSsDwdJYsxy2Tadds0CcfM00bPssqaBCHvVnB2
# pFEBKCiy6esfW9pjYSykk458vK86Aovp8iKIHeTZHmClVeAOahWNLl4lLtaNZH3/
# gdel1/dtWPQBP/S0dVLUJDPF4qluy04CyTjNYD5uRorOtfcQPaJbmHTqjnRRV80o
# Q1rjq5jSo7gEBbUyDq8WwQtr/TUX1Pm1mXalhJwaf34NAgSwrhraBHjqLDWECbsH
# 1zx/PoB3xI4AxmQf46KtQwDTqoBi+5hG8AwkdaScW2bpf0TGBoS0CMKWYL7M9Wed
# q8kZ+QcBzVLpULraNlYDolciYTejXE61m/ZMQUmKSi6NYGVjlMkZwQmH+2etHcWB
# A1xTjzxJw+Y2s8zxvcCbZyE3uoD7FNmgOtkiqJsbyP1plAfl0HAIcyx0NgdSC4OT
# myVSoENvkrONqqATo08uH1Q=
# SIG # End Windows Authenticode signature block