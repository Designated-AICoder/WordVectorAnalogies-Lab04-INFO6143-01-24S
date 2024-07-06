import numpy as np

# Global Variables
words = []
vectors = None
matches = ["" for _ in range(20)]
word_count = 0 # Total number of words in the dataset
dim_count = 0 # size of the word vectors

# Load the word list and set of vectors
def load_word_vectors(input_file):
    global words, vectors, word_count, dim_count
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # The first line of the file contains the number of words in the vocabulary and the size of the vectors
    # https://fasttext.cc/docs/en/english-vectors.html#format
    args = lines[0].split()
    word_count = int(args[0])
    dim_count = int(args[1])

    # Initialize the words and vectors lists
    words = [None] * word_count
    vectors = np.zeros((word_count, dim_count))

    # Load the words and vectors into the lists
    count = 0
    for line in lines[1:]:
        tokens = line.split()
        words[count] = tokens[0]
        vectors[count] = np.array(tokens[1:], dtype=float)
        count += 1

# Retrieve the 300 element float array for the designated word
def get_vect(word):
    if word in words:
        index = words.index(word)
        return vectors[index]
    return None

# Add or subtract the 2 vectors based on op
def add_vect(vec1, vec2, op):
    if op == 1:
        return vec1 + vec2
    else:
        return vec1 - vec2

# Adjust the "matches" string array based on the cosine similarity result
def match_vect(x, cos_sim):
    global matches
    s_cos_sim = str(cos_sim)
    d_cos_sim = 0.0

    for i in range(len(matches)):
        if matches[i] != "":
            args = matches[i].split('_')
            d_cos_sim = float(args[0])
        else:
            d_cos_sim = 0.0

        # If the cosine similarity is greater than the current value, replace it
        if cos_sim > d_cos_sim:
            matches[-1] = s_cos_sim + "_" + words[x]
            matches.sort(reverse=True)
            break

# Calculate the cosine similarity for the 2 vectors
def calculate_cosine_similarity(vecA, vecB):
    dot_product = np.dot(vecA, vecB)
    magnitude_of_A = np.linalg.norm(vecA)
    magnitude_of_B = np.linalg.norm(vecB)
    return dot_product / (magnitude_of_A * magnitude_of_B)

# Main function to process analogies
def find_analogies():
    print("Analogies take the form: A is to B as C is to D")
    print("Example: 'man is to woman as king is to queen'")
    print("Enter the previous example as: man woman king")
    print("The computer will return the full solution: man is to woman as king is to queen")

    while True:
        analogy = input("\nEnter 3 analogy word tokens: ").strip()
        analogy_args = analogy.split()

        if analogy == "":
            break

        if len(analogy_args) != 3:
            print("Must be 3 words, Please redo")
            continue

        print(f"Processing analogy... \n{analogy_args[0]} is to {analogy_args[1]} as {analogy_args[2]} is to ",end="")

        # Retrieve the vectors for the 3 input words
        vect1 = get_vect(analogy_args[0])
        vect2 = get_vect(analogy_args[1])
        vect3 = get_vect(analogy_args[2])

        if vect1 is None or vect2 is None or vect3 is None:
            print("One or more words not found in the dictionary.")
            continue

        vect4 = add_vect(vect2, vect1, -1)
        vect5 = add_vect(vect4, vect3, 1)

        vect6 = np.zeros(dim_count)

        for i in range(len(matches)):
            matches[i] = ""

        # Calculate the cosine similarity for all the words in the dictionary
        for i in range(word_count):
            vect6 = vectors[i]
            cos_similarity = calculate_cosine_similarity(vect5, vect6)
            match_vect(i, cos_similarity)

        # Print the best matching word
        for match in matches:
            argsM = match.split('_')
            found = False

            for arg in analogy_args:
                if arg == argsM[1]:
                    found = True

            if not found:
                print(argsM[1])
                print("\nDebug information (top similarities)")
                for m in matches[1:]:
                    print(m.replace("_", " "))
                break




input_file = 'c:\data\wiki-news-300d-1M.vec'
print("Loading Dictionary....")
load_word_vectors(input_file)
print("Dictionary Loaded....")
find_analogies()
