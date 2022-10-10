#!/usr/bin/env python3

import tkinter as tk
import tkinter.font as tkFont
import sys
from sequence import *

class App:
    # GUI Program
    def __init__(self, root):
        self.init_app(root)

    def init_app(self, root):
        #setting title
        root.title("Convert DNA/RNA sequences with polarity!")
        #setting window size
        width=729
        height=385
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
       
        self.calls_to_check = 0

        # Initialization of console
        self.console=tk.Text(root)
        self.console["bg"] = "#000000"
        self.ft = tkFont.Font(family='Cambria Math',size=10)
        self.console["font"] = self.ft
        self.console["fg"] = "#2cff02"
        self.console.place(x=60,y=80,width=626,height=273)

        # Initialization of convert button
        self.convert_button=tk.Button(root)
        self.convert_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Calibri',size=10)
        self.convert_button["font"] = ft
        self.convert_button["fg"] = "#000000"
        self.convert_button["justify"] = "center"
        self.convert_button["text"] = "Convert!"
        self.convert_button.place(x=620,y=40,width=66,height=30)
        self.convert_button["command"] = self.convert_button_command
        
        # Initialization of input sequence entry box
        self.input_seq=tk.Entry(root)
        self.input_seq["borderwidth"] = "1px"
        ft = tkFont.Font(family='Calibri',size=10)
        self.input_seq["font"] = ft
        self.input_seq["fg"] = "#333333"
        self.input_seq["justify"] = "center"
        self.input_seq["text"] = "Enter sequence..."
        self.input_seq.place(x=60,y=40,width=547,height=30)

        # Sets default value of radio buttons
        self.radio_val = 5

        # Initialization of 5' radio buttoni
        self.radio_5=tk.Radiobutton(root)
        ft = tkFont.Font(family='Calibri',size=10)
        self.radio_5["font"] = ft
        self.radio_5["fg"] = "#333333"
        self.radio_5["justify"] = "center"
        self.radio_5["text"] = "5'-"
        self.radio_5['value'] = 5
        self.radio_5['variable'] = self.radio_val
        self.radio_5.place(x=10,y=35,width=45,height=18)
        self.radio_5["command"] = self.radio_5_command
        self.radio_5.select()
        
        # Initialization of 3' radio button
        self.radio_3=tk.Radiobutton(root)
        ft = tkFont.Font(family='Calibri',size=10)
        self.radio_3["font"] = ft
        self.radio_3["fg"] = "#333333"
        self.radio_3["justify"] = "center"
        self.radio_3["text"] = "3'-"
        self.radio_3['value'] = 3
        self.radio_3['variable'] = self.radio_val
        self.radio_3.place(x=10,y=55,width=45,height=18)
        self.radio_3["command"] = self.radio_3_command
        self.radio_3.deselect()

        # Default operations
        self.operations = ['replication','transcription','translation']


        # Initialization of replication check box
        self.replication = tk.IntVar()
        self.replication_check=tk.Checkbutton(root)
        self.replication_check['variable'] = self.replication
        ft = tkFont.Font(family='Calibri',size=10)
        self.replication_check["font"] = ft
        self.replication_check["fg"] = "#333333"
        self.replication_check["justify"] = "center"
        self.replication_check["text"] = "Replication"
        self.replication_check.place(x=80,y=10,width=110,height=30)
        self.replication_check["offvalue"] = 0
        self.replication_check["onvalue"] = 1
        self.replication_check["command"] = self.check_command()
        self.replication_check.select()

        # Initialization of transcription check box
        self.transcription = tk.IntVar()
        self.transcription_check=tk.Checkbutton(root)
        self.transcription_check['variable'] = self.transcription
        ft = tkFont.Font(family='Calibri',size=10)
        self.transcription_check["font"] = ft
        self.transcription_check["fg"] = "#333333"
        self.transcription_check["justify"] = "center"
        self.transcription_check["text"] = "Transcription"
        self.transcription_check.place(x=210,y=10,width=115,height=30)
        self.transcription_check["offvalue"] = 0
        self.transcription_check["onvalue"] = 1
        self.transcription_check["command"] = self.check_command()
        self.transcription_check.select()

        # Initialization of translation check box
        self.translation = tk.IntVar()
        self.translation_check=tk.Checkbutton(root)
        self.translation_check['variable'] = self.translation
        ft = tkFont.Font(family='Calibri',size=10)
        self.translation_check["font"] = ft
        self.translation_check["fg"] = "#333333"
        self.translation_check["justify"] = "center"
        self.translation_check["text"] = "Translation"
        self.translation_check.place(x=325,y=10,width=110,height=30)
        self.translation_check["offvalue"] = 0
        self.translation_check["onvalue"] = 1
        self.translation_check["command"] = self.check_command()
        self.translation_check.select()

        # Initialization of reverse transcription check box
        self.rev_trans = tk.IntVar()
        self.rev_trans_check=tk.Checkbutton(root)
        self.rev_trans_check['variable'] = self.rev_trans
        ft = tkFont.Font(family='Calibri',size=10)
        self.rev_trans_check["font"] = ft
        self.rev_trans_check["fg"] = "#333333"
        self.rev_trans_check["justify"] = "center"
        self.rev_trans_check["text"] = "Reverse Transciption"
        self.rev_trans_check.place(x=440,y=10,width=165,height=30)
        self.rev_trans_check["offvalue"] = 0
        self.rev_trans_check["onvalue"] = 1
        self.rev_trans_check["command"] = self.check_command()
        self.rev_trans_check.deselect() 

    def write_to_console(self, text):
        # Equivalent to 'print()' for console in App.
        self.console.insert(tk.END, f'{text}\n')

    def get_strand(self):
        # Determines 'coding' or 'template' strand input
        return 'coding'

    def get_trans(self):
        # Determines 1 or 3 letter abbreviation for translation output
        return '1'

    def convert_button_command(self):
        # Clears console
        self.console.delete('1.0','end')

        # Gets input sequence and polarity
        var = self.input_seq.get()
        polarity = self.radio_val
        seq = f"{polarity}-{var}"
        s_type = seq_type(seq)
        strand = self.get_strand()
        
        # Determines which funcitons will be performed
        vals = self.check_vars()
        translation_output = self.get_trans()
        
        # Makes sure input makes sense with selected functions
        if (vals['rev_trans']) and (s_type == 'DNA'):
            self.write_to_console(f'Cannot reverse transcribe DNA!')
            return
        elif (vals['replication']) and (s_type == 'RNA'):
            self.write_to_console('Cannot replicate RNA')
            return

        # Beginning of output
        self.write_to_console(f'\nSequence provided: ({s_type})')
        self.write_to_console(f'{seq}\n')

        if s_type != 'RNA':
            # Handles coding or template strand
            if strand == 'template':
                dna_c = DNA_DNA(seq)
                dna_t = DNA_DNA(dna_c)
            else:
                dna_c = False
                dna_t = DNA_DNA(seq)
            
            rna = None

            # Handles order of operations
            if dna_c:
                dna_t = DNA_DNA(dna_c)
                dna_c = DNA_DNA(dna_t)
            else:
                dna_t = DNA_DNA(seq)
                dna_c = DNA_DNA(dna_t)
        else:
            rna = seq
            dna_t = RNA_DNA(rna)
            dna_c = DNA_DNA(dna_t)

        if vals['replication']:
            # Replication
            self.write_to_console('DNA')
            self.write_to_console(f'{dna_c}\n{dna_t}\n')

        if vals['rev_trans']:
            # Reverse transcription
            self.write_to_console('DNA')
            self.write_to_console(f'{dna_c}\n{dna_t}\n')

        if dna_t is None:
            dna = dna_c
        else:
            dna = dna_t

        rna = DNA_RNA(dna)
            
        if vals['transcription']:
            # Transcription
            self.write_to_console('mRNA')
            self.write_to_console(f'{rna}\n')


        if vals['translation']:
            # Translation
            if rna is None:
                rna = seq
            self.write_to_console('Protein')
            self.write_to_console(f'{RNA_Protein(rna, write=translation_output)}\n')


    def radio_5_command(self):
        self.radio_val = 5 # 5 prime

    def radio_3_command(self):
        self.radio_val = 3 # 3 prime

    def check_vars(self):
        # Create dictionary for check variables
        return {'replication': self.replication.get(),
                'transcription': self.transcription.get(),
                'translation': self.translation.get(),
                'rev_trans': self.rev_trans.get()} 

    def check_command(self):
        # Function for checking of box
        pass

if __name__ == "__main__":
    root = tk.Tk() # Launch tkinter
    app = App(root) # Initialize application
    root.mainloop() # Start application
