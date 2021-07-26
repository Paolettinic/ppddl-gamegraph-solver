# This file is part of pypddl-parser.

# pypddl-parser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pypddl-parser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pypddl-parser.  If not, see <http://www.gnu.org/licenses/>.


class Action(object):

    def __init__(self, name, params, precond, effects):
        self._name    = name
        self._params  = params
        self._precond = precond
        self._effects = self.compute_probability(effects)


    def compute_probability(self, effects):
        print(effects)
        final = []
        for e in effects:
            if isinstance(e,tuple):
                p, effect = e
                if not isinstance(effect, list):
                    final.append(e)   
                else:
                    final += [(p*sub_p, sub_e) for sub_p, sub_e in self.compute_probability(effect)]
            elif isinstance(e,list):
                for p, effect in e:
                    final += [(p*sub_p, sub_e) for sub_p, sub_e in self.compute_probability(effect)]
        return final   


    @property
    def name(self):
        return self._name

    @property
    def params(self):
        return self._params[:]

    @property
    def preconditions(self):
        return self._precond[:]

    @property
    def effects(self):
        return self._effects[:]
    #TODO: separare effetti probabilistici da effetti non probabilistici

    @property
    def is_probabilistic(self):
        for e in self.effects:
            if e[0] < 1.0:
                return True
        return False

    def __str__(self):
        operator_str  = '{0}({1})\n'.format(self._name, ', '.join(map(str, self._params)))
        operator_str += '>> precond: {0}\n'.format(', '.join(map(str, self._precond)))
        operator_str += '>> effects: {0}\n'.format(', '.join(map(str, self._effects)))
        return operator_str
