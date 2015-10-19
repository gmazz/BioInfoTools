#_author: Julian Zubek

import numpy as np
import aaindex

aaindex.init(path='.', index='1')
HQI8_descriptors_v1 = ["BLAM930101", # Alpha helix propensity
                    "BIOV880101", # Accessibility
                    "MAXF760101", # Normalized frequency of alpha-helix (Maxfield-Scheraga, 1976)
                    "TSAJ990101", # Volumes including the crystallographic waters using the ProtOr (Tsai et al., 1999)
                    "NAKH920108", # AA composition of MEM of multi-spanning proteins (Nakashima-Nishikawa, 1992)
                    "CEDJ970104", # Composition of amino acids in intracellular proteins (percent) (Cedano et al., 1997)
                    "LIFS790101", # Conformational preference for all beta-strands (Lifson-Sander, 1979)
                    "MIYS990104"
                   ] 

HQI8_descriptors_v2 = [#"BULH740102", # Apparent partial specific volume (Bull-Breese, 1974)
                      "CHAM820101", # Polarizability parameter (Charton-Charton, 1982)
                      "GOLD730101", # Hydrophobicity factor (Goldsack-Chalifoux, 1973)
                      "LEVM760106", # Van der Waals parameter R0 (Levitt, 1976)
                      "CHOC750101",  # Average volume of buried residue (Chothia, 1975)
                      "FAUJ880103", # Normalized van der Waals volume (Fauchere et al., 1988)
                      #"TSAJ990101", # Volumes including the crystallographic waters using the ProtOr (Tsai et al., 1999)
                   ]

HQI8_descriptors = ["BHAR880101", # Average flexibility indices (Bhaskaran-Ponnuswamy, 1988)
                    "CIDH920105", # Normalized average hydrophobicity scales (Cid et al., 1992)
                    "CHAM820101", # Polarizability parameter (Charton-Charton, 1982)
                    "FAUJ880103", # Normalized van der Waals volume (Fauchere et al., 1988)
                    #"LEVM760106", # Van der Waals parameter R0 (Levitt, 1976)
                    #"GOLD730101", # Hydrophobicity factor (Goldsack-Chalifoux, 1973)
                    #"CHOC750101",  # Average volume of buried residue (Chothia, 1975)
                    #"TSAJ990101", # Volumes including the crystallographic waters using the ProtOr (Tsai et al., 1999)
                   ]

def get_aaindex_feature(amino_acid, aai_record, seq):
    # B and Z are ambiguous amino acids.
    if amino_acid == "B":
        val = (aai_record.get("D") + aai_record.get("N")) / 2
    elif amino_acid == "Z":
        val = (aai_record.get("E") + aai_record.get("Q")) / 2
    elif amino_acid == "O":
        val = aai_record.get("K")
    elif amino_acid == "U":
        val = aai_record.get("C")
    elif amino_acid in "X*-":
        val = 0.0
    else:
        val = aai_record.get(amino_acid)
    # Checking for "None" type in case of an unspecified amino acid character.
    if not isinstance(val, float):
        print("""Unrecognised amino acid symbol {0} found in sequence {1}
                 for descriptor {2}""".format(amino_acid, seq, aai_record))
        exit(-1)
    return val


def encode_aaindex_features(sequences):
    aaindex.init(path='.', index='1')
    aai_recs = [aaindex.get(d) for d in HQI8_descriptors]
    return np.array([[get_aaindex_feature(aa, r, seq) for aa in seq
                      for r in aai_recs] for seq in sequences], dtype=np.float_)
