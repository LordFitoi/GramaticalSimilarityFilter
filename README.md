# GramaticalSimilarityFilter
This is a free-use text filter, it filters the words according to how similar the words are with the forbidden words. The objective of this algorithm is to detect and filter those unwanted words even if they are not written explicitly. That is, words with symbols in between, or with letters replacing others or even with numbers replacing letters, will be detected and filtered by the algorithm. 

* **Examples:** Banana, B4n4n4, Ba-na-na, Vanana.

The algorithm is inspired by how the simple perceptron works, that is, it is the algorithm itself that will be adjusted to give the best performance based on the test data that is shown.

> *Note: The parameter that will define whether or not a word passes the filter is bias.*

# Update: GramaticalSimilarityFilter v2
This is an special version of the algorithm, this version solve the performance of the last version, changing it from **O(n^2) to O(n)**. Likewise, it simplifies the code, giving a performance similar to the previous version without having to use the evaluation functions already mentioned.

# How to use
By default the filter brings a list of banned words as an example, it also brings a dataset which is used to calibrate the algorithm to our needs.

To quickly use the algorithm, you only have to use the **"Word_Filter.train(dataset, black_list, epochs)"** method, this to adjust the filter and already to be able to filter text just use the **"Word_Filter.filter_text(text, black_list)"** method.
```python
Word_Filter.train(dataset, black_list, 100)
print(Word_Filter.filter_text("Insert your text with banned words here.", black_list))
```

If what you want is to quickly test how accurate the algorithm is, you can use the **"Word_Filter.test(dataset, black_list)"** method, this will return a score of how accurate it was and also print which words I censor and which do not.
```python
Word_Filter.test(dataset, black_list)
```
If what you are looking for is not to directly censor a word, you can choose to use the function **"Word_Filter.predict(word, black_list)"**, this will do it to return true or false according to whether or not the word is one of the searched.
```python
Word_Filter.predict("Your word here", black_list)
```
When creating a dataset, the only thing we must do is put words that are written very similar to those prohibited or derived from the prohibited word and mark it 1 or 0 depending on whether it is banned or not.

* **black_list.json example file**
```json
{
  "words" : [
    "banana",
    "shit",
    "man"
  ]
}
```

* **dataset.json example file**
```json
{
  "pairs" : [
    ["bananas", 1],
    ["bananasplit", 1]
    ["apple", 0],
    ["shitter", 1],
    ["this", 0],
    ["hits", 0],
    ["woman", 1],
    ["man", 0]
  ]
}
```
> *Note: Depending on how good your dataset is compared to the list of prohibited words, it will show more or less performance. Marking words very different from those in the list as prohibited in the dataset could cause performance problems.*

# Technical information
It works by using metrics that analize gramaticaly two words.

1) The first metric analize if two words have similar letter secuence, the formulas are:
Being A & B = the letter secuence of their respective words, example;
if the word is apple, **A = {(a, p), (p, p), (p, l), (l, e)}**

* f(x) = x^2 > **#This is an evaluation function.**
* metric_1 = f(AnB) / f(AuB) **#This is the common secuence metric.**

2) The second one analize if two words have similar shape, the formulas are:
Being A & B = the two respective words length.

* f(x) = sqrt(x) **#This is another evaluation function.**
* metric_2 = f(min(A, B)) / f(max(A, B)) **#This is the shape metric.**

3) Finally we get the output by taking the average of the metrics;
* output = (metric_1 + metric_2) / 2

4) Affter getting the output we will use a number that we will call bias, its function will be uniquely and exclusively
to compare if 2 words are definitely the same, like this;

* Are similar <-> output >= bias

> *Note: The bias can be defined manually, the problem is that the recommended bias to obtain the best performance varies according to the training data and the list of banned words that we give it, so we have chosen to use optimization techniques. In other words, the bias adjusts itself based on the error obtained during training.*
