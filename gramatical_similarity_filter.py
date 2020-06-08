# Author: Nahum Santana
# Discord: Lord Fitoi >83#6492

# @ Description:
# I have created this code for a game in which I participate in its development,
# the objective of this filter was that it would be capable of filtering as many
# words without creating a long list in which each variant had to be added, it is
# say to avoid using slightly altered words but clearly noticing what they were.

# I publish this algorithm with the purpose that it is not forgotten. It can be 
# used both in video game chats, or personal apps, as well as in disc bots or other
#  social networks.

# < Imports >
import json, os, math
# < Imports end >

# < Loads dataset and black list >
main_dir = os.path.dirname(os.path.abspath(__file__))
black_list_path = os.path.join(main_dir, "black_list.json") 
dataset_path = os.path.join(main_dir, "dataset.json")

with open(black_list_path, "rb") as file:
    black_list = json.load(file)

with open(dataset_path, "rb") as file:
    dataset = json.load(file)
# < Loads end >

# < Word Filter >
class Word_Filter:
    key_dict = {
        # Insert here all symbols that you want to replace or delete from the words during the format.
        "4" : "a", "0" : "o", "3" : "e", "7" : "t",
        "-" : "", "_" : "", "." : "", "," : "",
        "?" : "", "!" : "", "@" : "", "#" : "",
        "&" : ""
    }
    
    lr = 0.0005 # This determines how fast the bias adjusts, recommended low values like this one.
    bias = 1 # Recommended to keep it in one to get always the best performace
    
    @staticmethod
    def get_letter_secuence(word):
        """Returns the letters secuence of the word, dtype -> list(of tuple)"""
        return list(set([(word[i], word[i + 1]) for i in range(len(word) - 1)]))

    @classmethod
    def get_parameters(cls, wordA, wordB):
        """Returns the parameters that will be used to for filter words, dtype -> list(of int)"""
        wordA_letters = cls.get_letter_secuence(wordA)
        wordB_letters = cls.get_letter_secuence(wordB)
        
        common_letters = [letter for letter in wordA_letters if letter in wordB_letters]
        words_letters = list(set(wordA_letters + wordB_letters))

        return [len(common_letters), len(wordB_letters), len(wordA), len(wordB)]

    @staticmethod
    def get_similarity(parameters, funcA, funcB):
        """Returns the similarity of two word. this's works with two metrics,the secuence of letters
        and the shape of both words. Note: diferents evaluation function can change
        the performance, dtype -> float"""

        # This metric is used for get words with a similar letter secuence.
        common_letter_metric = funcA(parameters[0]) / funcA(parameters[1])
        
        # This metric is used for get words with a similar shape.
        min_shape_value = min(parameters[2], parameters[3])
        max_shape_value = max(parameters[2], parameters[3])
        shape_metric = funcB(min_shape_value) / funcB(max_shape_value)

        # At the end the average is returned.
        return (common_letter_metric + shape_metric) / 2
    
    @classmethod
    def format(cls, word):
        """Remove junk characters and replaces others with their equivalents, dtype -> str"""
        new_word = word.lower()
        for key in cls.key_dict:
            new_word = new_word.replace(key, cls.key_dict[key])

        return new_word

    @classmethod
    def predict(cls, wordA, black_list):
        """Returns true if the word is banned, dtype -> bool"""
        # This are the evalution functions.
        funcA = lambda x: x**2
        funcB = lambda x: math.sqrt(x)
        
        is_banned_word = False
        for wordB in black_list["words"]:
            # First, we get the parameters that we will use.
            parameters = cls.get_parameters(cls.format(wordA), cls.format(wordB))
            
            # Second, we compare how similar these two words are.
            output = cls.get_similarity(parameters, funcA, funcB)
            
            # Finally, we compare if the output is above to the bias.
            # Note: One highest bias wont filter words, but one smallest will filter all them.
            if output >= cls.bias: is_banned_word = True; break
        
        return is_banned_word

    @staticmethod
    def filter_word(word):
        """returns a character string with the form of the word, dtype -> str"""
        return "".join(["*" for i in range(len(word))])

    @classmethod
    def train(cls, dataset, black_list, epochs = 50):
        """Fit the bias based on the examples given and the list of banned words"""

        # This function is used to automatically fit the bias, this works like a neural network or similars.
        print("\n< Training start >")
        for epoch in range(epochs):
            for wordA, expected_output in dataset["pairs"]:
                output = cls.predict(wordA, black_list)
                cls.bias += (output - expected_output) * cls.lr
                
            if not epoch%9:
                print(f"Current Epoch {epoch}, bias value {round(cls.bias, 3)}")
        print("< Training end >\n")
            
    @classmethod
    def test(cls, dataset, black_list):
        """Tests the score of the algorithm. Note: the score can change by adding more
        training data banned words or by changing evalution functions"""
        score = 0
        for wordA, expected_output in dataset["pairs"]:
            output = cls.predict(wordA, black_list)

            # This part, print if the word was filtered or not.
            if output: print(cls.filter_word(wordA))
            else: print(wordA)

            score += int(output == expected_output)

        print(f"\nTotal score: {round(score / len(dataset['pairs']) * 100)}%\n")
    
    @classmethod
    def filter_text(cls, text, black_list):
        """returns text by filtering banned words, dtype -> str"""
        word_list = text.split(" ")
        for index, word in enumerate(word_list):
            output = cls.predict(word, black_list)
            if output: word_list[index] = cls.filter_word(word)
        
        return " ".join(word_list)

# < Word Filter end >

# < Training and Testing >

Word_Filter.test(dataset, black_list)
Word_Filter.train(dataset, black_list, 100)
Word_Filter.test(dataset, black_list)

# < Training and Testing end >

# This part is for the user to test the filter.
# Somethings that you can try:
# - Write words with symbols in the middle, like; B-a-n.a@n.a.
# - Write words with numbers as equivalent of letters, like; 4ppl3 (this is apple)
# - Write variants of the words, like: work, worker, works, working...

# If you want to filter a new word, just add it to the black list file.

# Recommended: If you add a new word to the black list, try to add some example of

# case that you want the filter need to do the work and when not.

while True:
    text = input("\n>> ")
    if text.lower() == "exit": break
    else:
        censored_text = Word_Filter.filter_text(text, black_list)
        print(censored_text)
