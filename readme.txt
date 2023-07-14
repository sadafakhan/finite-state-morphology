
Q1.
(a) Let R be a relation. Let L = {x | there exists y, such that (x, y) ∊ R}. If R is a regular relation, then L is a regular language. 

R is regular relation, and thus has an FST that can process it. Duplicate this FST and convert all the output characters (effectively, deleting all y) in each arc to the empty string. It is now an FST that produces no output, which matches the definition of an FSA (recall that FSA is just a special case of FST). This FSA effectively accepts the language L, as it only takes x as input. Because there is an FSA that accepts it, L is a regular language. 

(b) Let L1 and L2 be two languages. Let R be the cross product of L1 and L2. That is, R = {(x, y) | x ∊ L1 and y ∊ L2}. If L1 and L2 are regular languages, then R is a regular relation. 

True. Regular relations are defined as for all (x,y) in AB1 x AB2, {(x,y)} is a regular relation. That is to say, any item from the cross-product of two alphabets constitutes a regular relation. The cross product of L1 and L2 is akin to the cross product of these alphabets, in the sense that every string in a regular language can be reinterpreted as a new representative symbol. For example, the regular language a* is written over the alphabet epsilon, a, but can be reinterpreted as the set {epsilon, a, aa, aaa, aaaa, ...}. 

*discarded argument*
If L1 and L2 are regular languages, there are FSAs that accept them.  Recall that FSAs are a special case of FST, where arcs output only the empty string. Thus we can conceptualize L1 and L2 as regular relations themselves, where (x, e) is in L1, and (y, e) is in L2 (e stands for epsilon here). Regular relations are closed under cross product by definition, so the cross product of L1 and L2 is {(}


Q2.
I didn't complete the expand_fsa part of last week's assignment, so I will be making hypothetical observations on the differences between the two. Assumedly because the prior is an fsa expander, it cannot produce an output, and thus all arcs produce the empty string. Because it's not possible to print out a class-label, this algorithm should produce a slightly smaller fst expand_fst. This is because the intermediate state added between the end of a "word's" input and the original destination state doesn't need to exist (in my implementation, this state is called $[class label]). One can simply transduce on the last character in a "word" to the original destination state. Since these intermediate class-label states don't exist, neither do the arcs coming into and out of it, leading to a reduction in the total number of arcs by a factor of how many class-label states exist. This is because even though the arcs from the class-label state to the original destination state are being deleted, the arcs traveling on the last character of a given "word" still exist and thus travel directly to the destination state. 

For example, consider the word "walked". 

In the FST, this set of transitions looks like: 
(q0 (%26% "w" "w"))
(%26% (%27% "a" "a"))
(%27% (%28% "l" "l"))
(%28% ($reg_verb_stem "k" "k"))
($reg_verb_stem (q1 *e* "reg_verb_stem"))
(q1 (%51% "e" "e"))
(%51% ($past_participle "d" "d"))
($past_participle (q3 *e* "past_participle"))

These 8 arcs produce the output: "w" "a" "l" "k" "reg_verb_stem" "e" "d" "past_participle". 

In the FSA, this would look like: 
(q0 (%26% "w"))
(%26% (%27% "a"))
(%27% (%28% "l"))
(%28% (q1 "k"))
(q1 (%51% "e"))
(%51% (q3 "d"))

Notice how there are two fewer states (corresponding to the class labels) and two fewer arcs (also corresponding to the class labels). 

Additional readme notes: 

I again had trouble with this assignment when it came to the carmel handling. Although my fst seemed fine to me, it couldn't process anything. I ran both of the following from patas to test it: 
-bash-4.2$ echo walked | /NLP_TOOLS/ml_tools/FST/carmel/latest/bin/carmel -sli sadaf.out
Input line 1: walked
	(0 states / 0 arcs)
Empty or invalid result of composition with transducer sadaf.out.

-bash-4.2$ echo "w" "a" "l" "k" "e" "d" | /NLP_TOOLS/ml_tools/FST/carmel/latest/bin/carmel -sli sadaf.out
Input line 1: w a l k e d
	(0 states / 0 arcs)
Empty or invalid result of composition with transducer sadaf.out.

What confused me here is that my fst seems like it should be able to handle this. The states in it are as shown above in Q2, with the additional line showing that q3 is the final state. Because of this, I wasn't able to finish the rest of the assignment. 

I still have trouble figuring out how to access values output from a carmel decision to manipulate later in python, nor do I know how to acquire the morph values? Are they simply printed out from carmel if the transducer worked? Regardless, I created some flawed code so that I could actually run the data, but this isn't working either: 

Traceback (most recent call last):
  File "./morph_acceptor.py", line 16, in <module>
    results = subprocess.check_output(command, shell=True)
  File "/opt/python-3.4.1/lib/python3.4/subprocess.py", line 620, in check_output
    raise CalledProcessError(retcode, process.args, output=output)
subprocess.CalledProcessError: Command 'echo 'cut' | /NLP_TOOLS/ml_tools/FST/carmel/latest/bin/carmel -esli sadaf.out' returned non-zero exit status 255

I feel in retrospect like we rushed past how to use carmel. The tutorial provided is a bit dense, and the descriptions carmel itself provides for the use of each suffix are personally also unclear. I attend office hours, but I can't seem to recreate errors at those times (not because they aren't occurring, but because the process of getting carmel to run and to find a viable test fsa/fst and test data are tedious and overwhelming). It's frustrating because this is the third time I've run into issues as a result of not being able to figure out how to interface carmel and python (or more broadly python and the command line). 