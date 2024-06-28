# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Commands related to managing Service Fabric services"""

from knack.util import CLIError


def correlation_desc(correlated_service, correlation):
    """Get a service correlation description"""
    from azure.servicefabric.models import ServiceCorrelationDescription

    if not any([correlated_service, correlation]):
        return None

    if (any([correlated_service, correlation]) and
            not all([correlated_service, correlation])):
        raise CLIError('Must specify both a correlation service and '
                       'correlation scheme')

    return ServiceCorrelationDescription(scheme=correlation, service_name=correlated_service)


def parse_load_metrics(formatted_metrics):
    """Parse a service load metric description from a string"""
    from azure.servicefabric.models import ServiceLoadMetricDescription

    s_load_list = None
    if formatted_metrics:
        s_load_list = []
        for item in formatted_metrics:
            l_name = item.get('name', None)
            if l_name is None:
                raise CLIError('Could not find specified load metric name')
            l_weight = item.get('weight', None)
            l_primary = item.get('primary_default_load', None)
            l_secondary = item.get('secondary_default_load', None)
            l_default = item.get('default_load', None)
            l_desc = ServiceLoadMetricDescription(name=l_name,
                                                  weight=l_weight,
                                                  primary_default_load=l_primary,
                                                  secondary_default_load=l_secondary,
                                                  default_load=l_default)
            s_load_list.append(l_desc)

    return s_load_list


def parse_placement_policies(formatted_placement_policies):
    """"Parse a placement policy description from a formatted policy"""

    from azure.servicefabric.models import (ServicePlacementNonPartiallyPlaceServicePolicyDescription, # pylint: disable=line-too-long
                                            ServicePlacementPreferPrimaryDomainPolicyDescription,
                                            ServicePlacementRequiredDomainPolicyDescription,
                                            ServicePlacementRequireDomainDistributionPolicyDescription) # pylint: disable=line-too-long

    if formatted_placement_policies:
        policy_list = []
        # Not entirely documented but similar to the property names
        for policy in formatted_placement_policies:
            p_type = policy.get("type", None)
            if p_type is None:
                raise CLIError(
                    'Could not determine type of specified placement policy'
                )
            if p_type not in ['NonPartiallyPlaceService',
                              'PreferPrimaryDomain', 'RequireDomain',
                              'RequireDomainDistribution']:
                raise CLIError('Invalid type of placement policy specified')
            p_domain_name = policy.get('domain_name', None)

            if p_domain_name is None and p_type != 'NonPartiallyPlaceService':
                raise CLIError(
                    'Placement policy type requires target domain name'
                )
            if p_type == 'NonPartiallyPlaceService':
                policy_list.append(
                    ServicePlacementNonPartiallyPlaceServicePolicyDescription()
                )
            elif p_type == 'PreferPrimaryDomain':
                policy_list.append(
                    ServicePlacementPreferPrimaryDomainPolicyDescription(domain_name=p_domain_name)
                )
            elif p_type == 'RequireDomain':
                policy_list.append(
                    ServicePlacementRequiredDomainPolicyDescription(domain_name=p_domain_name)
                )
            elif p_type == 'RequireDomainDistribution':
                policy_list.append(
                    ServicePlacementRequireDomainDistributionPolicyDescription(
                        domain_name=p_domain_name
                    )
                )
        return policy_list
    return None


def validate_move_cost(move_cost):
    """Validate move cost argument"""

    if move_cost not in [None, 'Zero', 'Low', 'Medium', 'High', 'VeryHigh']:
        raise CLIError('Invalid move cost specified')


def stateful_flags(rep_restart_wait=None, quorum_loss_wait=None,
                   standby_replica_keep=None, service_placement_time=None):
    """Calculate an integer representation of flag arguments for stateful
    services"""

    flag_sum = 0
    if rep_restart_wait is not None:
        flag_sum += 1
    if quorum_loss_wait is not None:
        flag_sum += 2
    if standby_replica_keep is not None:
        flag_sum += 4
    if service_placement_time is not None:
        flag_sum += 8
    return flag_sum


