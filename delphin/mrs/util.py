class AccumulationDict(dict):
    def __init__(self, accumulator, *args, **kwargs):
        if not hasattr(accumulator, '__call__'):
            raise TypeError('Accumulator must be a binary function.')
        self.accumulator = accumulator
        self.accumulate(*args, **kwargs)

    def __additem__(self, key, value):
        if key in self:
            self[key] = self.accumulator(self[key], value)
        else:
            self[key] = value

    def __add__(self, other):
        result = AccumulationDict(self.accumulator, self)
        result.accumulate(other)
        return result

    def accumulate(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, list):
                for (key, value) in arg:
                    self.__additem__(key, value)
            elif isinstance(arg, dict):
                for (key, value) in arg.items():
                    self.__additem__(key, value)
            else:
                raise TypeError('Argument must be of type list or dict.')
        for key in kwargs:
            self.__additem__(key, kwargs[key])

def dict_of_dicts(triples, dicttype=dict):
    d = dicttype()
    for a, b, c in triples:
        try:
            d[a][b] = c
        except KeyError:
            d[a] = dicttype()
            d[a][b] = c
    return d
