import time,sys,random

def print_logo(self):
    clear = "\x1b[0m"
    colors = [36, 32, 34, 35, 31, 37]

    x = """


                UnderCover(Darklight)

██╗     ██████╗  ██╗ ██╗██╗ 
██║     ██╔══██╗██╔╝███║╚██╗
██║     ██████╔╝██║ ╚██║ ██║
██║     ██╔══██╗██║  ██║ ██║
███████╗██║  ██║╚██╗ ██║██╔╝
╚══════╝╚═╝  ╚═╝ ╚═╝ ╚═╝╚═╝ 
                            

 Note! :this script for LR(1) Parser .       
"""
    for N, line in enumerate(x.split("\n")):
        sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
        time.sleep(0.05)