def service_update_flags(  # pylint: disable=too-many-arguments, too-many-branches
        target_rep_size=None, instance_count=None, rep_restart_wait=None,
        quorum_loss_wait=None, standby_rep_keep=None, min_rep_size=None,
        placement_constraints=None, placement_policy=None, correlation=None,
        metrics=None, move_cost=None, scaling_policy=None, service_placement_time=None,
        tags_required_to_place=None, tags_required_to_run=None):
    """Calculate an integer representation of flag arguments for updating
    stateful services"""

    flag_sum = 0
    if (target_rep_size is not None) or (instance_count is not None):
        flag_sum += 1
    if rep_restart_wait is not None:
        flag_sum += 2
    if quorum_loss_wait is not None:
        flag_sum += 4
    if standby_rep_keep is not None:
        flag_sum += 8
    if min_rep_size is not None:
        flag_sum += 16
    if placement_constraints is not None:
        flag_sum += 32
    if placement_policy is not None:
        flag_sum += 64
    if correlation is not None:
        flag_sum += 128
    if metrics is not None:
        flag_sum += 256
    if move_cost is not None:
        flag_sum += 512
    if scaling_policy is not None:
        flag_sum += 1024
    if service_placement_time is not None:
        flag_sum += 2048
    if tags_required_to_place is not None:
        flag_sum += 1048576
    if tags_required_to_run is not None:
        flag_sum += 2097152
    return flag_sum


def validate_service_create_params(stateful, stateless, singleton_scheme,  # pylint: disable=too-many-arguments
                                   int_scheme, named_scheme, instance_count,
                                   target_rep_set_size, min_rep_set_size):
    """Validate service creation arguments"""
    if sum([stateful, stateless]) != 1:
        raise CLIError(
            'Specify either stateful or stateless for the service type'
        )
    if sum([singleton_scheme, named_scheme, int_scheme]) != 1:
        raise CLIError('Specify exactly one partition scheme from --singleton-scheme, '
                       '--named-scheme, or --int-scheme')
    if stateful and instance_count is not None:
        raise CLIError('Cannot specify instance count for stateful services')
    if stateless and instance_count is None:
        raise CLIError('Must specify instance count for stateless services')
    if stateful and not all([target_rep_set_size, min_rep_set_size]):
        raise CLIError(
            'Must specify minimum and replica set size for stateful services'
        )
    if stateless and any([target_rep_set_size, min_rep_set_size]):
        raise CLIError(
            'Cannot specify replica set sizes for stateless services'
        )


def parse_partition_policy(named_scheme, named_scheme_list, int_scheme,  # pylint: disable=too-many-arguments
                           int_scheme_low, int_scheme_high, int_scheme_count,
                           singleton_scheme):
    """Create a partition scheme"""
    from azure.servicefabric.models import (NamedPartitionSchemeDescription,
                                            SingletonPartitionSchemeDescription,
                                            UniformInt64RangePartitionSchemeDescription)

    if named_scheme and not named_scheme_list:
        raise CLIError('When specifying named partition scheme, must include '
                       'list of names')
    if (int_scheme
            and not all([int_scheme_low, int_scheme_high, int_scheme_count])):
        raise CLIError('Must specify the full integer range and partition '
                       'count when using an uniform integer partition scheme')

    if not sum([named_scheme, int_scheme, singleton_scheme]) == 1:
        raise CLIError('Specify exactly one partition scheme from --singleton-scheme, '
                       '--named-scheme, or --int-scheme')

    if named_scheme:
        return NamedPartitionSchemeDescription(count=len(named_scheme_list),
                                               names=named_scheme_list)
    if int_scheme:
        return UniformInt64RangePartitionSchemeDescription(count=int_scheme_count,
                                                           low_key=int_scheme_low,
                                                           high_key=int_scheme_high)
    if singleton_scheme:
        return SingletonPartitionSchemeDescription()

    return None


def validate_activation_mode(activation_mode):
    """Validate activation mode parameters"""
    if activation_mode not in [None, 'SharedProcess', 'ExclusiveProcess']:
        raise CLIError('Invalid activation mode specified')


