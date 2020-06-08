# GramaticalSimilarityFilter
This is a free use text filter, filter words based on how similar the prohibited words are.

# How to use
Just use the method Word_Filter.filter_text(text, black_list).
The first parameter is the text that you want to filter, and the second one is the list of words you want to filter.

If you want to make your own list, just edit the black_list.json file, the dataset.json file only contains a
few samples of words which are used to calibrate the filter, if you create your own blacklist it is important
that samples of which words should be censored and which not, if they are words that are they are very similar
but with different meanings better. To indicate that it is a banned word just put 1, otherwise 0.

# Technical information
It works by using metrics that analize gramaticaly two words.

1) The first metric analize if two words have similar letter secuence, the formulas are:
Being A & B = the letter secuence of their respective words example;
if the word is apple, **A = {(a, p), (p, p), (p, l), (l, e)}**

* f(x) = x^2 > **#This is an evaluation function.
* metric_1 = f(AnB) / f(AuB) **#This is the common secuence metric.**

2) The second one analize if two words have similar shape, the formulas are:
Being A & B = the two respective words

* f(x) = sqrt(x) **#This is another evalution function.**
* metric_2 = f(min(A, B)) / f(max(A, B)) **#This is the shape metric.**

3) Finally we get the output by taking the average of the metrics;
* output = (metric_1 + metric_2) / 2

4) Affter getting the output we will use a number that we will call bias, its function will be uniquely and exclusively
to compare if 2 words are definitely the same, like this;

* Are similar <-> output >= bias

Glosary:

- **Evaluation function:** It is a mathematical function which serves to control the behavior of the analysis in the metric.


> **Note: We can put manually the bias value, but i recomment to use optimization techniquies, because performance is strongly
affected by this factor, a very high bias would make the words have to be exactly the same for them to be filtered, and
a very low bias would make all the words be filtered, therefore it is important to find the balance where All or most
of the words are filtered correctly.**
