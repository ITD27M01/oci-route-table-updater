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
    rt_id  = data.oci_core_vcn.right_vcn.default_route_table_id
    cidr   = data.oci_core_vcn.left_vcn.cidr_block
    lpg_id = oci_core_local_peering_gateway.right_lpg.id
  }

  provisioner "local-exec" {
    command = "ortu --rt-ocid ${self.triggers.rt_id} --cidr ${self.triggers.cidr} --ne-ocid ${self.triggers.lpg_id}"
  }
  provisioner "local-exec" {
    when    = destroy
    command = "ortu delete --rt-ocid ${self.triggers.rt_id} --cidr ${self.triggers.cidr} --ne-ocid ${self.triggers.lpg_id}"
  }
}

resource "null_resource" "left_route_table_update" {
  triggers = {
    rt_id  = data.oci_core_vcn.left_vcn.default_route_table_id
    cidr   = data.oci_core_vcn.right_vcn.cidr_block
    lpg_id = oci_core_local_peering_gateway.left_lpg.id
  }

  provisioner "local-exec" {
    command = "ortu --rt-ocid ${self.triggers.rt_id} --cidr ${self.triggers.cidr} --ne-ocid ${self.triggers.lpg_id}"
  }
  provisioner "local-exec" {
    when    = destroy
    command = "ortu delete --rt-ocid ${self.triggers.rt_id} --cidr ${self.triggers.cidr} --ne-ocid ${self.triggers.lpg_id}"
  }
}
```

There is a default route table updated. Don't forget to ignore the `route_rules` changes for this resource:

```terraform
resource "oci_core_default_route_table" "default_route_table" {
  manage_default_resource_id = oci_core_vcn.vcn.default_route_table_id

  display_name = var.vcn_name

  freeform_tags = merge(local.default_tags, var.tags)

  lifecycle {
    ignore_changes = [
      route_rules,
    ]
  }
}

resource "null_resource" "default_route_table_update" {
  triggers = {
    rt_id = oci_core_default_route_table.default_route_table.id
    ig_id = oci_core_internet_gateway.internet_gateway.id
    cidr  = local.anywhere
  }

  provisioner "local-exec" {
    command = "ortu --rt-ocid ${self.triggers.rt_id} --cidr ${self.triggers.cidr} --ne-ocid ${self.triggers.ig_id} --debug"
  }
  provisioner "local-exec" {
    when    = destroy
    command = "ortu delete --rt-ocid ${self.triggers.rt_id} --cidr ${self.triggers.cidr} --ne-ocid ${self.triggers.ig_id} --debug"
  }
}
```
## Authentication

I'm using Ansible in my projects, so, this tool relies on `~/.oci/config` and `OCI_CONFIG_PROFILE` environment variable.