def parse_scaling_mechanism(scaling_mechanism):
    """"Parse a scaling mechanism description"""
    from azure.servicefabric.models import (AddRemoveIncrementalNamedPartitionScalingMechanism,
                                            PartitionInstanceCountScaleMechanism)

    if scaling_mechanism:
        p_kind = scaling_mechanism.get('kind')
        if p_kind is None:
            raise CLIError('Invalid scaling mechanism specified')
        if p_kind not in ['PartitionInstanceCount', 'AddRemoveIncrementalNamedPartition']:
            raise CLIError('Invalid scaling mechanism specified')
        if p_kind == 'PartitionInstanceCount':
            p_min_count = scaling_mechanism.get('min_instance_count', None)
            p_max_count = scaling_mechanism.get('max_instance_count', None)
            p_scale_increment = scaling_mechanism.get('scale_increment', None)
            return PartitionInstanceCountScaleMechanism(
                min_instance_count=p_min_count,
                max_instance_count=p_max_count,
                scale_increment=p_scale_increment
            )
        if p_kind == 'AddRemoveIncrementalNamedPartition':
            p_min_count = scaling_mechanism.get('min_partition_count', None)
            p_max_count = scaling_mechanism.get('max_partition_count', None)
            p_scale_increment = scaling_mechanism.get('scale_increment', None)
            return AddRemoveIncrementalNamedPartitionScalingMechanism(
                min_partition_count=p_min_count,
                max_partition_count=p_max_count,
                scale_increment=p_scale_increment
            )

    return None


def parse_scaling_trigger(scaling_trigger):
    """"Parse a scaling trigger description"""
    from azure.servicefabric.models import (AveragePartitionLoadScalingTrigger,
                                            AverageServiceLoadScalingTrigger)

    if scaling_trigger:
        p_kind = scaling_trigger.get('kind')
        if p_kind is None:
            raise CLIError('Invalid scaling trigger specified')
        if p_kind not in ['AveragePartitionLoad', 'AverageServiceLoad']:
            raise CLIError('Invalid scaling trigger specified')
        if p_kind == 'AveragePartitionLoad':
            p_metricname = scaling_trigger.get('metric_name', None)
            p_upper_load_threshold = scaling_trigger.get('upper_load_threshold', None)
            p_lower_load_threshold = scaling_trigger.get('lower_load_threshold', None)
            p_scale_interval = scaling_trigger.get('scale_interval_in_seconds', None)
            return AveragePartitionLoadScalingTrigger(
                metric_name=p_metricname,
                lower_load_threshold=p_lower_load_threshold,
                upper_load_threshold=p_upper_load_threshold,
                scale_interval_in_seconds=p_scale_interval
            )

        if p_kind == 'AverageServiceLoad':
            p_metricname = scaling_trigger.get('metric_name', None)
            p_upper_load_threshold = scaling_trigger.get('upper_load_threshold', None)
            p_lower_load_threshold = scaling_trigger.get('lower_load_threshold', None)
            p_scale_interval = scaling_trigger.get('scale_interval_in_seconds', None)
            p_scale_interval = scaling_trigger.get('scale_interval_in_seconds', None)
            p_use_only_primary_load  = scaling_trigger.get('use_only_primary_load', False)
            return AverageServiceLoadScalingTrigger(
                metric_name=p_metricname,
                lower_load_threshold=p_lower_load_threshold,
                upper_load_threshold=p_upper_load_threshold,
                scale_interval_in_seconds=p_scale_interval,
                use_only_primary_load=p_use_only_primary_load
            )

    return None


def parse_scaling_policy(formatted_scaling_policy):
    """"Parse a scaling policy description from a formatted policy"""
    from azure.servicefabric.models import ScalingPolicyDescription
    scaling_list = None
    if formatted_scaling_policy:
        scaling_list = []
        for item in formatted_scaling_policy:
            scaling_trigger_string = item.get('trigger', None)
            if scaling_trigger_string is None:
                raise CLIError('No scaling trigger specified')
            scaling_trigger = parse_scaling_trigger(scaling_trigger_string)
            scaling_mechanism_string = item.get('mechanism', None)
            if scaling_mechanism_string is None:
                raise CLIError('No scaling mechanism specified')
            scaling_mechanism = parse_scaling_mechanism(scaling_mechanism_string)
            scaling_policy = ScalingPolicyDescription(scaling_trigger=scaling_trigger,
                                                      scaling_mechanism=scaling_mechanism)
            scaling_list.append(scaling_policy)

    return scaling_list

def parse_service_tags(service_tags):
    """Parse service tags from string"""
    from azure.servicefabric.models import NodeTagsDescription
    if service_tags:
        return NodeTagsDescription(count=len(service_tags),
                                    tags=service_tags)
    return None


