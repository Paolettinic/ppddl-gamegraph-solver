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