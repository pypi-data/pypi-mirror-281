# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric Chaos commands."""

from knack.help_files import helps

helps['chaos start'] = """
    type: command
    short-summary: Starts Chaos in the cluster.
    long-summary: If Chaos is not already running in the cluster, it starts Chaos with
        the passed in Chaos parameters.
        If Chaos is already running when this call is made, the call fails with
        the error code FABRIC_E_CHAOS_ALREADY_RUNNING.
        Refer to the article [Induce controlled Chaos in Service Fabric
        clusters](https://docs.microsoft.com/azure/service-fabric/service-fabric-controlled-chaos)
        for more details.
    parameters:
        - name: --time-to-run
          type: string
          short-summary: Total time (in seconds) for which Chaos will run
            before automatically stopping. The maximum allowed value is 4,294,967,295
            (System.UInt32.MaxValue).
        - name: --warning-as-error
          type: bool
          short-summary: Indicates whether warnings are treated with the same severity as errors.
        - name: --max-cluster-stabilization
          type: int
          short-summary: The maximum amount of time to wait
            for all cluster entities to become stable and healthy.
          long-summary: Chaos executes in iterations and at the start of
            each iteration it validates the health of cluster entities.
            During validation if a cluster entity is not stable and healthy
            within MaxClusterStabilizationTimeoutInSeconds,
            Chaos generates a validation failed event.
        - name: --max-concurrent-faults
          type: int
          short-summary: The maximum number of concurrent faults induced
            per iteration. Chaos executes in iterations and two consecutive
            iterations are separated by a validation phase. The higher
            the concurrency, the more aggressive the injection of
            faults -- inducing more complex series of states to uncover bugs.
            The recommendation is to start with a value of 2 or 3 and to
            exercise caution while moving up.
        - name: --disable-move-replica-faults
          type: bool
          short-summary: Disables the move primary and move secondary faults.
        - name: --wait-time-between-faults
          type: int
          short-summary: Wait time (in seconds) between consecutive faults
            within a single iteration.
          long-summary: The larger the value, the lower the overlapping
            between faults and the simpler the sequence of state transitions
            that the cluster goes through. The recommendation is to start
            with a value between 1 and 5 and exercise caution while moving up.
        - name: --wait-time-between-iterations
          type: int
          short-summary: Time-separation (in seconds) between two consecutive
            iterations of Chaos. The larger the value, the lower the fault
            injection rate.
        - name: --max-percent-unhealthy-nodes
          type: int
          short-summary: When evaluating cluster health during Chaos, the
            maximum allowed percentage of unhealthy nodes before
            reporting an error.
          long-summary: The maximum allowed percentage of unhealthy nodes
            before reporting an error. For example, to allow 10% of nodes
            to be unhealthy, this value would be 10. The percentage represents
            the maximum tolerated percentage of nodes that can be unhealthy
            before the cluster is considered in error. If the percentage is
            respected but there is at least one unhealthy node, the health
            is evaluated as Warning. The percentage is calculated by dividing
            the number of unhealthy nodes over the total number of nodes
            in the cluster. The computation rounds up to tolerate one failure
            on small numbers of nodes. Default percentage is zero.
            In large clusters, some nodes will always be down or out for
            repairs, so this percentage should be configured to tolerate that.
        - name: --max-percent-unhealthy-apps
          type: int
          short-summary: When evaluating cluster health during Chaos,
            the maximum allowed percentage of unhealthy applications
            before reporting an error.
          long-summary: The maximum allowed percentage of unhealthy
            applications before reporting an error. For example,
            to allow 10% of applications to be unhealthy, this value would be 10.
            The percentage represents the maximum tolerated percentage
            of applications that can be unhealthy before the cluster is
            considered in error. If the percentage is respected but
            there is at least one unhealthy application, the health
            is evaluated as Warning. This is calculated by dividing
            the number of unhealthy applications over the total number
            of application instances in the cluster, excluding applications
            of application types that are included in the
            ApplicationTypeHealthPolicyMap. The computation rounds up
            to tolerate one failure on small numbers of applications.
            Default percentage is zero.
        - name: --app-type-health-policy-map
          type: string
          short-summary: JSON encoded list with max
            percentage unhealthy applications for specific application
            types. Each entry specifies as a key the application type
            name and as  a value an integer that represents the
            MaxPercentUnhealthyApplications percentage used to evaluate
            the applications of the specified application type.
          long-summary: Defines a map with max percentage unhealthy
            applications for specific application types. Each entry
            specifies as key the application type name and as value
            an integer that represents the MaxPercentUnhealthyApplications
            percentage used to evaluate the applications of the specified
            application type. The application type health policy map
            can be used during cluster health evaluation to describe
            special application types. The application types included
            in the map are evaluated against the percentage specified
            in the map, and not with the global MaxPercentUnhealthyApplications
            defined in the cluster health policy. The applications of
            application types specified in the map are not counted against
            the global pool of applications. For example, if some
            applications of a type are critical, the cluster administrator
            can add an entry to the map for that application type and assign
            it a value of 0% (that is, do not tolerate any failures).
            All other applications can be evaluated with
            MaxPercentUnhealthyApplications set to 20% to tolerate
            some failures out of the thousands of application instances.
            The application type health policy map is used only if the
            cluster manifest enables application type health evaluation
            using the configuration entry for
            HealthManager/EnableApplicationTypeHealthEvaluation.
        - name: --context
          type: string
          short-summary: JSON encoded map of (string, string) type key-value
            pairs. The map can be used to record information about the Chaos
            run. There cannot be more than 100 such pairs and each
            string (key or value) can be at most 4095 characters long.
            This map is set by the starter of the Chaos run to optionally
            store the context about the specific run.
        - name: --chaos-target-filter
          type: string
          short-summary: JSON encoded dictionary with two
            string type keys. The two keys are NodeTypeInclusionList and
            ApplicationInclusionList. Values for both of these keys are list of
            string. chaos_target_filter defines all filters for targeted
            Chaos faults, for example, faulting only certain node types or
            faulting only certain applications.
          long-summary: If chaos_target_filter is not used, Chaos faults all cluster entities.
            If chaos_target_filter is used, Chaos faults only the entities that
            meet the chaos_target_filter specification. NodeTypeInclusionList
            and ApplicationInclusionList allow a union semantics only. It is
            not possible to specify an intersection of NodeTypeInclusionList
            and ApplicationInclusionList. For example,
            it is not possible to specify "fault this application only when
            it is on that node type." Once an entity is included in either
            NodeTypeInclusionList or ApplicationInclusionList, that entity cannot
            be excluded using ChaosTargetFilter. Even if applicationX does not
            appear in ApplicationInclusionList, in some Chaos iteration
            applicationX can be faulted because it happens to be on a node of
            nodeTypeY that is included in NodeTypeInclusionList.
            If both NodeTypeInclusionList and ApplicationInclusionList
            are empty, an ArgumentException is thrown.
            All types of faults (restart node, restart code package, remove replica,
            restart replica, move primary, and move secondary) are enabled for
            the nodes of these node types.
            If a node type (say NodeTypeX) does not appear in the
            NodeTypeInclusionList, then node level faults (like NodeRestart)
            will never be enabled for the nodes of NodeTypeX, but code package
            and replica faults can still be enabled for NodeTypeX
            if an application in the ApplicationInclusionList happens to
            reside on a node of NodeTypeX.
            At most 100 node type names can be included in this list,
            to increase this number, a config upgrade is required for
            MaxNumberOfNodeTypesInChaosEntityFilter configuration.
            All replicas belonging to services of these applications are
            amenable to replica faults (restart replica, remove replica,
            move primary, and move secondary) by Chaos.
            Chaos may restart a code package only if the code package hosts
            replicas of these applications only.
            If an application does not appear in this list, it can still
            be faulted in some Chaos iteration if the application ends
            up on a node of a node type that is included in NodeTypeInclusionList.
            However if applicationX is tied to nodeTypeY through placement
            constraints and applicationX is absent from ApplicationInclusionList
            and nodeTypeY is absent from NodeTypeInclusionList, then
            applicationX will never be faulted. At most 1000 application
            names can be included in this list, to increase this number,
            a config upgrade is required for
            MaxNumberOfApplicationsInChaosEntityFilter configuration.
"""

