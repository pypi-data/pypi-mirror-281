import os,argparse
import sys
        
class Filter:
    def __init__(self, args) :
        self.outdir = os.path.abspath(os.path.join(args.outdir, args.name))
        self.repseq = args.repseq

    def run(self):
        from dnbc4tools.vdj.src.filter_annotation import filter_annotation
        from dnbc4tools.tools.utils import str_mkdir, judgeFilexits, get_formatted_time
        from dnbc4tools.__init__ import __root_dir__
        judgeFilexits(
            f'{self.outdir}/02.assembly/tcrbcr_airr_align.tsv',
            f'{self.outdir}/02.assembly/tcrbcr_annot.fa',
            f'{self.outdir}/02.assembly/tcrbcr_cdr3.out',
            f'{self.outdir}/01.data/cell.sequencing.csv',
            )
        str_mkdir('%s/03.filter'%self.outdir)
        str_mkdir('%s/log'%self.outdir)

        print(f'\n{get_formatted_time()}\n'
            f'Cell calling and generate clonotypes.')
        
        sys.stdout.flush()

        filter_annotation(
            f'{self.outdir}/02.assembly/tcrbcr_cdr3.out',
            f'{self.outdir}/02.assembly/tcrbcr_annot.fa',
            f'{self.outdir}/02.assembly/tcrbcr_airr_align.tsv',
            f'{self.outdir}/01.data/cell.sequencing.csv',
            self.repseq,
            f'{self.outdir}/03.filter'
        )

def filter(args):
    """
    Run the pipeline using the specified arguments.
    """
    Filter(args).run()

def helpInfo_filter(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """
    Define the command line arguments for the pipeline.
    """
    parser.add_argument(
        '--name',
        type=str, 
        metavar='STR',
        help='Sample ID'
    )
    parser.add_argument(
        '--outdir', 
        metavar='PATH',
        help='Output directory, [default: current directory].', 
        default=os.getcwd()
    )
    parser.add_argument(
        '--repseq', 
        metavar='STR',
        help='the data is from tcr or bcr.',
        type=str,
        required=True,
        choices=['TR', 'IG']
    )
    return parser