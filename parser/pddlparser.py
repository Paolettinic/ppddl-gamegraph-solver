
from ply import lex
from ply import yacc

from parser.term import Term
from parser.literal import Literal
from parser.predicate import Predicate
from parser.action import Action
from parser.domain import Domain
from parser.problem import Problem
from parser.function import Function

tokens = (
    'NAME',
    'VARIABLE',
    'PROBABILITY',
    'NUMBER',
    'BINARYCOMP',
    'BINARYOP',
    'LPAREN',
    'RPAREN',
    'HYPHEN',
    'EQUALS',
    'NEGATIVE_PRECONDITIONS_KEY',
    'DISJUNCTIVE_PRECONDITIONS_KEY',
    'EXISTENTIAL_PRECONDITIONS_KEY',
    'UNIVERSAL_PRECONDITIONS_KEY',
    'QUANTIFIED_PRECONDITIONS_KEY',
    'CONDITIONAL_EFFECT_KEY',
    'PROBABILISTIC_EFFECTS_KEY',
    'REWARDS_KEY',
    'ADL_KEY',
    'MDP_KEY',
    'DEFINE_KEY',
    'DOMAIN_KEY',
    'REQUIREMENTS_KEY',
    'STRIPS_KEY',
    'EQUALITY_KEY',
    'TYPING_KEY',
    'TYPES_KEY',
    'CONSTANTS_KEY',
    'PREDICATES_KEY',
    'EITHER_KEY',
    'ACTION_KEY',
    'PARAMETERS_KEY',
    'PRECONDITION_KEY',
    'EFFECT_KEY',
    'AND_KEY',
    'NOT_KEY',
    'ASSIGN_KEY',
    'SCALE_UP_KEY',
    'SCALE_DOWN_KEY',
    'INCREASE_KEY',
    'REWARD_KEY',
    'MINIMIZE_KEY',
    'MAXIMIZE_KEY',
    'EXISTENTIAL_KEY',
    'FORALL_KEY',
    'WHEN_KEY',
    'PROBABILISTIC_KEY',
    'TOTALTIME_KEY',
    'GOALACHIEVED_KEY',
    'FUNCTIONS_KEY',
    'PROBLEM_KEY',
    'OBJECTS_KEY',
    'METRIC_KEY',
    'INIT_KEY',
    'GOAL_KEY'
)

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_HYPHEN = r'\-'
t_EQUALS = r'='

t_ignore = ' \t'

reserved = {
    'define'                     : 'DEFINE_KEY',
    'domain'                     : 'DOMAIN_KEY',
    ':requirements'              : 'REQUIREMENTS_KEY',
    ':strips'                    : 'STRIPS_KEY',
    ':equality'                  : 'EQUALITY_KEY',
    ':negative-preconditions'    : 'NEGATIVE_PRECONDITIONS_KEY',
    ':disjunctive-preconditions' : 'DISJUNCTIVE_PRECONDITIONS_KEY',
    ':existential-preconditions' : 'EXISTENTIAL_PRECONDITIONS_KEY',
    ':universal-preconditions'   : 'UNIVERSAL_PRECONDITIONS_KEY',
    ':quantified-preconditions'  : 'QUANTIFIED_PRECONDITIONS_KEY',
    ':conditional-effects'       : 'CONDITIONAL_EFFECTS_KEY',
    ':probabilistic-effects'     : 'PROBABILISTIC_EFFECTS_KEY',
    ':rewards'                   : 'REWARDS_KEY',
    ':fluents'                   : 'FLUENTS_KEY',
    ':adl'                       : 'ADL_KEY',
    ':mdp'                       : 'MDP_KEY',
    ':typing'                    : 'TYPING_KEY',
    ':types'                     : 'TYPES_KEY',
    ':constants'                 : 'CONSTANTS_KEY',
    ':predicates'                : 'PREDICATES_KEY',
    ':action'                    : 'ACTION_KEY',
    ':parameters'                : 'PARAMETERS_KEY',
    ':precondition'              : 'PRECONDITION_KEY',
    ':effect'                    : 'EFFECT_KEY',
    'and'                        : 'AND_KEY',
    'not'                        : 'NOT_KEY',
    'either'                     : 'EITHER_KEY',
    'exists'                     : 'EXISTENTIAL_KEY',
    'forall'                     : 'FORALL_KEY',
    'when'                       : 'WHEN_KEY',
    'probabilistic'              : 'PROBABILISTIC_KEY',
    'problem'                    : 'PROBLEM_KEY',
    'assign'                     : 'ASSIGN_KEY',
    'scale-up'                   : 'SCALE_UP_KEY',
    'scale-down'                 : 'SCALE_DOWN_KEY',
    'increase'                   : 'INCREASE_KEY',
    'decrease'                   : 'DECREASE_KEY',
    'reward'                     : 'REWARD_KEY',
    'minimize'                   : 'MINIMIZE_KEY',
    'maximize'                   : 'MAXIMIZE_KEY',
    'total-time'                 : 'TOTALTIME_KEY',
    'goal-achieved'              : 'GOALACHIEVED_KEY',
    ':domain'                    : 'DOMAIN_KEY',
    ':objects'                   : 'OBJECTS_KEY',
    ':functions'                 : 'FUNCTIONS_KEY',
    ':metric'                    : 'METRIC_KEY',
    ':init'                      : 'INIT_KEY',
    ':goal'                      : 'GOAL_KEY'
}

