

class Term(object):

    def __init__(self, **kwargs):
        self._name  = kwargs.get('name',  None)
        self._type  = kwargs.get('type',  None)
        self._value = kwargs.get('value', None)

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    def is_variable(self):
        return self._name is not None

    def is_typed(self):
        return self._type is not None

    def is_constant(self):
        return self._value is not None

    @classmethod
    def variable(cls, name, type=None):
        return Term(name=name, type=type)

    @classmethod
    def constant(cls, val, type=None):
        return Term(value=val, type=type)

    def __str__(self):
        if self.is_variable() and self.is_typed():
            return '{0} - {1}'.format(self._name, self._type)
        if self.is_variable():
            return '{0}'.format(self._name)
        if self.is_constant() and self.is_typed():
            return '{0} - {1}'.format(self._value, self._type)
        if self.is_constant():
            return '{0}'.format(self._value)

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type and self.value == other.value
    def __hash__(self):
        return hash((self.name,self.type,self.value))