from os import environ, path
from oci import config, core


def _get_oci_config():
    oci_config_file = path.join(path.expanduser("~"), ".oci", "config")
    oci_config_profile = 'DEFAULT'

    if "OCI_CONFIG_PROFILE" in environ:
        oci_config_profile = environ.get("OCI_CONFIG_PROFILE")

    return config.from_file(file_location=oci_config_file, profile_name=oci_config_profile)


def get_network_client():
    oci_config = _get_oci_config()
    return core.VirtualNetworkClient(oci_config)