helps['chaos schedule set'] = """
    type: command
    short-summary: Set the schedule used by Chaos.
    long-summary:
        Chaos will automatically schedule runs based on the Chaos Schedule.
        The Chaos Schedule will be updated if the provided version matches the
        version on the server.
        When updating the Chaos Schedule, the version on the server is
        incremented by 1.
        The version on the server will wrap back to 0 after reaching a large
        number.
        If Chaos is running when this call is made, the call will fail.
    examples:
        - name: The following command sets a schedule (assuming the current schedule has version 0) that starts on 2016-01-01 and expires on 2038-01-01 that runs Chaos 24 hours of the day, 7 days a week. Chaos will be scheduled on the cluster for that time.
          text: sfctl chaos schedule set --version 0 --start-date-utc "2016-01-01T00:00:00.000Z" --expiry-date-utc "2038-01-01T00:00:00.000Z" --chaos-parameters-dictionary [{\\\"Key\\\":\\\"adhoc\\\",\\\"Value\\\":{\\\"MaxConcurrentFaults\\\":3,\\\"EnableMoveReplicaFaults\\\":true,\\\"ChaosTargetFilter\\\":{\\\"NodeTypeInclusionList\\\":[\\\"N0010Ref\\\",\\\"N0020Ref\\\",\\\"N0030Ref\\\",\\\"N0040Ref\\\",\\\"N0050Ref\\\"]},\\\"MaxClusterStabilizationTimeoutInSeconds\\\":60,\\\"WaitTimeBetweenIterationsInSeconds\\\":15,\\\"WaitTimeBetweenFaultsInSeconds\\\":30,\\\"TimeToRunInSeconds\\\":\\\"600\\\",\\\"Context\\\":{\\\"Map\\\":{\\\"test\\\":\\\"value\\\"}},\\\"ClusterHealthPolicy\\\":{\\\"MaxPercentUnhealthyNodes\\\":0,\\\"ConsiderWarningAsError\\\":true,\\\"MaxPercentUnhealthyApplications\\\":0}}}] --jobs [{\\\"ChaosParameters\\\":\\\"adhoc\\\",\\\"Days\\\":{\\\"Sunday\\\":true,\\\"Monday\\\":true,\\\"Tuesday\\\":true,\\\"Wednesday\\\":true,\\\"Thursday\\\":true,\\\"Friday\\\":true,\\\"Saturday\\\":true},\\\"Times\\\":[{\\\"StartTime\\\":{\\\"Hour\\\":0,\\\"Minute\\\":0},\\\"EndTime\\\":{\\\"Hour\\\":23,\\\"Minute\\\":59}}]}]




    parameters:
        - name: --version
          type: int
          short-summary: The version number of the Schedule.
        - name: --start-date-utc
          type: string
          short-summary: The date and time for when to start using the Schedule to schedule Chaos.
        - name: --expiry-date-utc
          type: string
          short-summary: The date and time for when to stop using the Schedule to schedule Chaos.
        - name: --chaos-parameters-dictionary
          type: string
          short-summary: JSON encoded list representing a mapping of string names to
            ChaosParameters to be used by Jobs.
        - name: --jobs
          type: string
          short-summary: JSON encoded list of ChaosScheduleJobs representing when to run Chaos and
            with what parameters to run Chaos with.
"""

