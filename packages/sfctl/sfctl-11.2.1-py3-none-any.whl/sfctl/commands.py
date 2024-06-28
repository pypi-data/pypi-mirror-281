# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Command and help loader for the Service Fabric CLI.

Commands are stored as one to one mappings between command line syntax and
python function.
"""

from collections import OrderedDict
from knack.commands import CLICommandsLoader, CommandGroup
from knack.help import CLIHelp
from sfctl.apiclient import create as client_create

# Need to import so global help dict gets updated
import sfctl.helps.app  # pylint: disable=unused-import
import sfctl.helps.settings  # pylint: disable=unused-import
import sfctl.helps.main  # pylint: disable=unused-import
import sfctl.helps.health  # pylint: disable=unused-import
import sfctl.helps.cluster_upgrade  # pylint: disable=unused-import
import sfctl.helps.compose  # pylint: disable=unused-import
import sfctl.helps.container  # pylint: disable=unused-import
import sfctl.helps.property  # pylint: disable=unused-import
import sfctl.helps.app_type  # pylint: disable=unused-import
import sfctl.helps.chaos  # pylint: disable=unused-import
import sfctl.helps.infrastructure  # pylint: disable=unused-import
import sfctl.helps.node # pylint: disable=unused-import

EXCLUDED_PARAMS = ['self', 'raw', 'custom_headers', 'operation_config',
                   'content_version', 'kwargs', 'client']

class SFCommandHelp(CLIHelp):
    """Service Fabric CLI help loader"""

    def __init__(self, cli_ctx=None):
        header_msg = 'Service Fabric Command Line'

        super(SFCommandHelp, self).__init__(cli_ctx=cli_ctx, welcome_message=header_msg)


class SFCommandLoader(CLICommandsLoader):
    """Service Fabric CLI command loader, containing command mappings"""

    def __init__(self, *args, **kwargs):
        super(SFCommandLoader, self).__init__(
            *args,
            excluded_command_handler_args=EXCLUDED_PARAMS,
            **kwargs)

    def load_command_table(self, args):  # pylint: disable=too-many-statements
        """Load all Service Fabric commands"""

        # -----------------
        # Standard commands
        # -----------------

        client_func_path = 'azure.servicefabric#ServiceFabricClientAPIs.{}'

        with CommandGroup(self, 'rpm', client_func_path,
                          client_factory=client_create) as group:
            group.command('delete', 'delete_repair_task')
            group.command('list', 'get_repair_task_list')
            group.command('approve-force', 'force_approve_repair_task')

        with CommandGroup(self, 'sa-cluster', client_func_path,
                          client_factory=client_create) as group:
            group.command('config', 'get_cluster_configuration')
            group.command('upgrade-status',
                          'get_cluster_configuration_upgrade_status')

        with CommandGroup(self, 'cluster', client_func_path,
                          client_factory=client_create) as group:
            group.command('health', 'get_cluster_health')
            group.command('manifest', 'get_cluster_manifest')
            group.command(
                'code-versions',
                'get_provisioned_fabric_code_version_info_list'
            )
            group.command(
                'config-versions',
                'get_provisioned_fabric_config_version_info_list'
            )
            group.command('upgrade-status', 'get_cluster_upgrade_progress')
            group.command('recover-system', 'recover_system_partitions')
            group.command('operation-list', 'get_fault_operation_list')
            group.command('operation-cancel', 'cancel_operation')
            group.command('provision', 'provision_cluster')
            group.command('unprovision', 'unprovision_cluster')
            group.command('upgrade-rollback', 'rollback_cluster_upgrade')
            group.command('upgrade-resume', 'resume_cluster_upgrade')

        with CommandGroup(self, 'node', client_func_path,
                          client_factory=client_create) as group:
            group.command('list', 'get_node_info_list')
            group.command('info', 'get_node_info')
            group.command('health', 'get_node_health')
            group.command('load', 'get_node_load_info')
            group.command('disable', 'disable_node')
            group.command('enable', 'enable_node')
            group.command('remove-state', 'remove_node_state')
            group.command('restart', 'restart_node')
            group.command('transition', 'start_node_transition')
            group.command(
                'transition-status',
                'get_node_transition_progress'
            )
            group.command(
                'add-configuration-parameter-overrides',
                'add_configuration_parameter_overrides'
            )
            group.command(
                'get-configuration-overrides',
                'get_configuration_overrides'
            )
            group.command(
                'remove-configuration-overrides',
                'remove_configuration_overrides'
            )

        with CommandGroup(self, 'application', client_func_path,
                          client_factory=client_create) as group:
            group.command('type-list', 'get_application_type_info_list')
            group.command('type', 'get_application_type_info_list_by_name')
            group.command('unprovision', 'unprovision_application_type')
            group.command('delete', 'delete_application')
            group.command('list', 'get_application_info_list')
            group.command('info', 'get_application_info')
            group.command('health', 'get_application_health')
            group.command('upgrade-status', 'get_application_upgrade')
            group.command('upgrade-resume', 'resume_application_upgrade')
            group.command(
                'upgrade-rollback',
                'rollback_application_upgrade'
            )
            group.command(
                'deployed-list',
                'get_deployed_application_info_list'
            )
            group.command('deployed', 'get_deployed_application_info')
            group.command(
                'deployed-health',
                'get_deployed_application_health'
            )
            group.command('manifest', 'get_application_manifest')
            group.command('load', 'get_application_load_info')

        with CommandGroup(self, 'service', client_func_path,
                          client_factory=client_create) as group:
            group.command('type-list', 'get_service_type_info_list')
            group.command('manifest', 'get_service_manifest')
            group.command(
                'deployed-type-list',
                'get_deployed_service_type_info_list'
            )
            group.command(
                'deployed-type',
                'get_deployed_service_type_info_by_name'
            )
            group.command('list', 'get_service_info_list')
            group.command('info', 'get_service_info')
            group.command('app-name', 'get_application_name_info')
            group.command('delete', 'delete_service')
            group.command('description', 'get_service_description')
            group.command('health', 'get_service_health')
            group.command('resolve', 'resolve_service')
            group.command('recover', 'recover_service_partitions')
            group.command(
                'package-list',
                'get_deployed_service_package_info_list'
            )
            group.command(
                'package-info',
                'get_deployed_service_package_info_list_by_name'
            )
            group.command(
                'package-health',
                'get_deployed_service_package_health'
            )
            group.command(
                'code-package-list',
                'get_deployed_code_package_info_list'
            )
            group.command(
                'get-container-logs',
                'get_container_logs_deployed_on_node'
            )

        with CommandGroup(self, 'partition', client_func_path,
                          client_factory=client_create) as group:
            group.command('list', 'get_partition_info_list')
            group.command('info', 'get_partition_info')
            group.command('svc-name', 'get_service_name_info')
            group.command('health', 'get_partition_health')
            group.command('load', 'get_partition_load_information')
            group.command('load-reset', 'reset_partition_load')
            group.command('recover', 'recover_partition')
            group.command('recover-all', 'recover_all_partitions')
            group.command('data-loss', 'start_data_loss')
            group.command('data-loss-status', 'get_data_loss_progress')
            group.command('quorum-loss', 'start_quorum_loss')
            group.command('quorum-loss-status', 'get_quorum_loss_progress')
            group.command('restart', 'start_partition_restart')
            group.command(
                'restart-status',
                'get_partition_restart_progress'
            )
            group.command(
                'move-primary-replica',
                'move_primary_replica',
            )
            group.command(
                'move-secondary-replica',
                'move_secondary_replica',
            )
            group.command(
                'move-instance',
                'move_instance',
            )
            group.command(
                'get-loaded-partition-info-list',
                'get_loaded_partition_info_list',
            )

        with CommandGroup(self, 'replica', client_func_path,
                          client_factory=client_create) as group:
            group.command('list', 'get_replica_info_list')
            group.command('info', 'get_replica_info')
            group.command('health', 'get_replica_health')
            group.command(
                'deployed-list',
                'get_deployed_service_replica_info_list'
            )
            group.command(
                'deployed',
                'get_deployed_service_replica_detail_info'
            )
            group.command('restart', 'restart_replica')
            group.command('remove', 'remove_replica')

        with CommandGroup(self, 'compose', client_func_path,
                          client_factory=client_create) as group:
            group.command('status', 'get_compose_deployment_status')
            group.command('list', 'get_compose_deployment_status_list')
            group.command('remove', 'remove_compose_deployment')
            group.command('upgrade-status',
                          'get_compose_deployment_upgrade_progress')
            group.command('upgrade-rollback', 'start_rollback_compose_deployment_upgrade')

        with CommandGroup(self, 'chaos', client_func_path,
                          client_factory=client_create) as group:
            group.command('stop', 'stop_chaos')
            group.command('events', 'get_chaos_events')
            group.command('get', 'get_chaos')

        with CommandGroup(self, 'chaos schedule', client_func_path,
                          client_factory=client_create) as group:
            group.command('get', 'get_chaos_schedule')

        with CommandGroup(self, 'store', client_func_path,
                          client_factory=client_create) as group:
            group.command('stat', 'get_image_store_content')
            group.command('delete', 'delete_image_store_content')
            group.command('root-info', 'get_image_store_root_content')

        with CommandGroup(self, 'property', client_func_path,
                          client_factory=client_create) as group:
            group.command('list', 'get_property_info_list')
            group.command('get', 'get_property_info')
            group.command('delete', 'delete_property')

        with CommandGroup(self, 'events', client_func_path,
                          client_factory=client_create) as group:
            group.command('cluster-list', 'get_cluster_event_list')
            group.command('all-nodes-list', 'get_nodes_event_list')
            group.command('node-list', 'get_node_event_list')
            group.command('all-applications-list', 'get_applications_event_list')
            group.command('application-list', 'get_application_event_list')
            group.command('all-services-list', 'get_services_event_list')
            group.command('service-list', 'get_service_event_list')
            group.command('all-partitions-list', 'get_partitions_event_list')
            group.command('partition-list', 'get_partition_event_list')
            group.command('partition-all-replicas-list', 'get_partition_replicas_event_list')
            group.command('partition-replica-list', 'get_partition_replica_event_list')

        # ---------------
        # Custom commands
        # ---------------

        with CommandGroup(self, 'container', 'sfctl.custom_container#{}',
                          client_factory=client_create) as group:
            group.command('invoke-api', 'invoke_api')
            group.command('logs', 'logs')

        with CommandGroup(self, 'cluster', 'sfctl.custom_cluster_upgrade#{}',
                          client_factory=client_create) as group:
            group.command('upgrade', 'upgrade')
            group.command('upgrade-update', 'update_upgrade')

        with CommandGroup(self, 'sa-cluster', 'sfctl.custom_cluster_upgrade#{}',
                          client_factory=client_create) as group:
            group.command('config-upgrade', 'sa_configuration_upgrade')

        with CommandGroup(self, 'compose', 'sfctl.custom_compose#{}',
                          client_factory=client_create) as group:
            group.command('upgrade', 'upgrade')
            group.command('create', 'create')

        with CommandGroup(self, 'application', 'sfctl.custom_app#{}',
                          client_factory=client_create) as group:
            group.command('create', 'create')
            group.command('upgrade', 'upgrade')

        with CommandGroup(self, 'application', 'sfctl.custom_app#{}') as group:
            group.command('upload', 'upload')

        # Need an empty client for the select and upload operations
        with CommandGroup(self, 'cluster', 'sfctl.custom_cluster#{}') as group:
            group.command('select', 'select')
            group.command('show-connection', 'show_connection')

        with CommandGroup(self, 'chaos', 'sfctl.custom_chaos#{}',
                          client_factory=client_create) as group:
            group.command('start', 'start')

        with CommandGroup(self, 'chaos schedule', 'sfctl.custom_chaos_schedule#{}',
                          client_factory=client_create) as group:
            group.command('set', 'set_chaos_schedule')

        with CommandGroup(self, 'service', 'sfctl.custom_service#{}',
                          client_factory=client_create) as group:
            group.command('create', 'create')
            group.command('update', 'update')
            group.command('package-deploy', 'package_upload')

        with CommandGroup(self, 'is', 'sfctl.custom_is#{}',
                          client_factory=client_create) as group:
            group.command('command', 'is_command')
            group.command('query', 'is_query')

        with CommandGroup(self, 'property', 'sfctl.custom_property#{}',
                          client_factory=client_create) as group:
            group.command('put', 'naming_property_put')

        with CommandGroup(self, 'application', 'sfctl.custom_app_type#{}',
                          client_factory=client_create) as group:
            group.command('provision', 'provision_application_type')

        client_func_path_health = 'sfctl.custom_health#{}'

        with CommandGroup(self, 'application', client_func_path_health,
                          client_factory=client_create) as group:
            group.command('report-health', 'report_app_health')

        with CommandGroup(self, 'service', client_func_path_health,
                          client_factory=client_create) as group:
            group.command('report-health', 'report_svc_health')

        with CommandGroup(self, 'partition', client_func_path_health,
                          client_factory=client_create) as group:
            group.command('report-health', 'report_partition_health')

        with CommandGroup(self, 'replica', client_func_path_health,
                          client_factory=client_create) as group:
            group.command('report-health', 'report_replica_health')

        with CommandGroup(self, 'node', client_func_path_health,
                          client_factory=client_create) as group:
            group.command('report-health', 'report_node_health')

        with CommandGroup(self, 'cluster', client_func_path_health,
                          client_factory=client_create) as group:
            group.command('report-health', 'report_cluster_health')

        with CommandGroup(self, 'node', 'sfctl.custom_node#{}',
                          client_factory=client_create) as group:
            group.command('add-node-tags', 'add_node_tags')
            group.command('remove-node-tags', 'remove_node_tags')

        # ---------------
        # Settings
        # ---------------

        with CommandGroup(self, 'settings telemetry', 'sfctl.custom_settings#{}') as group:
            group.command('set-telemetry', 'set_telemetry')

        return OrderedDict(self.command_table)

    def load_arguments(self, command):
        """Load specialized arguments for commands"""
        from sfctl.params import custom_arguments

        custom_arguments(self, command)

        super(SFCommandLoader, self).load_arguments(command)

# SIG # Begin Windows Authenticode signature block
# MIIoKgYJKoZIhvcNAQcCoIIoGzCCKBcCAQExDzANBglghkgBZQMEAgEFADB5Bgor
# BgEEAYI3AgEEoGswaTA0BgorBgEEAYI3AgEeMCYCAwEAAAQQse8BENmB6EqSR2hd
# JGAGggIBAAIBAAIBAAIBAAIBADAxMA0GCWCGSAFlAwQCAQUABCCdUdn1z0VOpW80
# /AsjRkZKM0FPTUvWFBOPaYBCBgWzmqCCDXYwggX0MIID3KADAgECAhMzAAADrzBA
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
# MAwGCisGAQQBgjcCARUwLwYJKoZIhvcNAQkEMSIEIHlBhVVacsJ9HIFVfENywosG
# W4gOqx4sWQAOMayKP8AhMEIGCisGAQQBgjcCAQwxNDAyoBSAEgBNAGkAYwByAG8A
# cwBvAGYAdKEagBhodHRwOi8vd3d3Lm1pY3Jvc29mdC5jb20wDQYJKoZIhvcNAQEB
# BQAEggEASeQj42qFQr2VA1O0TGOEh9/8dE/eNF7ShLWiUgrLZt3hDhFwbLlOwaKW
# dparZMf23OjQf/umfOKw4BUX2ogmuqp5IPR1pvjBglrGiz7UVDlJFycLq2iWH1tz
# ZTbPhxFI44yMltn+HVoVfROoIUGzK35FwT7LzwAeP/mWH56LyQVcfT3eCwJ5TtS9
# B2epnSf9++Rh51xyqIvRqNkF9aRmbtVt2YDLcbyr6Iiqp5yBiM6uIpLqYTTL+No7
# bJaORoAbUUg5rcGEBxY+xP5WjTEipSPyb0oVeAsfY+/PpknOI0cwNfGcp4MJjpTY
# JaY10jpNvxIRi/y752R3q+EitbTpJaGCF5QwgheQBgorBgEEAYI3AwMBMYIXgDCC
# F3wGCSqGSIb3DQEHAqCCF20wghdpAgEDMQ8wDQYJYIZIAWUDBAIBBQAwggFSBgsq
# hkiG9w0BCRABBKCCAUEEggE9MIIBOQIBAQYKKwYBBAGEWQoDATAxMA0GCWCGSAFl
# AwQCAQUABCD7WwShF+KLuiHz2i3FWkYHiF8zZfUIXThx9BQxmX6WagIGZmrZP54r
# GBMyMDI0MDYyMDE1MDAwNC4xMzNaMASAAgH0oIHRpIHOMIHLMQswCQYDVQQGEwJV
# UzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwGA1UE
# ChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSUwIwYDVQQLExxNaWNyb3NvZnQgQW1l
# cmljYSBPcGVyYXRpb25zMScwJQYDVQQLEx5uU2hpZWxkIFRTUyBFU046QTQwMC0w
# NUUwLUQ5NDcxJTAjBgNVBAMTHE1pY3Jvc29mdCBUaW1lLVN0YW1wIFNlcnZpY2Wg
# ghHqMIIHIDCCBQigAwIBAgITMwAAAezgK6SC0JFSgAABAAAB7DANBgkqhkiG9w0B
# AQsFADB8MQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UE
# BxMHUmVkbW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSYwJAYD
# VQQDEx1NaWNyb3NvZnQgVGltZS1TdGFtcCBQQ0EgMjAxMDAeFw0yMzEyMDYxODQ1
# MzhaFw0yNTAzMDUxODQ1MzhaMIHLMQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2Fz
# aGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENv
# cnBvcmF0aW9uMSUwIwYDVQQLExxNaWNyb3NvZnQgQW1lcmljYSBPcGVyYXRpb25z
# MScwJQYDVQQLEx5uU2hpZWxkIFRTUyBFU046QTQwMC0wNUUwLUQ5NDcxJTAjBgNV
# BAMTHE1pY3Jvc29mdCBUaW1lLVN0YW1wIFNlcnZpY2UwggIiMA0GCSqGSIb3DQEB
# AQUAA4ICDwAwggIKAoICAQCwR/RuCTbgxUWVm/Vdul22uwdEZm0IoAFs6oIr39VK
# /ItP80cn+8TmtP67iabB4DmAKJ9GH6dJGhEPJpY4vTKRSOwrRNxVIKoPPeUF3f4V
# yHEco/u1QUadlwD132NuZCxbnh6Mi2lLG7pDvszZqMG7S3MCi2bk2nvtGKdeAIL+
# H77gL4r01TSWb7rsE2Jb1P/N6Y/W1CqDi1/Ib3/zRqWXt4zxvdIGcPjS4ZKyQEF3
# SEZAq4XIjiyowPHaqNbZxdf2kWO/ajdfTU85t934CXAinb0o+uQ9KtaKNLVVcNf5
# QpS4f6/MsXOvIFuCYMRdKDjpmvowAeL+1j27bCxCBpDQHrWkfPzZp/X+bt9C7E5h
# PP6HVRoqBYR7u1gUf5GEq+5r1HA0jajn0Q6OvfYckE0HdOv6KWa+sAmJG7PDvTZa
# e77homzx6IPqggVpNZuCk79SfVmnKu9F58UAnU58TqDHEzGsQnMUQKstS3zjn6SU
# 0NLEFNCetluaKkqWDRVLEWbu329IEh3tqXPXfy6Rh/wCbwe9SCJIoqtBexBrPyQY
# A2Xaz1fK9ysTsx0kA9V1JwVV44Ia9c+MwtAR6sqKdAgRo/bs/Xu8gua8LDe6KWyu
# 974e9mGW7ZO8narDFrAT1EXGHDueygSKvv2K7wB8lAgMGJj73CQvr+jqoWwx6Xdy
# eQIDAQABo4IBSTCCAUUwHQYDVR0OBBYEFPRa0Edk/iv1whYQsV8UgEf4TIWGMB8G
# A1UdIwQYMBaAFJ+nFV0AXmJdg/Tl0mWnG1M1GelyMF8GA1UdHwRYMFYwVKBSoFCG
# Tmh0dHA6Ly93d3cubWljcm9zb2Z0LmNvbS9wa2lvcHMvY3JsL01pY3Jvc29mdCUy
# MFRpbWUtU3RhbXAlMjBQQ0ElMjAyMDEwKDEpLmNybDBsBggrBgEFBQcBAQRgMF4w
# XAYIKwYBBQUHMAKGUGh0dHA6Ly93d3cubWljcm9zb2Z0LmNvbS9wa2lvcHMvY2Vy
# dHMvTWljcm9zb2Z0JTIwVGltZS1TdGFtcCUyMFBDQSUyMDIwMTAoMSkuY3J0MAwG
# A1UdEwEB/wQCMAAwFgYDVR0lAQH/BAwwCgYIKwYBBQUHAwgwDgYDVR0PAQH/BAQD
# AgeAMA0GCSqGSIb3DQEBCwUAA4ICAQCSvMSkMSrvjlDPag8ARb0OFrAQtSLMDpN0
# UY3FjvPhwGKDrrixmnuMfjrmVjRq1u8IhkDvGF/bffbFTr+IAnDSeg8TB9zfG/4y
# bknuopklbeGjbt7MLxpfholCERyEc20PMZKJz9SvzfuO1n5xrrLOL8m0nmv5kBcv
# +y1AXJ5QcLicmhe2Ip3/D67Ed6oPqQI03mDjYaS1NQhBNtu57wPKXZ1EoNToBk8b
# A6839w119b+a9WToqIskdRGoP5xjDIv+mc0vBHhZGkJVvfIhm4Ap8zptC7xVAly0
# jeOv5dUGMCYgZjvoTmgd45bqAwundmPlGur7eleWYedLQf7s3L5+qfaY/xEh/9uo
# 17SnM/gHVSGAzvnreGhOrB2LtdKoVSe5LbYpihXctDe76iYtL+mhxXPEpzda3bJl
# hPTOQ3KOEZApVERBo5yltWjPCWlXxyCpl5jj9nY0nfd071bemnou8A3rUZrdgKIa
# utsH7SHOiOebZGqNu+622vJta3eAYsCAaxAcB9BiJPla7Xad9qrTYdT45VlCYTtB
# SY4oVRsedSADv99jv/iYIAGy1bCytua0o/Qqv9erKmzQCTVMXaDc25DTLcMGJrRu
# a3K0xivdtnoBexzVJr6yXqM+Ba2whIVRvGcriBkKX0FJFeW7r29XX+k0e4DnG6iB
# HKQjec6VNzCCB3EwggVZoAMCAQICEzMAAAAVxedrngKbSZkAAAAAABUwDQYJKoZI
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
# MCUGA1UECxMeblNoaWVsZCBUU1MgRVNOOkE0MDAtMDVFMC1EOTQ3MSUwIwYDVQQD
# ExxNaWNyb3NvZnQgVGltZS1TdGFtcCBTZXJ2aWNloiMKAQEwBwYFKw4DAhoDFQCO
# HPtgVdz9EW0iPNL/BXqJoqVMf6CBgzCBgKR+MHwxCzAJBgNVBAYTAlVTMRMwEQYD
# VQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVNaWNy
# b3NvZnQgQ29ycG9yYXRpb24xJjAkBgNVBAMTHU1pY3Jvc29mdCBUaW1lLVN0YW1w
# IFBDQSAyMDEwMA0GCSqGSIb3DQEBCwUAAgUA6h6RkDAiGA8yMDI0MDYyMDExMzEy
# OFoYDzIwMjQwNjIxMTEzMTI4WjB0MDoGCisGAQQBhFkKBAExLDAqMAoCBQDqHpGQ
# AgEAMAcCAQACAggGMAcCAQACAhNsMAoCBQDqH+MQAgEAMDYGCisGAQQBhFkKBAIx
# KDAmMAwGCisGAQQBhFkKAwKgCjAIAgEAAgMHoSChCjAIAgEAAgMBhqAwDQYJKoZI
# hvcNAQELBQADggEBADEUnqpOO4ssnLP9MW3rdZWF8MtyBLv8vAj4EN4wDNT3S+eM
# jq+TbfGYqz/91mOuQYAqtUxW2z5FzTK7oGLUlqLBTf4kaOjQ3bIbej7CspO8WhDG
# vCFnqWmTjx9909/nMuvAsNRUdl15PPsL9g4/koQrbWPSip4cQ1rhpnxEo7kkP4YP
# tV0GVlAxKmkgsmakeNH8d8caZxTmYxB7fKQdlRq52fwnkxwTd/XjjhlNiJn+9o5s
# /HrYaJx4G/fUc9zbT/23waOqkJBF4Mga06lSPMKCow7qxXbXsq+kXyzg5Onk2+eu
# WppA+xQVQzMCd/gLBJd3VDkCaux84EikAdYdYZ4xggQNMIIECQIBATCBkzB8MQsw
# CQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9u
# ZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSYwJAYDVQQDEx1NaWNy
# b3NvZnQgVGltZS1TdGFtcCBQQ0EgMjAxMAITMwAAAezgK6SC0JFSgAABAAAB7DAN
# BglghkgBZQMEAgEFAKCCAUowGgYJKoZIhvcNAQkDMQ0GCyqGSIb3DQEJEAEEMC8G
# CSqGSIb3DQEJBDEiBCDVggJ/oDFgEq8vx/BsRuSc3mkJmanSsPMfd1lHBmyVuDCB
# +gYLKoZIhvcNAQkQAi8xgeowgecwgeQwgb0EICcJ5vVqfTfIhx21QBBbKyo/xciQ
# IXaoMWULejAE1QqDMIGYMIGApH4wfDELMAkGA1UEBhMCVVMxEzARBgNVBAgTCldh
# c2hpbmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29mdCBD
# b3Jwb3JhdGlvbjEmMCQGA1UEAxMdTWljcm9zb2Z0IFRpbWUtU3RhbXAgUENBIDIw
# MTACEzMAAAHs4CukgtCRUoAAAQAAAewwIgQgJfj+/uHgptLFvuzTKH4AJJaJUS86
# 8THuToorLBW/tyQwDQYJKoZIhvcNAQELBQAEggIAZFZ3DOvlqBwqf8qHSM8A6vRc
# 1cdDjySWgTjTI6Xs7HeSN7/kNI9KjBkzu/2fUszZZqFE6RjIUGe4F6+qeu+MMlFa
# bRQqoJdiznR5rg2pf2VGXozJZAIo1O+aPsly30MUx1KDSObzTNvyvZ++tWWDNwG+
# qEL+wbtPwBt5G0HkseEGYA2VbH38C6/EWEGpiwPQsG7sdGLHGp4qE8zYQaBtqixr
# VpMr5Ob120NsB0ugwv5Q3/1nA+aIOfkrjDI5NsbQN4eYE6coxZ+0J4Dyho/rpNXA
# +pOc2sInHcd5FSRzp65UkbF/+c7BXHu3C+4zsvBAbScB2MwC4CphYNGeEGBcimeK
# PzGFXcJn1HzPE33nCDStOYMhRgjj/HWVH8VvvGSD2Iw9VFP1sSL9Crwj7BFZUUfB
# oZklOW3GW0d/SWyfLdy5qUVmURfueQ1+t9Fous5aBenwtf3bXt1xc1OWdmLgUSKk
# 62AVRfbviaGjT1B9j/ttqhMmkaTj8nx0e7gEZ1svPu/ZOo6ICCzG4VrUVPeAjgMr
# hC02JY8t4i02338lqCokJw3Wd/2x8DR6M6AGX5JmUnKzM4dCbr+IbLML6y4iUgyP
# dgDF0Ea6sgHB+/X9DJJ6zQUXHcgJBrhn0aDbFc4r71wy3q9oEmEMmjW7cCuPJcwt
# B0HEW4EAJP7fl9Owc2I=
# SIG # End Windows Authenticode signature block