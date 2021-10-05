class Action(object):

    def __init__(self, name, params, precond, effects):
        self._name    = name
        self._params  = params
        self._precond = precond
        self._effects = self.compute_probability(self.ground_probability(effects))


    def compute_probability(self, effects):
        # print(effects)
        final = []
        if len(effects) == 1:
            return effects
        for probability, effect in effects:
            final += [(probability * sub_p, sub_e) for sub_p, sub_e in self.compute_probability(effect)]
        return final  

    def ground_probability(self, effects):
        det_list = []
        prob_list = []
        prob_count = 0
        for p,e in effects:
            if p<1:
                prob_list.append((p,e))
                prob_count += p
            else:
                det_list.append((p,e))

         
        if not len(prob_list) == 0:

            if prob_count < 1:
                prob_list.append((1-prob_count, []))

            new_prob_list = []
            for p,e in prob_list:
                for d in det_list:
                    e.append(d)
                new_prob_list.append((p,self.ground_probability(e)))
            # print(prob_list)
            return new_prob_list
        else:
            return [(1.0 ,[eff for _,eff in det_list])]
    
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
