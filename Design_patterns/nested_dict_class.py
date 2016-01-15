class NestedDict(dict):
    def __getitem__(self, item):
	print item
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

a = NestedDict()
#a = dict()
a['michal']['pon']['godz_1'] = 'sleep'
a['giovanni']['niedziela']['godz_1'] = 'uspi matylda'
print a
