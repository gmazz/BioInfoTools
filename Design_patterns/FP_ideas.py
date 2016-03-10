
def map_filter_reduce(l):

    ## MAP
    l1 = map(lambda x: x + 1, l)

    ## FILTER
    l_even = filter(lambda x: x % 2 == 0, l)

    ## REDUCE
    l_sum = reduce(lambda accum, x: accum + x, l, 0)

    print l
    print l1
    print l_even
    print l_sum


def use_partial(l):

    import operator
    from functools import partial

    # Generates function that add 10 a given element
    add_10 = partial(operator.add, 10)

    # Let use add_10 on the list l
    print map(lambda x: add_10(x), l)


def iterator(l):
    return iter(l)

if __name__ == '__main__':
    l = [1,2,3,4,5,6,7,8,9,10]
    #map_filter_reduce(l)
    #use_partial(l)
    myi = iterator(l)

