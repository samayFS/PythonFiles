import os
import sys
import dramatiq
from subprocess import Popen, PIPE
from subprocess import call
@dramatiq.actor
# def Funct2():
#     process = Popen(['python3', 'FiletoParse.py'], stdout=PIPE, stderr=PIPE)
#     stdout, stderr = process.communicate()
#     print(stdout)
#     # os.system("python3 FiletoParse.py")
#
# Funct2.send()
def GetData(args):
        print(args)




