'''The Orchest APICLI.
'''

from _version import __version__
from gettext import gettext
import click
import cmds
import collections
import typing as t


class ClickCommonOptionsCmd(click.Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add the common commands to the beginning of the list so that
        # they are displayed first in the help menu.
        self.params: t.List[click.Option] = [
            click.Option(
                ('--url',),
                envvar='URL',
                required=True,
                help='Url of the Orchest instance',
            ),
            click.Option(
                ('--username',),
                envvar='USERNAME',
                required=True,
                help='Username to log in the Orchest instance',
            ),
            click.Option(
                ('--password',),
                envvar='PASSWORD',
                required=True,
                help='Password for the user to log in the Orchest instance',
            ),
        ] + self.params


# Largely a copy-paste from the original source code, but extended to
# display separated categories in the help menu.
class ClickHelpCategories(click.Group):
    def format_commands(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        '''Extra format methods for multi methods that adds all the commands
        after the options.
        '''
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            categories: t.Dict[
                str, t.List[t.Tuple[str, str]]
            ] = collections.defaultdict(list)
            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)

                categories['API Commands'].append((subcommand, help))

            if categories:
                for category, rows in categories.items():
                    with formatter.section(gettext(category)):
                        formatter.write_dl(rows)


class MultiChoice(click.ParamType):
    name = 'multi_choice'

    def __init__(self, choices):
        self.choices = choices

    def convert(self, value, param, ctx):
        if not value:  # Handle the case where no value is provided
            return []
        selected_values = value.split(',')
        for val in selected_values:
            if val not in self.choices:
                self.fail(
                    f"invalid choice: {val}. (choose from {', '.join(self.choices)})", param, ctx)
        return selected_values


@click.group(
    context_settings={
        "help_option_names": ["-h", "--help"],
    },
    cls=ClickHelpCategories,
)
@click.version_option(version=__version__, prog_name="ttoa-cli")
def cli():
    '''The TapTarget Orchest API CLI to interact with the Orchest instance.

    \b
    Exit status:
        0   if OK,
        1   if Failure.

    '''
    pass


@click.option(
    "--export",
    is_flag=True,
    default=False,
    show_default=True,
    help="Export the result to a .json file",
)
@cli.command(cls=ClickCommonOptionsCmd)
def get_projects(
    export: bool,
    **common_options,
) -> None:
    '''Get all projects'''
    cmds.OrchestAPICmds(**common_options).get_projects(
        export,
        **common_options,
    )


statusses_choices = ['STARTED', 'PENDING', 'SUCCESS', 'FAILURE', 'ABORTED']

@click.option(
    "--export",
    is_flag=True,
    default=False,
    show_default=True,
    help="Export the result to a .json file",
)
@click.option(
    "--statusses",
    default=[],
    type=MultiChoice(statusses_choices),
    help=f'Select multiple options separated by commas (e.g., "STARTED,PENDING"). Choices: {", ".join(statusses_choices)}'
)
@click.option(
    "--cancel",
    is_flag=True,
    default=False,
    show_default=True,
    help="Cancel the STARTED and PENDING jobs.",
)
@cli.command(cls=ClickCommonOptionsCmd)
def get_pipeline_runs(
    export: bool,
    statusses: list,
    cancel: list,
    **common_options,
) -> None:
    '''Get all pipeline runs'''
    cmds.OrchestAPICmds(**common_options).get_pipeline_runs(
        export,
        statusses,
        cancel,
        **common_options,
    )


if __name__ == '__main__':
    cli()
