import os
import json

def read_high_confidences(base_path: str) -> dict:
    """
    Reads JSON files from subfolders and checks if entries at indexes [2][3] and [2][4]
    of the "my_key" matrix are both greater than 0.7.

    Additionally, reads data from "data.json" in the same subfolder and includes it in the result.

    Args:
        base_path (str): The path to the base folder containing subfolders.

    Returns:
        dict: A dictionary where keys are folder names and values are tuples containing the pair of numbers
              and the content from "data.json".
    """
    result = {}

    # Iterate through subfolders
    for subfolder in os.listdir(base_path):
        subfolder_path = os.path.join(base_path, subfolder)

        # Check if it's a directory
        if os.path.isdir(subfolder_path):
            summary_values = None
            additional_data = None

            # Find the JSON files
            for file_name in os.listdir(subfolder_path):
                json_path = os.path.join(subfolder_path, file_name)

                if file_name.endswith("summary_confidences.json"):
                    try:
                        # Read and parse the JSON file
                        with open(json_path, 'r') as json_file:
                            data = json.load(json_file)
                            matrix = data.get("chain_pair_iptm", [])

                            # Ensure the matrix has valid dimensions
                            if len(matrix) > 2 and len(matrix[2]) > 4:
                                value_23 = matrix[2][3]
                                value_24 = matrix[2][4]

                                # Check if both values are greater than 0.7
                                if value_23 >= 0.8 or value_24 >= 0.8:
                                    summary_values = (value_23, value_24)
                    except (json.JSONDecodeError, KeyError, IOError) as e:
                        print(f"Error reading file {json_path}: {e}")

                elif file_name.endswith("data.json"):
                    try:
                        with open(json_path, 'r') as json_file:
                            additional_data = json.load(json_file)
                            additional_data = additional_data["sequences"]
                            # assert False
                            # print(additional_data[0]["protein"]["sequence"])
                            # assert False

                            additional_data = {data["protein"]["id"]: data["protein"]["sequence"] for data in additional_data}
                            # print(additional_data)
                    except (json.JSONDecodeError, IOError) as e:
                        print(f"Error reading file {json_path}: {e}")
                    except TypeError as e:
                        print(f"Unexpected error reading file {json_path}")

            if summary_values is not None:
                result[subfolder] = (*summary_values, additional_data)

    return result

# Example usage
base_path = "af_output/"
print(json.dumps(read_high_confidences(base_path), indent=4))
