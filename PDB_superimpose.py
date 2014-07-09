import Bio.PDB
import os, sys, re


def chainIter(model, atoms_selection):
    atoms = []
    for chain in model:
        for res in chain:
            if res.get_id()[1] in atoms_selection:
                atoms.append(res['CA'])
    return atoms


def SingleIter (ref_ID, sample_file):

    ref_file = "%s.pdb" % ref_ID
    sample_ID = sample_file.split('.pdb')[0]
    output_name = "%s_superimposed.pdb" % sample_ID

    #Atoms selection
    start_id = 1
    end_id   = 235
    atoms_selection = range(start_id, end_id + 1)

    # Start the parser
    pdb_parser = Bio.PDB.PDBParser(QUIET = True)

    ref_structure = pdb_parser.get_structure(ref_ID, ref_file)
    sample_structure = pdb_parser.get_structure(sample_ID, sample_file)

    if len(ref_structure) > 1:
	    print "Your PDB reference contains multiple structures. The 1st will be considered"
    if len(sample_structure) > 1:
	    print "Your PDB model contains multiple structures. The 1st will be considered"

    #Take 1st PDB in case the files contains more than 1
    ref_model    = ref_structure[0]
    sample_model = sample_structure[0]

    ref_atoms = chainIter(ref_model, atoms_selection)
    sample_atoms = chainIter(sample_model, atoms_selection)

    # For Superposition the lenght of the selected lists of atoms shuold be equal
    if len(ref_atoms) != len(sample_atoms):
	    print "Attention: the number of selected atoms in %s and %s are unequal. Superposition can't be performed" %(ref_ID, sample_ID)

    # Initiate the superimposer:
    super_imposer = Bio.PDB.Superimposer()
    super_imposer.set_atoms(ref_atoms, sample_atoms)
    super_imposer.apply(sample_model.get_atoms())

    # Print RMSD:
    print super_imposer.rms

    # Save the aligned version of 1UBQ.pdb
    io = Bio.PDB.PDBIO()
    io.set_structure(sample_structure)
    io.save(output_name)

def main():
    rootdir = os.getcwd()
    pdb_list = [f for f in os.listdir(rootdir) if f.endswith('.pdb')]
    ref_ID = "4EDA"
    for sample_file in pdb_list:
        SingleIter(ref_ID, sample_file)

main()
