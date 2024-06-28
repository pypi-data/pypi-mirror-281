import os,collections
import argparse
import time

class Runpipe:
    def __init__(self, args):
        self.name = args.name
        self.fastq1 = args.fastq1
        self.fastq2= args.fastq2
        self.ref = args.ref
        self.beadstrans = args.beadstrans
        self.chain = args.chain
        
        self.outdir = os.path.abspath(args.outdir)
        self.threads = args.threads
        self.darkreaction = args.darkreaction
        self.customize = args.customize
        
        self.process = args.process
        self.singleEnd = args.singleEnd

        
    def runpipe(self):
        ### import lib
        from dnbc4tools.tools.utils import str_mkdir,judgeFilexits,start_print_cmd,read_json,bin_path
        from dnbc4tools.__init__ import __root_dir__
        
        ### run

        if self.ref.upper() == "HUMAN":
            coordinate = f"{__root_dir__}/config/vdj/GRCh38_bcrtcr.fa"
            imgtbase = f"{__root_dir__}/config/vdj/human_IMGT+C.fa"
            species = "Homo_sapiens"

        elif self.ref.upper() == "MOUSE":
            coordinate = f"{__root_dir__}/config/vdj/GRCm38_bcrtcr.fa"
            imgtbase = f"{__root_dir__}/config/vdj/mouse_IMGT+C.fa"
            species = "Mus_musculus"

        elif os.path.exists(os.path.join(self.ref,"ref.json")):
            indexConfig = read_json(os.path.join(self.ref,"ref.json"))
            coordinate = indexConfig['coordinate']
            imgtbase = indexConfig['IMGT']
            species = indexConfig['species']

        judgeFilexits(self.fastq1,self.fastq2)
        data_cmd = [
            f"{bin_path()}/dnbc4tools vdj data",
            f"--fastq1 {self.fastq1}",
            f"--fastq2 {self.fastq2}",
            f"--threads {self.threads}",
            f"--name {self.name}",
            f"--darkreaction {self.darkreaction}",
            f"--outdir {self.outdir}",
            f"--coordinate {coordinate}",
            f"--beadstrans {self.beadstrans}"
        ]
        if not self.singleEnd:
            data_cmd += ['--pairedreads']
        if self.customize:
            data_cmd += [f'--customize {self.customize}']

        data_cmd = ' '.join(data_cmd)

        assembly_cmd = [
            f"{bin_path()}/dnbc4tools vdj assembly",
            f"--name {self.name}",
            f"--outdir {self.outdir}",
            f"--threads {self.threads}",
            f"--coordinate {coordinate}",
            f"--IMGT {imgtbase}",
        ]
        if not self.singleEnd:
            assembly_cmd += ['--pairedreads']
        assembly_cmd = ' '.join(assembly_cmd)    

        filter_cmd = [
            f"{bin_path()}/dnbc4tools vdj filter",
            f"--name {self.name}",
            f"--repseq {self.chain}", 
            f"--outdir {self.outdir}"
        ]
        filter_cmd =' '.join(filter_cmd) 
        
        report_cmd = [
            f"{bin_path()}/dnbc4tools vdj report",
            f"--name {self.name}",
            f"--outdir {self.outdir}",
            f"--repseq {self.chain}", 
            f"--species {species}"

        ]
        report_cmd = ' '.join(report_cmd)

       
        pipelist = str(self.process).split(',')
        for pipe in pipelist:
            if pipe not in ['data','assembly','filter','report','']:
                print('\033[0;31;40mUnable to recognize pipe!\033[0m')
                raise Exception('Unable to recognize pipe!')
        
        cmdlist = collections.OrderedDict()
        if 'data' in pipelist:
            cmdlist['data'] = data_cmd
        if 'assembly' in pipelist:
            cmdlist['assembly'] = assembly_cmd
        if 'filter' in pipelist:
            cmdlist['filter'] = filter_cmd
        if 'report' in pipelist:
            cmdlist['report'] = report_cmd

        start_time = time.time()
        str_mkdir('%s/log'%os.path.join(self.outdir,self.name))
        for pipe,pipecmd in cmdlist.items():
            start_print_cmd(pipecmd,os.path.join(self.outdir,self.name))
        end_time = time.time()

        analysis_time = end_time - start_time
        analysis_time_minutes, analysis_time_seconds = divmod(analysis_time, 60)
        analysis_time_hours, analysis_time_minutes = divmod(analysis_time_minutes, 60)

        print(f'\nAnalysis Finished')
        print(f'Elapsed Time: {int(analysis_time_hours)} hours {int(analysis_time_minutes)} minutes {int(analysis_time_seconds)} seconds')

def run(args):
    Runpipe(args).runpipe()

def helpInfo_run(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """
    Define the command line arguments for the pipeline.
    """
    parser.add_argument(
        '--name', 
        metavar='<SAMPLE_ID>',
        help='User-defined sample ID.', 
        type=str,
        required=True
    )
    parser.add_argument(
        '--fastq1', 
        metavar='<FQ1FILES>',
        help='The input R1 fastq files.', 
        required=True
    )
    parser.add_argument(
        '--fastq2', 
        metavar='<FQ2FILES>',
        help='The input R2 fastq files.', 
        required=True
    )
    parser.add_argument(
        '--outdir', 
        metavar='<OUTDIR>',
        help='Output directory, [default: current directory].', 
        default=os.getcwd()
    )
    parser.add_argument(
        '--ref',
        type=str, 
        metavar='<REF>',
        help="Set the reference database, choose from 'human' and 'mouse'.",
        required=True
    )
    parser.add_argument(
        '--chain', 
        metavar='<CHAIN>',
        help="Chain type to display metrics for: 'TR' for T cell receptors, 'IG' for B cell receptors.",
        type=str,
        required=True,
        choices=['IG', 'TR']
    )
    parser.add_argument(
        '--beadstrans',
        type=str, 
        metavar='<SINGLECELL>',
        required=True,
        help="Beads converted into cells file in rna summary file 'output/singlecell.csv'."
    )
    parser.add_argument(
        '--threads',
        type=int, 
        metavar='<CORENUM>',
        default=10,
        help='Number of threads used for analysis, [default: 10].'
    )
    parser.add_argument(
        '--darkreaction',
        metavar='<DARKCYCLE>',
        help='Sequencing dark cycles. Automatic detection is recommended, [default: auto].', 
        default='auto'
    )
    parser.add_argument(
        '--customize',
        metavar='<STRUCTURE>',
        help='Customize whitelist and readstructure files in JSON format.'
    )
    parser.add_argument(
        '--process', 
        metavar='<ANALYSIS_STEPS>',
        help='Custom analysis steps enable the skipping of unnecessary steps, [default: data,assembly,filter,report].',
        type=str,
        default='data,assembly,filter,report'
    )
    parser.add_argument(
        '--singleEnd',
        action='store_true',
        help='Assemble using single-end data.'
    )

    return parser