# PySeq
Convert DNA/RNA sequences with polarity.
(Now includes GUI)

Functions:
- Convert DNA to DNA (replication)
  - Displays coding and template strand
- Convert DNA to RNA (translation)
  - Displays mRNA 5' -> 3'
- Convert RNA to DNA (reverse transcription)
  - Displays coding and template strand
- Convert RNA to protein (translation)
  - Displays AA sequence N -> C
  - Can detect start & stop codons
  - Can print 1 or 3 letter abbreviations

Examples:

`$ sequence.py TATACGATGCGCTTATGCTGACCGGTA`

```
Sequence provided (DNA)
TATACGATGCGCTTATGCTGACCGGTA

DNA -> DNA
(No polarity given)
5’-TATACGATGCGCTTATGCTGACCGGTA-3’ (Coding strand)
3’-ATATGCTACGCGAATACGACTGGCCAT-5’ (Template strand)

DNA -> mRNA
5’-UAUACGAUGCGCUUAUGCUGACCGGUA-3’

mRNA -> Protein
N-YTMRLC_PV-C
```

`$ sequence.py --start --stop TATACGATGCGCTTATGCTGACCGGTA`

```
Sequence provided (DNA)
TATACGATGCGCTTATGCTGACCGGTA

DNA -> DNA
(No polarity given)
5’-TATACGATGCGCTTATGCTGACCGGTA-3’ (Coding strand)
3’-ATATGCTACGCGAATACGACTGGCCAT-5’ (Template strand)

DNA -> mRNA
5’-UAUACGAUGCGCUUAUGCUGACCGGUA-3’

mRNA -> Protein
N-MRLC-C
```

`$ sequence.py --three ATGCGCTTATGC`

```
Sequence provided (DNA)
ATGCGCTTATGC

DNA -> DNA
(No polarity given)
5’-ATGCGCTTATGC-3’ (Coding strand)
3’-TACGCGAATACG-5’ (Template strand)

DNA -> mRNA
5’-AUGCGCUUAUGC-3’

mRNA -> Protein
N-Met-Arg-Leu-Cys-C
```

`$ sequence.py UAUACGAUGCGCUUAUGCUGACCGGUA`

```
Sequence provided (RNA)
UAUACGAUGCGCUUAUGCUGACCGGUA

RNA -> DNA
(No polarity given)
5’-TATACGATGCGCTTATGCTGACCGGTA-3’ (Coding strand)
3’-ATATGCTACGCGAATACGACTGGCCAT-5’ (Template strand)

mRNA -> Protein
N-YTMRLC_PV-C
```

`$ sequence.py --translation --start --stop UAUACGAUGCGCUUAUGCUGACCGGUA`

```
Sequence provided (RNA)
UAUACGAUGCGCUUAUGCUGACCGGUA

mRNA -> Protein
N-MRLC-C
```

`$ sequence.py --replication 3’-TATACGATGCGCTTATGCTGACCGGTA`

```
Sequence provided (DNA)
3’-TATACGATGCGCTTATGCTGACCGGTA

DNA -> DNA
3’-TATACGATGCGCTTATGCTGACCGGTA-5’ (Coding strand)
5’-ATATGCTACGCGAATACGACTGGCCAT-3’ (Template strand)
```

`$ sequence.py --template 5’-TATACGATGCGCTTATGCTGACCGGTA`

```
Sequence provided (DNA)
5’-TATACGATGCGCTTATGCTGACCGGTA

DNA -> DNA
3’-ATATGCTACGCGAATACGACTGGCCAT-5’ (Coding strand)
5’-TATACGATGCGCTTATGCTGACCGGTA-3’ (Template strand)

DNA -> mRNA
5’-UACCGGUCAGCAUAAGCGCAUCGUAUA-3’

mRNA -> Protein
N-YRSA_AHRI-C
```

`$ sequence.py --template --transcription --translation --stop 5’-TATACGATGCGCTTATGCTGACCGGTA`

```
Sequence provided (DNA)
5’-TATACGATGCGCTTATGCTGACCGGTA

DNA -> mRNA
5’-UACCGGUCAGCAUAAGCGCAUCGUAUA-3’

mRNA -> Protein
N-YRSA-C
```
