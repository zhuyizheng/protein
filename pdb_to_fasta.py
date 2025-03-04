import pymol
from pymol import cmd

# pdb_filename = "./20241106_merged3/selected/3.pdb"
pdb_filename = "./7re7.pdb"
# pdb_filename = "6nca.pdb"
# chains_to_extract = ['A', 'B', 'C', 'H', 'L']
# chains_to_extract = ['Y', 'I', 'd']
chains_to_extract = ['A', 'B', 'C', 'H', 'L']


def pdb_to_fasta(pdb_filename, chains_to_extract):
    pymol.cmd.load(pdb_filename)

    # print("chains:", pymol.cmd.get_chains())

    fasta_seq = ""

    # Get sequence information for each chain to identify the peptide
    for chain in chains_to_extract:
    # for chain in pymol.cmd.get_chains():
        pymol.cmd.delete("all")
        pymol.cmd.load(pdb_filename)
        seq = cmd.get_fastastr(f'chain {chain}')
        
        # extract the value of seq from the second line on
        # split() returns a list where elements are separated by whitespace
        # [1] gets the second element of the list
        # strip() removes leading and trailing whitespaces
        seq = '\n'.join(seq.split('\n')[1:]).strip()

        # print(f'Chain {chain} sequence:')
        # print(seq)
        fasta_seq += f">protein|name={chain}\n{seq}\n"
    
    pymol.cmd.delete("all")
    return fasta_seq


def get_chain_seq(pdb_filename, chain):
    print("pdb_to_fasta function called with pdb_filename:", pdb_filename)
    pymol.cmd.load(pdb_filename)
    
    seq = cmd.get_fastastr(f'chain {chain}')
    seq = ''.join(seq.split('\n')[1:]).strip()
    pymol.cmd.delete("all")
    return seq

fasta_sequence = pdb_to_fasta(pdb_filename, chains_to_extract)
print(fasta_sequence)
