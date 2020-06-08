# GramaticalSimilarityFilter
This is a free use text filter, filter words based on how similar the prohibited words are.

# How to use
By default the filter brings a list of banned words as an example, it also brings a dataset which is used to calibrate the algorithm to our needs.

To quickly use the algorithm, you only have to use the "Word_Filter.train(dataset, black_list, epochs)" method, this to adjust the filter and already to be able to filter text just use the "Word_Filter.filter_text(text, black_list)" method.
```python
Word_Filter.train(dataset, black_list, 100)
print(Word_Filter.filter_text("Insert your text with banned words here.", black_list))
```

If what you want is to quickly test how accurate the algorithm is, you can use the Word_Filter.test () method, this will return a score of how accurate it was and also print which words I censor and which do not.
```python
Word_Filter.test(dataset, black_list)
```

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

# Evaluation Functions
In this algorithm is a mathematical function that is used to control the behavior of the analysis in the metric. Different functions exert different properties and performance within the algorithm. What I will put next are the different evaluation functions that I test and their behavior within the filter.

* **Cuadratic Evaluation:** f(x) = x^2, It makes the relationship between two groups easily distinguishable.
* ![alt text](https://github.com/LordFitoi/GramaticalSimilarityFilter/blob/master/GSF_images/cuadratic_evaluation.PNG)

* **Square Root Evaluation:** f(x) = sqrt(x), It makes the relationship between two groups easily alike. It is usually more unstable when two groups are very different.
* ![alt text](https://github.com/LordFitoi/GramaticalSimilarityFilter/blob/master/GSF_images/square_root_evaluation.PNG)

* **Logaritmic Evaluation:** f(x) = log10(x + 1), Similar to the square root evaluation with the difference that it does not present instability when two groups are completely different. 

* ![alt text](https://github.com/LordFitoi/GramaticalSimilarityFilter/blob/master/GSF_images/logaritmic_evaluation.PNG)

> **Note: We can put manually the bias value, but i recomment to use optimization techniquies, because performance is strongly
affected by this factor, a very high bias would make the words have to be exactly the same for them to be filtered, and
a very low bias would make all the words be filtered, therefore it is important to find the balance where All or most
of the words are filtered correctly.**
