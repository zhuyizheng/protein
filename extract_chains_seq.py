import os
from Bio import PDB
from Bio.PDB.Polypeptide import PPBuilder
import pathlib

def extract_sequence_from_chain(chain):
    """Extract amino acid sequence from a chain using PPBuilder."""
    ppb = PPBuilder()
    seq = ""
    for pp in ppb.build_peptides(chain):
        seq += str(pp.get_sequence())
    return seq

def process_pdb_file(input_path, output_base_path, H_name='H', L_name='L'):
    """Process a single PDB file and save H and L chains."""
    # Create parser
    parser = PDB.PDBParser(QUIET=True)
    
    # Parse structure
    structure = parser.get_structure('structure', input_path)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_base_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Dictionary to store H and L sequences
    sequences = {}
    
    # Extract sequences for H and L chains
    for model in structure:
        for chain in model:
            chain_id = chain.get_id()
            if chain_id in [H_name, L_name]:
                sequence = extract_sequence_from_chain(chain)
                if sequence:
                    sequences[chain_id] = sequence
    
    # Only save if both H and L chains are present
    if H_name in sequences and L_name in sequences:
        output_file = f"{output_base_path}.fasta"
        with open(output_file, 'w') as f:
            f.write(f">{os.path.basename(input_path)}_H\n")
            f.write(f"{sequences[H_name]}\n")
            f.write(f">{os.path.basename(input_path)}_L\n")
            f.write(f"{sequences[L_name]}\n")

def main():
    input_base = "20241106_merged3"
    output_base = "20241106_merged3_seq"
    
    # Find all PDB files recursively
    for root, dirs, files in os.walk(input_base):
        for file in files:
            if file.endswith('.pdb'):
                # Get input file path
                input_path = os.path.join(root, file)
                
                # Create corresponding output path
                relative_path = os.path.relpath(input_path, input_base)
                output_path = os.path.join(output_base, relative_path)
                output_path = os.path.splitext(output_path)[0]  # Remove .pdb extension
                
                try:
                    process_pdb_file(input_path, output_path)
                    print(f"Processed: {input_path}")
                except Exception as e:
                    print(f"Error processing {input_path}: {str(e)}")

if __name__ == "__main__":
    main()
