import argparse


def args_parser():
    parser = argparse.ArgumentParser(description='Updates OCI route table')
    parser.add_argument('--rt-ocid', type=str, action='store',
                        help='Route table OCI ID')

    parser.add_argument('--cidr', type=str, action='store',
                        help='Destination network in CIDR notation - xxx.xxx.xxx.xxx/xx')

    parser.add_argument('--ne-ocid', type=str, action='store',
                        help='Network entity OCI ID')

    parser.add_argument('--debug', default=False, action='store_true',
                        help='Shows detailed update process')

    parser.add_argument('--dry-run', default=False, action='store_true',
                        help='Dry run update. Useful with --debug')

    return parser.parse_args()
