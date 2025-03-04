from Bio.PDB import PDBParser, PDBIO, Select

class ChainSelector(Select):
    def __init__(self, chains_to_keep):
        self.chains_to_keep = chains_to_keep

    def accept_chain(self, chain):
        # Accept only the chains specified
        return chain.id in self.chains_to_keep

def extract_chains(input_pdb, output_pdb, chains):
    """
    Extract specified chains from a PDB file and save to a new PDB file.

    Args:
        input_pdb (str): Path to the input PDB file.
        output_pdb (str): Path to save the new PDB file.
        chains (list): List of chain IDs to extract.
    """
    # Parse the structure
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("structure", input_pdb)

    # Set up the PDB writer and selector
    io = PDBIO()
    io.set_structure(structure)
    io.save(output_pdb, ChainSelector(chains))


def extract_chains_auto_filename(input_pdb, chains):
    chains_str = ''.join(chains)
    output_pdb = input_pdb[:-len('.pdb')] + f'_{chains_str}.pdb'
    extract_chains(input_pdb, output_pdb, chains)

# Example usage:
# Extract chains A, B, and C from 'input.pdb' and save to 'output.pdb'
# extract_chains("7re7.pdb", "7re7_HL.pdb", ["H", "L"])
extract_chains_auto_filename("6nca.pdb", ["Y", "I"])