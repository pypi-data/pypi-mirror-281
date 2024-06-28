import argparse
import time
from sc3dg.utils.download import make_index as download_make_index


def index(genome, aligner, path):
    download_make_index(path, genome, aligner)


def setup_parser(parser):
    parser.add_argument('-g', '--genome', choices=['hg38', 'hg19', 'mm10', 'mm9'], required=True,
                        help='Choose from hg38, hg19, mm10, mm9')
    parser.add_argument('-a', '--aligner', choices=['bowtie2', 'bwa'], required=True, help='Choose from bowtie2, bwa')
    parser.add_argument('-p', '--path', required=True, help='Path to save index')

    args = parser.parse_args()

    index(args.genome, args.aligner, args.path)

