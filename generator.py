import random

def construct_sentence(words):
    # Sample sentence structures
    sentence_structures = [
        "{subject} {verb} {object}.",
        "{subject} {verb} the {object}.",
        "The {object} was {verb} by the {subject}.",
        "{subject} quickly {verb} the {object}.",
        "Did the {subject} {verb} the {object}?",
    ]

    # Basic lists of subjects, verbs, and objects for sentence creation
    subjects = ["dog", "cat", "child", "teacher", "doctor", "bird", "robot"]
    verbs = ["saw", "liked", "ate", "played with", "found", "fixed"]
    objects = ["apple", "ball", "car", "computer", "garden", "book"]

    # Match words with categories
    word_mapping = {"subject": [], "verb": [], "object": []}
    for word in words:
        if word in subjects:
            word_mapping["subject"].append(word)
        elif word in verbs:
            word_mapping["verb"].append(word)
        elif word in objects:
            word_mapping["object"].append(word)
    

    #A feedback if no valid words are found
    if not any(word_mapping.values()):
        return "No valid words provided."
    
    # Pick one of each if available or default to random selection
    subject = random.choice(word_mapping["subject"] or subjects)
    verb = random.choice(word_mapping["verb"] or verbs)
    object_ = random.choice(word_mapping["object"] or objects)

    # Construct sentence from random structure
    sentence_structure = random.choice(sentence_structures)
    sentence = sentence_structure.format(subject=subject, verb=verb, object=object_)
    return sentence.capitalize()

# Example usage
random_words = ["dog", "played with", "ball"]
sentence = construct_sentence(random_words)
print(sentence)
