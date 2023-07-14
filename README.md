# finite-state-morphology

Q2: Write ```expand_fst.sh```, which builds an expanded FST given a lexicon and morphotactic rules expressed by an FSA.

Args: 
* ```lexicon```: The lexicon file has the format “word classLabel”
* ```morph_rules```: The morph_rules file is an FSA (in the Carmel format) that encodes the morphotactic rules; that is, the input symbols in the FSA are class labels (e.g., regular_verb_stem).

Returns: 
* ```output_fst```: the expanded FST (in the Carmel format), where an arc in the morph_rule FSA is replaced by multiple paths and each path corresponds to a word in the lexicon that belongs to that category

To run: 
```
src/expand_fst.sh lexicon morph_rules output/output_fst
```

Note: only toy data is available under /input. 

Q3:  Write ```morph_acceptor.sh```, which checks whether the input words are accepted by the FST created in Q2. 

Args: 
* ```fst_file```: an FST (in the Carmel format).
*```word_list```: a list of words, one word per line 

Returns: 
* ```output_file```: has the format “word => answer” for each word in the word_list


To run: 
```
src/morph_acceptor.sh fst_file word_list output/output_file
```
Note: only toy data is available under /input. 

HW5 OF LING570 (11/04/2021)