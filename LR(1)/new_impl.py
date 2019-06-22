from state import State
from copy import deepcopy


#############################
### find term and nonterm
#############################
def term_and_nonterm(grammar,term,non_term):
    for prod in grammar:
        if prod[0] not in non_term:# all left hands sides are non terms and all non terms must appear in left hand side
            non_term.append(prod[0])
        for char in prod[1]:
            if not char.isupper():
                if char not in term:
                    term.append(char)# if a char is lower case, it is term


def calculate_first(grammar,first,term,non_term):
    for t in term:
        first[t] = t;# first of a term is that term
    for nt in non_term:
        first[nt] = set({})
    for nt in non_term:
        get_first(nt,grammar,first,term)


def get_first(nt,grammar,first,term):
    for prod in grammar:# find the productions that NT has came as their left hand side
        if nt in prod[0]:
            rhs = prod[1]
            first_char = rhs[0]# initial first char
            if first_char in term:# we are if it is true
                first[nt].add(first[first_char])
            else:
                for char in rhs:
                    if not first[char] and nt != char:#cases that we have to calculate other nonterm firsts in order to calculate NT's first
                        get_first(char,grammar,first,term)

                i = 0
                while i < len(rhs) and 'e' in first[rhs[i]]:#while we have e in current rhs nonterm
                    for elem in first[rhs[i]]:
                        if 'e' != elem:#           e must only be added when all rhs goes to e
                            first[nt].add(elem)
                    i += 1
                if i == len(rhs):
                    first[nt].add('e')#if all rhs goes to e, i gets past the rhs hence lhs could produce e, so we add e
                else:
                    for elem in first[rhs[i]]:
                        first[nt].add(elem)


def calculate_follow(grammar,first,follow,term,non_term):
    for nt in non_term:
        follow[nt] = set({})
    follow[non_term[0]].add('$') #         follow of start symbol includes $
    for nt in non_term:
        get_follow(nt,grammar,first,follow,term)


def get_follow(nt,grammar,first,follow,term):
	for prod in grammar:
		if nt in prod[1]:#find productions that NT comes in their rhs
			rhs = prod[1].split(nt)[1]# find the right side of where NT was found
			i = 0
			for char in rhs:
				i+=1
				for elem in first[char]:
					if elem !='e':#we should not add e to follow of anything
						follow[nt].add(elem)
				if 'e' not in first[char]:#we should not continue
					i=-1
					break
			if nt!=prod[0] and i==len(rhs):# if right side of NT can go to e then we have to add lhs'follow to NT's follow
				if not follow[prod[0]]:# there is no point in adding it's follow to itself :) and if lhs'follow is not calculated, calculate it
					get_follow(prod[0],grammar,first,follow,term)
				for char in follow[prod[0]]:
					follow[nt].add(char)


def get_augmented(grammar,augment_grammar):
    augment_grammar.append([grammar[0][0]+"'",grammar[0][0]])#grammar==S->...  and augmented_grammar == S'->S
    augment_grammar.extend(grammar)

def closure(I,augment_grammar,first,non_term):#I is a list of states, it appears like I[0] = [lhs,rhs with . , follows]
    while True:
        new_item_added = False
        for item in I:
            cursor_pos = item[1].index('.')
            if cursor_pos == (len(item[1])-1):# in case . is at right end of production, we are done
                continue
            next_char = item[1][cursor_pos+1]
            if next_char in non_term:           # if char after . is non term then we need to add it's productions
                for prod in augment_grammar:
                    if next_char == prod[0]: # if char is in lhs of any production of grammar, we add it
                        if prod[1] == 'e':   # if the productions right hand side is only E then we have to add something like A->e. otherwise A->.(alpha)
                            rhs = 'e.'      
                        else:
                            rhs = '.' + prod[1]

                        new_item = [next_char,rhs]  # now we add new item to our states
                        if new_item not in I:                       
                            I.append(new_item)
                            new_item_added = True

        if not new_item_added:#we couldn't create new item so we are done :)
            break

def goto(I,X,augment_grammar,first,non_term):
    J =[]
    for item in I:
        cursor_pos = item[1].index('.')
        if cursor_pos < len(item[1])-1:# if . pos is not at the end of the production, we have goto move
            next_char = item[1][cursor_pos+1]
            if next_char == X :
                new_rhs = item[1].replace('.'+X,X+'.')#perform the goto move
                new_item = [item[0],new_rhs]
                J.append(new_item)#add the item after performing goto
    closure(J,augment_grammar,first,non_term)# do the rest of calculations for current closure
    return J# returns the closure produced after performing goto

def init_first(augment_grammar,first,non_term):
    I = [[augment_grammar[0][0],'.'+augment_grammar[0][1]]]# it is a list of production, first initilialized to only have start augmented production
    closure(I,augment_grammar,first,non_term)#here we calculate it's full closure
    return I

def isSame(states,new_state,I,X):#to check if the new state already exists
    for J in states:
        if J.state == new_state:
            I.update_goto(X,J)
            return True#if merge happend, return True
    return False

def find_states(states,augment_grammar,first,term,non_term):#calculates all the states and adds them to states (CLR states)
    first_state = init_first(augment_grammar,first,non_term)
    I = State(first_state)
    states.append(I)#states is self.state in parser which is a list
    all_symb = non_term + term
    while True:
        new_state_added =False#we have to continue untill no new state is added
        for I in states:
            for X in all_symb:
                new_state = goto(I.state,X,augment_grammar,first,non_term)
                if (new_state != [] ) and not isSame(states,new_state,I,X):#if we didn't have this new state, add it
                    N = State(new_state)
                    I.update_goto(X,N)
                    N.update_parentName(I,X)
                    states.append(N)
                    new_state_added = True

        if not new_state_added:
            break

def new_get_parse_table(parse_table,states,augmented_grammar,follow):                      #here states -> lalr_states
    ambiguous = False
    for index, I in enumerate(states):
        parse_table.append(I.actions)#add all goto actions
        for item in I.state:
            rhs_list = item[1].split('.') # for each item in state i 
            if rhs_list[1] == '':         # if . is  in right end of it add reduce actions aswell
                prod_no = augmented_grammar.index([item[0],rhs_list[0]])
                for la in follow[item[0]]:
                    if la in parse_table[index].keys():# in this case, we have already seen it so we have a conflict
                        ambiguous = True
                    else:
                        parse_table[index][la] = -prod_no# this - is added for being able to easily print the parse_table

    if ambiguous:
        print("Ambiguous Grammar!!\n\nGiving priority to Shift over Reduce")