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

########################
## first
########################
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
#########################
## Follow
#########################

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
