import os
from Bio import PDB
from Bio.PDB.Polypeptide import PPBuilder
import pathlib


def fasta_to_dict(fasta_file):
    """
    Convert a FASTA file to a dictionary where keys are chain names and values are sequences.
    
    Args:
        fasta_file (str): Path to the FASTA file
        
    Returns:
        dict: Dictionary with chain names as keys and sequences as values
    """
    sequences = {}
    current_chain = None
    current_sequence = []
    
    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            if line.startswith('>'):  # Header line
                if current_chain is not None:  # Save the previous sequence
                    sequences[current_chain] = ''.join(current_sequence)
                current_chain = line[1:]  # Remove the '>' character
                current_sequence = []
            else:  # Sequence line
                current_sequence.append(line)
    
    # Don't forget to save the last sequence
    if current_chain is not None:
        sequences[current_chain] = ''.join(current_sequence)
    
    return sequences



print(fasta_to_dict('copied_results_chains/results/6nca_7re7/codesign_multicdrs_6666666666/6_Ab_0009.pdb_2025_01_28__02_02_46/reference.fasta'))
# print(fasta_to_dict('results_20250120_chains/6nca_7re7/codesign_multicdrs_6/6_Ab_0057.pdb_2025_01_20__02_08_18/reference.fasta'))

# def process_pdb_file(input_path, output_base_path):
#     """Process a single PDB file and save H and L chains."""
#     # Create parser
#     parser = PDB.PDBParser(QUIET=True)
    
#     # Parse structure
#     structure = parser.get_structure('structure', input_path)
    
#     # Create output directory if it doesn't exist
#     output_dir = os.path.dirname(output_base_path)
#     os.makedirs(output_dir, exist_ok=True)
    
#     # Dictionary to store H and L sequences
#     sequences = {}
    
#     # Extract sequences for H and L chains
#     for model in structure:
#         for chain in model:
#             chain_id = chain.get_id()
#             if chain_id in ['H', 'L']:
#                 sequence = extract_sequence_from_chain(chain)
#                 if sequence:
#                     sequences[chain_id] = sequence
    
#     # Only save if both H and L chains are present
#     if 'H' in sequences and 'L' in sequences:
#         output_file = f"{output_base_path}.fasta"
#         with open(output_file, 'w') as f:
#             f.write(f">{os.path.basename(input_path)}_H\n")
#             f.write(f"{sequences['H']}\n")
#             f.write(f">{os.path.basename(input_path)}_L\n")
#             f.write(f"{sequences['L']}\n")

# def main():
#     input_base = "results_20250120"
#     output_base = "results_20250120_chains"
    
#     # Find all PDB files recursively
#     for root, dirs, files in os.walk(input_base):
#         for file in files:
#             if file.endswith('.pdb'):
#                 # Get input file path
#                 input_path = os.path.join(root, file)
                
#                 # Create corresponding output path
#                 relative_path = os.path.relpath(input_path, input_base)
#                 output_path = os.path.join(output_base, relative_path)
#                 output_path = os.path.splitext(output_path)[0]  # Remove .pdb extension
                
#                 try:
#                     process_pdb_file(input_path, output_path)
#                     print(f"Processed: {input_path}")
#                 except Exception as e:
#                     print(f"Error processing {input_path}: {str(e)}")

# if __name__ == "__main__":
#     main()
