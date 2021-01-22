import logging
from sys import exit
from ortu.arguments import args_parser
from ortu.oci_route_table import get_route_table, check_route, update_route_table

_log = logging.getLogger(name=__name__)


def main():
    args = args_parser()

    if args.debug:
        level = getattr(logging, 'DEBUG', None)
    else:
        level = getattr(logging, 'INFO', None)

    logging.basicConfig(level=level)

    exit_code = 1
    try:
        if args.rt_ocid:
            route_table = get_route_table(args.rt_ocid)
            _log.debug(f"Route table: {route_table}")
        else:
            exit_code = 2
            raise ValueError("Route table OCID is required")

        if args.cidr and args.ne_ocid:
            is_route_present = check_route(route_table, args.cidr, args.ne_ocid)
            _log.debug(f"Is route present in route table?: {is_route_present}")
        else:
            exit_code = 2
            raise ValueError("Both cidr and network entity id are required")

        if (is_route_present and args.action == 'create') or (not is_route_present and args.action == 'delete'):
            _log.debug("Just sit around")
        else:
            update_route_table(route_table, args.cidr, args.ne_ocid, args.action, args.dry_run)

        exit_code = 0
    except Exception as e:
        print(f"Something went wrong: {e}. Try to --debug it")

    return exit_code


if __name__ == '__main__':
    exit(main())
