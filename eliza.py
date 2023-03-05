'''
Programming Assignment 1 - ELIZA
Class: CMSC416 Natural Language Processing
Author: Pranaav Rao
Date: 2/8/2022

This is a program that engages a dialogue with the user through the role of a psychotherapist.

Directions: Communicate with the program using plain-text English. It runs smoother with less punctuation.
            Submit an empty response to end the program.

            Usage: from command line, traverse to file location and use command 'python3 eliza.py'
Example of Program Output:
--------------
    HI, I'M ELIZA, A PSYCHOTHERAPIST. WHAT IS YOUR NAME?
    whats good
    HOW DOES THAT MAKE YOU FEEL?
    not bout 
    CAN YOU ELABORATE ON THAT?
    no
    I SEE.
-------------

Algorithm: The program begins with a predefined statement. Once the user responds, input is collected and used as the parameter for
the reassemble function. This function compares the user response to a list of reassembly rules based on regular expressions. If the
user response matches any of the specified regular expressions, ELIZA will return the correlating, predefined response which will
include the keyword in the user input as well as use the transform function to transform any possessive words to their counterpart.

Sources:
https://www.w3schools.com/python/python_regex.asp
https://docs.python.org/3/library/re.html
'''

import re
import random

# a dictionary of transformations used in transform function
transformations = {
  "am"   : "are",
  "was"  : "were",
  "i"    : "you",
  "i'd"  : "you would",
  "i've"  : "you have",
  "i'll"  : "you will",
  "my"  : "your",
  "are"  : "am",
  "you've": "I have",
  "you'll": "I will",
  "your"  : "my",
  "yours"  : "mine",
  "you"  : "me",
  "me"  : "you"
}
#transform function with String parameter as input
def transform(userin):
    words = userin.lower().split()  #input is divided into a list of the lowercase words composing it
    for i in range(0, len(words)):  #for each word
      if words[i] in transformations.keys():    #if that word is found in the transformations dictionary
        words[i] = transformations[words[i]]    #the word is replaced by the value of that key
    return ' '.join(words)      #sentence is compiled and returned

# a 3D array of reassembly rules used in reassemble function
#   the first item of each 2nd level array is the regex pattern the input is compared to
#   the second item is an array of predefined responses which may use the group noted in the first item
reassembly_rules = [
  [r'My name is (.*)',
  ["Hello %1. How are you today?",
   "How are you %1?"]],

  [r'don\'?t ([^\?]*)\??',
  [  "Do you really think I don't %1?",
    "Do you really want me to %1?"]],

  [r'can\'?t (.*)',
  [  "How do you know you can't %1?",
    "Perhaps you could %1 if you tried.",
    "What would it take for you to %1?"]],

  [r'I[\'?| a]m (.*)',
  [  "Did you come to me because you are %1?",
    "How long have you been %1?",
    "Why do you tell me you're %1?",
    "Why do you think you're %1?"]],

  [r'What (.*)',
  [  "Why do you ask?",
    "What do you think?"]],

  [r'How (.*)',
  [  "How do you suppose?",
    "What is it you're really asking?"]],
  
  [r'When (.*)',
  [  "Are you sure you can do it?"
     "Why not now?"]],

  [r'Because (.*)',
  [  "Is that really why?",
    "If %1, what else must be true?"]],

  [r'sorry',
  [  "Don't apologize, there is nothing wrong with that.",
    "Do you really feel that?"]],

  [r'Hello(.*)',
  [  "Hello... I'm glad you could drop by today.",
    "Hi there... how are you today?",
    "Hello, how are you feeling today?"]],
  
  [r'I think (.*)',
  [  "Do you doubt %1?",
    "Do you really think so?",
    "But you're not sure %1?"]],

  [r'Yes',
  [  "You seem quite sure.",
    "OK, but can you elaborate a bit?"]],

  [r'No',
  [  "Is it really that?",
    "Yes may be a possiblity.",]],

  [r'Is it (.*)',
  [  "Do you think it is %1?",
    "It is likely that %1."]],

  [r'It is (.*)',
  [  "You seem very certain."]],

  [r'Can I ([^\?]*)\??',
  [  "Perhaps you don't want to %1.",
    "Do you want to be able to %1?",
    "If you could %1, would you?"]],

  [r'You are (.*)',
  [  "Why do you think I am %1?",
    "Does it please you to think that I'm %1?",
    "Perhaps you would like me to be %1.",
    "Perhaps you're really talking about yourself?"]],

  [r'You\'?re (.*)',
  [  "Why do you say I am %1?",
    "Why do you think I am %1?",
    "Are we talking about you, or me?"]],

  [r'I don\'?t (.*)',
  [  "Don't you really %1?",
    "Why don't you %1?",
    "Do you want to %1?"]],

  [r'I feel (.*)',
  [  "Good, tell me more."]],

  [r'I have (.*)',
  [  "Why do you tell me that you've %1?",
    "Have you really %1?",
    "Now that you have %1, what will you do next?"]],

  [r'I would (.*)',
  [  "Could you explain why you would %1?",
    "Why would you %1?",
    "Who else knows that you would %1?"]],

  [r'My (.*)',
  [  "I see, your %1.",
    "Why do you say that your %1?",
    "When your %1, how do you feel?"]],

  [r'You (.*)',
  [  "We should be discussing you, not me.",
    "Why do you say that about me?",
    "Why do you care whether I %1?"]],

  [r'Why (.*)',
  [  "Why don't you tell me the reason why %1?",
    "Why do you think %1?" ]],

  [r'(.*)',
  [  "Please tell me more.",
    "Can you elaborate?",
    "Why do you say that %1?",
    "I see.",
    "Very interesting.",
    "%1."]]
  ]
# maps the first item regex pattern into a keys list
keys = list(map(lambda x: re.compile(x[0], re.IGNORECASE), reassembly_rules))
# maps the second item predefined responses into a values list
values = list(map(lambda x: x[1], reassembly_rules))

# function that takes user input and reassembles it according to the reassembly_rules array
def reassemble(input):
    for i in range(0, len(keys)):
      match = keys[i].match(input)  
      if match:                     #if input matches any regex pattern key
        response = random.choice(values[i])     #response is initialized to random string in corresponding value array 
        position = response.find('%')   #record position of the %
        while position > -1:            #if there is a %
          grp = int(response[position+1:position+2])        
          response = response[:position] + transform(match.group(grp)) + response[position+2:]
          position = response.find('%')
        return response
    return None

# main function
if __name__ == "__main__":
  print("---to stop dialogue, respond with empty string---\n"+("Hi, I'm ELIZA, a psychotherapist. What is your name?").upper())
  flag = True
  while flag:
    userin = input()
    if len(userin) == 0:
        #if user input is blank, the program ends
        flag = False
    else:
        print(reassemble(userin).upper())  # ELIZA will always respond in uppercase as to distinguish the user
