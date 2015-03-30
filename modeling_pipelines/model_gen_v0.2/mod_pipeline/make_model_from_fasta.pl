#!/usr/bin/perl

#v.0.1

use Bio::Perl;
#use Bio::DB::GenBank;

GetArgs();

#Modus operandi
#1. read file
#2. prepare template part
#2a. pick template and it's align
#2d. fasta_from_pdb.9v2 to get pir
#2e. Get first 2 lines into templates.pir file
#2f. add alignment
#2g. repeat for all templates
#3. pick target
#4. create dir
#5. count target length and prepare pir header
#6. write align.pir (target header + target align + templates.pir)
#7. write model.py
#7a. parse restraints, adjust chain according to chain break, print restraints
#8. copy templates
#9. create target.queue
#10. append run.sh and queue.sh


#$base_path=`cd ..; pwd`;
$base_path=`pwd`;
chomp($base_path);

`echo '#!/bin/bash' >sequence_modeler_run.sh`;
`echo '#!/bin/bash' >queue_modeler_run.sh`;
`chmod +x sequence_modeler_run.sh`;
`chmod +x queue_modeler_run.sh`;


@seq_list=read_all_sequences($setup->{'source'},'fasta');
if (!defined $#seq_list) {
    print "ERROR: cannot read alignment file.\n";
    Help();
    exit(1);
}

#templates
@template_list=split(',',$setup->{'templates'});
    `rm -f template.pir &>/dev/null`;

for ($i=0;$i<=$#template_list;$i++) {
    $tmp_seq=GetSeq($template_list[$i]);
    
    $t_file=$template_list[$i].'.pdb';
    $t_file_seq=$template_list[$i].'.seq';
    `./fasta_from_pdb_9v2.py $t_file &>/dev/null`;
    `head -n 3 $t_file_seq |tail -n 2 >>template.pir`;
    $tmp_seq=$tmp_seq.'*';
    `echo $tmp_seq >>template.pir`;
    `rm -f $t_file_seq`;
    
    $t_known="'".$template_list[$i]."'";
    push(@tmp_knowns,$t_known);
    
}
    $knowns=join(',',@tmp_knowns);

#targets
@target_list=split(',',$setup->{'targets'});

#processing alpha restraints string
if (defined $setup->{'alpha'}) {
    @target_alpha=split(',',$setup->{'alpha'});
}
#processing beta restraints string
if (defined $setup->{'beta'}) {
    @target_beta=split(',',$setup->{'beta'});
}


for ($i=0;$i<=$#target_list;$i++) {

    $tmp_align=GetSeq($target_list[$i]);
    $tmp_seq=$tmp_align;
    $tmp_seq=~s/-//g; #wywalamy gapy
    $tmp_seq=~s/\///g; # wywalamy chain break
    $tmp_len=length($tmp_seq);
    $tmp_align=$tmp_align.'*';
    
    `mkdir $target_list[$i]`;
    `echo '>P1;$target_list[$i]' >$target_list[$i]/align.pir`;
    `echo 'sequence:$target_list[$i]:1\:\:$tmp_len\:\:\:\:-1.00:-1.00'>> $target_list[$i]/align.pir`;
    `echo $tmp_align >> $target_list[$i]/align.pir`;
    `cat template.pir >> $target_list[$i]/align.pir`;
    
    open (OU,">$target_list[$i]/model.py");

    print {OU} <<"XXX";
#!/usr/bin/python
from modeller import *
from modeller.automodel import * # Load the automodel class
log.verbose()
env = environ()
env.io.atom_files_directory = './:../atom_files'
class mymodel(automodel):
    def special_restraints(self, aln):
	rsr = self.restraints
	at = self.atoms
XXX

    if ((defined $setup->{'alpha'}) and ($target_alpha[$i] ne '')) {
	$tmp_alpha=$target_alpha[$i];
	@t_alpha=split('-',$tmp_alpha);
	for ($j=0;$j<=$#t_alpha;$j++) {
	    $t_alpha_chain=GetChain($tmp_align,$t_alpha[$j]);
	    $t_alpha[$j]=$t_alpha[$j].$t_alpha_chain;
	}
	#wpisywanie alpha restraints
	for ($j=0;$j<=$#t_alpha;$j=$j+2) {
	    print {OU} "\trsr.add(secondary_structure.alpha(self.residue_range('".$t_alpha[$j]."', '".$t_alpha[$j+1]."')))\n";
	}
	
	
	
    }

    print {OU} <<"XXX";
a = mymodel(env,alnfile = 'align.pir',knowns = ($knowns),sequence = '$target_list[$i]')
a.starting_model = 1
a.ending_model = $setup->{'no_models'}
a.md_level=refine.$setup->{'md_type'}
a.initial_malign3d = False
a.final_malign3d = True
a.make()
XXX

close(OU);

    for ($j=0;$j<=$#template_list;$j++) {
	$t_file=$template_list[$j].'.pdb';
	`cp $t_file $target_list[$i]/`;
    }
    
    `chmod +x $target_list[$i]/model.py`;

    $path=$base_path.'/'.$target_list[$i];
    $path=~s/ /\\ /g;
    
    `echo '$path/model.py > $path/model.log' >> sequence_modeler_run.sh`;

    
    `echo '#!/bin/bash' > $target_list[$i]/run.qsub`;
    `echo '#PBS -S /bin/bash' >> $target_list[$i]/run.qsub`;
    $t_name=$target_list[$i].'_modeling';
    `echo '#PBS -N $t_name' >> $target_list[$i]/run.qsub`;
#    `echo '#PBS -l mem=4gb,nodes=1:ppn=1,walltime=72:00:00' >> $target_list[$i]/run.qsub`;
    `echo '#PBS -l mem=4gb,nodes=1:ppn=1' >> $target_list[$i]/run.qsub`;
    `echo '#PBS -k n' >> $target_list[$i]/run.qsub`;
    `echo '#PBS -j eo' >> $target_list[$i]/run.qsub`;
    `echo 'cd $path' >> $target_list[$i]/run.qsub`;
    `echo './model.py >>model.log' >> $target_list[$i]/run.qsub`;

    `echo 'qsub $path/run.qsub' >> queue_modeler_run.sh`;
}

