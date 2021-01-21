# Simple utility to insert route rule to OCI Route table

![tests](https://github.com/ITD27M01/oci-route-table-updater/workflows/tests_workflow/badge.svg)

The reason behind this utility is described here: [1251](https://github.com/terraform-providers/terraform-provider-oci/issues/1251)

This simple utility is intended to update the routing table during the terraform run.
It inserts the routing rule in an idempotent way (so, it checks first if exact rule is present in routing table).

## Examples

The example usage is inside `null_resource` terraform resource after VCN peering establishment:


```terraform
resource "null_resource" "right_route_table_update" {
  triggers = {
    right_lpg = oci_core_local_peering_gateway.right_lpg.id
  }

  provisioner "local-exec" {
    command = "ortu --rt-ocid ${data.oci_core_route_tables.right_route_table.route_tables[0].id} --cidr ${data.oci_core_vcn.left_vcn.cidr_block} --ne-ocid ${oci_core_local_peering_gateway.right_lpg.id}"
  }
}

resource "null_resource" "left_route_table_update" {
  triggers = {
    left_lpg = oci_core_local_peering_gateway.left_lpg.id
  }

  provisioner "local-exec" {
    command = "ortu --rt-ocid ${data.oci_core_route_tables.left_route_table.route_tables[0].id} --cidr ${data.oci_core_vcn.right_vcn.cidr_block} --ne-ocid ${oci_core_local_peering_gateway.left_lpg.id}"
  }
}
```

## Authentication

I'm using Ansible in my projects, so, this tool relies on `~/.oci/config` and `OCI_CONFIG_PROFILE` environment variable.
