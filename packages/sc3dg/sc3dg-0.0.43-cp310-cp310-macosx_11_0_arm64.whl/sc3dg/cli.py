import click
from sc3dg.commands.count import count
from sc3dg.commands.model import model

from sc3dg.commands.impute import impute
from sc3dg.commands.ssce import ssce
from sc3dg.commands.merge import merge
from sc3dg.commands.accum import accum
from sc3dg.commands.nDS import nDS


@click.group()
def cli():
    pass


cli.add_command(count)
cli.add_command(model)
cli.add_command(impute)
cli.add_command(ssce)
cli.add_command(merge)
cli.add_command(accum)
cli.add_command(nDS)


if __name__ == '__main__':
    cli()
