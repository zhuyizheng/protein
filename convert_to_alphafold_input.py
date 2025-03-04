from dataclasses import dataclass
from fasta_to_dict import fasta_to_dict
import json
import os

@dataclass
class ABCChains:
    name: str
    chainA: str
    chainB: str
    chainC: str



def convert_to_sequences_json(H_seq: str, L_seq: str, chains: ABCChains, copies=1) -> list:
    def convert_to_entry(id: str, sequence: str) -> dict:
        return {
            "protein": {
                "id": id,
                "sequence": sequence
            }
        }
    
    letter_mapping = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ret = []
    for i in range(copies):
        letter = letter_mapping[i] if copies > 1 else ""
        ret.append(convert_to_entry(f"A{letter}", chains.chainA))
        ret.append(convert_to_entry(f"B{letter}", chains.chainB))
        ret.append(convert_to_entry(f"C{letter}", chains.chainC))
        ret.append(convert_to_entry(f"L{letter}", L_seq))
        ret.append(convert_to_entry(f"H{letter}", H_seq))
    return ret


def convert_to_alphafold_input_one_fasta(output_filename: str, chains: ABCChains, H_seq, L_seq, copies=1) -> None:
    json_output = {
        "name": chains.name,
        "sequences": convert_to_sequences_json(H_seq, L_seq, chains, copies),
        "modelSeeds": [1],
        "dialect": "alphafold3",
        "version": 1
    }

    output_dir = os.path.dirname(output_filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_filename, 'w') as f:
        json.dump(json_output, f, indent=4)


def convert_folder(input_base, output_base, chainA, chainB, chainC, copies):
    # Find all PDB files recursively
    for root, dirs, files in os.walk(input_base):
        for file in files:
            if file.endswith('.fasta'):
                # Get input file path
                input_path = os.path.join(root, file)
                
                # Create corresponding output path
                relative_path = os.path.relpath(input_path, input_base)
                output_path = os.path.join(output_base, relative_path)
                output_path = os.path.splitext(output_path)[0] + '.json'  # Remove .pdb extension
                output_path = str(output_path).replace('/', '__')
                
                chains = ABCChains(name=output_path.split('.')[0], chainA=chainA, chainB=chainB, chainC=chainC)
                HL_dict = fasta_to_dict(input_path)
                for chain_id, sequence in HL_dict.items():
                    if chain_id.endswith('H'):
                        H_seq = sequence
                    elif chain_id.endswith('L'):
                        L_seq = sequence

                try:
                    convert_to_alphafold_input_one_fasta(output_path, chains, H_seq, L_seq, copies)
                    print(f"Processed: {input_path}")
                except Exception as e:
                    print(f"Error processing {input_path}: {str(e)}")


if __name__ == "__main__":

    ### 6nca
    input_base = "copied_results_chains"
    output_base = "copied_results_chains_af_input"
    chainA = "GSHSMRYFFTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDGETRKVKAHSQTHRVDLGTLRGYYNQSEAGSHTVQRMYGCDVGSDWRFLRGYHQYAYDGKDYIALKEDLRSWTAADMAAQTTKHKWEAAHVAEQLRAYLEGTCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGQEQRYTCHVQHEGLPKPLTLRWE"
    chainB = "MIQRTPKIQVYSRHPAENGKSNFLNCYVSGFHPSDIEVDLLKNGERIEKVEHSDLSFSKDWSFYLLYYTEFTPTEKDEYACRVNHVTLSQPKIVKWDRDM"
    chainC = "YVLDHLIVV"
    copies = 1
    convert_folder(input_base, output_base, chainA, chainB, chainC, copies)


    # ### 5grd
    # input_base = "20241106_merged3_seq"
    # output_base = "20241106_merged3_seq_af_input"
    # chainA = "GSHSMRYFYTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDQETRNVKAQSQTDRVDLGTLRGYYNQSEDGSHTIQIMYGCDVGPDGRFLRGYRQDAYDGKDYIALNEDLRSWTAADMAAQITKRKWEAAHAAEQQRAYLEGRCVEWLRRYLENGKETLQRTDPPKTHMTHHPISDHEATLRCWALGFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGEEQRYTCHVQHEGLPKPLTLRW"
    # chainB = "IQRTPKIQVYSRHPAENGKSNFLNCYVSGFHPSDIEVDLLKNGERIEKVEHSDLSFSKDWSFYLLYYTEFTPTEKDEYACRVNHVTLSQPKIVKWDRDM"
    # chainC = "SSCSSCPLSK"
    # copies = 1
    # convert_folder(input_base, output_base, chainA, chainB, chainC, copies)


    # ### 7re7 original (to check correctness of alphafold)
    # chainA = "GSHSMRYFFTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDGETRKVKAHSQTHRVDLGTLRGYYNQSEAGSHTVQRMYGCDVGSDWRFLRGYHQYAYDGKDYIALKEDLRSWTAADMAAQTTKHKWEAAHVAEQLRAYLEGTCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQKWAAVVVPSGQEQRYTCHVQHEGLPKPLTLRWEP"
    # chainB = "MIQRTPKIQVYSRHPAENGKSNFLNCYVSGFHPSDIEVDLLKNGERIEKVEHSDLSFSKDWSFYLLYYTEFTPTEKDEYACRVNHVTLSQPKIVKWDRDM"
    # chainC = "FMNKFIYEI"
    # H_seq = "EVQLVQSGAEVKKPGESLTISCKASGYSFPNYWITWVRQMSGGGLEWMGRIDPGDSYTTYNPSFQGHVTISIDKSTNTAYLHWNSLKASDTAMYYCARYYVSLVDIWGQGTLVTVSSASTKGPSVFPLAPSSGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEP"
    # L_seq = "SVLTQPASVSGSPGQSITISCTGTSSDVGGYNYVSWYQQHPGKAPKLMIYDVNNRPSEVSNRFSGSKSGNTASLTISGLQAEDEADYYCSSYTTGSRAVFGGGTKLTVLGQPKANPTVTLFPPSSEELQANKATLVCLISDFYPGAVTVAWKADGSPVKAGVETTKPSKQSNNKYAASSYLSLTPEQWKSHRSYSCQVTHEGSTVEKTVAP"
    # copies = 1
    # chains = ABCChains(name="7re7_orig", chainA=chainA, chainB=chainB, chainC=chainC)
    # # convert_to_alphafold_input_one_fasta('af_input/7re7_orig.json', chains, H_seq, L_seq, copies=copies)
    
