import os,argparse
import sys
import shutil
import warnings
warnings.filterwarnings("ignore")
        
class Report:

    def __init__(self, args) :
        self.name = args.name
        self.species = args.species
        self.outdir = os.path.abspath(os.path.join(args.outdir, args.name))
        self.repseq = args.repseq

    def run(self):
        from dnbc4tools.vdj.src.generate_report import generate_report_summary
        from dnbc4tools.tools.utils import str_mkdir, judgeFilexits, get_formatted_time
        from dnbc4tools.__init__ import __root_dir__

        judgeFilexits(
            f'{self.outdir}/01.data/sequencing_report.csv',
            f'{self.outdir}/01.data/tcrbcr_bc.fa',
            f'{self.outdir}/01.data/cell.sequencing.csv',
            f'{self.outdir}/02.assembly/tcrbcr_assembled_reads.fa',
            f'{self.outdir}/02.assembly/tcrbcr_airr_align.tsv',
            f'{self.outdir}/02.assembly/tcrbcr_annot.fa',
            f'{self.outdir}/02.assembly/tcrbcr_cdr3.out',
            f'{self.outdir}/03.filter/all_contig_annotations.csv',
            f'{self.outdir}/03.filter/filtered_contig_annotations.csv',
            
            f'{self.outdir}/03.filter/clonotypes.csv',
            )
        str_mkdir('%s/04.report/div'%self.outdir)
        str_mkdir('%s/04.report/table'%self.outdir)
        str_mkdir('%s/log'%self.outdir)

        print(f'\n{get_formatted_time()}\n'
            f'Statistical analysis and report generation for results.')
        
        sys.stdout.flush()

        generate_report_summary(
            self.name,
            self.species,
            self.outdir,
            self.repseq,
            f'{__root_dir__}/config/template/',
        )

        # ### copy file
        str_mkdir('%s/output'%self.outdir)
        if os.path.exists(f'{self.outdir}/03.filter/all_contig_annotations.csv'):
            shutil.copy(f'{self.outdir}/03.filter/all_contig_annotations.csv',f'{self.outdir}/output')
        if os.path.exists(f'{self.outdir}/03.filter/all_contig.fasta'):
            shutil.copy(f'{self.outdir}/03.filter/all_contig.fasta',f'{self.outdir}/output')
        if os.path.exists(f'{self.outdir}/03.filter/clonotypes.csv'):
            shutil.copy(f'{self.outdir}/03.filter/clonotypes.csv',f'{self.outdir}/output')
        if os.path.exists(f'{self.outdir}/03.filter/consensus.fasta'):
            shutil.copy(f'{self.outdir}/03.filter/consensus.fasta',f'{self.outdir}/output')
        if os.path.exists(f'{self.outdir}/03.filter/filtered_contig_annotations.csv'):
            shutil.copy(f'{self.outdir}/03.filter/filtered_contig_annotations.csv',f'{self.outdir}/output')
        if os.path.exists(f'{self.outdir}/03.filter/filtered_contig.fasta'):
            shutil.copy(f'{self.outdir}/03.filter/filtered_contig.fasta',f'{self.outdir}/output')
        if os.path.exists(f'{self.outdir}/03.filter/airr_rearrangement.tsv'):
            shutil.copy(f'{self.outdir}/03.filter/airr_rearrangement.tsv',f'{self.outdir}/output')
        if os.path.exists(f'{self.outdir}/04.report/{self.name}_scVDJ_{self.repseq}_report.html'):
            shutil.copy(f'{self.outdir}/04.report/{self.name}_scVDJ_{self.repseq}_report.html',f'{self.outdir}/output')
        if os.path.exists(f'{self.outdir}/04.report/metrics_summary.xls'):
            shutil.copy(f'{self.outdir}/04.report/metrics_summary.xls',f'{self.outdir}/output')

def report(args):
    """
    Run the pipeline using the specified arguments.
    """
    Report(args).run()

def helpInfo_report(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """
    Define the command line arguments for the pipeline.
    """
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
    parser.add_argument(
        '--species',
        type=str, 
        metavar='STR',
        help='Species name'
    )
    parser.add_argument(
        '--name',
        type=str, 
        metavar='STR',
        help='Sample ID'
    )
    return parser