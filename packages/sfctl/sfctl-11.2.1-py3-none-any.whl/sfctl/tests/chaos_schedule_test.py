# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom chaos schedule command related tests"""
import unittest
import sfctl.custom_chaos_schedule as sf_c

#pylint: disable=invalid-name,line-too-long

class ChaosScheduleTests(unittest.TestCase):
    """Chaos Schedule tests"""

    def test_parse_none_time_of_day(self):
        """Parsing None TimeOfDay should return None"""

        res = sf_c.parse_time_of_day(None)
        self.assertIs(res, None)

    def test_parse_valid_time_of_day(self):
        """Parse a valid TimeOfDay"""
        from azure.servicefabric.models import TimeOfDay

        res = sf_c.parse_time_of_day({
            'Hour': 23,
            'Minute': 59
        })

        self.assertIsInstance(res, TimeOfDay)

        self.assertEqual(res.hour, 23)
        self.assertEqual(res.minute, 59)

        res2 = sf_c.parse_time_of_day({
            'Hour': 0,
            'Minute': 0
        })

        self.assertIsInstance(res2, TimeOfDay)

        self.assertEqual(res2.hour, 0)
        self.assertEqual(res2.minute, 0)

    def test_parse_none_time_range(self):
        """Parsing None TimeRange should return None"""

        res = sf_c.parse_time_range(None)
        self.assertIs(res, None)

    def test_parse_valid_time_range(self):
        """Parse a valid time range"""
        from azure.servicefabric.models import TimeRange, TimeOfDay

        res = sf_c.parse_time_range({
            'StartTime': {
                'Hour': 0,
                'Minute': 0
            },
            'EndTime': {
                'Hour': 23,
                'Minute': 59,
            }
        })

        self.assertIsInstance(res, TimeRange)

        self.assertIsInstance(res.start_time, TimeOfDay)
        self.assertEqual(res.start_time.hour, 0)
        self.assertEqual(res.start_time.minute, 0)

        self.assertIsInstance(res.end_time, TimeOfDay)
        self.assertEqual(res.end_time.hour, 23)
        self.assertEqual(res.end_time.minute, 59)

    def test_parse_none_active_time_ranges(self):
        """Parsing None ActiveTimeRanges should return an empty list"""

        res = sf_c.parse_active_time_ranges(None)

        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 0)

    def test_parse_valid_active_time_ranges(self):
        """Parse a list of valid time ranges"""
        from azure.servicefabric.models import TimeRange, TimeOfDay

        res = sf_c.parse_active_time_ranges(
            [
                {
                    'StartTime': {
                        'Hour': 0,
                        'Minute': 0
                    },
                    'EndTime': {
                        'Hour': 12,
                        'Minute': 0,
                    }
                },
                {
                    'StartTime': {
                        'Hour': 12,
                        'Minute': 0
                    },
                    'EndTime': {
                        'Hour': 23,
                        'Minute': 59,
                    }
                }
            ]
        )

        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 2)

        self.assertIsInstance(res[0], TimeRange)
        self.assertIsInstance(res[0].start_time, TimeOfDay)
        self.assertEqual(res[0].start_time.hour, 0)
        self.assertEqual(res[0].start_time.minute, 0)

        self.assertIsInstance(res[0].end_time, TimeOfDay)
        self.assertEqual(res[0].end_time.hour, 12)
        self.assertEqual(res[0].end_time.minute, 0)

        self.assertIsInstance(res[1], TimeRange)
        self.assertIsInstance(res[1].start_time, TimeOfDay)
        self.assertEqual(res[1].start_time.hour, 12)
        self.assertEqual(res[1].start_time.minute, 0)

        self.assertIsInstance(res[1].end_time, TimeOfDay)
        self.assertEqual(res[1].end_time.hour, 23)
        self.assertEqual(res[1].end_time.minute, 59)

    def test_parse_none_active_days(self):
        """Parsing None ChaosScheduleActiveDays should return None"""

        res = sf_c.parse_active_days(None)
        self.assertIs(res, None)

    def test_parse_valid_active_days(self):
        """Parse a valid active days"""
        from azure.servicefabric.models import ChaosScheduleJobActiveDaysOfWeek

        res = sf_c.parse_active_days({
            'Monday': True,
            'Tuesday': True,
            'Wednesday': True,
            'Thursday': True,
            'Friday': True
        })

        self.assertIsInstance(res, ChaosScheduleJobActiveDaysOfWeek)
        self.assertEqual(res.sunday, False)
        self.assertEqual(res.monday, True)
        self.assertEqual(res.tuesday, True)
        self.assertEqual(res.wednesday, True)
        self.assertEqual(res.thursday, True)
        self.assertEqual(res.friday, True)
        self.assertEqual(res.saturday, False)

    def test_parse_none_job(self):
        """Parsing None ChaosScheduleJob should return None"""

        res = sf_c.parse_job(None)
        self.assertIs(res, None)

    def test_parse_valid_job(self):
        """Parse a valid ChaosScheduleJob"""
        from azure.servicefabric.models import (TimeRange,
                                                ChaosScheduleJob,
                                                TimeOfDay,
                                                ChaosScheduleJobActiveDaysOfWeek)

        res = sf_c.parse_job({
            'ChaosParameters': 'myParametersName',
            'Days': {
                'Monday': True,
                'Tuesday': True,
                'Wednesday': True,
                'Thursday': True,
                'Friday': True
            },
            'Times': [
                {
                    'StartTime': {
                        'Hour': 0,
                        'Minute': 0
                    },
                    'EndTime': {
                        'Hour': 6,
                        'Minute': 0,
                    }
                },
                {
                    'StartTime': {
                        'Hour': 18,
                        'Minute': 0
                    },
                    'EndTime': {
                        'Hour': 23,
                        'Minute': 59,
                    }
                }
            ]
        })

        self.assertIsInstance(res, ChaosScheduleJob)

        self.assertEqual(res.chaos_parameters, 'myParametersName')

        self.assertIsInstance(res.days, ChaosScheduleJobActiveDaysOfWeek)
        self.assertEqual(res.days.sunday, False)
        self.assertEqual(res.days.monday, True)
        self.assertEqual(res.days.tuesday, True)
        self.assertEqual(res.days.wednesday, True)
        self.assertEqual(res.days.thursday, True)
        self.assertEqual(res.days.friday, True)
        self.assertEqual(res.days.saturday, False)

        self.assertIsInstance(res.times, list)
        self.assertEqual(len(res.times), 2)

        self.assertIsInstance(res.times[0], TimeRange)
        self.assertIsInstance(res.times[0].start_time, TimeOfDay)
        self.assertEqual(res.times[0].start_time.hour, 0)
        self.assertEqual(res.times[0].start_time.minute, 0)
        self.assertIsInstance(res.times[0].end_time, TimeOfDay)
        self.assertEqual(res.times[0].end_time.hour, 6)
        self.assertEqual(res.times[0].end_time.minute, 0)

        self.assertIsInstance(res.times[1], TimeRange)
        self.assertIsInstance(res.times[1].start_time, TimeOfDay)
        self.assertEqual(res.times[1].start_time.hour, 18)
        self.assertEqual(res.times[1].start_time.minute, 0)
        self.assertIsInstance(res.times[1].end_time, TimeOfDay)
        self.assertEqual(res.times[1].end_time.hour, 23)
        self.assertEqual(res.times[1].end_time.minute, 59)

    def test_parse_none_jobs(self):
        """Parsing None ChaosScheduleJobs should return an empty list"""

        res = sf_c.parse_jobs(None)
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 0)

    def test_parse_valid_jobs(self):
        #pylint: disable=too-many-statements
        """Parse a valid list of ChaosScheduleJobs"""
        from azure.servicefabric.models import (TimeRange,
                                                ChaosScheduleJobActiveDaysOfWeek,
                                                TimeOfDay,
                                                ChaosScheduleJob)


        res = sf_c.parse_jobs([
            {
                'ChaosParameters': 'myParametersName',
                'Days': {
                    'Monday': True,
                    'Tuesday': True,
                    'Wednesday': True,
                    'Thursday': True,
                    'Friday': True
                },
                'Times': [
                    {
                        'StartTime': {
                            'Hour': 0,
                            'Minute': 0
                        },
                        'EndTime': {
                            'Hour': 6,
                            'Minute': 0,
                        }
                    },
                    {
                        'StartTime': {
                            'Hour': 18,
                            'Minute': 0
                        },
                        'EndTime': {
                            'Hour': 23,
                            'Minute': 59,
                        }
                    }
                ]
            },
            {
                'ChaosParameters': 'myOtherParametersName',
                'Days': {
                    'Sunday': True,
                    'Saturday': True,
                },
                'Times': [
                    {
                        'StartTime': {
                            'Hour': 12,
                            'Minute': 0
                        },
                        'EndTime': {
                            'Hour': 14,
                            'Minute': 0,
                        }
                    }
                ]
            }
        ])

        self.assertIsInstance(res, list)

        self.assertIsInstance(res[0], ChaosScheduleJob)
        self.assertEqual(res[0].chaos_parameters, 'myParametersName')

        self.assertIsInstance(res[0].days, ChaosScheduleJobActiveDaysOfWeek)
        self.assertEqual(res[0].days.sunday, False)
        self.assertEqual(res[0].days.monday, True)
        self.assertEqual(res[0].days.tuesday, True)
        self.assertEqual(res[0].days.wednesday, True)
        self.assertEqual(res[0].days.thursday, True)
        self.assertEqual(res[0].days.friday, True)
        self.assertEqual(res[0].days.saturday, False)

        self.assertIsInstance(res[0].times, list)
        self.assertEqual(len(res[0].times), 2)

        self.assertIsInstance(res[0].times[0], TimeRange)
        self.assertIsInstance(res[0].times[0].start_time, TimeOfDay)
        self.assertEqual(res[0].times[0].start_time.hour, 0)
        self.assertEqual(res[0].times[0].start_time.minute, 0)
        self.assertIsInstance(res[0].times[0].end_time, TimeOfDay)
        self.assertEqual(res[0].times[0].end_time.hour, 6)
        self.assertEqual(res[0].times[0].end_time.minute, 0)

        self.assertIsInstance(res[0].times[1], TimeRange)
        self.assertIsInstance(res[0].times[1].start_time, TimeOfDay)
        self.assertEqual(res[0].times[1].start_time.hour, 18)
        self.assertEqual(res[0].times[1].start_time.minute, 0)
        self.assertIsInstance(res[0].times[1].end_time, TimeOfDay)
        self.assertEqual(res[0].times[1].end_time.hour, 23)
        self.assertEqual(res[0].times[1].end_time.minute, 59)

        self.assertIsInstance(res[1], ChaosScheduleJob)
        self.assertEqual(res[1].chaos_parameters, 'myOtherParametersName')

        self.assertIsInstance(res[1].days, ChaosScheduleJobActiveDaysOfWeek)
        self.assertEqual(res[1].days.sunday, True)
        self.assertEqual(res[1].days.monday, False)
        self.assertEqual(res[1].days.tuesday, False)
        self.assertEqual(res[1].days.wednesday, False)
        self.assertEqual(res[1].days.thursday, False)
        self.assertEqual(res[1].days.friday, False)
        self.assertEqual(res[1].days.saturday, True)

        self.assertIsInstance(res[1].times, list)
        self.assertEqual(len(res[1].times), 1)

        self.assertIsInstance(res[1].times[0], TimeRange)
        self.assertIsInstance(res[1].times[0].start_time, TimeOfDay)
        self.assertEqual(res[1].times[0].start_time.hour, 12)
        self.assertEqual(res[1].times[0].start_time.minute, 0)
        self.assertIsInstance(res[1].times[0].end_time, TimeOfDay)
        self.assertEqual(res[1].times[0].end_time.hour, 14)
        self.assertEqual(res[1].times[0].end_time.minute, 0)

    def test_parse_none_chaos_parameters_dictionary(self):
        """Parsing None parameters dictionary should return an empty list"""

        res = sf_c.parse_chaos_params_dictionary(None)

        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 0)

    def test_parse_valid_chaos_parameters_dictionary(self):
        #pylint: disable=too-many-statements
        """Parse a valid ChaosParametersDictionary"""
        from azure.servicefabric.models import (ChaosParametersDictionaryItem,
                                                ChaosParameters,
                                                ClusterHealthPolicy,
                                                ChaosTargetFilter,
                                                ChaosContext)

        res = sf_c.parse_chaos_params_dictionary([
            {
                'Key': 'myParametersName',
                'Value':  {
                    'MaxConcurrentFaults': 1,
                    'TimeToRunInSeconds': '600',
                    'MaxClusterStabilizationTimeoutInSeconds': 60,
                    'WaitTimeBetweenIterationsInSeconds': 15,
                    'WaitTimeBetweenFaultsInSeconds': 30,
                    'EnableMoveReplicaFaults': True,
                    'ClusterHealthPolicy': {
                        'MaxPercentUnhealthyNodes': 0,
                        'ConsiderWarningAsError': True,
                        'MaxPercentUnhealthyApplications': 0
                    },
                    'Context': {
                        'Map': {
                            'myContextKey': 'myContextValue'
                        }
                    },
                    'ChaosTargetFilter': {
                        'NodeTypeInclusionList': [
                            'N0010Ref',
                            'N0020Ref'
                        ]
                    }

                }
            },
            {
                'Key': 'myOtherParametersName',
                'Value': {
                    'MaxConcurrentFaults': 4,
                    'TimeToRunInSeconds': '300',
                    'MaxClusterStabilizationTimeoutInSeconds': 20,
                    'WaitTimeBetweenIterationsInSeconds': 10,
                    'WaitTimeBetweenFaultsInSeconds': 50,
                    'EnableMoveReplicaFaults': False,
                    'ClusterHealthPolicy': {
                        'MaxPercentUnhealthyNodes': 2,
                        'ConsiderWarningAsError': False,
                        'MaxPercentUnhealthyApplications': 5
                    },
                    'Context': {
                        'Map': {
                            'myOtherContextKey': 'myOtherContextValue'
                        }
                    },
                    'ChaosTargetFilter': {
                        'NodeTypeInclusionList': [
                            'N0030Ref',
                            'N0040Ref'
                        ]
                    }

                }
            }
        ])

        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 2)

        self.assertIsInstance(res[0], ChaosParametersDictionaryItem)
        self.assertEqual(res[0].key, 'myParametersName')
        self.assertIsInstance(res[0].value, ChaosParameters)
        self.assertEqual(res[0].value.time_to_run_in_seconds, '600')
        self.assertEqual(
            res[0].value.max_cluster_stabilization_timeout_in_seconds, 60)
        self.assertEqual(res[0].value.max_concurrent_faults, 1)
        self.assertEqual(res[0].value.enable_move_replica_faults, True)
        self.assertEqual(res[0].value.wait_time_between_faults_in_seconds, 30)
        self.assertEqual(
            res[0].value.wait_time_between_iterations_in_seconds, 15)

        cluster_health_policy = res[0].value.cluster_health_policy
        self.assertIsInstance(cluster_health_policy, ClusterHealthPolicy)
        self.assertEqual(cluster_health_policy.max_percent_unhealthy_nodes, 0)
        self.assertEqual(cluster_health_policy.consider_warning_as_error, True)
        self.assertEqual(
            cluster_health_policy.max_percent_unhealthy_applications, 0)

        self.assertIsInstance(res[0].value.context, ChaosContext)
        self.assertIsInstance(res[0].value.context.map, dict)
        self.assertEqual(
            res[0].value.context.map['myContextKey'], 'myContextValue')

        chaos_target_filter = res[0].value.chaos_target_filter
        self.assertIsInstance(chaos_target_filter, ChaosTargetFilter)
        self.assertIsInstance(
            chaos_target_filter.node_type_inclusion_list, list)
        self.assertEqual(len(chaos_target_filter.node_type_inclusion_list), 2)
        self.assertEqual(
            chaos_target_filter.node_type_inclusion_list[0], 'N0010Ref')
        self.assertEqual(
            chaos_target_filter.node_type_inclusion_list[1], 'N0020Ref')

        self.assertIsInstance(res[1], ChaosParametersDictionaryItem)
        self.assertEqual(res[1].key, 'myOtherParametersName')
        self.assertIsInstance(res[1].value, ChaosParameters)
        self.assertEqual(res[1].value.time_to_run_in_seconds, '300')
        self.assertEqual(
            res[1].value.max_cluster_stabilization_timeout_in_seconds, 20)
        self.assertEqual(res[1].value.max_concurrent_faults, 4)
        self.assertEqual(res[1].value.enable_move_replica_faults, False)
        self.assertEqual(res[1].value.wait_time_between_faults_in_seconds, 50)
        self.assertEqual(
            res[1].value.wait_time_between_iterations_in_seconds, 10)

        cluster_health_policy2 = res[1].value.cluster_health_policy
        self.assertIsInstance(cluster_health_policy2, ClusterHealthPolicy)
        self.assertEqual(cluster_health_policy2.max_percent_unhealthy_nodes, 2)
        self.assertEqual(
            cluster_health_policy2.consider_warning_as_error, False)
        self.assertEqual(
            cluster_health_policy2.max_percent_unhealthy_applications, 5)

        self.assertIsInstance(res[1].value.context, ChaosContext)
        self.assertIsInstance(res[1].value.context.map, dict)
        self.assertEqual(
            res[1].value.context.map['myOtherContextKey'],
            'myOtherContextValue')

        chaos_target_filter2 = res[1].value.chaos_target_filter
        self.assertIsInstance(chaos_target_filter2, ChaosTargetFilter)
        self.assertIsInstance(
            chaos_target_filter2.node_type_inclusion_list, list)
        self.assertEqual(
            len(chaos_target_filter2.node_type_inclusion_list), 2)
        self.assertEqual(
            chaos_target_filter2.node_type_inclusion_list[0],
            'N0030Ref')
        self.assertEqual(
            chaos_target_filter2.node_type_inclusion_list[1],
            'N0040Ref')

