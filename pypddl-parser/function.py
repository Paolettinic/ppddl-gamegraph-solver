class Function:
    def __init__(self, name, parameter = None, type = None) -> None:
        self._name = name
        self._paramenter = None
        self._type = None

        if parameter:
            self._paramenter = parameter
        if type:
            self._type = type

    @property
    def name(self):
        return self._name
    @property
    def parameter(self):
        return self._paramenter
    @property
    def type(self):
        return self._type

    def __str__(self) -> str:
        function_str = f"\n{self._name}\n"
        if self._paramenter:
            function_str += f"\t>>> parameter: {self._paramenter}\n"
        if self._type:
            function_str += f"\t>>> type: {self._type}\n"

        return function_str