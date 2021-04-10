
import json, math

with open("blacklist.json", "r") as jsonfile:
    blacklist = json.load(jsonfile)["words"]

with open("dataset.json", "r") as file:
    dataset = json.load(file)

class HashmapFilter:
    key_dict = {
        # Insert here all symbols that you want to replace or delete from the words during the format.
        "4" : "a", "0" : "o", "3" : "e", "7" : "t",
        "-" : "", "_" : "", "." : "", "," : "",
        "?" : "", "!" : "", "@" : "", "#" : "",
        "&" : ""
    }
    lr = 0.001 # This determines how fast the bias adjusts, recommended low values like this one.
    bias = 0 # Recommended to keep it in one to get always the best performace

    def __init__(self, k):
        self.word_list = set()
        self.max_size = k

    def add_word(self, word):
        group_size = min(int(math.sqrt(len(word))) + 1 , self.max_size)
        if len(word) >= group_size:
            for i in range(len(word) - group_size + 1):
                self.word_list.add(word[i : i + group_size])
        
        else: print(f"Palabra {word} es demaciado corta.")

    def get_probability(self, word):
        probability = 0
        word = self.format(word)
        group_size = min(int(math.sqrt(len(word))) + 1 , self.max_size)
        if len(word) >= group_size:
            for i in range(len(word) - group_size + 1):
                group = word[i : i + group_size]
                probability += int(group in self.word_list)
        
            return math.sqrt(probability / (len(word) - group_size + 1))
        else: return 0

    def format(self, word):
        """Remove junk characters and replaces others with their equivalents, dtype -> str"""
        new_word = word.lower()
        for key in self.key_dict:
            new_word = new_word.replace(key, self.key_dict[key])

        return new_word

    @staticmethod
    def filter_word(word):
        """returns a character string with the form of the word, dtype -> str"""
        return "".join(["*" for i in range(len(word))])

    def train(self, dataset, epochs = 50):
        """Fit the bias based on the examples given and the list of banned words"""

        # This function is used to automatically fit the bias, this works like a neural network or similars.
        print("\n< Training start >")
        for epoch in range(epochs):
            for wordA, expected_output in dataset["pairs"]:
                output = int(self.get_probability(wordA) >= self.bias)
                self.bias += (output - expected_output) * self.lr
                
            if not epoch%9:
                print(f"Current Epoch {epoch}, bias value {round(self.bias, 3)}")
        print("< Training end >\n")
    

    def test(self, dataset):
        """Tests the score of the algorithm. Note: the score can change by adding more
        training data banned words or by changing evalution functions"""
        score = 0
        for wordA, expected_output in dataset["pairs"]:
            output = int(self.get_probability(wordA.lower()) >= self.bias)

            # This part, print if the word was filtered or not.
            if output: print(f"{self.filter_word(wordA)} | {wordA} -> {expected_output}")
            else: print(f"{wordA} -> {expected_output}")

            score += int(output == expected_output)

        print(f"\nTotal score: {round(score / len(dataset['pairs']) * 100)}%\n")
    
    def filter_text(self, text):
        """returns text by filtering banned words, dtype -> str"""
        word_list = text.split(" ")
        for index, word in enumerate(word_list):
            output = self.get_probability(word)
            if output: word_list[index] = self.filter_word(word)
        
        return " ".join(word_list)

word_filter = HashmapFilter(3)

for word in blacklist:
    word_filter.add_word(word.lower())

word_filter.test(dataset)
word_filter.train(dataset, 200)
word_filter.test(dataset)


while True:
    text = input(">> ")
    if text.lower() == "exit": break
    else:
        print(word_filter.filter_text(text))
