import pickle
import os

# Define the Levenshtein distance function
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

# Define the spell check function
def spell_check(input_name):
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the file path
        file_path = os.path.join(current_dir, 'words.pickle')

        # Load Tamil words from pickle file
        with open(file_path, 'rb') as tamil_words_file:
            tamil_words = pickle.load(tamil_words_file)
    except FileNotFoundError:
        print(f"File '{file_path}' not found")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    threshold = 4
    closest_word = None
    min_distance = threshold
    for word in tamil_words:
        distance = levenshtein_distance(input_name, word)
        if distance < min_distance:
            min_distance = distance
            closest_word = word

    print(closest_word if closest_word else "No close match found")

if __name__ == '_main_':
    find_closest_word = input("Enter the word to check: ")
    spell_check(find_closest_word)