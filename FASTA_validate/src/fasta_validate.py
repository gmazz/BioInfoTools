from Bio import SeqIO
import os, sys
import itertools


def define_parameters():
    os.chdir('../data')
    root = os.getcwd()
    test_file = root + '/wrong_1.fas'
    #test_file = root + '/ok.fas'
    os.chdir('../src')
    parameters = {
            'parameters' : '',
            'file' : test_file,
            'error_message' : ''
            }
    return parameters


def list_validate(parameters): # Returns the file content as list with alternated header and sequences.
    str_check = ''
    list_check = []
    handle = open(parameters['file'], 'r+')
    for line in handle.readlines():
        line = line.rstrip('\n')
        if line.startswith('>'):
            if str_check:
                list_check.append(str_check)
            list_check.append(line)
            str_check = ''
        else:
            str_check += line
    return list_check


def validate_step_1(parameters):
    list_check = list_validate(parameters)
    headers = list_check[0::2] # Take the positions where the FASTA headers should be located
    header_check = all([h.startswith('>') for h in headers])
    return header_check, list_check


def validate_step_2(list_check):
    valid_symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '*', '-']
    symbol_check = all(list(itertools.chain(*[[aa in valid_symbols for aa in seq] for seq in list_check[1::2]])))
    return symbol_check


def validate(parameters):
    try:
        header_check, list_check = validate_step_1(parameters)
        if header_check == False:
            parameters['error_message'] = 'The given file is not properly formatted (missing protein ID)'
            return False, parameters

        symbol_check = validate_step_2(list_check)
        if symbol_check == False:
            parameters['error_message'] = 'One or more sequences contain invalid FASTA symbols'
            return False, parameters

        parameters['parameters'] = list(SeqIO.parse(parameters['file'], "fasta"))
        return True, parameters

    except Exception:
        parameters['error_message'] = 'The give file cannot be opened!'
        return False, parameters


parameters = define_parameters()
valid, params_out = validate(parameters)
print valid, params_out