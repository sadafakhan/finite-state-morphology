import sys
import os
from nltk import word_tokenize, RegexpTokenizer
tokenizer = RegexpTokenizer(r'\"?\w+\.?\w+\"?')

# load in the data
unformat_lexicon = open(os.path.join(os.path.dirname(__file__), sys.argv[1]), 'r').read().split("\n")
unformat_morphrules = open(os.path.join(os.path.dirname(__file__), sys.argv[2]), 'r').read().split("\n")

# clean out the lexicon
lexicon = []
for entry in unformat_lexicon:
    if entry == '':
        pass
    else:
        new_entry = entry.split()
        lexicon.append(new_entry)


accept = unformat_morphrules.pop(0)

# clean out the morphrules but preserve the epsilon transitions
morphrules = []
for entry in unformat_morphrules:
    if entry == '' or entry == '\n':
        pass
    else:
        new_entry = tokenizer.tokenize(entry)
        if len(new_entry) == 2:
            new_entry.append('*e*')
        morphrules.append(new_entry)


# helper function for finding lexical items with a given class label
def find_pos(lexical_list, pos):
    match = []
    for list in lexical_list:
        if list[1] == pos:
            match.append(list)
    return match


# recreate a representation of the fsa where dict keys are class-labels and vals are transitions
fsa = {}
for entry in morphrules:
    pos = entry[2]
    if pos == "*e*":
        if pos in fsa:
            fsa[pos].append(entry)
        else:
            fsa[pos] = []
            fsa[pos].append(entry)
    for matching in find_pos(lexicon, pos):
        new_transition = [entry[0], entry[1], matching[0]]
        if pos in fsa:
            fsa[pos].append(new_transition)
        else:
            fsa[pos] = []
            fsa[pos].append(new_transition)


dummy_count = 0
fst = []
# from the fsa, create an fst and create new arcs/states to travel on each char and output class labels
for pos in fsa:
    for transition in fsa[pos]:
        initial = transition[0]
        end = transition[1]
        whole_input = transition[2]
        if whole_input == "*e*":
            exp_trans = [initial, end, whole_input, whole_input]
            fst.append(exp_trans)
        elif len(whole_input) == 1:
            tran1 = [initial, '$' + pos, whole_input, whole_input]
            tran2 = ['$' + pos, end, "*e*" , pos]
            fst.append(tran1)
            fst.append(tran2)
        else:
            for i in range (len(whole_input)):
                if i == 0:
                    exp_trans = [initial, '%' + str(dummy_count) + '%', whole_input[i], whole_input[i] ]
                elif i == (len(whole_input)-1):
                    exp_trans = ['%' + str(dummy_count) + '%', '$'+ pos, whole_input[i], whole_input[i]]
                else:
                    exp_trans = ['%' + str(dummy_count) + '%', '%' + str(dummy_count + 1) + '%', whole_input[i], whole_input[i]]
                    dummy_count += 1
                fst.append(exp_trans)
            dummy_count += 1
            final = ['$'+ pos, end, "*e*" , pos]
            if final in fst:
                pass
            else:
                fst.append(final)


# The output_fst file is the expanded FST (in the Carmel format), where an arc in the morph_rule FSA is replaced by
# multiple paths and each path corresponds to a word in the lexicon that belongs to that category:
with open(sys.argv[3], 'w') as of:
    of.write(accept)
    of.write("\n")
    for transition in fst:
        from_state = transition[0]
        to_state = transition[1]
        input_char = transition[2]
        output_char = transition[3]
        if output_char == '*e*' and input_char == '*e*':
            to_string = "(" + from_state + " (" + to_state + " " + input_char + " " + output_char + "))"
        elif output_char == '*e*':
            to_string = "(" + from_state + " (" + to_state + " \"" + input_char + "\" " + output_char + "))"
        elif input_char == '*e*':
            to_string = "(" + from_state + " (" + to_state + " " + input_char + " \"" + output_char +"\"))"
        else:
            to_string = "(" + from_state + " (" + to_state + " \"" + input_char + "\" \"" + output_char +"\"))"
        of.write(to_string)
        of.write("\n")