def create(  # pylint: disable=too-many-arguments, too-many-locals
        client, app_id, name, service_type, stateful=False, stateless=False,
        singleton_scheme=False, named_scheme=False, int_scheme=False,
        named_scheme_list=None, int_scheme_low=None, int_scheme_high=None,
        int_scheme_count=None, constraints=None, correlated_service=None,
        correlation=None, load_metrics=None, placement_policy_list=None,
        move_cost=None, activation_mode=None, dns_name=None,
        target_replica_set_size=None, min_replica_set_size=None,
        replica_restart_wait=None, quorum_loss_wait=None,
        stand_by_replica_keep=None, no_persisted_state=False,
        instance_count=None, timeout=60, scaling_policies=None,
        service_placement_time=None, tags_required_to_place=None, tags_required_to_run=None):
    """
    Creates the specified Service Fabric service.
    :param str app_id: The identity of the application. This is
    typically the full name of the application without the 'fabric:' URI
    scheme. Starting from version 6.0, hierarchical names are delimited with
    the '~' character. For example, if the application name is
    'fabric:/myapp/app1', the application identity would be 'myapp~app1' in
    6.0+ and 'myapp/app1' in previous versions.
    :param str name: Name of the service. This should be a child of the
    application id. This is the full name including the `fabric:` URI.
    For example service `fabric:/A/B` is a child of application
    `fabric:/A`.
    :param str service_type: Name of the service type.
    :param bool stateful: Indicates the service is a stateful service.
    :param bool stateless: Indicates the service is a stateless service.
    :param bool singleton_scheme: Indicates the service should have a single
    partition or be a non-partitioned service.
    :param bool named_scheme: Indicates the service should have multiple named
    partitions.
    :param list of str named_scheme_list: JSON encoded list of names to
    partition the service across, if using the named partition scheme
    :param bool int_scheme: Indicates the service should be uniformly
    partitioned across a range of unsigned integers.
    :param str int_scheme_low: The start of the key integer range, if using an
    uniform integer partition scheme.
    :param str int_scheme_high: The end of the key integer range, if using an
    uniform integer partition scheme.
    :param str int_scheme_count: The number of partitions inside the integer
    key range to create, if using a uniform integer partition scheme.
    :param str constraints: The placement constraints as a string. Placement
    constraints are boolean expressions on node properties and allow for
    restricting a service to particular nodes based on the service
    requirements. For example, to place a service on nodes where NodeType
    is blue specify the following:"NodeColor == blue".
    :param str correlation: Correlate the service with an existing service
    using an alignment affinity. Possible values include: 'Invalid',
    'Affinity', 'AlignedAffinity', 'NonAlignedAffinity'.
    :param str load_metrics: JSON encoded list of metrics used when load
    balancing services across nodes.
    :param str placement_policy_list: JSON encoded list of placement policies
    for the service, and any associated domain names. Policies can be one or
    more of: `NonPartiallyPlaceService`, `PreferPrimaryDomain`,
    `RequireDomain`, `RequireDomainDistribution`.
    :param str correlated_service: Name of the target service to correlate
    with.
    :param str move_cost: Specifies the move cost for the service. Possible
    values are: 'Zero', 'Low', 'Medium', 'High', 'VeryHigh'.
    :param str activation_mode: The activation mode for the service package.
    Possible values include: 'SharedProcess', 'ExclusiveProcess'.
    :param str dns_name: The DNS name of the service to be created. The Service
    Fabric DNS system service must be enabled for this setting.
    :param int target_replica_set_size: The target replica set size as a
    number. This applies to stateful services only.
    :param int min_replica_set_size: The minimum replica set size as a number.
    This applies to stateful services only.
    :param int replica_restart_wait: The duration, in seconds, between when a
    replica goes down and when a new replica is created. This applies to
    stateful services only.
    :param int quorum_loss_wait: The maximum duration, in seconds, for which a
    partition is allowed to be in a state of quorum loss. This applies to
    stateful services only.
    :param int stand_by_replica_keep: The maximum duration, in seconds,  for
    which StandBy replicas will be maintained before being removed. This
    applies to stateful services only.
    :param bool no_persisted_state: If true, this indicates the service has no
    persistent state stored on the local disk, or it only stores state in
    memory.
    :param int instance_count: The instance count. This applies to stateless
    services only.
    :param str scaling_policies: JSON encoded list of scaling policies for this service.
    :param list of str tags_required_to_place: JSON encoded list of tags to
    require to place the service, if using node tagging feature
    :param list of str tags_required_to_run: JSON encoded list of tags to
    require to run the service, if using node tagging feature
    :param int service_placement_time: The duration for which replicas can stay
    InBuild before reporting that build is stuck. This
    applies to stateful services only.
    """
    from azure.servicefabric.models import StatelessServiceDescription, StatefulServiceDescription

    validate_service_create_params(stateful, stateless, singleton_scheme,
                                   int_scheme, named_scheme, instance_count,
                                   target_replica_set_size,
                                   min_replica_set_size)
    partition_desc = parse_partition_policy(named_scheme, named_scheme_list,
                                            int_scheme, int_scheme_low,
                                            int_scheme_high, int_scheme_count,
                                            singleton_scheme)
    cor_desc = correlation_desc(correlated_service, correlation)
    load_list = parse_load_metrics(load_metrics)
    place_policy = parse_placement_policies(placement_policy_list)
    validate_move_cost(move_cost)
    validate_activation_mode(activation_mode)
    scaling_policy_description = parse_scaling_policy(scaling_policies)
    tags_required_to_place_description = parse_service_tags(tags_required_to_place)
    tags_required_to_run_description = parse_service_tags(tags_required_to_run)

    if stateless:
        svc_desc = StatelessServiceDescription(service_name=name,
                                               service_type_name=service_type,
                                               partition_description=partition_desc,
                                               instance_count=instance_count,
                                               application_name="fabric:/" + app_id,
                                               initialization_data=None,
                                               placement_constraints=constraints,
                                               correlation_scheme=cor_desc,
                                               service_load_metrics=load_list,
                                               service_placement_policies=place_policy,
                                               default_move_cost=move_cost,
                                               is_default_move_cost_specified=bool(move_cost),
                                               service_package_activation_mode=activation_mode,
                                               service_dns_name=dns_name,
                                               scaling_policies=scaling_policy_description,
                                               tags_required_to_place=tags_required_to_place_description,
                                               tags_required_to_run=tags_required_to_run_description)

    if stateful:
        flags = stateful_flags(replica_restart_wait, quorum_loss_wait,
                               stand_by_replica_keep, service_placement_time)
        svc_desc = StatefulServiceDescription(
            service_name=name,
            service_type_name=service_type,
            partition_description=partition_desc,
            target_replica_set_size=target_replica_set_size,
            min_replica_set_size=min_replica_set_size,
            has_persisted_state=not no_persisted_state,
            application_name="fabric:/" + app_id,
            initialization_data=None,
            placement_constraints=constraints,
            correlation_scheme=cor_desc,
            service_load_metrics=load_list,
            service_placement_policies=place_policy,
            default_move_cost=move_cost,
            is_default_move_cost_specified=bool(move_cost),
            service_package_activation_mode=activation_mode,
            service_dns_name=dns_name,
            scaling_policies=scaling_policy_description,
            flags=flags,
            replica_restart_wait_duration_seconds=replica_restart_wait,
            quorum_loss_wait_duration_seconds=quorum_loss_wait,
            stand_by_replica_keep_duration_seconds=stand_by_replica_keep,
            service_placement_time_limit_seconds=service_placement_time,
            tags_required_to_place=tags_required_to_place_description,
            tags_required_to_run=tags_required_to_run_description)

    client.create_service(app_id, svc_desc, timeout)


