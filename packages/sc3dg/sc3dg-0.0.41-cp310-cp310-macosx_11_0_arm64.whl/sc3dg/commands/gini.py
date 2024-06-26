import click
from sc3dg.analysis.api import MMCooler



@click.command('gini')
@click.option('--mcool',  help='mcool path',required=True, default=None)
@click.option('--output',  help='output path',required=True, default=None)
@click.option('--resolution', help='resolution',required=True,  type=str)
def gini(mcool, output, resolution):
    '''
    Parameters
    ----------
    mcool:str
        mcool file path
    output:
        output file path
    resolution:
        resolution
    Returns
    -------
    '''
    ob1 = MMCooler(directory=mcool,
                   resolution=resolution.split(','),
                   describe = 'gini',
                   merge=False
                   )
    gini = ob1.get_gini()

    gini.to_csv(output, sep='\t')