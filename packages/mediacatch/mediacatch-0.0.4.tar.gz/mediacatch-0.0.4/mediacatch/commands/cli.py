from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from mediacatch.commands.vision import VisionCLI


def main():
    parser = ArgumentParser(
        prog='MediaCatch CLI tool',
        usage='mediacatch <command> [<args>]',
        description='MediaCatch CLI tool',
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    commands_parser = parser.add_subparsers(help='mediacatch command helpers')

    # Register commands
    VisionCLI.register_subcommand(commands_parser)

    # Let's go
    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        exit(1)

    # Run
    service = args.func(args)
    service.run()


if __name__ == '__main__':
    main()