# SIG # Begin Windows Authenticode signature block
# MIInvwYJKoZIhvcNAQcCoIInsDCCJ6wCAQExDzANBglghkgBZQMEAgEFADB5Bgor
# BgEEAYI3AgEEoGswaTA0BgorBgEEAYI3AgEeMCYCAwEAAAQQse8BENmB6EqSR2hd
# JGAGggIBAAIBAAIBAAIBAAIBADAxMA0GCWCGSAFlAwQCAQUABCC/N594nbWCMm1h
# 6Q/Y+wD1/JVI3SVm9n0zyVigw+D9DKCCDXYwggX0MIID3KADAgECAhMzAAADrzBA
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
# /Xmfwb1tbWrJUnMTDXpQzTGCGZ8wghmbAgEBMIGVMH4xCzAJBgNVBAYTAlVTMRMw
# EQYDVQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVN
# aWNyb3NvZnQgQ29ycG9yYXRpb24xKDAmBgNVBAMTH01pY3Jvc29mdCBDb2RlIFNp
# Z25pbmcgUENBIDIwMTECEzMAAAOvMEAOTKNNBUEAAAAAA68wDQYJYIZIAWUDBAIB
# BQCgga4wGQYJKoZIhvcNAQkDMQwGCisGAQQBgjcCAQQwHAYKKwYBBAGCNwIBCzEO
# MAwGCisGAQQBgjcCARUwLwYJKoZIhvcNAQkEMSIEIGxJW9idLGY3/TVl97A8hQMl
# XlTbTDoq3E/oxtXr5DOsMEIGCisGAQQBgjcCAQwxNDAyoBSAEgBNAGkAYwByAG8A
# cwBvAGYAdKEagBhodHRwOi8vd3d3Lm1pY3Jvc29mdC5jb20wDQYJKoZIhvcNAQEB
# BQAEggEAJDxXlAFYCypaOB6gxqF/vgOuVuuf4oUPVy19k2Ofm9+qNwBG/RHfliPt
# jsWgisoqNalEgdJ8sB7uqC29o7/phmK1eABltWC1JJJdQzxjmD4ub0Q5mxKr0OHm
# 0E4XQpYyVhk8My1Xc6cVOk6iCcBpU95au9XDk1kqmRHixfR17zOdSSWjskRfQfT8
# luLvYbAPLYGed2d5O+tNMoru6LWmizy40OhY5Bsd5hfqrt5c0ex91Pg8gD5tatud
# u+tOvP9GW8EO5R0HKaMiSG6yz6LB3fcOG0gL0mzJVB50u1TTNcrLWPkLy2XS7zHk
# tkw9L8tZfV5/VfJMXYVjtIG03UTCyqGCFykwghclBgorBgEEAYI3AwMBMYIXFTCC
# FxEGCSqGSIb3DQEHAqCCFwIwghb+AgEDMQ8wDQYJYIZIAWUDBAIBBQAwggFZBgsq
# hkiG9w0BCRABBKCCAUgEggFEMIIBQAIBAQYKKwYBBAGEWQoDATAxMA0GCWCGSAFl
# AwQCAQUABCAh4voFv/Kwvc9EkcRtCnx8DANk8/8tLugzMX/kvcnt6AIGZnMHwCeP
# GBMyMDI0MDYyMDE1MDAwNi41MDVaMASAAgH0oIHYpIHVMIHSMQswCQYDVQQGEwJV
# UzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwGA1UE
# ChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMS0wKwYDVQQLEyRNaWNyb3NvZnQgSXJl
# bGFuZCBPcGVyYXRpb25zIExpbWl0ZWQxJjAkBgNVBAsTHVRoYWxlcyBUU1MgRVNO
# OkZDNDEtNEJENC1EMjIwMSUwIwYDVQQDExxNaWNyb3NvZnQgVGltZS1TdGFtcCBT
# ZXJ2aWNloIIReDCCBycwggUPoAMCAQICEzMAAAHimZmV8dzjIOsAAQAAAeIwDQYJ
# KoZIhvcNAQELBQAwfDELMAkGA1UEBhMCVVMxEzARBgNVBAgTCldhc2hpbmd0b24x
# EDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29mdCBDb3Jwb3JhdGlv
# bjEmMCQGA1UEAxMdTWljcm9zb2Z0IFRpbWUtU3RhbXAgUENBIDIwMTAwHhcNMjMx
# MDEyMTkwNzI1WhcNMjUwMTEwMTkwNzI1WjCB0jELMAkGA1UEBhMCVVMxEzARBgNV
# BAgTCldhc2hpbmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jv
# c29mdCBDb3Jwb3JhdGlvbjEtMCsGA1UECxMkTWljcm9zb2Z0IElyZWxhbmQgT3Bl
# cmF0aW9ucyBMaW1pdGVkMSYwJAYDVQQLEx1UaGFsZXMgVFNTIEVTTjpGQzQxLTRC
# RDQtRDIyMDElMCMGA1UEAxMcTWljcm9zb2Z0IFRpbWUtU3RhbXAgU2VydmljZTCC
# AiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBALVjtZhV+kFmb8cKQpg2mzis
# DlRI978Gb2amGvbAmCd04JVGeTe/QGzM8KbQrMDol7DC7jS03JkcrPsWi9WpVwsI
# ckRQ8AkX1idBG9HhyCspAavfuvz55khl7brPQx7H99UJbsE3wMmpmJasPWpgF05z
# ZlvpWQDULDcIYyl5lXI4HVZ5N6MSxWO8zwWr4r9xkMmUXs7ICxDJr5a39SSePAJR
# IyznaIc0WzZ6MFcTRzLLNyPBE4KrVv1LFd96FNxAzwnetSePg88EmRezr2T3HTFE
# lneJXyQYd6YQ7eCIc7yllWoY03CEg9ghorp9qUKcBUfFcS4XElf3GSERnlzJsK7s
# /ZGPU4daHT2jWGoYha2QCOmkgjOmBFCqQFFwFmsPrZj4eQszYxq4c4HqPnUu4hT4
# aqpvUZ3qIOXbdyU42pNL93cn0rPTTleOUsOQbgvlRdthFCBepxfb6nbsp3fcZaPB
# fTbtXVa8nLQuMCBqyfsebuqnbwj+lHQfqKpivpyd7KCWACoj78XUwYqy1HyYnStT
# me4T9vK6u2O/KThfROeJHiSg44ymFj+34IcFEhPogaKvNNsTVm4QbqphCyknrwBy
# qorBCLH6bllRtJMJwmu7GRdTQsIx2HMKqphEtpSm1z3ufASdPrgPhsQIRFkHZGui
# hL1Jjj4Lu3CbAmha0lOrAgMBAAGjggFJMIIBRTAdBgNVHQ4EFgQURIQOEdq+7Qds
# lptJiCRNpXgJ2gUwHwYDVR0jBBgwFoAUn6cVXQBeYl2D9OXSZacbUzUZ6XIwXwYD
# VR0fBFgwVjBUoFKgUIZOaHR0cDovL3d3dy5taWNyb3NvZnQuY29tL3BraW9wcy9j
# cmwvTWljcm9zb2Z0JTIwVGltZS1TdGFtcCUyMFBDQSUyMDIwMTAoMSkuY3JsMGwG
# CCsGAQUFBwEBBGAwXjBcBggrBgEFBQcwAoZQaHR0cDovL3d3dy5taWNyb3NvZnQu
# Y29tL3BraW9wcy9jZXJ0cy9NaWNyb3NvZnQlMjBUaW1lLVN0YW1wJTIwUENBJTIw
# MjAxMCgxKS5jcnQwDAYDVR0TAQH/BAIwADAWBgNVHSUBAf8EDDAKBggrBgEFBQcD
# CDAOBgNVHQ8BAf8EBAMCB4AwDQYJKoZIhvcNAQELBQADggIBAORURDGrVRTbnulf
# sg2cTsyyh7YXvhVU7NZMkITAQYsFEPVgvSviCylr5ap3ka76Yz0t/6lxuczI6w7t
# Xq8n4WxUUgcj5wAhnNorhnD8ljYqbck37fggYK3+wEwLhP1PGC5tvXK0xYomU1nU
# +lXOy9ZRnShI/HZdFrw2srgtsbWow9OMuADS5lg7okrXa2daCOGnxuaD1IO+65E7
# qv2O0W0sGj7AWdOjNdpexPrspL2KEcOMeJVmkk/O0ganhFzzHAnWjtNWneU11WQ6
# Bxv8OpN1fY9wzQoiycgvOOJM93od55EGeXxfF8bofLVlUE3zIikoSed+8s61NDP+
# x9RMya2mwK/Ys1xdvDlZTHndIKssfmu3vu/a+BFf2uIoycVTvBQpv/drRJD68eo4
# 01mkCRFkmy/+BmQlRrx2rapqAu5k0Nev+iUdBUKmX/iOaKZ75vuQg7hCiBA5xIm5
# ZIXDSlX47wwFar3/BgTwntMq9ra6QRAeS/o/uYWkmvqvE8Aq38QmKgTiBnWSS/uV
# PcaHEyArnyFh5G+qeCGmL44MfEnFEhxc3saPmXhe6MhSgCIGJUZDA7336nQD8fn4
# y6534Lel+LuT5F5bFt0mLwd+H5GxGzObZmm/c3pEWtHv1ug7dS/Dfrcd1sn2E4gk
# 4W1L1jdRBbK9xwkMmwY+CHZeMSvBMIIHcTCCBVmgAwIBAgITMwAAABXF52ueAptJ
# mQAAAAAAFTANBgkqhkiG9w0BAQsFADCBiDELMAkGA1UEBhMCVVMxEzARBgNVBAgT
# Cldhc2hpbmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29m
# dCBDb3Jwb3JhdGlvbjEyMDAGA1UEAxMpTWljcm9zb2Z0IFJvb3QgQ2VydGlmaWNh
# dGUgQXV0aG9yaXR5IDIwMTAwHhcNMjEwOTMwMTgyMjI1WhcNMzAwOTMwMTgzMjI1
# WjB8MQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMH
# UmVkbW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSYwJAYDVQQD
# Ex1NaWNyb3NvZnQgVGltZS1TdGFtcCBQQ0EgMjAxMDCCAiIwDQYJKoZIhvcNAQEB
# BQADggIPADCCAgoCggIBAOThpkzntHIhC3miy9ckeb0O1YLT/e6cBwfSqWxOdcjK
# NVf2AX9sSuDivbk+F2Az/1xPx2b3lVNxWuJ+Slr+uDZnhUYjDLWNE893MsAQGOhg
# fWpSg0S3po5GawcU88V29YZQ3MFEyHFcUTE3oAo4bo3t1w/YJlN8OWECesSq/XJp
# rx2rrPY2vjUmZNqYO7oaezOtgFt+jBAcnVL+tuhiJdxqD89d9P6OU8/W7IVWTe/d
# vI2k45GPsjksUZzpcGkNyjYtcI4xyDUoveO0hyTD4MmPfrVUj9z6BVWYbWg7mka9
# 7aSueik3rMvrg0XnRm7KMtXAhjBcTyziYrLNueKNiOSWrAFKu75xqRdbZ2De+JKR
# Hh09/SDPc31BmkZ1zcRfNN0Sidb9pSB9fvzZnkXftnIv231fgLrbqn427DZM9itu
# qBJR6L8FA6PRc6ZNN3SUHDSCD/AQ8rdHGO2n6Jl8P0zbr17C89XYcz1DTsEzOUyO
# ArxCaC4Q6oRRRuLRvWoYWmEBc8pnol7XKHYC4jMYctenIPDC+hIK12NvDMk2ZItb
# oKaDIV1fMHSRlJTYuVD5C4lh8zYGNRiER9vcG9H9stQcxWv2XFJRXRLbJbqvUAV6
# bMURHXLvjflSxIUXk8A8FdsaN8cIFRg/eKtFtvUeh17aj54WcmnGrnu3tz5q4i6t
# AgMBAAGjggHdMIIB2TASBgkrBgEEAYI3FQEEBQIDAQABMCMGCSsGAQQBgjcVAgQW
# BBQqp1L+ZMSavoKRPEY1Kc8Q/y8E7jAdBgNVHQ4EFgQUn6cVXQBeYl2D9OXSZacb
# UzUZ6XIwXAYDVR0gBFUwUzBRBgwrBgEEAYI3TIN9AQEwQTA/BggrBgEFBQcCARYz
# aHR0cDovL3d3dy5taWNyb3NvZnQuY29tL3BraW9wcy9Eb2NzL1JlcG9zaXRvcnku
# aHRtMBMGA1UdJQQMMAoGCCsGAQUFBwMIMBkGCSsGAQQBgjcUAgQMHgoAUwB1AGIA
# QwBBMAsGA1UdDwQEAwIBhjAPBgNVHRMBAf8EBTADAQH/MB8GA1UdIwQYMBaAFNX2
# VsuP6KJcYmjRPZSQW9fOmhjEMFYGA1UdHwRPME0wS6BJoEeGRWh0dHA6Ly9jcmwu
# bWljcm9zb2Z0LmNvbS9wa2kvY3JsL3Byb2R1Y3RzL01pY1Jvb0NlckF1dF8yMDEw
# LTA2LTIzLmNybDBaBggrBgEFBQcBAQROMEwwSgYIKwYBBQUHMAKGPmh0dHA6Ly93
# d3cubWljcm9zb2Z0LmNvbS9wa2kvY2VydHMvTWljUm9vQ2VyQXV0XzIwMTAtMDYt
# MjMuY3J0MA0GCSqGSIb3DQEBCwUAA4ICAQCdVX38Kq3hLB9nATEkW+Geckv8qW/q
# XBS2Pk5HZHixBpOXPTEztTnXwnE2P9pkbHzQdTltuw8x5MKP+2zRoZQYIu7pZmc6
# U03dmLq2HnjYNi6cqYJWAAOwBb6J6Gngugnue99qb74py27YP0h1AdkY3m2CDPVt
# I1TkeFN1JFe53Z/zjj3G82jfZfakVqr3lbYoVSfQJL1AoL8ZthISEV09J+BAljis
# 9/kpicO8F7BUhUKz/AyeixmJ5/ALaoHCgRlCGVJ1ijbCHcNhcy4sa3tuPywJeBTp
# kbKpW99Jo3QMvOyRgNI95ko+ZjtPu4b6MhrZlvSP9pEB9s7GdP32THJvEKt1MMU0
# sHrYUP4KWN1APMdUbZ1jdEgssU5HLcEUBHG/ZPkkvnNtyo4JvbMBV0lUZNlz138e
# W0QBjloZkWsNn6Qo3GcZKCS6OEuabvshVGtqRRFHqfG3rsjoiV5PndLQTHa1V1QJ
# sWkBRH58oWFsc/4Ku+xBZj1p/cvBQUl+fpO+y/g75LcVv7TOPqUxUYS8vwLBgqJ7
# Fx0ViY1w/ue10CgaiQuPNtq6TPmb/wrpNPgkNWcr4A245oyZ1uEi6vAnQj0llOZ0
# dFtq0Z4+7X6gMTN9vMvpe784cETRkPHIqzqKOghif9lwY1NNje6CbaUFEMFxBmoQ
# tB1VM1izoXBm8qGCAtQwggI9AgEBMIIBAKGB2KSB1TCB0jELMAkGA1UEBhMCVVMx
# EzARBgNVBAgTCldhc2hpbmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoT
# FU1pY3Jvc29mdCBDb3Jwb3JhdGlvbjEtMCsGA1UECxMkTWljcm9zb2Z0IElyZWxh
# bmQgT3BlcmF0aW9ucyBMaW1pdGVkMSYwJAYDVQQLEx1UaGFsZXMgVFNTIEVTTjpG
# QzQxLTRCRDQtRDIyMDElMCMGA1UEAxMcTWljcm9zb2Z0IFRpbWUtU3RhbXAgU2Vy
# dmljZaIjCgEBMAcGBSsOAwIaAxUAFpuZafp0bnpJdIhfiB1d8pTohm+ggYMwgYCk
# fjB8MQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMH
# UmVkbW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSYwJAYDVQQD
# Ex1NaWNyb3NvZnQgVGltZS1TdGFtcCBQQ0EgMjAxMDANBgkqhkiG9w0BAQUFAAIF
# AOoeLucwIhgPMjAyNDA2MjAxMjMwMzFaGA8yMDI0MDYyMTEyMzAzMVowdDA6Bgor
# BgEEAYRZCgQBMSwwKjAKAgUA6h4u5wIBADAHAgEAAgIVzDAHAgEAAgIRSjAKAgUA
# 6h+AZwIBADA2BgorBgEEAYRZCgQCMSgwJjAMBgorBgEEAYRZCgMCoAowCAIBAAID
# B6EgoQowCAIBAAIDAYagMA0GCSqGSIb3DQEBBQUAA4GBADczcO5SYBxUfgfrFZJH
# Hm9s/SFyhOJRYs8HtTuPqzLuXHKccXrFXdh7n35lDBpxLn/pFTRqI8HURItxAhcL
# GaHHUgzSXtUP2GZDo/KMHuRppy6Yt6VJu8IQL1Lc77IV9bktf+tTjOL/W/tQ4ToS
# OtkfYNjiMS8O1BIJSyrbxKKDMYIEDTCCBAkCAQEwgZMwfDELMAkGA1UEBhMCVVMx
# EzARBgNVBAgTCldhc2hpbmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoT
# FU1pY3Jvc29mdCBDb3Jwb3JhdGlvbjEmMCQGA1UEAxMdTWljcm9zb2Z0IFRpbWUt
# U3RhbXAgUENBIDIwMTACEzMAAAHimZmV8dzjIOsAAQAAAeIwDQYJYIZIAWUDBAIB
# BQCgggFKMBoGCSqGSIb3DQEJAzENBgsqhkiG9w0BCRABBDAvBgkqhkiG9w0BCQQx
# IgQgiizl43pGvsU1UU8I3lIiRc9r7DxF3XIZ0VdBs13Dv/wwgfoGCyqGSIb3DQEJ
# EAIvMYHqMIHnMIHkMIG9BCAriSpKEP0muMbBUETODoL4d5LU6I/bjucIZkOJCI9/
# /zCBmDCBgKR+MHwxCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpXYXNoaW5ndG9uMRAw
# DgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVNaWNyb3NvZnQgQ29ycG9yYXRpb24x
# JjAkBgNVBAMTHU1pY3Jvc29mdCBUaW1lLVN0YW1wIFBDQSAyMDEwAhMzAAAB4pmZ
# lfHc4yDrAAEAAAHiMCIEIME4FCPh6Qv1wgFMwDj+4ZJomuNK8nJ3QEYJIf7IilWH
# MA0GCSqGSIb3DQEBCwUABIICACzZCbYIq+XA3/TX8bsbqR1x+oq8hP8gizLj0r2Y
# irHIHPdJJtnzoh37gE3sPF78OaowEU9uJRsK0V3uoeNH3M5/fv5AO16Tgpo8dhW+
# jDkF5+aZDyiOVZsjOptC/BfQeIo3gkVzLXE3KpKEXtQ30JgB3OrL5RvPZxHRBDag
# BpCezVVcfXltnXRmMcLFwzAuo1k9cM/yt6KDQv7WdH3bqiqIfslWvI5pWKOjj+Mc
# VVtn2tTFfE454UUyaHGWr0cV1V7FRi5+Aq5bXLYXtRw710xxyFG4+8sPrLRgoyPz
# 1J/uQLiRnmjjIS2HpZuS1G21kF1n7Kr6kv0ebJ2ufwvptNLEvv1hCXOlllIAlJEc
# juICEkdY+zsL9v/Rae1/J4+zDKmraBUw2aoPp7g6lQLOGOwHsC0bZSRLML4OE/5U
# WkwgIJtXmGZQSzJr2VuVy6cCQMVn3QVJVf7roXD2BnbfuLIQCch9Lr/rWRhbmp1v
# XYyGkw4fOuSRG6QIrlpJJNZfQwxyFvs38QlXs4eRuM6sEOrQOtg7inotLfuhL0x1
# JIA1f69buxT7nRZSGxqCOneAsd8gY006RiFOo7juSZTVOv08PkcmBsIzvrHjQM5K
# j2XPPo8BSaiEV8fR8Ck04TnvZ758jSRGNozCcCVL/xaU6ZiPAAsX9d8vaqGtT9l0
# Chak
# SIG # End Windows Authenticode signature block