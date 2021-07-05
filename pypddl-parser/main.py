# This file is part of pypddl-PDDLParser.

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


import argparse
from pddlparser import PDDLParser
import networkx as nx



class Stato:
    def __init__(self,tipo, set) -> None:
        self._type = tipo
        self._set = set
        self._value = 0
    
    @property
    def type(self):
        return self._type
    @property
    def set(self):
        return self._set
    @property
    def value(self):
        return self._value
    
    def __str__(self):
        str = f"Tipo:\t\t{self._type}\n"
        str += f"Set:\t\t{self._set}"
        return str

def parse():
    usage = 'python3 main.py <DOMAIN> <INSTANCE>'
    description = 'pypddl-parser is a PDDL parser built on top of ply.'
    parser = argparse.ArgumentParser(usage=usage, description=description)

    parser.add_argument('domain',  type=str, help='path to PDDL domain file')
    parser.add_argument('problem', type=str, help='path to PDDL problem file')

    return parser.parse_args()

def execute_actions(state, actions):
    for a in actions:
        check = 0
        for prec in a.preconditions:
            p = str(prec)
            if not p in state:
                check = 1
        if check == 0:
            '''all conditions verified'''
            print("verified")
        else:
            print("not verified")
            check=0

if __name__ == '__main__':
    args = parse()

    domain  = PDDLParser.parse(args.domain)         # Vedi classe Domain
    problem = PDDLParser.parse(args.problem)        # Vedi classe Problem  
    
    print(domain)
    print(problem)
    # # execute_actions(problem.init, domain.operators)
    # print(problem.init)
    # for o in domain.operators:
    #     print(o)