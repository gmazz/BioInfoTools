
def btw_comp(str_a, str_b):
    return reduce((lambda x, y: x | y), [ord(x)^ord(y) for x,y in zip(str_a, str_b)]) == 0
    

if __name__ == '__main__':
    str_1 = 'e00000000000000000011144444440000000000559559'
    str_2 = 'e00000000000000000011144444440000000000559558' 
    str_3 = 'e00000000000000000011144444440000000000559559'
    
    str_a = str_1
    str_b = str_3

    print "%s is equal to %s : %s " %(str_a, str_b, btw_comp(str_a, str_b))
