import sys, os, re
from Bio import SeqIO


def remove_entry(vals):
    records = list(SeqIO.parse(vals[1], 'fasta'))
    updated_records = filter(lambda x: x.id != str(vals[2]), records)
    return updated_records


def write_out(updated_records, vals):
    out_file_name = "%s_without_%s.fas" % (vals[1].split('.')[0], vals[2])
    out_file = open(out_file_name, "w")
    for rec in updated_records:
        out_file.write('>%s\n%s\n' % (rec.id, rec.seq))


def main():
    print "	Please give me both fasta filename and the name of the entry to remove"
    print " e.g. python remove_fasta_entry.py crystals.fa 3qqi"
    if len(sys.argv) != 3:
        print "Please check the parameters"
    else:
        updated_records = remove_entry(sys.argv)
        write_out(updated_records, sys.argv)


main()
