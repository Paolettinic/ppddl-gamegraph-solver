
from parser.term import Term


class Predicate(object):

    def __init__(self, name, args=[]):
        self._name = name
        self._args = args

    @property
    def name(self):
        return self._name

    @property
    def args(self):
        return self._args[:]

    @property
    def arity(self):
        return len(self._args)

    def __eq__(self, other):
        return self.name == other.name and self.args == other.args

        

    def __hash__(self):
        return hash(
            (
                self.name,
                str(list(map(str,self.args)))
            )
        )


    def __str__(self):
        if self._name == '=':
            return '{0} = {1}'.format(str(self._args[0]), str(self._args[1]))
        elif self.arity == 0:
            return self._name
        else:
            return '{0}({1})'.format(self._name, ', '.join(map(str, self._args)))
