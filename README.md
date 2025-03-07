# protein tools

## Display all the chains of a pdb file and visualizing the 3D structure

[visualize.ipynb](./visualize.ipynb)

## Downloading pdb files

The pdb files can be downloaded from https://www.rcsb.org/. Type in the search box for its short name. For example, type in `5GRD` and we can find  https://www.rcsb.org/structure/5GRD. Type in `7RE7` and we can find https://www.rcsb.org/structure/7RE7.

After downloading the pdb files, you can see the chains and the 3D structure with [visualize.ipynb](./visualize.ipynb) by changing the variable `pdb_filename`. 

## Removing some chains of pdb files

In [extract_chains_pdb.py](./extract_chains_pdb.py), if you uncomment 
```
extract_chains("7re7.pdb", "7re7_HL.pdb", ["H", "L"])
```
then the output file `7re7_HL.pdb` contains only the `H`, `L` chains of `7re7.pdb`.

Example run:

We need to extract the `A`, `C` chains of 5GRD, and the `H`, `L` chains of `7re7.pdb`. That is, 
```
extract_chains("5grd.pdb", "C.pdb", ["A", "C"])
extract_chains("7re7.pdb", "H.pdb", ["H", "L"])
```

Explanation: `H`, `L` are antibodies. `C` is antigen. `A`, `B` are places that `C` sits in. We need to use `7re7.pdb` as a template to generate new `H`, `L` chains that binds to the `C` chain of `5grd.pdb`. After removing `B`, we only simulate against `A`, `C`. This gives a higher chance of the resulting `H`, `L` being close to `C`. 

## Generate candidate antibodies using DiffAb

DiffAb library: https://github.com/luost26/diffab

Need to copy `/data4/yizheng/createpl` and `/data4/yizheng/hdock` to `./bin` and make these two files executable.

To run: save the resulting `C.pdb` and `H.pdb` to `./pdb`. Then run

```
python design_dock.py \
    --antigen pdb/C.pdb \
    --antibody pdb/H.pdb \
    --config ./configs/test/codesign_multicdrs.yml \
    -n 100 \
    -o ./results/5grd
```
The generated pdb files are in `./results/5grd`.

## Filter the candidates by choosing only the ones whose H or L is close to C

Run [interface_residues.py](./interface_residues.py). On the screen prints the paths to pdbs whose H or L is close to C

## Convert the candidates from pdb to fasta

Run [extract_chains_seq.py](./extract_chains_seq.py) where `input_base` is the directory containing all the pdbs from the last step. `output_base` contains the resulting fasta files

## Alphafold3

Alphafold3 library: https://github.com/google-deepmind/alphafold3

Steps:

1.  Convert the fasta files from the last step to the ones readable by Alphafold3. 
[convert_to_alphafold_input.py](./convert_to_alphafold_input.py), where `input_base` is the directory containing all the fasta files from the last step. 

2. Copy the output folder by step 1 to `~/af_input`

3. Run alphafold. (Need contents of `/data4/yizheng/alphafold/` and `/data4/yizheng/public_databases/`)
```
docker run -it     --volume $HOME/af_input:/root/af_input     --volume $HOME/af_output:/root/af_output     --volume /data4/yizheng/alphafold:/root/models     --volume /data4/yizheng/public_databases:/root/public_databases     --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=3,4,5,6     alphafold3     python run_alphafold.py     --input_dir=/root/af_input     --model_dir=/root/models     --output_dir=/root/af_output
```

4. Copy [read_confidences.py](./read_confidences.py) to `~/` and run 
```
cd
python read_confidences.py
```

5. The output in the terminal is in json format. It consists of chains whose ipTM score is >= 0.8, either (C, L) or (C, H). The ones already run are [5grd](./selected_chains/5grd.json) and [6nca](./selected_chains/6nca.json). For example, for the first entry in [5grd](./selected_chains/5grd.json):
- The (C,H) ipTM score is 0.78
- The (C,L) ipTM score is 0.68
- the results are in `~/af_output/20241106_merged3_seq_af_input__2__d_ab_0067_20250205_165643`. In that folder, look for the `.cif` file. That file is the 3D shape of the protein complex. Download the file.

6. On the local computer, install Obabel from https://openbabel.org/docs/Command-line_tools/babel.html. Convert the downloaded `.cif` file from Step 5 to `.pdb` using `obabel your_file.cif -O your_file.pdb`

7. You can visualize this pdb file using [visualize.ipynb](./visualize.ipynb) by changing the variable `pdb_filename`. 

## Already have results
5grd at [5grd.json](./selected_chains/5grd.json) and [alphafold_interactions_5grd](./alphafold_interactions_5grd.xlsx). 6nca at [6nca.json](./selected_chains/6nca.json) and [alphafold_interactions_6nca.xlsx](./alphafold_interactions_6nca.xlsx).
