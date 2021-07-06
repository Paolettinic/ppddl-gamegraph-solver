class Function:
    def __init__(self, name, parameter = None, predicate = None) -> None:
        self._name = name
        self._paramenter = None
        self._predicate = None

        if parameter:
            self._paramenter = parameter
        if predicate:
            self._predicate = predicate

    @property
    def name(self):
        return self._name
    @property
    def parameter(self):
        return self._paramenter
    @property
    def predicate(self):
        return self._predicate

    def __str__(self) -> str:
        function_str = f"\n{self._name}\n"
        if self._paramenter:
            function_str += f"\t>>> parameter: {self._paramenter}\n"
        if self._predicate:
            function_str += f"\t>>> predicate: {self._predicate}\n"

        return function_str