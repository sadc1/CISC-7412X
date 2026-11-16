# Summary

This homework uses this dataset: https://archive.ics.uci.edu/dataset/228/sms+spam+collection

The program is a spam classifier that will classify a given message as spam or non-spam ("ham" internally).

# Program Documentation

***file_path*** is the actual data file extracted from the .zip file linked above. There is no file extension. The path in the variable assumes you're running the program in the same directory as it.

The ***msg*** **class** stores a lower-case version of the supplied text message (msg.raw_text) and whether it is classified as spam in the dataset (msg.is_spam). This class is used only when processing the dataset, no *msg* objects are made after opening the file pointed to by *file_path*. All processed *msg* objects are stored in ***msg_list***.

***spam_list*** and ***ham_list*** store *msg* objects that have msg.is_spam set to True (goes in *spam_list*) or False (goes in *ham_list*). **class_list_setup()** performs this task, a parameter of True for *spam_list* and False for *ham_list*.

Since this program implements a Naive Bayes classifier with spam and non-spam, the probability functions involving spam and non-spam are all in the same functions. This refers to the functions **class_find()**, **class_prob()**, and **class_size()** which all return values based on *spam_list* or *ham_list* if their parameter is passed True or False. **class_find()** returns either list. **class_prob()** returns the probability associated with each list. **class_size()** returns the size of either list (variables ***total_spam*** and ***total_ham***).

**num_word_in_class()** returns the amount of times a word appears in *spam_list* or *ham_list*, depending on the parameter value.

Given a message, **tokenize()** returns a list of distinct tokenized words from the message. It returns everything in lower-case. This is essential since if the message is not tokenized, substrings can be double counted and improperly count words. For example, the word "hi" would be counted not only in any message "..hi.." but also in messages such as "It is high up."

## Probability Calculations
All words can be assumed to be conditionally independent given the class.

**prob_spam()** returns the percent of spam messages in the dataset. It can be represented as **P(spam)**. **prob_ham()** is similar, except it's the complement of P(spam) (the percent of non-spam messages in the dataset). It can be represented as **P(not spam)**.

**prob_word_in_class()** returns the probability a word appears in either *spam_list* or *ham_list*. This is mathematically **num_word_in_class()** / **class_size()**, but 1 and 2 are added to the numerator and denominator (respectively) to prevent products of 0, as well as dividing by 0. It can be represented as **P(word | spam)** or **P(word | not spam)**, depending on which list is going to be used.

**prob_word()** returns the probability a word appears in the entire dataset, which is the amount of times it appears in the entire dataset / size of the entire dataset. It can be represented as **P(word)**, equal to **P(spam) x P(word | spam) + P(not spam) x P(word | not spam).**

The entire goal of the program is to classify any given message as either spam or non-spam, which is the probability that a message is spam. It can be represented as **P(spam | msg)**, which is calculated by **prob_spam_given_msg()**. 

**P(spam | msg)** is equal to **(P(msg | spam) * P(spam)) / P(msg)** (Bayes' rule).

**P(msg | spam)** is the probability of each word independently being spam, all multiplied together. Given a message msg consisting of word1, word2, ..., word_n, it is equal to P(word1 | spam) * P(word2 | spam) * ... * P(word_n | spam). The same applies to **P(msg | not spam)**, except all spam events are replaced with not spam events.

**P(msg**), the probability a message appears in the entire dataset, is equal to **P(msg | spam)P(spam) + P(msg | not spam)P(not spam)**.

Therefore, **P(spam | msg)** is equal to **(P(msg | spam) * P(spam)) / P(msg) = (P(spam) * prob of each word given spam) / (P(spam) * prob of each word given spam + P(not spam) * prob of each word given not spam)**.
