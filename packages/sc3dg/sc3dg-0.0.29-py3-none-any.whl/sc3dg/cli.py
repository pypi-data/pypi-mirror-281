import click


#
# from sc3dg.commands.ssce import ssce
# from sc3dg.commands.merge import merge
# from sc3dg.commands.accum import accum
# from sc3dg.commands.nDS import nDS
# from sc3dg.commands.make_index import make_index

@click.group()
def cli():
    pass


@cli.command()
@click.pass_context
def cmd_count(ctx):
    from sc3dg.commands.count import count
    ctx.forward(count)

@cli.command()
@click.pass_context
def cmd_model(ctx):
    from sc3dg.commands.model import model
    ctx.forward(model)

@cli.command()
@click.pass_context
def cmd_impute(ctx):
    from sc3dg.commands.impute import impute
    ctx.forward(impute)

@cli.command()
@click.pass_context
def cmd_ssce(ctx):
    from sc3dg.commands.ssce import ssce
    ctx.forward(ssce)

@cli.command()
@click.pass_context
def cmd_merge(ctx):
    from sc3dg.commands.merge import merge
    ctx.forward(merge)

@cli.command()
@click.pass_context
def cmd_accum(ctx):
    from sc3dg.commands.accum import accum
    ctx.forward(accum)

@cli.command()
@click.pass_context
def cmd_nDS(ctx):
    from sc3dg.commands.nDS import nDS
    ctx.forward(nDS)


@cli.command()
@click.pass_context
def cmd_make_index(ctx):
    from sc3dg.commands.make_index import make_index
    ctx.forward(make_index)




# cli.add_command(count)
# cli.add_command(model)
# cli.add_command(impute)
# cli.add_command(ssce)
# cli.add_command(merge)
# cli.add_command(accum)
# cli.add_command(nDS)
# cli.add_command(make_index)


if __name__ == '__main__':
    cli()
