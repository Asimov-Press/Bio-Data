## Cell Size Dataset

This script takes the raw Bionumbers dataset and pulls out two sets of size information:
- Size of things within a cell, in this case with a focus on E. coli.
- Size of different cells themselves across different organisms.

The main [script](./gen_cell_sizes.py) is used to generate the data for our first data brief.

### Data sample

Note that in this case, we found that there really wasn't that much size related data for a meaningful plot, so this is temporary punted unless we revisit and clean the data a bit more.

```
+---------------+------------------------------------------+-----------+------+-------+------------+
| Property Type | Property Of                              | Value     | Min  | Max   | Units      |
+---------------+------------------------------------------+-----------+------+-------+------------+
| Diameter      | each fliC monomer                        | 5.0       |      |       | nm         |
| Diameter      | pili                                     | 7.0       |      |       | nm         |
| Diameter      | 70S (intact) ribosome                    | 26.0      |      |       | nm         |
| Diameter      | cell                                     | 0.79      |      |       | µm         |
| Diameter      | cell                                     | 1.0       |      |       | µm         |
| Diameter      | condensed chromosome                     | 17.0      |      |       | µm         |
| Diameter      | relaxed circular chromosome              | 490.0     |      |       | µm         |
| Diameter      | fimbriae of E. coli and Salmonella       |           | 2.0  | 8.0   | nm         |
| Diameter      | cell                                     |           | 1.0  | 1.1   | µm         |
| Diameter      | flagella                                 |           |      |       | nm         |
| Diameter      | diffusion channel formed by OmpA [outer  |           |      |       | Å          |
| Diameter      | ribosome                                 | 30.0      |      |       | nm         |
| Diameter      | water molecule                           | 2.8       |      |       | Å          |
| Diameter      | DNA double helix                         | 20.4      |      |       | Å          |
| Diameter      | caveola                                  |           | 50.0 | 100.0 | nm         |
| Diameter      | fibrin microthread                       |           | 50.0 | 100.0 | µm         |
| Diameter      | fabricated tip in electrochemical etchin |           |      |       | nm         |
| Radius        | cell                                     | 380.0     |      |       | nm         |
| Radius        | Glycerol conducting channel              | 3.5       |      |       | Angstrom   |
| Radius        | objects identified as fragments of the b |           |      |       | nm         |
| Radius        | insulin growth factor-i stokes-einstein  | 1.54      |      |       | nm         |
| Radius        | curvature at centerline of DNA in nucleo | 4.5       |      |       | nm         |
| Radius        | curvature below which pure actin breaks  | 180.0     |      |       | nm         |
| Radius        | the crystal size of sodium ion           | 0.9       |      |       | Angstrom   |
| Radius        | Potassium ion                            | 1.33      |      |       | Angstrom   |
| Radius        | the crystal size of potassium ion        | 1.33      |      |       | Angstrom   |
| Radius        | ATP molecule                             |           |      |       | nm         |
| Size          | 70s (intact) of ribosome                 | 21.0      |      |       | nm         |
| Size          | phenylalanine pool                       | 0.2       |      |       | µmol/g     |
| Size          | methionine pool                          | 0.29      |      |       | µmol/g     |
| Size          | imp pool                                 | 0.38      |      |       | µmol/g     |
| Size          | tyrosine pool                            | 0.41      |      |       | µmol/g     |
| Size          | carbamoyl aspartate pool                 | 0.84      |      |       | µmol/g     |
| Size          | proline pool                             | 1.1       |      |       | µmol/g     |
| Size          | threonine pool                           | 1.34      |      |       | µmol/g     |
| Size          | asparagine pool                          | 2.02      |      |       | µmol/g     |
| Size          | valine pool                              | 2.41      |      |       | µmol/g     |
| Size          | glutamine pool                           | 3.92      |      |       | µmol/g     |
| Size          | aspartate pool                           | 6.45      |      |       | µmol/g     |
| Size          | alanine pool                             | 6.81      |      |       | µmol/g     |
| Size          | glutamate pool                           | 100.55    |      |       | µmol/g     |
| Size          | lacz gene                                | 3075.0    |      |       | base pairs |
| Size          | genome                                   | 4600000.0 |      |       | Base pairs |
| Size          | the LacY transporter                     |           |      |       | nanometer  |
| Size          | cell after recovery from hyperosmotic sh |           |      |       | µm         |
| Size          | glucose molecule (open chain form)       | 1.5       |      |       | nm         |
| Size          | globular protein diameter - characterist | 5.0       |      |       | nm         |
| Size          | paraspeckle                              | 0.5       |      |       | µm         |
| Size          | typical tether in Tethered Particle Moti | 1000.0    |      |       | bp         |
| Size          | clastosomes                              |           | 0.1  | 2.0   | µm         |
| Size          | typical polystrene bead in Tethered Part |           | 0.2  | 1.0   | Î¼m        |
| Size          | perinuclear compartments                 |           | 0.3  | 1.0   | µm         |
| Size          | aggregosome                              |           | 2.0  | 10.0  | µm         |
| Size          | amino acid molecule estimated based on b |           |      |       | Å          |
| Size          | glucose ring molecule                    |           |      |       | Å          |
| Size          | GFP                                      |           |      |       | nm         |
| Size          | RuBisCO (shaped like a rounded cube)     |           |      |       | nm         |
| Size          | initially multilamellar spherical vesicl |           |      |       | nan        |
+---------------+------------------------------------------+-----------+------+-------+------------+
```

### Steps

- Filter for keywords related to size.
- Use an exclusion list to remove any false positives.
- Clean the data / units:
    - Pull out the primary value, or the range if available.
    - Convert to a standard unit.
- Save the cleaned data to a CSV file within the `output/` folder.

### Output

The output is a timestamped CSV file within the `output/` folder.
