import logging
from ortu.oci_auth import get_network_client
from oci.core.models import UpdateRouteTableDetails, RouteRule


_log = logging.getLogger(name=__name__)


def _construct_route_rule(cidr, ne_ocid):
    route_rule = RouteRule(
        destination=cidr,
        destination_type="CIDR_BLOCK",
        network_entity_id=ne_ocid
    )
    return route_rule


def get_route_table(rt_ocid):
    network_client = get_network_client()
    return network_client.get_route_table(rt_ocid).data


def check_route(route_table, cidr, ne_ocid):
    route_rule = _construct_route_rule(cidr, ne_ocid)
    _log.debug(f"Route rule: {route_rule}")

    filtered_rules = list(filter(lambda rule: rule.destination == cidr and rule.network_entity_id == ne_ocid,
                                 route_table.route_rules))

    if filtered_rules:
        return True
    else:
        return False


def update_route_table(route_table, cidr, ne_ocid, action, dry_run):
    network_client = get_network_client()

    route_rules = route_table.route_rules.copy()

    if action == 'create':
        route_rules.append(_construct_route_rule(cidr, ne_ocid))
    elif action == 'delete':
        filtered_rules = list(filter(lambda rule: rule.destination != cidr and rule.network_entity_id != ne_ocid,
                                     route_rules))

        route_rules = filtered_rules
    else:
        raise ValueError(f"Action {action} is not implemented yet")

    update_route_table_details = UpdateRouteTableDetails(
        route_rules=route_rules
    )

    if not dry_run:
        network_client.update_route_table(route_table.id, update_route_table_details=update_route_table_details)
    else:
        _log.debug(f"Route table update details: {update_route_table_details}")
