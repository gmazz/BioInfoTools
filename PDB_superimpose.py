import Bio.PDB
import os, sys, re


def chainIter(model, atoms_selection):
    atoms = []
    for chain in model:
        for res in chain:
            if res.get_id()[1] in atoms_selection:  # # PROBABLE MAJOR BUG in HERE
                print "res.get_%s:%s" % (model.get_full_id(), res.get_id()[1])
                atoms.append(res['CA'])
    return atoms


def atomSel(ref_model, sample_model, atoms_selection):
    ref_atoms = chainIter(ref_model, atoms_selection)
    sample_atoms = chainIter(sample_model, atoms_selection)
    print len(ref_atoms), len(sample_atoms)  # Error here they are never equal they should be.
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

    # For Superposition the length of the selected lists of atoms should be equal. This is fixed automatically taking the smaller number of atoms
    while len(ref_atoms) != len(sample_atoms):
        print "\nAttention: the number of selected atoms in %s and %s are unequal!\n" % (ref_ID, sample_ID)
        # print " %s:%s\t%s:%s" %(ref_ID, len(ref_atoms), sample_ID, len(sample_atoms)
        upbound = min(len(ref_atoms), len(sample_atoms))
        #print "\nThe superposition will be performed on the minimal number of common residues: %s\n" % upbound
        atoms_selection = range(1, upbound + 1)
        ref_atoms, sample_atoms = atomSel(ref_model, sample_model, atoms_selection)
        #print "\n\nref_atoms:%s sample_atoms:%s\n\n" % (len(ref_atoms), len(sample_atoms))

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