#!/usr/bin/env python3

# USAGE:
# ./sequence.py {OPTIONS} SEQUENCE

import sys

def display_help():
    print()
    print('Convert DNA/RNA sequences with polarity')
    print('By default, detects DNA or RNA; displays replication, transcription, & translation')
    print('(Made by Spencer Wozniak)')
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
    for char in sequence:
        if char == 'T':
            return 'DNA'
        elif char == 'U':
            return 'RNA'

selection = False
replication = False
transcription = False
reverse_transcription = False
translation = False
start_codon = False
stop_codon = False
translation_output = '1'
strand = 'coding'

for arg in sys.argv[1:]:
    if arg in ('-h','-help','--help'):
        display_help()
    elif arg == '--replication':
        replication = True
        selection = True
        sys.argv.remove(arg)
    elif arg == '--transcription':
        transcription = True
        selection = True
        sys.argv.remove(arg)
    elif arg == '--reverse-transcription':
        reverse_transcription = True
        selection = True
        sys.argv.remove(arg)
    elif arg == '--three':
        translation_output = '3'
        sys.argv.remove(arg)
    elif arg == '--template':
        strand = 'template'
        sys.argv.remove(arg)
    elif arg == '--coding':
        strand = 'coding'
        sys.argv.remove(arg)
    elif arg == '--start':
        start_codon = True
        sys.argv.remove(arg)
    elif arg == '--stop':
        stop_codon = True
        sys.argv.remove(arg)
    elif arg[0:2] == '--':
        raise ValueError(f'"{arg}" is not a valid argument. Use "-h" to see arguments.')

sequence = ''.join(sys.argv[1:])

if not selection:
    if seq_type(sequence) == 'DNA':
        replication = True
        transcription = True
        translation = True
    elif seq_type(sequence) == 'RNA':
        reverse_transcription = True
        translation = True


def check_polarity(char: str):
    if char == '5':
        return ('3','5')
    elif char == '3':
        return ('5','3')
    elif char in ('G','C','U','T','A'):
        sys.stderr.write('(No polarity given)\n')
        return ('3','5')
    else:
        raise ValueError('Invalid polarity')

def DNA_DNA(sequence: str):
    p = check_polarity(sequence[0])
    new = []
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
    p = check_polarity(sequence[0])
    new = f"{p[0]}’-"
    for char in sequence:
        if char not in ('5',"'",'`','3','-',' ','’'):
            if char.upper() == 'G':
                new += 'C'
            elif char.upper() == 'C':
                new += 'G'
            elif char.upper() == 'A':
                new += 'U'
            elif char.upper() == 'T':
                new += 'A'
            else:
                raise ValueError(f'{char} is not a valid DNA nucleotide')
    new += f"-{p[1]}’"
    return new

def RNA_DNA(sequence: str):
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

    aas = {
        'I':'Ile', 'M':'Met', 'T':'Thr', 'N':'Asn',
        'K':'Lys', 'S':'Ser', 'R':'Arg', 'L':'Leu',
        'P':'Pro', 'H':'His', 'Q':'Gln', 'V':'Val',
        'A':'Ala', 'D':'Asp', 'E':'Glu', 'G':'Gly',
        'F':'Phe', 'Y':'Tyr', 'C':'Cys', 'W':'Trp'
    }
    
        
    seq = ''.join([char for char in sequence if char in ['A','U','C','G']])

    protein = 'N-'
    
    if start_codon:
        starting_index = 0

        for i, char in enumerate(seq):
            if seq[i:i+3] == 'AUG':
                starting_index = i
                break

        seq = seq[i:]

    if stop_codon:
        end_index = len(seq)

        for i, char in enumerate(seq):
            if codons[seq[i:i+3]] == '_':
                end_index = i
                break

        seq = seq[:i]

    if len(seq)%3 == 0:
        for i in range(0, len(seq), 3):
            codon = seq[i:i + 3]
            if write == '1':
                protein += codons[codon]
            if write == '3':
                if i != 0:
                    protein += '-'
                protein += aas[codons[codon]]
    else:
        protein += ' (Not a valid sequence for translation) '

    protein += '-C'
    return protein

def main():
    sequence = ''.join(sys.argv[1:])
    print(f'\nSequence provided ({seq_type(sequence)})')
    print(sequence)
    print()
    
    if strand == 'template':
        dna_c = DNA_DNA(sequence)
    else:
        dna_c = False
    
    if replication:
        print('DNA -> DNA')
        if dna_c:
            dna_t = DNA_DNA(dna_c)
            dna_c = DNA_DNA(dna_t)
        else:
            dna_t = DNA_DNA(sequence)
            dna_c = DNA_DNA(dna_t)

        print(dna_c, '(Coding strand)')
        print(dna_t, '(Template strand)')
        print()
    
    if transcription:
        print('DNA -> mRNA')
        rna = DNA_RNA(dna_t)
        print(rna)
        print()
    if reverse_transcription:
        print('RNA -> DNA')
        rna = sequence
        dna = RNA_DNA(rna)
        print(dna)
        print()
    if translation:
        print('mRNA -> Protein')
        print(RNA_Protein(rna, write=translation_output))
        print()

if __name__ == '__main__':
    main()
