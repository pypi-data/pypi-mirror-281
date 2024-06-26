# Description: This script is used to make index for bowtie2 or bwa
import click
import time
from sc3dg.utils.download import make_index

@click.command()
@click.option('-g', '--genome', type=click.Choice(['hg38', 'hg19', 'mm10', 'mm9']), required=True, help='Choose from hg38, hg19, mm10, mm9')
@click.option('-a', '--aligner', type=click.Choice(['bowtie2', 'bwa']), required=True, help='Choose from bowtie2, bwa')
@click.option('-p', '--path', required=True, help='Path to save index')
def make_index(genome, aligner, path):
    make_index(path, genome, aligner)

if __name__ == '__main__':
    start_time = time.time()
    make_index()
    print('=============time spent:', time.time() - start_time, 'seconds===================')
