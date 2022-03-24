from os import environ, path
from oci import config, core, auth


def _get_oci_config():
    """
    To unify different tools (oci-cli, ortu, ansible, terraform), I'm using the following doc
    https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/clienvironmentvariables.htm#CLI_Environment_Variables
    :return: oci_config
    """
    oci_user = environ.get("OCI_CLI_USER")
    oci_fingerprint = environ.get("OCI_CLI_FINGERPRINT")
    oci_tenancy = environ.get("OCI_CLI_TENANCY")
    oci_region = environ.get("OCI_CLI_REGION")
    oci_key_file = environ.get("OCI_CLI_KEY_FILE")
    oci_key_content = environ.get("OCI_CLI_KEY_CONTENT")

    if oci_user and oci_fingerprint and oci_tenancy and oci_region and (oci_key_file or oci_key_content):
        oci_config = {
            "user": oci_user,
            "fingerprint": oci_fingerprint,
            "tenancy": oci_tenancy,
            "region": oci_region
        }

        if oci_key_file:
            oci_config["key_file"] = oci_key_file
        else:
            oci_config["key_content"] = oci_key_content

    else:
        oci_config_file = environ.get("OCI_CLI_CONFIG_FILE",
                                      path.join(path.expanduser("~"), ".oci", "config"))
        oci_config_profile = environ.get("OCI_CONFIG_PROFILE",
                                         environ.get("OCI_CLI_PROFILE", "DEFAULT"))

        oci_config = config.from_file(file_location=oci_config_file, profile_name=oci_config_profile)

    config.validate_config(oci_config)

    return oci_config


def get_network_client():
    oci_config = {}
    signer = None

    # https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/clienvironmentvariables.htm#environmentvariabletable
    auth_type = environ.get("OCI_CLI_AUTH", "api_key")
    if auth_type == "api_key":
        oci_config = _get_oci_config()
    elif auth_type == "instance_principal":
        signer = auth.signers.InstancePrincipalsSecurityTokenSigner()

    return core.VirtualNetworkClient(config=oci_config, signer=signer)
