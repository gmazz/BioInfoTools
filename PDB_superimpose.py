import Bio.PDB
import os, sys, re


def chainIter(model, atoms_selection):
    atoms_id = []
    for chain in model:
        for res in chain:
            if res.get_id()[1] in atoms_selection:
                atoms_id.append(res.get_id()[1])
    return atoms_id

def atomAPP(model, new_atoms_selection):
    atoms = []
    for chain in model:
        for res in chain:
            if res.get_id()[1] in new_atoms_selection:
                atoms.append(res['CA'])
    return atoms

def atomSel(ref_model, sample_model, atoms_selection):

    ref_atoms_id = chainIter(ref_model, atoms_selection)
    sample_atoms_id = chainIter(sample_model, atoms_selection)

    # Takes the number of common residues
    common = min(len(ref_atoms_id), len(sample_atoms_id))
    ref_atoms_selection = ref_atoms_id[0:common]
    sample_atoms_selection = sample_atoms_id[0:common]

    ref_atoms = atomAPP(ref_model, ref_atoms_selection)
    sample_atoms = atomAPP(sample_model, sample_atoms_selection)

    return ref_atoms, sample_atoms

def singleIter(ref_file, sample_file):
    ref_ID = ref_file.split('.pdb')[0]
    sample_ID = sample_file.split('.pdb')[0]
    output_name = "%s_superimposed.pdb" % sample_ID

    # Start the parser
    pdb_parser = Bio.PDB.PDBParser(QUIET = True)

    ref_structure = pdb_parser.get_structure(ref_ID, ref_file)
    sample_structure = pdb_parser.get_structure(sample_ID, sample_file)

    if len(ref_structure) > 1:
	    print "Your PDB reference contains multiple structures. The 1st will be considered"
    if len(sample_structure) > 1:
	    print "Your PDB model contains multiple structures. The 1st will be considered"

    #Take 1st PDB in case the files contains more than 1
    ref_model = ref_structure[0]
    sample_model = sample_structure[0]

    # Atoms selection
    start_id = 1
    end_id = 300
    atoms_selection = range(start_id, end_id + 1)
    ref_atoms, sample_atoms = atomSel(ref_model, sample_model, atoms_selection)

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


def main(ref_file):
    rootdir = os.getcwd()
    pdb_list = [f for f in os.listdir(rootdir) if f.endswith('.pdb')]
    for sample_file in pdb_list:
        singleIter(ref_file, sample_file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "\n Please use template.ID as an argument. e.g.: $PDB_superimpose.py 4EDA.pdb\n"
    ref_file = sys.argv[1]
    main(ref_file)