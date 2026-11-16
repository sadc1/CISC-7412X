import re

file_path = 'SMSSpamCollection'
class msg:
    def __init__(self, col1, col2): # Column 1 is ham/spam identifier, column 2 is the raw text
        self.is_spam = True if col1 == "spam" else False
        self.raw_text = col2.lower()
msg_list = []
spam_list = []
ham_list = []

with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        # Split each line by the tab character
        parts = line.strip().split('\t')
        if len(parts) == 2:
            label, message = parts
            # print(f"Label: {label} | Message: {message}")
            msg_list.append(msg(label, message))

# print(f"{msg_list}")

def class_find(is_spam):
    return spam_list if is_spam else ham_list

def class_prob(is_spam):
    return prob_spam() if is_spam else prob_ham()

def class_size(is_spam):
    return total_spam if is_spam else total_ham

def class_list_setup(is_spam):
    target_list = class_find(is_spam)
    for m in msg_list:
        if m.is_spam == is_spam:
            target_list.append(m)

class_list_setup(True)
class_list_setup(False)

total_msg = len(msg_list) # 5,574
total_spam = len(spam_list)
total_ham = len(ham_list)


def prob_spam(): # P(spam)
    return total_spam / total_msg

def prob_ham(): # P(not spam)
    return total_ham / total_msg

def tokenize(m): # Tokenize a message to look at individual words and not substrings, P(free | spam) is 0.22 with tokenization and 0.26 without tokenization
    return re.findall(r'\b[a-z0-9]+\b', m.lower())

def num_word_in_class(is_spam, word): # Count the amount of times a word appears in spam or non-spam datasets
    target_list = class_find(is_spam)
    word_l = word.lower()
    amount = 0
    for m in target_list:
        if word_l in tokenize(m.raw_text): # Incorrect way -> if word_l in m.raw_text
            amount += 1
    return amount

def prob_word_in_class(is_spam, word): # P(word | spam/not spam), probability of word appearing in spam/not spam list
    return (num_word_in_class(is_spam, word) + 1) / (class_size(is_spam) + 2) # + 1 and + 2 to account for words that do not appear in the dataset to prevent multipliers of 0 (and division by 0)

# P(spam | msg) = (P(msg | spam) * P(spam)) / P(msg)
# P(msg | spam) = P(word1 | spam) * P(word2 | spam) * ... * P(word_n | spam) (Conditional independence
# P(msg | ham) = the same but ham instead of spam
# P(msg) = P(msg | spam)P(spam) + P(msg | ham)P(ham)

# P(spam | msg) = (P(msg | spam) * P(spam)) / P(msg) = (P(spam) * prob of each word given spam) / (P(spam) * prob of each word given spam + P(ham) * prob of each word given ham)

def prob_word(word): # P(word)
    return (prob_spam() * prob_word_in_class(True, word)) + (prob_ham() * prob_word_in_class(False, word))

def prob_spam_given_msg(msg):
    word_list = set(tokenize(msg.lower())) # Remove duplicates
    word_prob_map = {}
    for w in word_list:
        word_prob_map[w] = {}
        word_prob_map[w]["prob_word_in_spam"] = prob_word_in_class(True, w)
        word_prob_map[w]["prob_word_in_ham"] = prob_word_in_class(False, w)
        word_prob_map[w]["prob_word"] = prob_word(w)
    num = prob_spam()
    denom_spam = prob_spam()
    denom_ham = prob_ham()
    for word, prob_map in word_prob_map.items(): # A redundant loop but it makes it easier to understand for myself
        num *= prob_map["prob_word_in_spam"]
        denom_spam *= prob_map["prob_word_in_spam"]
        denom_ham *= prob_map["prob_word_in_ham"]
    denom = denom_spam + denom_ham
    print(f"\nMessage: {msg}")
    print(f"Probability of being spam: {num / denom}")
    print(f"Probability of being non-spam: {1 - (num / denom)}")
    for word, prob_map in word_prob_map.items():
        print(f"P(w | spam) Word '{word}' chance to be spam: {prob_map["prob_word_in_spam"]}")
        print(f"P(w | non-spam) Word '{word}' chance to be spam: {prob_map["prob_word_in_ham"]}")
        word_count = num_word_in_class(True, word) + num_word_in_class(False, word)
        print(f"P(w) Word '{word}' probability: {prob_map["prob_word"]}, counted {word_count} times. {word_count} / total messages = {word_count / total_msg}")
    print(f"Numerator: {num}")
    print(f"Denominator: {denom}")
    return num / denom

print(f"Total messages: {total_msg}")
print(f"Total spam: {total_spam}")
print(f"Total non-spam: {total_ham}")
print(f"\n% of spam messages: {prob_spam()}")
print(f"% of non-spam messages: {prob_ham()}")

selected_words = ["free", "urgent", "yup", "u", "dis", "bank"]
print("\nSample selected words from the dataset that seem relevant enough")
for word in selected_words:
    print(f"Word {word} has {prob_word_in_class(True, word)} chance to be spam, {prob_word_in_class(False, word)} chance to be non-spam") # Chance to be non-spam is not necessarily 1 - spam chance
# print(f"{prob_word_in_class(True, "free")}")
# print(prob_spam_given_msg("Call now for FREE MONEY"))

# Test messages that I made up
prob_spam_given_msg("Call now for FREE MONEY")
prob_spam_given_msg("How ya doing?")
prob_spam_given_msg("Where you been?")
prob_spam_given_msg("We have been trying to reach you about extending your cars warranty")
