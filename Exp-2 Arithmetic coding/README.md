Aim: Demonstration of arithmetic coding.

Equipment/Software: Octave

Theory:

Arithmetic coding overcomes the problem of assigning integer codes to the individual
symbols by assigning one (normally long) code to the entire input file. The method starts with a
certain interval, it reads the input file symbol by symbol, and it uses the probability of each symbol
to narrow the interval. Specifying a narrower interval requires more bits, so the number
constructed by the algorithm grows continuously. To achieve compression, the algorithm is
designed such that a high‐probability symbol narrows the interval less than a low‐probability
symbol, with the result that high‐probability symbols contribute fewer bits to the output. An
interval can be specified by its lower and upper limits or by one limit and width. The interval [0, 1]
can be specified by the two 1‐bit numbers 0 and 1. The interval [0.1, 0.512] can be specified by the
longer numbers 0.1 and 0.412. The very narrow interval [0.12575, 0.1257586] is specified by the
long numbers 0.12575 and 0.0000086.
The output of arithmetic coding is interpreted as a number in the range [0, 1). [The notation [a, b)
means the range of real numbers from a to b, including a but not including b. The range is “closed”
at a and “open” at b.] Thus the code 9746509 is be interpreted as 0.9746509, although the 0. part is
not included in the output file.
The main steps of arithmetic coding are summarized below:
1. Start by defining the “current interval” as [0, 1).
2. Repeat the following two steps for each symbol s in the input stream:
2.1. Divide the current interval into subintervals whose sizes are proportional to the symbols’
probabilities.
2.2. Select the subintervals for s and define it as the new current interval.
3. When the entire input stream has been processed in this way, the output should be any number
that uniquely identifies the current interval (i.e., any number inside the current interval).
For each symbol processed, the current interval gets smaller, so it takes more bits to express it, but
the point is that the final output is a single number and does not consist of codes for the individual
symbols. The average code size can be obtained by dividing the size of the output (in bits) by the
size of the input (in symbols).
