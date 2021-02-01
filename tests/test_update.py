from ortu.oci_route_table import construct_update_details
from oci.core.models import RouteTable, RouteRule


WO_CIDR_ROUTE_RULES = [
    RouteRule(
        destination='192.168.1.0/24',
        destination_type='CIDR_BLOCK',
        network_entity_id='ocid1.localpeeringgateway.oc1.region.lpgid'
    ),
    RouteRule(
        destination='all-fra-services-in-oracle-services-network',
        destination_type='SERVICE_CIDR_BLOCK',
        network_entity_id='ocid1.servicegateway.oc1.region.sgwid'
    )
]

WO_SERVICE_ROUTE_RULES = [
    RouteRule(
        destination='0.0.0.0/0',
        destination_type='CIDR_BLOCK',
        network_entity_id='ocid1.internetgateway.oc1.region.igid'
    ),
    RouteRule(
        destination='192.168.1.0/24',
        destination_type='CIDR_BLOCK',
        network_entity_id='ocid1.localpeeringgateway.oc1.region.lpgid'
    )
]

CIDR_ROUTE_RULES = [
    RouteRule(
        destination='192.168.1.0/24',
        destination_type='CIDR_BLOCK',
        network_entity_id='ocid1.localpeeringgateway.oc1.region.lpgid'
    ),
    RouteRule(
        destination='all-fra-services-in-oracle-services-network',
        destination_type='SERVICE_CIDR_BLOCK',
        network_entity_id='ocid1.servicegateway.oc1.region.sgwid'
    ),
    RouteRule(
        destination='0.0.0.0/0',
        destination_type='CIDR_BLOCK',
        network_entity_id='ocid1.internetgateway.oc1.region.igid'
    )
]

SERVICE_ROUTE_RULES = [
    RouteRule(
        destination='0.0.0.0/0',
        destination_type='CIDR_BLOCK',
        network_entity_id='ocid1.internetgateway.oc1.region.igid'
    ),
    RouteRule(
        destination='192.168.1.0/24',
        destination_type='CIDR_BLOCK',
        network_entity_id='ocid1.localpeeringgateway.oc1.region.lpgid'
    ),
    RouteRule(
        destination='all-fra-services-in-oracle-services-network',
        destination_type='SERVICE_CIDR_BLOCK',
        network_entity_id='ocid1.servicegateway.oc1.region.sgwid'
    )
]

WO_CIDR_ROUTE_TABLE = RouteTable(
    route_rules=WO_CIDR_ROUTE_RULES
)

WO_SERVICE_ROUTE_TABLE = RouteTable(
    route_rules=WO_SERVICE_ROUTE_RULES
)

ROUTE_TABLE = RouteTable(
    route_rules=SERVICE_ROUTE_RULES
)

CIDR = '0.0.0.0/0'
IG_ID = 'ocid1.internetgateway.oc1.region.igid'
SERVICE_CIDR = 'all-fra-services-in-oracle-services-network'
SG_ID = 'ocid1.servicegateway.oc1.region.sgwid'


def test_create_cidr():
    assert construct_update_details(WO_CIDR_ROUTE_TABLE, CIDR, IG_ID, 'create').route_rules == \
           CIDR_ROUTE_RULES


def test_create_service():
    assert construct_update_details(WO_SERVICE_ROUTE_TABLE, SERVICE_CIDR, SG_ID, 'create').route_rules == \
           SERVICE_ROUTE_RULES


def test_delete_cidr():
    assert construct_update_details(ROUTE_TABLE, CIDR, IG_ID, 'delete').route_rules == \
           WO_CIDR_ROUTE_RULES


def test_delete_service():
    assert construct_update_details(ROUTE_TABLE, SERVICE_CIDR, SG_ID, 'delete').route_rules == \
           WO_SERVICE_ROUTE_RULES
