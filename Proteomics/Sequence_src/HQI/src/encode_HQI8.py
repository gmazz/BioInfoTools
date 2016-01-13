#_author: Julian Zubek

import numpy as np
import aaindex

aaindex.init(path='.', index='1')
HQI8_descriptors = ["BLAM930101", "BIOV880101", "MAXF760101", "TSAJ990101",
                    "NAKH920108", "CEDJ970104", "LIFS790101", "MIYS990104"]


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
