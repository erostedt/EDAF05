import sys

matrix = []
letter_key = []
sequences = []
sigma = -4


def parse():
    """
    Reads the file of weights and input and converts into different lists and matrices. Returns the words that will be changed.
    :return: list of words, two on each line
    """
    for x in range(26):
        letter_key.append(0)
    lines = open("data//secret//2med.in", "r")  # sys.stdin.readlines()
    first_line = (lines.readline()).split()

    for letter in range(len(first_line)):
        letter_key[ord(first_line[letter]) - 65] = letter

    for row in lines:
        matrix.append(row.split())

    for row in range(len(matrix) - 1, 0, -1):
        sequences.append(matrix[row])
        if (len(matrix[row]) == 1):
            break

    sequences.pop(-1)
    for line in range(len(sequences)):
        sequences[line] = [list(sequences[line][0]), list(sequences[line][1])]

    return sequences


def change_cost(letter1, letter2):
    """
    Finds the cost of replacing one letter with another using the weight matrix.
    :input 1: letter one
    :input 2: letter two
    :return: cost of replacing the first letter with the second
    """
    return int(matrix[letter_key[ord(letter1) - 65]][letter_key[ord(letter2) - 65]])


def init_solve(input_words):
    """
    Initializes the matching process.
    :input: list of sequences, two sequences per line in the list
    :return: The matched lists
    """
    final_answer=[]
    input_words=input_words[::-1]
    for line in input_words:
        final_answer.append(solve("".join(line[0]), "".join(line[1])))
    return final_answer


def solve(word1, word2):
    """
    Matches two sequences together, creating an "opt" matrix. This matrix is then sent to the "backtrack" function.
    :input 1: Sequence one
    :input 2: Sequence two
    :return: The two words, with changed letters and/or inserted "*" signs.
    """
    n = len(word2)
    m = len(word1)

    opt = [[0 for i in range(n + 1)] for j in range(m + 1)]

    for i in range(1, m + 1):
        opt[i][0] = sigma * i
    for j in range(1, n + 1):
        opt[0][j] = sigma * j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            opt[i][j] = max(opt[i - 1][j - 1] + change_cost(word1[i - 1], word2[j - 1]), opt[i - 1][j] + sigma,
                            opt[i][j - 1] + sigma)

    return backtrack(word1, word2, opt)


def backtrack(word1, word2, opt):
    """
    Finds the actual sequences from the opt matrix.
    :input 1: Word one
    :input 2: Word two
    :input 3: The opt matrix
    :return: The matched sequences
    """
    j = len(word2)
    i = len(word1)

    string1 = ""
    string2 = ""

    while not (i == 0 or j == 0):
        largest = max(opt[i - 1][j - 1]+change_cost(word1[i - 1], word2[j - 1]), opt[i - 1][j]+sigma, opt[i][j - 1]+sigma)

        diag = opt[i - 1][j - 1]+change_cost(word1[i - 1], word2[j - 1])
        firstmove = opt[i - 1][j]+sigma
        secondmove = opt[i][j - 1]+sigma

        if largest == diag:
            string1 = string1 + (word1[i - 1])
            string2 = string2 + (word2[j - 1])
            i = i - 1
            j = j - 1

        if largest == firstmove:
            string1 = string1 + (word1[i - 1])
            string2 = string2 + "*"
            i = i - 1

        if largest == secondmove:
            string2 = string2 + (word2[j - 1])
            string1 = string1 + ("*")
            j = j - 1

    return(string1[::-1], string2[::-1])


parse()
print(init_solve(sequences))