def validate_update_service_params(stateless, stateful, target_rep_set_size,  # pylint: disable=too-many-arguments
                                   min_rep_set_size, rep_restart_wait,
                                   quorum_loss_wait, stand_by_replica_keep,
                                   instance_count, service_placement_time):
    """Validate update service parameters"""

    if sum([stateless, stateful]) != 1:
        raise CLIError('Must specify either stateful or stateless, not both')

    if stateless:
        if target_rep_set_size is not None:
            raise CLIError('Cannot specify target replica set size for '
                           'stateless service')
        if min_rep_set_size is not None:
            raise CLIError('Cannot specify minimum replica set size for '
                           'stateless service')
        if rep_restart_wait is not None:
            raise CLIError('Cannot specify replica restart wait duration '
                           'for stateless service')
        if quorum_loss_wait is not None:
            raise CLIError('Cannot specify quorum loss wait duration for '
                           'stateless service')
        if stand_by_replica_keep is not None:
            raise CLIError('Cannot specify standby replica keep duration for '
                           'stateless service')
        if service_placement_time is not None:
            raise CLIError('Cannot specify service placement time limit for '
                           'stateless service')
    if stateful:
        if instance_count is not None:
            raise CLIError('Cannot specify an instance count for a stateful '
                           'service')


def update(client, service_id, stateless=False, stateful=False,  # pylint: disable=too-many-locals,too-many-arguments
           constraints=None, correlation=None, correlated_service=None,
           load_metrics=None, placement_policy_list=None,
           move_cost=None, instance_count=None, target_replica_set_size=None,
           min_replica_set_size=None, replica_restart_wait=None,
           quorum_loss_wait=None, stand_by_replica_keep=None, timeout=60,
           scaling_policies=None, service_placement_time=None,
           tags_required_to_place=None, tags_required_to_run=None):
    """
    Updates the specified service using the given update description.
    :param str service_id: The identity of the service. This is typically the
    full name of the service without the 'fabric:' URI scheme. Starting from
    version 6.0, hierarchical names are delimited with the "~" character. For
    example, if the service name is 'fabric:/myapp/app1/svc1', the service
    identity would be 'myapp~app1~svc1' in 6.0+ and 'myapp/app1/svc1' in
    previous versions.
    :param bool stateless: Indicates the target service is a stateless service.
    :param bool stateful: Indicates the target service is a stateful service.
    :param str constraints: The placement constraints as a string. Placement
    constraints are boolean expressions on node properties and allow for
    restricting a service to particular nodes based on the service
    requirements. For example, to place a service on nodes where NodeType is
    blue specify the following: "NodeColor == blue".
    :param str correlation: Correlate the service with an existing service
    using an alignment affinity. Possible values include: 'Invalid',
    'Affinity', 'AlignedAffinity', 'NonAlignedAffinity'.
    :param str correlated_service: Name of the target service to correlate
    with.
    :param str load_metrics: JSON encoded list of metrics
    used when load balancing across nodes.
    :param str placement_policy_list: JSON encoded list of placement policies
    for the service, and any associated domain names. Policies can be one or
    more of: `NonPartiallyPlaceService`, `PreferPrimaryDomain`,
    `RequireDomain`, `RequireDomainDistribution`.
    :param str move_cost: Specifies the move cost for the service. Possible
    values are: 'Zero', 'Low', 'Medium', 'High', 'VeryHigh'.
    :param int instance_count: The instance count. This applies to stateless
    services only.
    :param int target_replica_set_size: The target replica set size as a
    number. This applies to stateful services only.
    :param int min_replica_set_size: The minimum replica set size as a number.
    This applies to stateful services only.
    :param str replica_restart_wait: The duration, in seconds, between when a
    replica goes down and when a new replica is created. This applies to
    stateful services only.
    :param str quorum_loss_wait: The maximum duration, in seconds, for which a
    partition is allowed to be in a state of quorum loss. This applies to
    stateful services only.
    :param str stand_by_replica_keep: The maximum duration, in seconds,  for
    which StandBy replicas will be maintained before being removed. This
    applies to stateful services only.
    :param str scaling_policies: JSON encoded list of scaling policies for this service.
    :param list of str tags_required_to_place: JSON encoded list of tags to
    require to place the service, if using node tagging feature
    :param list of str tags_required_to_run: JSON encoded list of tags to
    require to run the service, if using node tagging feature
    :param int service_placement_time: The duration for which replicas can stay
    InBuild before reporting that build is stuck. This
    applies to stateful services only.
    """
    from azure.servicefabric.models import (StatefulServiceUpdateDescription,
                                            StatelessServiceUpdateDescription)

    validate_update_service_params(stateless, stateful,
                                   target_replica_set_size,
                                   min_replica_set_size, replica_restart_wait,
                                   quorum_loss_wait, stand_by_replica_keep,
                                   instance_count, service_placement_time)

    cor_desc = correlation_desc(correlated_service, correlation)
    metric_desc = parse_load_metrics(load_metrics)
    place_desc = parse_placement_policies(placement_policy_list)
    validate_move_cost(move_cost)
    scaling_policy_description = parse_scaling_policy(scaling_policies)
    tags_required_to_place_description = parse_service_tags(tags_required_to_place)
    tags_required_to_run_description = parse_service_tags(tags_required_to_run)

    flags = service_update_flags(target_replica_set_size, instance_count,
                                 replica_restart_wait, quorum_loss_wait,
                                 stand_by_replica_keep, min_replica_set_size,
                                 constraints, place_desc, cor_desc,
                                 metric_desc, move_cost, scaling_policy_description,
                                 service_placement_time)

    update_desc = None
    if stateful:
        update_desc = StatefulServiceUpdateDescription(
            flags=flags,
            placement_constraints=constraints,
            correlation_scheme=cor_desc,
            load_metrics=metric_desc,
            service_placement_policies=place_desc,
            default_move_cost=move_cost,
            scaling_policies=scaling_policy_description,
            target_replica_set_size=target_replica_set_size,
            min_replica_set_size=min_replica_set_size,
            replica_restart_wait_duration_seconds=replica_restart_wait,
            quorum_loss_wait_duration_seconds=quorum_loss_wait,
            stand_by_replica_keep_duration_seconds=stand_by_replica_keep,
            service_placement_time_limit_seconds=service_placement_time,
            tags_required_to_place=tags_required_to_place_description,
            tags_required_to_run=tags_required_to_run_description)

    if stateless:
        update_desc = StatelessServiceUpdateDescription(flags=flags,
                                                        placement_constraints=constraints,
                                                        correlation_scheme=cor_desc,
                                                        load_metrics=metric_desc,
                                                        service_placement_policies=place_desc,
                                                        default_move_cost=move_cost,
                                                        scaling_policies=scaling_policy_description,
                                                        instance_count=instance_count,
                                                        tags_required_to_place=tags_required_to_place_description,
                                                        tags_required_to_run=tags_required_to_run_description)

    client.update_service(service_id, update_desc, timeout)


