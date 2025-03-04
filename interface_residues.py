from pymol import cmd
import re
import os

def find_interface_residues(pdb_filename, chain1, chain2, cutoff=5.0):
    """
    Identifies interface residues between two chains in the current PyMOL session.

    Parameters:
        chain1 (str): Chain ID of the first chain.
        chain2 (str): Chain ID of the second chain.
        cutoff (float): Distance cutoff for defining the interface (in Ångstroms).

    Returns:
        dict: A dictionary containing residues from both chains at the interface.
    """
    cmd.load(pdb_filename)
    # print("chains:", cmd.get_chains())
    # for chain in ['A', 'B', 'C', 'D', 'E']:
    #     seq = cmd.get_fastastr(f'chain {chain}')
    #     print(f'Chain {chain} sequence:')
    #     print(seq)

    # Create selections for the chains
    selection1 = f"chain {chain1}"
    selection2 = f"chain {chain2}"
    
    # Ensure the selections exist
    if not cmd.select(selection1) or not cmd.select(selection2):
        raise ValueError(f"One or both chain selections ({chain1}, {chain2}) do not exist.")
    
    # Identify atoms within the cutoff distance
    cmd.select("interface_atoms1", f"byres ({selection1} within {cutoff} of {selection2})")
    cmd.select("interface_atoms2", f"byres ({selection2} within {cutoff} of {selection1})")
    
    # Extract residues from the interface selections
    interface_residues1 = cmd.get_model("interface_atoms1")
    interface_residues2 = cmd.get_model("interface_atoms2")
    
    # Helper function to handle sorting of residues
    def parse_residue_id(residue):
        # This function will extract numeric and alphanumeric parts for proper sorting
        match = re.match(r'(\d+)([A-Za-z]*)', residue)
        if match:
            return int(match.group(1)), match.group(2)
        else:
            return 0, ""  # Default in case of missing match
    
    # Parse residue information
    residues1 = {(res.chain, res.resi, res.resn) for res in interface_residues1.atom}
    residues2 = {(res.chain, res.resi, res.resn) for res in interface_residues2.atom}
    
    # Sort residues based on the numeric and alphanumeric parts of their residue ID
    sorted_residues1 = sorted(residues1, key=lambda x: parse_residue_id(x[1]))
    sorted_residues2 = sorted(residues2, key=lambda x: parse_residue_id(x[1]))
    
    cmd.delete("all")

    # Return results
    return {
        "chain1_residues": sorted_residues1,
        "chain2_residues": sorted_residues2
    }



# Example Usage
if __name__ == "__main__":
    pdb_paths = []
    # traverse results/ recursively
    results_dir = "results"
    for root, dirs, files in os.walk(results_dir):
        for file in files:
            if file.endswith(".pdb"):
                pdb_path = os.path.join(root, file)
                print(f"Processing {pdb_path}")
                pdb_paths.append(pdb_path)


    # pdb_paths = [
        # "20241106_merged3/5/d_Ab_0082.pdb_2024_11_05__10_06_02/MultipleCDRs/0094.pdb",
        # "results/6nca_7re7/codesign_multicdrs_6/6_Ab_0000.pdb_2025_01_21__02_46_43/reference.pdb",
        # "20241106_merged3/2/d_Ab_0067.pdb_2024_11_05__09_18_29/MultipleCDRs/0032.pdb"
        # ]
    # pdb_paths = [
    #     "af_output/0.87/0.87.pdb"
    #     ]
    # chain1_id = "A"
    # chain2_id = "D"
    # chain2_name = 'H'
    # chain3_id = "E"
    # chain3_name = 'L'
    chain1_id = "A"
    chain2_id = "H"
    chain2_name = 'H'
    chain3_id = "L"
    chain3_name = 'L'
    cutoff_distance = 5.0
    
    output_paths = []
    for i, pdb_path in enumerate(pdb_paths):
        # print(f"**** {i + 1} ****")

        result = find_interface_residues(pdb_path, chain1_id, chain2_id, cutoff_distance)

        if result["chain1_residues"]:
            print(f"path: {pdb_path}")
            output_paths.append(pdb_path)
            print(f"Interface residues for Chain {chain1_id}:")
            for chain, resi, resn in result["chain1_residues"]:
                # print(f"Chain {chain} Residue {resn} ({resi})")
                print(f"{resn} ({resi})")
        
        if result["chain1_residues"]:
            print(f"\nInterface residues for Chain {chain2_name}:")
            for chain, resi, resn in result["chain2_residues"]:
                # print(f"Chain {chain} Residue {resn} ({resi})")
                print(f"{resn} ({resi})")

        result = find_interface_residues(pdb_path, chain1_id, chain3_id, cutoff_distance)

        if result["chain1_residues"]:
            print(f"path: {pdb_path}")
            output_paths.append(pdb_path)
            print(f"Interface residues for Chain {chain1_id}:")
            for chain, resi, resn in result["chain1_residues"]:
                # print(f"Chain {chain} Residue {resn} ({resi})")
                print(f"{resn} ({resi})")
        
        if result["chain1_residues"]:
            print(f"\nInterface residues for Chain {chain3_name}:")
            for chain, resi, resn in result["chain2_residues"]:
                # print(f"Chain {chain} Residue {resn} ({resi})")
                print(f"{resn} ({resi})")

    print(output_paths)

