from new_impl import calculate_first,calculate_follow, term_and_nonterm, get_augmented , find_states, new_get_parse_table
from  state import State
from logo import print_logo
from termcolor import colored
from First_Follow import *

####################
## parser class initial
####################
class parser():

    def __init__(self, parent = None):
        self.init()

    def init(self):
        self.grammar = []
        self.augment_grammar = []
        self.first = {}
        self.follow = {}
        self.term = []
        self.non_term = []
        self.states = []            
        self.parse_table = []
        State.state_count = -1
###################
# instruction 
###################
    def interpereter(self):
        print_logo(0)
        print("If you don't know about the options, enter----> help")
        while True:
            cmd = input ("> ")
            if cmd == "help":
                print ("all commands are exit help first follow display states")
            if cmd == "exit":
                break
            if cmd == "first":
                self.disp_first()
            if cmd == "follow":
               self.disp_follow()
            if cmd == "display":
                self.disp()
            if cmd == "states":
                self.disp_states()

    def check_changed(self):
        self.changed = True
        
######################
## read grammer from inputer
######################
    def read_input(self):
        self.init()
        lines = ""
        n_line = int(input ("number of lines? "))
        for i in range(n_line):
            line = input ()
            line += "\n";
            lines += line
        lines_list = lines.split('\n')
        try:
            for line in lines_list:
                line = line.replace(' ' ,'')
                if line != '':
                    line_list = line.split('->')

                    if line_list[0].isupper() and line_list[1] != '':
                        if '|' in line_list[1]:
                            prod_list = line_list[1].split('|')
                            for prod in prod_list:
                                self.grammar.append([line_list[0],prod])
                        else:
                            self.grammar.append(line_list)
                    else:
                        self.grammar = []
            if self.grammar != []:
                #print('a')
                term_and_nonterm(self.grammar,self.term,self.non_term)
                calculate_first(self.grammar,self.first,self.term,self.non_term)
                calculate_follow(self.grammar,self.first,self.follow,self.term,self.non_term)
                get_augmented(self.grammar,self.augment_grammar)              
                find_states(self.states,self.augment_grammar,self.first,self.term,self.non_term)
                print('a')
                self.changed = False

        except (KeyError, IndexError):
            print ("Invalid grammar")
            self.init()



############################ 
##         DISPLAY          
############################

    def disp(self):
        if self.grammar == [] or self.changed:
            self.read_input()

        if self.grammar != []:
            for prod in self.grammar:
                s =  prod[0]+ ' -> ' + prod[1]+'\n'
                print("\n"+ s)
            print ("\nNon Terminals : "+' '.join(self.non_term)+"\nTerminals : "+' '.join(self.term))

############################
## DISPLAY FIRST
############################
    def disp_first(self):
        if self.first == {} or self.changed:# if this is the first time :)
            self.read_input()
        if self.first != {}:
            print ("===========================================================================")
            for nonterm in self.non_term:
                print('First('+nonterm+') : '+' '.join(self.first[nonterm])+'\n')
            print ("===========================================================================")

###########################
## DISPLAY FOLLOW
###########################
    def disp_follow(self):
        if self.follow == {} or self.changed:
            self.read_input()
        if self.first !={}:
            print ("===========================================================================")
            for nonterm in self.non_term:
                print('Follow('+nonterm+') : '+' '.join(self.follow[nonterm])+'\n')
            print ("===========================================================================")

###########################
## DISPLAY STATES
###########################
    def disp_states(self):
        if self.states == [] or self.changed:
            self.read_input()
        if self.states != []:
            print("Number of CLR states : "+ str(self.states[len(self.states)-1].state_num + 1))# cause states are numbered from 0 to n-1 ....
            for state in self.states:
                print('----------------------------------------------------------------')
                if state.state_num == 0:
                    print("\nI"+str(state.state_num)+' : '+'\n')
                else:
                    print("\nI"+str(state.state_num)+' : '+' goto ( I'+str(state.parent[0])+" -> '"+ str(state.parent[1]) +"' )\n")
                for item in state.state:
                    print(item[0]+ ' -> ' + item[1])
                if state.actions != {}:
                    print('\nActions : ')
                    for k,v in state.actions.items():
                        print(str(k)+' -> '+str(abs(v))+'\t')





if __name__ == '__main__':

    myapp = parser()
    myapp.interpereter()