def t_KEYWORD(t):
    r':?[a-zA-Z_][a-zA-Z_0-9\-]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9\-]*'
    return t


def t_VARIABLE(t):
    r'\?[a-zA-Z_][a-zA-Z_0-9\-]*'
    return t

def t_PROBABILITY(t):
    #r'[0-1]\.\d+'
    r'(0\.\d+|1\.0+)'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'-?\d+\.?\d+'
    t.value = float(t.value)
    return t

# def t_BINARYCOMP(t):
#     r'<=|>=|<|>|='
#     return t


def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)


def t_error(t):
    print("Error: illegal character '{0}'".format(t.value[0]))
    t.lexer.skip(1)


# build the lexer
lex.lex()


def p_pddl(p):
    '''pddl : domain
            | problem'''
    p[0] = p[1]


def p_domain(p):
    '''domain : LPAREN DEFINE_KEY domain_def opt_dom_parts RPAREN'''
    p[0] = Domain(p[3], p[4])


def p_problem(p):
    '''problem : LPAREN DEFINE_KEY problem_def domain_def opt_prob_parts goal_def RPAREN'''
    p[0] = Problem(p[3], p[4], p[5], p[6])


def p_domain_def(p):
    '''domain_def : LPAREN DOMAIN_KEY NAME RPAREN'''
    p[0] = p[3]


def p_problem_def(p):
    '''problem_def : LPAREN PROBLEM_KEY NAME RPAREN'''
    p[0] = p[3]

def p_opt_dom_parts(p):
    '''opt_dom_parts : opt_dom_part opt_dom_parts
                       | opt_dom_part'''
    if len(p) == 2:
        p[0] = [p[1]]
    if len(p) == 3:
        p[0] = [p[1]] + p[2] 

def p_opt_dom_part(p):
    '''opt_dom_part : require_def
                       | types_def
                       | constants_def
                       | predicates_def
                       | actions_def
                       | functions_def
                       | empty'''
    p[0] = p[1]

def p_opt_prob_parts(p):
    '''opt_prob_parts : opt_prob_parts opt_prob_part 
                       | opt_prob_part'''
    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 3:
        p[0] = [p[1]] + [p[2]] 

def p_opt_prob_part(p):
    '''opt_prob_part : require_def
                        | objects_def
                        | init_def
                        | empty'''
    p[0] = p[1]



def p_objects_def(p):
    '''objects_def : LPAREN OBJECTS_KEY typed_constants_lst RPAREN'''
    p[0] = {"objects":p[3]}


