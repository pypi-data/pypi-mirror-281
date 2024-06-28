import argparse

from colorama import init
from .printcd import run_printcd
from .printinfo import run_printinfo
from .printsrc import run_printsrc
from .lsprintcd import run_lsprintcd

init()

def main():
    parser = argparse.ArgumentParser(description="Command Terminal: Directory Tree Generator")
    subparsers = parser.add_subparsers(dest="command")

    generate_parser = subparsers.add_parser("generate", help="-> generate directory tree")
    generate_parser.add_argument("--start", action="store_true", help="-> specify if you desire to generate helper contents (will overwrite existing)")
    generate_parser.add_argument("--parent", action="store_true", help="-> specify if you want to scan for subdirectories")
    generate_parser.add_argument("--source", action="store_true", help="-> specify if you desire to add /%%src contents")

    args = parser.parse_args()

    if args.command == "generate":
        # if args.start and args.parent and args.source:
        #     run_lsprintcdinfoandsource()
        # elif args.start and args.parent:
        #     run_lsprintinfo()
        # elif args.start and args.source:
        #     run_printinfoandsource()
        # elif args.parent and args.source:
        #     run_lsprintsource()
        if args.start:
            run_printinfo()
        elif args.parent:
            run_lsprintcd()
        elif args.source:
            run_printsrc()
        else:
            run_printcd()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