def parse_package_sharing_policies(formatted_policies):
    """Parse package sharing policy description from a JSON encoded set of
    policies"""
    from azure.servicefabric.models import PackageSharingPolicyInfo
    if not formatted_policies:
        return None

    list_psps = []
    for policy in formatted_policies:
        policy_name = policy.get("name", None)
        if policy_name is None:
            raise CLIError('Could not find name of sharing policy element')
        policy_scope = policy.get("scope", None)
        if policy_scope not in [None, 'All', 'Code', 'Config', 'Data']:
            raise CLIError('Invalid policy scope specified')
        list_psps.append(PackageSharingPolicyInfo(shared_package_name=policy_name,
                                                  package_sharing_scope=policy_scope))
    return list_psps


def package_upload(client, node_name, service_manifest_name, app_type_name,  # pylint: disable=too-many-arguments
                   app_type_version, share_policy=None, timeout=60):
    """
    Downloads packages associated with specified service manifest to the image
    cache on specified node.
    :param str node_name: The name of the node.
    :param str service_manifest_name: The name of service manifest associated
    with the packages that will be downloaded.
    :param str app_type_name: The name of the application manifest for
    the corresponding requested service manifest.
    :param str app_type_version: The version of the application
    manifest for the corresponding requested service manifest.
    :param str share_policy: JSON encoded list of sharing policies. Each
    sharing policy element is composed of a 'name' and 'scope'. The name
    corresponds to the name of the code, configuration, or data package that
    is to be shared. The scope can be either 'None', 'All', 'Code', 'Config' or
    'Data'.
    """
    from azure.servicefabric.models import DeployServicePackageToNodeDescription

    list_psps = parse_package_sharing_policies(share_policy)

    desc = DeployServicePackageToNodeDescription(service_manifest_name=service_manifest_name,
                                                 application_type_name=app_type_name,
                                                 application_type_version=app_type_version,
                                                 node_name=node_name,
                                                 package_sharing_policy=list_psps)
    client.deployed_service_package_to_node(node_name, desc, timeout)