def p_init_def(p):
    '''init_def : LPAREN INIT_KEY LPAREN AND_KEY ground_predicates_lst RPAREN RPAREN
                | LPAREN INIT_KEY ground_predicates_lst RPAREN'''
    if len(p) == 5:
        p[0] = {"init":p[3]}
    elif len(p) == 8:
        p[0] = {"init":p[5]}


def p_goal_def(p):
    '''goal_def : LPAREN GOAL_KEY LPAREN AND_KEY ground_predicates_lst RPAREN RPAREN'''
    p[0] = p[5]


def p_require_def(p):
    '''require_def : LPAREN REQUIREMENTS_KEY require_key_lst RPAREN'''
    p[0] = {"requirements":p[3]}


def p_require_key_lst(p):
    '''require_key_lst : require_key require_key_lst
                       | require_key'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_require_key(p):
    '''require_key : STRIPS_KEY
                   | EQUALITY_KEY
                   | TYPING_KEY
                   | PROBABILISTIC_EFFECTS_KEY'''
    p[0] = str(p[1])


def p_types_def(p):
    '''types_def : LPAREN TYPES_KEY names_lst RPAREN'''
    p[0] = {"types":p[3]}

def p_constants_def(p):
    '''constants_def : LPAREN CONSTANTS_KEY typed_constants_lst RPAREN'''
    p[0] = {"constants":p[3]}


def p_predicates_def(p):
    '''predicates_def : LPAREN PREDICATES_KEY predicate_def_lst RPAREN'''
    p[0] = {"predicates":p[3]}


def p_predicate_def_lst(p):
    '''predicate_def_lst : predicate_def predicate_def_lst
                         | predicate_def'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_predicate_def(p):
    '''predicate_def : LPAREN NAME typed_variables_lst RPAREN
                     | LPAREN NAME RPAREN'''
    if len(p) == 4:
        p[0] = Predicate(p[2])
    elif len(p) == 5:
        p[0] = Predicate(p[2], p[3])


def p_functions_def(p):
    '''functions_def : LPAREN FUNCTIONS_KEY function_def_list RPAREN'''
    p[0] = {"functions":p[3]}

def p_function_def_list(p):
    '''function_def_list : function_def function_def_list 
                        |  function_def'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]

def p_function_def(p):
    '''function_def : LPAREN NAME VARIABLE HYPHEN NAME RPAREN
                    | LPAREN NAME RPAREN'''
    if len(p) == 7:
        p[0] = Function(p[2],p[3],p[5])
    elif len(p) == 4:
        p[0] = Function(p[2])

def p_actions_def(p):
    '''actions_def : action_def_lst'''
    p[0] = {"actions": p[1]}

def p_action_def_lst(p):
    '''action_def_lst : action_def action_def_lst
                      | action_def'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_action_def(p):
    '''action_def : LPAREN ACTION_KEY NAME parameters_def action_def_body RPAREN'''
    p[0] = Action(p[3], p[4], p[5][0], p[5][1])


def p_parameters_def(p):
    '''parameters_def : PARAMETERS_KEY LPAREN typed_variables_lst RPAREN
                      | PARAMETERS_KEY LPAREN RPAREN'''
    if len(p) == 4:
        p[0] = []
    elif len(p) == 5:
        p[0] = p[3]


def p_action_def_body(p):
    '''action_def_body : precond_def effects_def'''
    p[0] = (p[1], p[2])


def p_precond_def(p):
    '''precond_def : PRECONDITION_KEY LPAREN AND_KEY literals_lst RPAREN
                   | PRECONDITION_KEY literal'''
    if len(p) == 3:
        p[0] = [p[2]]
    elif len(p) == 6:
        p[0] = p[4]


# def p_effects_def(p):
#     '''effects_def : EFFECT_KEY LPAREN AND_KEY effects_lst RPAREN
#                    | EFFECT_KEY effect'''
#     if len(p) == 3:
#         p[0] = [p[2]]
#     elif len(p) == 6:
#         p[0] = p[4]


def p_effects_def(p):
    '''effects_def : EFFECT_KEY effects'''
    p[0] = p[2]


