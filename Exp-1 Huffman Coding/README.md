Aim: To study and implement of Huffman coding

Equipment/Software: Python, Colab and Huffman packages

Theory:

Huffman coding is a popular method for compressing data with variable‐length codes.
Given a set of data symbols (an alphabet) and their frequencies of occurrence (or, equivalently,
their probabilities), the method constructs a set of variable‐length codewords with the shortest
average length and assigns them to the symbols. Huffman coding serves as the basis for several
applications implemented on popular platforms. The Huffman method is somewhat similar to the
Shannon–Fano method, proposed independently by Claude Shannon and Robert Fano in the late
1940s .It generally produces better codes, and like the Shannon–Fano method, it produces the best
variable‐length codes when the probabilities of the symbols are negative powers of 2. The main
difference between the two methods is that Shannon–Fano constructs its codes from top to bottom
(and the bits of each codeword are constructed from left to right), while Huffman constructs a code
tree from the bottom up (and the bits of each codeword are constructed from right to left).
The algorithm starts by building a list of all the alphabet symbols in descending order of
their probabilities. It then constructs a tree, with a symbol at every leaf, from the bottom up. This is
done in steps, where at each step the two symbols with smallest probabilities are selected, added to
the top of the partial tree, deleted from the list, and replaced with an auxiliary symbol representing
the two original symbols. When the list is reduced to just one auxiliary symbol (representing the
entire alphabet), the tree is complete. The tree is then traversed to determine the codes of the
symbols.
The steps of Huffman coding algorithm are given below:
1. Arrange the source symbols in increasing order of heir probabilities.
2. Take the bottom two symbols & tie them together as shown in Figure 1. Add the probabilities of
the two symbols & write it on the combined node. Label the two branches with a ‘1’ & a ‘0’ as
depicted in Figure 1.
3. Treat this sum of probabilities as a new probability associated with a new symbol. Again pick the
two smallest probabilities, tie them together to form a new probability. Each time we perform the
combination of two symbols we reduce the total number of symbols by one. Whenever we tie
together two probabilities (nodes) we label the two branches with a ‘0’ & a ‘1’.

4. Continue the procedure until only one procedure is left (& it should be one if your addition is
correct). This completes the construction of the Huffman Tree.
5. To find out the prefix codeword for any symbol, follow the branches from the final node back to
the symbol. While tracing back the route read out the labels on the branches. This is the codeword
for the symbol.
The Huffman is an instantaneous uniquely decodable block code. It is a block code because
each source symbol is mapped into a fixed sequence of code symbols. It is instantaneous because
each codeword in a string of code symbols can be decoded without referencing succeeding symbols.
That is, in any given Huffman code, no codeword is a prefix of any other codeword. And it is
uniquely decodable because a string of code symbols can be decoded only in one way. Thus any
string of Huffman encoded symbols can be decoded by examining the individual symbols of the
string in left to right manner. Because we are using an instantaneous uniquely decodable block
code, there is no need to insert delimiters between the encoded pixels.
