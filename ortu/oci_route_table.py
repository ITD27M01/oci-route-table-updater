import logging
from re import match, compile
from ortu.oci_auth import get_network_client
from oci.core.models import UpdateRouteTableDetails, RouteRule


_log = logging.getLogger(name=__name__)


CIDR_DESTINATION_TYPE = "CIDR_BLOCK"
SERVICE_DESTINATION_TYPE = "SERVICE_CIDR_BLOCK"
CIDR_RE_PATTERN = compile('(?<!\d\.)(?<!\d)(?:\d{1,3}\.){3}\d{1,3}\/\d{1,2}(?!\d|(?:\.\d))')


def _construct_route_rule(cidr, ne_ocid):
    if match(CIDR_RE_PATTERN, cidr):
        route_rule = RouteRule(
            destination=cidr,
            destination_type=CIDR_DESTINATION_TYPE,
            network_entity_id=ne_ocid
        )
    else:
        route_rule = RouteRule(
            destination=cidr,
            destination_type=SERVICE_DESTINATION_TYPE,
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


def construct_update_details(route_table, cidr, ne_ocid, action):
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
    _log.debug(f"Route table update details: {update_route_table_details}")

    return update_route_table_details


def _do_update_route_table(route_table_id, update_route_table_details):
    network_client = get_network_client()
    response = network_client.update_route_table(route_table_id, update_route_table_details=update_route_table_details)

    return response.data


def update_route_table(route_table, cidr, ne_ocid, action, dry_run):
    update_route_table_details = construct_update_details(route_table, cidr, ne_ocid, action)
    _log.debug(f"Route table update details: {update_route_table_details}")

    if not dry_run:
        response = _do_update_route_table(route_table.id, update_route_table_details)
        _log.debug(f"{response}")

        return response
    else:
        _log.debug("Dry run, just sit around")

        return {}