sub GetChain {
    my $tmp_al=shift @_;
    my $tmp_pos=shift @_;
    my $tmp_chain=':';
    
    #tu dopisac rozpoznawanie chaina;
    
    return $tmp_chain;
    
}

sub GetSeq {
    my $tmp_id=shift @_;
    my $tidx=0;
    my $tres='0';
    
    for ($tidx=0;$tidx<=$#seq_list;$tidx++) {
	if ($seq_list[$tidx]->id() eq $tmp_id) {
	    $tres=$seq_list[$tidx]->seq();
	    last;
	}
    }
    return $tres;
}

sub GetArgs {

    if (!defined $ARGV[0]) {Help();exit(1)}

    my $arg;

    $setup->{'targets'} = '';
    $setup->{'templates'} = '';
    
    $setup->{'no_models'}=5;
    $setup->{'md_type'}='fast';
    
    while (defined ($arg = shift @ARGV)) {
    	if ($arg eq '-h') {
	    Help();
	    exit;
	} elsif ($arg eq '-i') {
	    #open (IN,"<", shift @ARGV) or die "Error: Cannot open input fasta file!\n";
	    #$setup->{'source'} = \*IN;
	    $setup->{'source'}= shift @ARGV;
	} elsif ($arg eq '-o') {
	    $setup->{'targets'} = shift @ARGV;
	} elsif ($arg eq '-t') {
	    $setup->{'templates'} = shift @ARGV;
	} elsif ($arg eq '-n') {
	    $setup->{'no_models'} = shift @ARGV;
	} elsif ($arg eq '-d') {
	    $setup->{'md_type'} = shift @ARGV;
	    if (($setup->{'md_type'} ne 'very_fast') and ($setup->{'md_type'} ne 'fast') and ($setup->{'md_type'} ne 'slow') and ($setup->{'md_type'} ne 'very_slow')) {
		print "ERROR: Wrong MD_TYPE ",$setup->{'md_type'}," {very_fast, fast, slow, very_slow} allowed.\n";
		exit(1);
	    }
	} elsif ($arg eq '-a') {
	    $setup->{'alpha'} = shift @ARGV;
	} elsif ($arg eq '-b') {
	    $setup->{'beta'} = shift @ARGV;
	    print "WARNING: Beta-strand restraints not coded yet. Option not used!\n";
	} elsif ($arg eq '-h') {
	    Help();
	    exit(0);
	}
    }

    if (($setup->{'targets'} eq '') or ($setup->{'templates'} eq '') or (!defined $setup->{'source'})) {
	print "ERROR: More parameters required!\n";
	Help();
	exit(1);
    }
}

sub Help {
    print << "XXX";

make_model_from_fasta.pl -i <source fasta file> -t <coma separated templates list> -o <coma separated target list> [-n -a -b -d]
    
The program will read fasta formated alignment file that contains sequences 
of templates and targets for modeling. The program will prepare directory 
structure (one dir for each modeing) and scripts to either run modelling tasks
in sequence of submit them to queue system. The script requires pdb files with
templates to be present in alignment file directory. The script DOES NOT RUN MODELLING 
TASK, you need to run it from either sequence_modeller_run.sh or queue_modeller_run.sh!
Adding restraints: add restraints for every terget, if target requires no restraint, 
leave ',,' separators so the list is full. Each alpha restraint shout have start 
and end separated with '-'. If there are multiple restraints for a target, separate 
them also with '-'. Make sure to have even number of positions for each target.

ToDo:
    1. add restraints beta
    2. add chain/chain break recognition
    
Options:
    -i 	: input fasta formated alignment file,
    -o 	: coma separated list of targets (names identical to those in file),
    -t 	: coma separated list of templates from file (all templates used),
    -n 	: numner of models to be created for each modelling (default 5),
    -d	: md_dynamics to use {very_fast, fast, slow, very_slow} (default fast),
    -a	: coma separated list of a-helical restraints for each target (ie. 12-17-22-28,13-18-22-28),
    -b	: ToDo: list of b-strand restraints for each target.

XXX
#exit(0);
}
