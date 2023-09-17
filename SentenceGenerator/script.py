import random
import os

def write_sentences(num:int) -> None:
    '''A function that creates meaningless sentences from a dictionary in the home directory.'''
    # A list of allowed starting word letters
    letters = []
    with open(f"{os.getcwd()}\\SentenceGenerator\\Sentences.txt", "w+") as sentences:
        # Get the allowed starting word letters
        for number in range(26):
            letter = "codedefghijklmnopqrstuvwxyz"[random.randrange(0,26)]
            letters.append(letter)
        with open(f"{os.getcwd()}\\SentenceGenerator\\dictionary.txt") as dictionary:
            # Lists for verbs, adjectives, subjects and objects that the sentences will be structured with
            verbs = []
            adjectives = []
            objects = []
            subjects = ["I am", "You are", "He is", "She is", "It is", "We are", "They are"]
            # Lists of allowed endings
            verb_endings = ('ing\n', 'ied\n')
            adjective_endings = ('able\n', "abled\n", 'ive\n', 'ful\n', 'less\n')
            not_object_endings = ('ing\n', 'ied\n', 'able\n', 'abled\n', 'ive\n', 'ful\n', 'less\n', 'ed\n')
            for word in dictionary.readlines():
                # Fill the above lists after recognising them as verbs, adjectives or objects, only if they start with a letter included in the starting letter list
                if word.endswith(verb_endings) and word[0] in letters and len(word) > 5:
                    verbs.append(word.rstrip())
                if word.endswith(adjective_endings) and word[0] in letters and len(word) > 5:
                    adjectives.append(word.rstrip())
                if not word.endswith(not_object_endings) and word[0] in letters and len(word) > 4:
                    objects.append(word.rstrip())
            # Write the sentences to the "sentences" file, by picking words at random indexes of the lists and adding spaces
            for i in range(num):
                sentences.write(subjects[random.randrange(0, len(subjects))] + " ")
                sentences.write(verbs[random.randrange(0, len(verbs))] + " ")
                sentences.write(adjectives[random.randrange(0, len(adjectives))] + " ")
                sentences.write(objects[random.randrange(0, len(objects))] + "\n")

number = input("How many sentences do you want? ")
write_sentences(int(number))