def p_effects(p):
    '''effects : effect
               | LPAREN AND_KEY effects_lst RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 5:
        p[0] = p[3]

def p_effects_lst(p):
    '''effects_lst : effect effects_lst
                   | effect'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]

def p_effect(p):
    '''effect : literal
              | LPAREN PROBABILISTIC_KEY probability_list RPAREN'''
    if len(p) == 2:
        p[0] = [(1.0, p[1])]
    elif len(p) == 5:
        p[0] = p[3]

def p_probability_list(p):
    '''probability_list : PROBABILITY effects
                        | PROBABILITY effects probability_list'''
    if len(p) == 3:
        p[0] = [(p[1],p[2])]
    elif len(p) == 4:
        p[0] = [(p[1],p[2])] + p[3]

def p_literals_lst(p):
    '''literals_lst : literal literals_lst
                    | literal'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_literal(p):
    '''literal : LPAREN NOT_KEY predicate RPAREN
               | predicate'''
    if len(p) == 2:
        p[0] = Literal.positive(p[1])
    elif len(p) == 5:
        p[0] = Literal.negative(p[3])


def p_ground_predicates_lst(p):
    '''ground_predicates_lst : ground_predicate ground_predicates_lst
                             | ground_predicate'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_predicate(p):
    '''predicate : LPAREN NAME variables_lst RPAREN
                 | LPAREN EQUALS VARIABLE VARIABLE RPAREN
                 | LPAREN NAME RPAREN'''
    if len(p) == 4:
        p[0] = Predicate(p[2])
    elif len(p) == 5:
        p[0] = Predicate(p[2], p[3])
    elif len(p) == 6:
        p[0] = Predicate('=', [p[3], p[4]])


def p_ground_predicate(p):
    '''ground_predicate : LPAREN NAME constants_lst RPAREN
                        | LPAREN NAME RPAREN'''
    if len(p) == 4:
        p[0] = Predicate(p[2])
    elif len(p) == 5:
        p[0] = Predicate(p[2], p[3])


def p_typed_constants_lst(p):
    '''typed_constants_lst : constants_lst HYPHEN type typed_constants_lst
                           | constants_lst HYPHEN type'''
    if len(p) == 4:
        p[0] = [ Term.constant(value, p[3]) for value in p[1] ]
    elif len(p) == 5:
        p[0] = [ Term.constant(value, p[3]) for value in p[1] ] + p[4]


def p_typed_variables_lst(p):
    '''typed_variables_lst : variables_lst HYPHEN type typed_variables_lst
                           | variables_lst HYPHEN type'''
    if len(p) == 4:
        p[0] = [ Term.variable(name, p[3]) for name in p[1] ]
    elif len(p) == 5:
        p[0] = [ Term.variable(name, p[3]) for name in p[1] ] + p[4]


def p_constants_lst(p):
    '''constants_lst : constant constants_lst
                     | constant'''
    if len(p) == 2:
        p[0] = [ Term.constant(p[1]) ]
    elif len(p) == 3:
        p[0] = [ Term.constant(p[1]) ] + p[2]


def p_variables_lst(p):
    '''variables_lst : VARIABLE variables_lst
                     | VARIABLE'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_names_lst(p):
    '''names_lst : NAME names_lst
                 | NAME'''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_type(p):
    '''type : NAME'''
    p[0] = p[1]


def p_constant(p):
    '''constant : NAME'''
    p[0] = p[1]

def p_empty(p):
     'empty :'
     p[0] = None

def p_error(p):
    print("Error: syntax error when parsing '{}'".format(p))


# build parser
yacc.yacc()


class PDDLParser(object):

    @classmethod
    def parse(cls, filename):
        data = cls.__read_input(filename)
        return yacc.parse(data)

    @classmethod
    def __read_input(cls, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = ''
            for line in file:
                line = line.rstrip().lower()
                line = cls.__strip_comments(line)
                data += '\n' + line
        return data

    @classmethod
    def __strip_comments(cls, line):
        pos = line.find(';')
        if pos != -1:
            line = line[:pos]
        return line
