from ortu.oci_route_table import check_route
from oci.core.models import RouteTable, RouteRule


SOURCE_ROUTE_RULES = [
    RouteRule(
        destination='0.0.0.0/0',
        destination_type='CIDR_BLOCK',
        network_entity_id='ocid1.internetgateway.oc1.region.somelongstring'
    )
]

SOURCE_ROUTE_TABLE = RouteTable(
    route_rules=SOURCE_ROUTE_RULES
)

NEW_ROUTE_RULES = [
    RouteRule(
        destination='0.0.0.0/0',
        destination_type='CIDR_BLOCK',
        network_entity_id='ocid1.internetgateway.oc1.region.somelongstring'
    ),
    RouteRule(
        destination='192.168.1.0/24',
        destination_type='CIDR_BLOCK',
        network_entity_id='ocid1.internetgateway.oc1.region.anotherlongcrazystring'
    ),
    RouteRule(
        destination='all-fra-services-in-oracle-services-network',
        destination_type='SERVICE_CIDR_BLOCK',
        network_entity_id='ocid1.servicegateway.oc1.region.anotherlongcrazystringforsg'
    )
]

NEW_ROUTE_TABLE = RouteTable(
    route_rules=NEW_ROUTE_RULES
)


CIDR = '192.168.1.0/24'
NE_OCID = 'ocid1.internetgateway.oc1.region.anotherlongcrazystring'


def test_check_update_needed():
    assert not check_route(SOURCE_ROUTE_TABLE, CIDR, NE_OCID)


def test_check_update_not_needed():
    assert check_route(NEW_ROUTE_TABLE, CIDR, NE_OCID)
