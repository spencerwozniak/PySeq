#!/usr/bin/env python3

#####################################
# USAGE:                            #
# ./sequence.py {OPTIONS} SEQUENCE  #
#####################################

############################################################
#                                                          #
#        Made by Spencer Wozniak (woznia79@msu.edu)        #
#                                                          #
############################################################

import sys

def display_help():
    # Displays help menu
    print()
    print('Convert DNA/RNA sequences with polarity.')  
    print()
    print('DEFAULT:')
    print('Detects DNA/RNA, polarity; displays replication, transcription, & translation.')
    print()
    print('USAGE:')
    print('./sequence.py {OPTIONS} SEQUENCE')
    print()
    print('OPTIONS:')
    print('               -h, --help : Display this menu')
    print('            --replication : DNA -> DNA')
    print('          --transcription : DNA -> RNA')
    print('  --reverse-transcription : RNA -> DNA')
    print('            --translation : DNA/RNA -> AA sequence')
    print('                 --coding : Sequence is the coding strand (Default)')
    print('               --template : Sequence is the template strand')
    print('                 --5first : 5’ always first')
    print('                 --3first : 3’ always first')
    print('                    --one : Print out one-letter AA abbreviations (Default)')
    print('                  --three : Print out three-letter AA abbreviations')
    print('                  --start : Account for start codon in translation.')
    print('                   --stop : Account for stop codon in translation.')
    print()
    exit()

def seq_type(sequence: str):
    # Determines whether input sequence is DNA or RNA
    for char in sequence:
        if char == 'T': # Thymine -> DNA
            return 'DNA'
        elif char == 'U': # Uracil -> RNA
            return 'RNA'

# Default settings
selection = False
replication = False
transcription = False
reverse_transcription = False
translation = False
start_codon = False
stop_codon = False
translation_output = '1'
strand = 'coding'

# Parse arguments
for arg in sys.argv[1:]:
    if arg in ('-h','-help','--help'):
        display_help() # Displays help menu if '-h' selected
    elif arg == '--replication':
        replication = True # Indicates replication
        selection = True # Indicates selection
        sys.argv.remove(arg)
    elif arg == '--transcription':
        transcription = True # Indicates transcription
        selection = True # Indicates selection
        sys.argv.remove(arg)
    elif arg == '--reverse-transcription':
        reverse_transcription = True # Indicates reverse transcription
        selection = True # Indicates selection
        sys.argv.remove(arg)
    elif arg == '--translation':
        translation = True # Indicates translation
        selection = True # Indicates selection
        sys.argv.remove(arg)
    elif arg == '--three':
        translation_output = '3' # Indicates three letter AA code
        sys.argv.remove(arg)
    elif arg == '--template':
        strand = 'template' # Indicates template strand input
        sys.argv.remove(arg)
    elif arg == '--coding':
        strand = 'coding' # Indicates coding strand input
        sys.argv.remove(arg)
    elif arg == '--start':
        start_codon = True # Detect start codon in mRNA
        sys.argv.remove(arg)
    elif arg == '--stop':
        stop_codon = True # Detect stop codon in mRNA
        sys.argv.remove(arg)
    elif arg[0] == '-':
        raise ValueError(
            f'"{arg}" is not a valid argument. Use "-h" to see arguments.'
                        )

# Get sequence from arguments 
# ? need here to prevent Exception ?
sequence = ''.join(sys.argv[1:])

# If selection not indicated, display all outputs.
if not selection:
    if seq_type(sequence) == 'DNA':
        replication = True
        transcription = True
        translation = True
    elif seq_type(sequence) == 'RNA':
        reverse_transcription = True
        translation = True

def check_polarity(char: str):
    # Checks polarity of input sequence.
    if char == '5':
        return ('3','5') # Output should be opposite the input
    elif char == '3':
        return ('5','3') # Output should be opposite the input
    elif char in ('G','C','U','T','A'):
        # If no polarity given, assume 5' first
        sys.stderr.write('(No polarity given)\n')
        return ('3','5') # Output will be 3'->5'
    else:
        raise ValueError('Invalid polarity') # Polarity should indicate 5' or 3'

def DNA_DNA(sequence: str):
    # Replication function
    p = check_polarity(sequence[0]) # Check polarity
    new = [] # Output sequence
    new.append(f"{p[0]}’-")
    for char in sequence:
        if char not in ('5',"'",'`','3','-',' ','’'):
            if char.upper() == 'G':
                new += 'C'
            elif char.upper() == 'C':
                new += 'G'
            elif char.upper() == 'A':
                new += 'T'
            elif char.upper() == 'T':
                new += 'A'
            else:
                raise ValueError(f'{char} is not a valid DNA nucleotide')
    new.append(f"-{p[1]}’")
    return ''.join(new)

def DNA_RNA(sequence: str):
    # Transcription function
    p = check_polarity(sequence[0]) # Check polarity
    new = []
    for char in sequence:
        if char not in ('5',"'",'`','3','-',' ','’'):
            if char.upper() == 'G':
                new.append('C')
            elif char.upper() == 'C':
                new.append('G')
            elif char.upper() == 'A':
                new.append('U')
            elif char.upper() == 'T':
                new.append('A')
            else:
                raise ValueError(f'{char} is not a valid DNA nucleotide')
    if p[0] == '3':
        new.reverse()
    new_str = f'5’-{"".join(new)}-3’'
    
    return new_str

