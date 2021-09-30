import io
from Bio.Seq import Seq
from .forms import SequenceForm, PrimerForm, SettingForm
from .models import Sequence, Primer, Setting

########## ########## ########## ########## ########## ########## ##########

def add_sequences_to_db(dataset, isfile): # dataset = [sequence, primer], isfile = Boolean
    for i in range(2):
        data = dataset[i] 
        if (data):
            names = []
            sequences = []
            current_sequence = ''
            
            # read file
            if (isfile):
                data = data.read().decode()
            
            # parse FASTA string
            line_data = io.StringIO(data)
            for line in line_data:
                if line.startswith('>'):
                    names.append(line.rstrip())
                    if (current_sequence != ''):
                        sequences.append(current_sequence)
                        current_sequence = ''
                else:
                    current_sequence += line.rstrip().upper()
            if (current_sequence != ''):
                sequences.append(current_sequence)
            
            # sequence handling
            if (i == 0 and len(names)>0 and len(sequences)>0):
                data = {'name':names[0], 'sequence':sequences[0]}
                form = SequenceForm(data)
                if form.is_valid():
                    Sequence.objects.all().delete()
                    form.save()
            elif (i == 0): 
                Sequence.objects.all().delete()
                data = {'name':"> sequence name", 'sequence':"SEQUENCE"}
                form = SequenceForm(data)
                form.save()
   
            # primer handling
            elif (len(names)>0 and len(sequences)>0):
                Primer.objects.all().delete()
                form = PrimerForm
                # forward primers
                for j in range(len(sequences)):
                    data = {'name':names[j], 'sequence':sequences[j], 'active': True, 'direction': True, 'mismatch_score': 0}
                    form = PrimerForm(data)
                    if form.is_valid():
                        form.save()
                # reverse primers
                for k in range(len(sequences)):
                    data = {'name':names[j], 'sequence':create_reverse_primer(sequences[k]), 'active': True, 'direction': False, 'mismatch_score': 0}
                    form = PrimerForm(data)
                    if form.is_valid():
                        form.save()
                
            else:
                Primer.objects.all().delete()
                data = {'name':"> primer name", 'sequence':"PRIMER", 'active': True, 'direction': True, 'mismatch_score': 0}
                form = PrimerForm(data)
                form.save()

########## ########## ########## ########## ########## ########## ##########

def add_covid_primers_to_db(use_covid_primers): #Bool
    covid_primers = """
>covid primer 1
ACCTACTGTCTTATT
>covid primer 2
ACCTACTGTCTTATT
>covid primer 3
TCATTTGAGTTATAGTAG
>covid primer 4
TTAGATGAACCTGTT
>covid primer 5
GTGTTGTCTGTAGTAAT
>covid primer 6
TCTCCTAAGAAGCT
>covid primer 7
TCTTGTAGATCTGTTC
>covid primer 8
TGATAGTGTTACAGTG
>covid primer 9
GTACAACATTTACTTATG
>covid primer 10
TTCAGTGTGTAGACTT
>covid primer 11
TAATTAGAGGTGATGA
>covid primer 12
TGGATTTGTCTTCT"""
    if(use_covid_primers):
        add_sequences_to_db([False, covid_primers], False)

########## ########## ########## ########## ########## ########## ##########

def create_reverse_primer(primer):
    primer =  str(Seq(primer).reverse_complement()) # for rna: reverse_complement_rna()
    return(primer)

########## ########## ########## ########## ########## ########## ##########

def add_settings_to_db(number_of_products, number_of_products_EACHONCE, global_termination_probability, local_termination_probability, chimerism_model, chimerism_probability):
    data = {'number_of_products':number_of_products,
    'number_of_products_EACHONCE': number_of_products_EACHONCE,
    'global_termination_probability':global_termination_probability,
    'local_termination_probability':local_termination_probability,
    'chimerism_model':chimerism_model,
    'chimerism_probability': chimerism_probability
    }
    form = SettingForm(data)
    if form.is_valid():
        Setting.objects.all().delete()
        form.save()
        

def update_primer_setting(primer_id, isactive, mismatches):
    entry = Primer.objects.filter(id=primer_id)
    entry.update(active=isactive, mismatch_score=mismatches)
