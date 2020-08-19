# Data-Encryption
In this experiment our aim is to find Compression ratio using LZ78.
We use Google Colab for the execution of the code

For LZ78

LZ78-based schemes work by entering phrases into a dictionary and then, when a repeat occurrence of that particular phrase is found, outputting the dictionary index instead of the phrase.
Every step LZ78 will send a pair (i,a) to the output, where i is an index of the phrase into the dictionary and a is the next symbol following immediately after the found phrase. The dictionary is represented like the trie with numbered nodes. If we go from the root to a certain node, we will get phrase from the input text.
In each step we look for the longest phrase in dictionary, that would correspond to the unprocessed part of the input text. Index of this phrase together with the symbol, which follows the found part in input text, are then send to the output. The old phrase extended by the new symbol is then put into dictionary. This new phrase is numbered by the smallest possible number.
The coding will start with tree, that has only one node, which represents empty string.