# SIG # Begin Windows Authenticode signature block
# MIIoLQYJKoZIhvcNAQcCoIIoHjCCKBoCAQExDzANBglghkgBZQMEAgEFADB5Bgor
# BgEEAYI3AgEEoGswaTA0BgorBgEEAYI3AgEeMCYCAwEAAAQQse8BENmB6EqSR2hd
# JGAGggIBAAIBAAIBAAIBAAIBADAxMA0GCWCGSAFlAwQCAQUABCBCzXuATpGdaaLV
# efyhzi/HkH8d3+yJ2oColdzHKcEZ76CCDXYwggX0MIID3KADAgECAhMzAAADrzBA
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
# MAwGCisGAQQBgjcCARUwLwYJKoZIhvcNAQkEMSIEIAWL86V0DHBaqmX/+06UNfTE
# 8kEgprHyKhhA1m41zRZeMEIGCisGAQQBgjcCAQwxNDAyoBSAEgBNAGkAYwByAG8A
# cwBvAGYAdKEagBhodHRwOi8vd3d3Lm1pY3Jvc29mdC5jb20wDQYJKoZIhvcNAQEB
# BQAEggEAdyNjO5OBLhNNaXeVGmeQV9TjAlY5OuQFqkaEjRZHEqWkQJQ3pQ2X1WIW
# k8o7xLYEnKmKk07kRNoIQX/mM/4dLCXNckWUY7otrAn7oRAwc4rwPm/1zc9Pu7aE
# /jx41hKI/IlkztyUfKJoZqyyh+f+eUKraicGx1nHCIDpcBywOCd4Rm3ooytCYf5N
# XuN9/MyNk139Zk/MHaFS+uF3mDrn0OY9uXdiQTlHzZLRjNM72bzagraZirz64Wji
# V5V+xV84phZbJ0MaaO99Z/jRLsQsLYadDtEYARMTtaTrsZX3HJF6CA+DJggMG7zE
# r7AHC+711g+31k+QbfGKWJM3G+OvvKGCF5cwgheTBgorBgEEAYI3AwMBMYIXgzCC
# F38GCSqGSIb3DQEHAqCCF3AwghdsAgEDMQ8wDQYJYIZIAWUDBAIBBQAwggFSBgsq
# hkiG9w0BCRABBKCCAUEEggE9MIIBOQIBAQYKKwYBBAGEWQoDATAxMA0GCWCGSAFl
# AwQCAQUABCA6taUMJKn2y7v9YXHId9ZK6M6/J1eXnSof4+TjheugHwIGZkY1Cc+Q
# GBMyMDI0MDYyMDE1MDAwMy45NjNaMASAAgH0oIHRpIHOMIHLMQswCQYDVQQGEwJV
# UzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwGA1UE
# ChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSUwIwYDVQQLExxNaWNyb3NvZnQgQW1l
# cmljYSBPcGVyYXRpb25zMScwJQYDVQQLEx5uU2hpZWxkIFRTUyBFU046MzcwMy0w
# NUUwLUQ5NDcxJTAjBgNVBAMTHE1pY3Jvc29mdCBUaW1lLVN0YW1wIFNlcnZpY2Wg
# ghHtMIIHIDCCBQigAwIBAgITMwAAAeqaJHLVWT9hYwABAAAB6jANBgkqhkiG9w0B
# AQsFADB8MQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UE
# BxMHUmVkbW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSYwJAYD
# VQQDEx1NaWNyb3NvZnQgVGltZS1TdGFtcCBQQ0EgMjAxMDAeFw0yMzEyMDYxODQ1
# MzBaFw0yNTAzMDUxODQ1MzBaMIHLMQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2Fz
# aGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENv
# cnBvcmF0aW9uMSUwIwYDVQQLExxNaWNyb3NvZnQgQW1lcmljYSBPcGVyYXRpb25z
# MScwJQYDVQQLEx5uU2hpZWxkIFRTUyBFU046MzcwMy0wNUUwLUQ5NDcxJTAjBgNV
# BAMTHE1pY3Jvc29mdCBUaW1lLVN0YW1wIFNlcnZpY2UwggIiMA0GCSqGSIb3DQEB
# AQUAA4ICDwAwggIKAoICAQC1C1/xSD8gB9X7Ludoo2rWb2ksqaF65QtJkbQpmsc6
# G4bg5MOv6WP/uJ4XOJvKX/c1t0ej4oWBqdGD6VbjXX4T0KfylTulrzKtgxnxZh7q
# 1uD0Dy/w5G0DJDPb6oxQrz6vMV2Z3y9ZxjfZqBnDfqGon/4VDHnZhdas22svSC5G
# HywsQ2J90MM7L4ecY8TnLI85kXXTVESb09txL2tHMYrB+KHCy08ds36an7IcOGfR
# mhHbFoPa5om9YGpVKS8xeT7EAwW7WbXL/lo5p9KRRIjAlsBBHD1TdGBucrGC3TQX
# STp9s7DjkvvNFuUa0BKsz6UiCLxJGQSZhd2iOJTEfJ1fxYk2nY6SCKsV+VmtV5ai
# PzY/sWoFY542+zzrAPr4elrvr9uB6ci/Kci//EOERZEUTBPXME/ia+t8jrT2y3ug
# 15MSCVuhOsNrmuZFwaRCrRED0yz4V9wlMTGHIJW55iNM3HPVJJ19vOSvrCP9lsEc
# EwWZIQ1FCyPOnkM1fs7880dahAa5UmPqMk5WEKxzDPVp081X5RQ6HGVUz6ZdgQ0j
# cT59EG+CKDPRD6mx8ovzIpS/r/wEHPKt5kOhYrjyQHXc9KHKTWfXpAVj1Syqt5X4
# nr+Mpeubv+N/PjQEPr0iYJDjSzJrqILhBs5pytb6vyR8HUVMp+mAA4rXjOw42vkH
# fQIDAQABo4IBSTCCAUUwHQYDVR0OBBYEFCuBRSWiUebpF0BU1MTIcosFblleMB8G
# A1UdIwQYMBaAFJ+nFV0AXmJdg/Tl0mWnG1M1GelyMF8GA1UdHwRYMFYwVKBSoFCG
# Tmh0dHA6Ly93d3cubWljcm9zb2Z0LmNvbS9wa2lvcHMvY3JsL01pY3Jvc29mdCUy
# MFRpbWUtU3RhbXAlMjBQQ0ElMjAyMDEwKDEpLmNybDBsBggrBgEFBQcBAQRgMF4w
# XAYIKwYBBQUHMAKGUGh0dHA6Ly93d3cubWljcm9zb2Z0LmNvbS9wa2lvcHMvY2Vy
# dHMvTWljcm9zb2Z0JTIwVGltZS1TdGFtcCUyMFBDQSUyMDIwMTAoMSkuY3J0MAwG
# A1UdEwEB/wQCMAAwFgYDVR0lAQH/BAwwCgYIKwYBBQUHAwgwDgYDVR0PAQH/BAQD
# AgeAMA0GCSqGSIb3DQEBCwUAA4ICAQAog61WXj9+/nxVbX3G37KgvyoNAnuu2w3H
# oWZj3H0YCeQ3b9KSZThVThW4iFcHrKnhFMBbXJX4uQI53kOWSaWCaV3xCznpRt3c
# 4/gSn3dvO/1GP3MJkpJfgo56CgS9zLOiP31kfmpUdPqekZb4ivMR6LoPb5HNlq0W
# bBpzFbtsTjNrTyfqqcqAwc6r99Df2UQTqDa0vzwpA8CxiAg2KlbPyMwBOPcr9hJT
# 8sGpX/ZhLDh11dZcbUAzXHo1RJorSSftVa9hLWnzxGzEGafPUwLmoETihOGLqIQl
# Cpvr94Hiak0Gq0wY6lduUQjk/lxZ4EzAw/cGMek8J3QdiNS8u9ujYh1B7NLr6t3I
# glfScDV3bdVWet1itTUoKVRLIivRDwAT7dRH13Cq32j2JG5BYu/XitRE8cdzaJmD
# VBzYhlPl9QXvC+6qR8I6NIN/9914bTq/S4g6FF4f1dixUxE4qlfUPMixGr0Ft4/S
# 0P4fwmhs+WHRn62PB4j3zCHixKJCsRn9IR3ExBQKQdMi5auiqB6xQBADUf+F7hSK
# ZfbA8sFSFreLSqhvj+qUQF84NcxuaxpbJWVpsO18IL4Qbt45Cz/QMa7EmMGNn7a8
# MM3uTQOlQy0u6c/jq111i1JqMjayTceQZNMBMM5EMc5Dr5m3T4bDj9WTNLgP8SFe
# 3EqTaWVMOTCCB3EwggVZoAMCAQICEzMAAAAVxedrngKbSZkAAAAAABUwDQYJKoZI
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
# MCUGA1UECxMeblNoaWVsZCBUU1MgRVNOOjM3MDMtMDVFMC1EOTQ3MSUwIwYDVQQD
# ExxNaWNyb3NvZnQgVGltZS1TdGFtcCBTZXJ2aWNloiMKAQEwBwYFKw4DAhoDFQCJ
# 2x7cQfjpRskJ8UGIctOCkmEkj6CBgzCBgKR+MHwxCzAJBgNVBAYTAlVTMRMwEQYD
# VQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVNaWNy
# b3NvZnQgQ29ycG9yYXRpb24xJjAkBgNVBAMTHU1pY3Jvc29mdCBUaW1lLVN0YW1w
# IFBDQSAyMDEwMA0GCSqGSIb3DQEBCwUAAgUA6h4skDAiGA8yMDI0MDYyMDA0MjAz
# MloYDzIwMjQwNjIxMDQyMDMyWjB3MD0GCisGAQQBhFkKBAExLzAtMAoCBQDqHiyQ
# AgEAMAoCAQACAgWPAgH/MAcCAQACAhNcMAoCBQDqH34QAgEAMDYGCisGAQQBhFkK
# BAIxKDAmMAwGCisGAQQBhFkKAwKgCjAIAgEAAgMHoSChCjAIAgEAAgMBhqAwDQYJ
# KoZIhvcNAQELBQADggEBAEvdeK316e8b+Kha3MgQkjCTkjujmWyi51pyE9O+yZlF
# +k3BpjkvDOwDi3OT7WmKlNAxC/c0CCbcsAyDf2pqvdr9er8jI8BL0IJpW48Ra4gw
# KYYkORXCpJwSBJk45ykeN0fSslBs/eaQ281GYEfEnyGM8golpG1p1zNhv4SniPhi
# PCoyCjWSXOjfU6E8S9vO8BVBwOQ1EW3Q3H9xfh9L1CxeFkwgZYTR+OpQCKBuEsXp
# +6x6u27sWL3LpMRR3rdI0Sa/THCyE4EvN5nEClep4mh18Eg3YOYCZ74NJ2uJ8x9R
# hZRMprwwybIkoStJAcWE3zpoq9BtpoRGjA9O+TBw0fgxggQNMIIECQIBATCBkzB8
# MQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVk
# bW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSYwJAYDVQQDEx1N
# aWNyb3NvZnQgVGltZS1TdGFtcCBQQ0EgMjAxMAITMwAAAeqaJHLVWT9hYwABAAAB
# 6jANBglghkgBZQMEAgEFAKCCAUowGgYJKoZIhvcNAQkDMQ0GCyqGSIb3DQEJEAEE
# MC8GCSqGSIb3DQEJBDEiBCDUDerHxS30u+dFQHSsnEbiob0tUo4abasw/XfvX/M2
# DDCB+gYLKoZIhvcNAQkQAi8xgeowgecwgeQwgb0EICmPodXjZDR4iwg0ltLANXBh
# 5G1uKqKIvq8sjKekuGZ4MIGYMIGApH4wfDELMAkGA1UEBhMCVVMxEzARBgNVBAgT
# Cldhc2hpbmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29m
# dCBDb3Jwb3JhdGlvbjEmMCQGA1UEAxMdTWljcm9zb2Z0IFRpbWUtU3RhbXAgUENB
# IDIwMTACEzMAAAHqmiRy1Vk/YWMAAQAAAeowIgQg/90bK9lyqyYP7/lrv6fwIU1n
# G5deX8tkv+O5WWrvR5MwDQYJKoZIhvcNAQELBQAEggIABaqLvr5WqGT5VmRi1JSg
# gJVdwGJeCWlylJhURK+BaYditBY7BnDwJ39dG/+PQWH52xEkEqGZNAJyFy/xQzfB
# 6huw6C9v8R9YTguWgSB5vImY0ioC+Hf9T0eiWR23jYru57Mhf1AGT6bi9MwComIo
# c1s/4lgxoObsm/G5VFAr1btc0gHlVq+CehW+7tVrWKGosrSxlxFcGpW7cGKgT0u2
# 1XO9P4qQEnYoKcY7M/4Cu+B2MUvSx9Mkz2uhC83xBhRokQ5Cb/zNj/CXjL0ilLuU
# QXqjCufmikR2Pn2mGfSf93lvyNwRGhHbdVt0WddIKBFmQh0U3NIiA4Qa/prfkga3
# JporvceGC/FbTrXQ+ECp9Jk9DhAY68R4Zpe1HncA1jOKVR0WN0vN/NpOiFb8L1CZ
# 5dcoOMu58ZIhRP3zly/1PG+r1zY9DX/gwCtrZWP462MbxQSDYqyyODGUAjc4n9f5
# 1Y6zoHQi5gLZi5gGdlGPHvMD3xiVg3JyvCphPaHScE9uxgZzRsGRmBRI+6zKoic9
# uYk4Sh2olbpKhSae6KgqzZAKxuDDr9HhgEst9rWkXnwrTXigH+4RCZiOdwe889wA
# q8leiibZmUZnsjyfICf9vSWiPZ34bn+2Heni7sb6vJBP9n9PfTI02TXnbO2VvJII
# w7sjyUSKe6bhjQAcaCMvAhA=
# SIG # End Windows Authenticode signature block