# SIG # Begin Windows Authenticode signature block
# MIIoKgYJKoZIhvcNAQcCoIIoGzCCKBcCAQExDzANBglghkgBZQMEAgEFADB5Bgor
# BgEEAYI3AgEEoGswaTA0BgorBgEEAYI3AgEeMCYCAwEAAAQQse8BENmB6EqSR2hd
# JGAGggIBAAIBAAIBAAIBAAIBADAxMA0GCWCGSAFlAwQCAQUABCBzXDF75nc1Izdq
# ZxrhF2re2tgSlMowy5WZfhqffrLxTqCCDXYwggX0MIID3KADAgECAhMzAAADrzBA
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
# MAwGCisGAQQBgjcCARUwLwYJKoZIhvcNAQkEMSIEINqebKmuywD+a3H9sM15+Ftl
# Fg8BGwA5gBNJC6Hks8ndMEIGCisGAQQBgjcCAQwxNDAyoBSAEgBNAGkAYwByAG8A
# cwBvAGYAdKEagBhodHRwOi8vd3d3Lm1pY3Jvc29mdC5jb20wDQYJKoZIhvcNAQEB
# BQAEggEAcrvbJDryK8VBkCP9JXdWSB9DzsELl9DNUGm9XgsOe014qiYPsw7EOVvw
# k7zUmw6j+5qnDReqra/3g136kYWcGjY2ZHEcEn6EfEIvQbl9D1aOCbEGfxm+Ym0N
# GnwBt9GEmtrkSTk3u/ZLRIUYNveQnPKr7Yui6YRrzt224gnSrxOp7MNiZJOgJtIv
# 8bX3/JMzL1ezbRfRCX0eiQai6U5plN539Lc8YEFwhSKfH2IcXBjdyWqbVvZZJrSU
# ShjLpLlsry/ueAaFzpkTlRPBzCt8NV/bkweemLS8s9ZSQXjHUf9XZyMXpmR4upMC
# fuQeyAzmTnLHlu4g446qrP6EuxJhtqGCF5QwgheQBgorBgEEAYI3AwMBMYIXgDCC
# F3wGCSqGSIb3DQEHAqCCF20wghdpAgEDMQ8wDQYJYIZIAWUDBAIBBQAwggFSBgsq
# hkiG9w0BCRABBKCCAUEEggE9MIIBOQIBAQYKKwYBBAGEWQoDATAxMA0GCWCGSAFl
# AwQCAQUABCBg87AVGxz/9EEEe0CPOqe4+Kz7/82pyHkevtkBOsSdcQIGZmrZP54n
# GBMyMDI0MDYyMDE1MDAwNC4xMTdaMASAAgH0oIHRpIHOMIHLMQswCQYDVQQGEwJV
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
# CSqGSIb3DQEJBDEiBCBO+3J+kZLznZ0xs+/QJD8O+ybV+kAjskakgyEOblW6hzCB
# +gYLKoZIhvcNAQkQAi8xgeowgecwgeQwgb0EICcJ5vVqfTfIhx21QBBbKyo/xciQ
# IXaoMWULejAE1QqDMIGYMIGApH4wfDELMAkGA1UEBhMCVVMxEzARBgNVBAgTCldh
# c2hpbmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29mdCBD
# b3Jwb3JhdGlvbjEmMCQGA1UEAxMdTWljcm9zb2Z0IFRpbWUtU3RhbXAgUENBIDIw
# MTACEzMAAAHs4CukgtCRUoAAAQAAAewwIgQgJfj+/uHgptLFvuzTKH4AJJaJUS86
# 8THuToorLBW/tyQwDQYJKoZIhvcNAQELBQAEggIAH8aFDAhkUIgctizF5pIjlHl+
# SVWnbN4541iacZ9Efg6rnEEhhQxr+OvBhpI6PxNWNVscBUY5qd1tk2tuRH/TY7Zt
# 6vU+DpP4+mvuCFEPJPY3OmfiG78B3YxZ+i42LY0wrSYMcCP2cLzRy/2MvWvA9TYU
# DPAmtVjJoiL5abhzEGHAo2r970PsQAVuSDNR2S9ultsJ14GZ4G0SgmkKCI9etqJF
# yZ2Dhb1nFb8rE6mRR18DrGkYeOBBK+kufeeeHuS4wwPebu4ec6wfZSzKu+mpJksz
# g8rqVwOn7rzvKg5V7/jkbhZwKlEf28PdhoJEtnfVCwkzNsZ1qVAYp2EP8vudjZue
# TGVU+n8lLUqVG+x6BH3dFjYY+Zg8nNvX8KWklFvwzn52r3XT656b5R7k0xKHQL3a
# MoANAGyHjpXysYBEe6KtMJRouwgvPyY/f7zbKmiQrt0q0wkDnJ7olrDb0blI0HVX
# Q/uNSaPsEEbaM/VLOfzZfPVC43QCso/u9bJe513K/VwNbcWhpz4ZX1BjwKav7oQV
# nSD/OegAYkPsQeYrQygIVd/jHGU0PqSFARivqnBsc/4VZzXY5kU3egeffhO3tixv
# 8QroJJQPvGlwrvW/Rw224AapOYbB6mlQyIpySSkvdqg4a5SPnCQv7spfM3zI/xvt
# CUXo30iT4GeE+vBKQZE=
# SIG # End Windows Authenticode signature block