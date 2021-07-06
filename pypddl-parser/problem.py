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

import itertools


class Problem(object):

    def __init__(self, name, domain, prob_body, goal):
        self._name = name
        self._domain = domain

        self._requirements = None
        self._objects = {}
        self._init = None

        for d in prob_body:
            k = next(iter(d))
            if k == "requirements":
                self._requirements = d[k]
            elif k == "objects":
                for obj in d[k]:
                    self._objects[obj.type] = self._objects.get(obj.type, [])
                    self._objects[obj.type].append(str(obj.value))
            elif k == "init":
                self._init = set(d[k])
        self._goal = set(goal)

    @property
    def name(self):
        return self._name

    @property
    def domain(self):
        return self._domain
    
    @property
    def requirements(self):
        return self._requirements

    @property
    def objects(self):
        return self._objects.copy()

    @property
    def init(self):
        return self._init.copy()

    @property
    def goal(self):
        return self._goal.copy()

    def __str__(self):
        problem_str  = '@ Problem: {0}\n'.format(self._name)
        problem_str += '>> domain: {0}\n'.format(self._domain)
        problem_str += '>> requirements: {0}\n'.format(', '.join(self._requirements)) if self._requirements else ""
        if self._objects:
            problem_str += '>> objects:\n'
            for type, objects in self._objects.items():
                problem_str += '{0} -> {1}\n'.format(type, ', '.join(sorted(objects)))
        problem_str += '>> init:\n{0}\n'.format(', '.join(sorted(self._init))) if self._init else ""
        problem_str += '>> goal:\n{0}\n'.format(', '.join(sorted(self._goal)))
        return problem_str