def RNA_DNA(sequence: str):
    # Reverse transription function
    p = check_polarity(sequence[0])
    new = f"{p[0]}’-"
    for char in sequence:
        if char not in ('5',"'",'`','3','-',' ','’'):
            if char.upper() == 'G':
                new += 'C'
            elif char.upper() == 'C':
                new += 'G'
            elif char.upper() == 'A':
                new += 'T'
            elif char.upper() == 'U':
                new += 'A'
            else:
                raise ValueError(f'{char} is not a valid RNA nucleotide')
    new += f"-{p[1]}’"
    return new

def RNA_Protein(sequence: str, start=True, stop=True, write='1'):
    # Translation function
    
    # Codon dictionary
    codons = {
        'AUA':'I', 'AUC':'I', 'AUU':'I', 'AUG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACU':'T',
        'AAC':'N', 'AAU':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGU':'S', 'AGA':'R', 'AGG':'R',                 
        'CUA':'L', 'CUC':'L', 'CUG':'L', 'CUU':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCU':'P',
        'CAC':'H', 'CAU':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGU':'R',
        'GUA':'V', 'GUC':'V', 'GUG':'V', 'GUU':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCU':'A',
        'GAC':'D', 'GAU':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGU':'G',
        'UCA':'S', 'UCC':'S', 'UCG':'S', 'UCU':'S',
        'UUC':'F', 'UUU':'F', 'UUA':'L', 'UUG':'L',
        'UAC':'Y', 'UAU':'Y', 'UAA':'_', 'UAG':'_',
        'UGC':'C', 'UGU':'C', 'UGA':'_', 'UGG':'W',
    }
    
    # AA name dictionary (1->3)
    aas = {
        'I':'Ile', 'M':'Met', 'T':'Thr', 'N':'Asn',
        'K':'Lys', 'S':'Ser', 'R':'Arg', 'L':'Leu',
        'P':'Pro', 'H':'His', 'Q':'Gln', 'V':'Val',
        'A':'Ala', 'D':'Asp', 'E':'Glu', 'G':'Gly',
        'F':'Phe', 'Y':'Tyr', 'C':'Cys', 'W':'Trp'
    }
    
    seq_list = [char for char in sequence if char in ['A','U','C','G']]
    if sequence[0] == '3':
        seq_list.reverse()
    seq = ''.join(seq_list)


    protein = 'N-'
    
    # Detection of start codon in mRNA
    if start_codon:
        starting_index = 0

        for i, char in enumerate(seq):
            if seq[i:i+3] == 'AUG':
                starting_index = i
                break

        seq = seq[i:]

    # Detection of stop codon in mRNA
    if stop_codon:
        end_index = len(seq)

        for i, char in enumerate(seq):
            if codons[seq[i:i+3]] == '_':
                end_index = i
                break

        seq = seq[:i]

    # Translation will only occur if there is an integer number of codons.
    x = 0
    y = False
    while x < 3:
        if len(seq)%3 == 0: # If there is an integer number of codons.
            for i in range(0, len(seq), 3):
                codon = seq[i:i + 3]
                if write == '1': # 1 letter abbreviations
                    protein += codons[codon]
                if write == '3': # 3 letter abbreviations
                    if i != 0:
                        protein += '-'
                    protein += aas[codons[codon]]
            break
        else:
            y = True
            seq = seq[:-1] # Trim last rNTP off sequence
            x += 1
    
    if y:
        protein += f'[{x}]' # Indicates number of rNTPs not included in translation.

    protein += '-C'
    return protein

def main():
    # Main
    sequence = ''.join(sys.argv[1:]) # Get sequence from arguments
    print(f'\nSequence provided ({seq_type(sequence)})') # Print input sequence type
    print(sequence) # Print input sequence
    print()
    
    dna_c = None
    dna_t = None

    # Handles coding or template strand
    if strand == 'template':
        dna_c = DNA_DNA(sequence)
        dna_t = DNA_DNA(dna_c)
    else:
        dna_c = False
        dna_t = DNA_DNA(sequence)
   
    rna = None

    if dna_c:
        dna_t = DNA_DNA(dna_c)
        dna_c = DNA_DNA(dna_t)
    else:
        dna_t = DNA_DNA(sequence)
        dna_c = DNA_DNA(dna_t)


    # Call replication function
    if replication:
        print('DNA -> DNA')
        print(dna_c, '(Coding strand)')
        print(dna_t, '(Template strand)')
        print()
        

    # Call transcription function
    if transcription:
        if dna_t is None:
            dna = dna_c
        else:
            dna = dna_t
        print('DNA -> mRNA')
        rna = DNA_RNA(dna)
        print(rna)
        print()

    # Call reverse transcription function
    if reverse_transcription:
        print('RNA -> DNA')
        rna = sequence
        dna_t = RNA_DNA(rna)
        dna_c = DNA_DNA(dna_t)
        print(dna_c, '(Coding strand)')
        print(dna_t, '(Template strand)')
        print()

    # Call translation function
    if translation:
        if rna is None:
            rna = sequence
        print('mRNA -> Protein')
        print(RNA_Protein(rna, write=translation_output))
        print()

if __name__ == '__main__':
    main()

############################################################
