import os
import sys
import subprocess

fst_file = sys.argv[1]
word_list = sys.argv[2]

words = open(os.path.join(os.path.dirname(__file__), word_list), 'r').read().split("\n")

with open(sys.argv[3], 'w') as of:
    for word in words:
        of.write(word)
        command = 'echo \'' + word + '\' | /NLP_TOOLS/ml_tools/FST/carmel/latest/bin/carmel -sli ' + fst_file
        results = subprocess.check_output(command, shell=True)
        answer = ''
        if len(results.decode('utf-8')) == 0:
            answer = '*NONE*'
        else:
            answer = word
        of.write(" => " + answer)
        of.write("\n")