import sys
from collections import defaultdict


def parse():
    """
    Parses the input. We construct the penalty matrix and a dictionary where the keys are pairs of character 
    and the values are the corresponding value from the penalty matrix. Lastly we construct a list of queries
    which we shall use for testing.
    :return penalty_pairs: Dictionary with pairs of characters as keys and values from the penalty matrix.
    :return queries: List of queries (tuples) to be testd on.
    """
    lines = sys.stdin.readlines()
    
    lines = [line for line in lines]
    characters = lines.pop(0).strip().split()
    num_chars = len(characters)
    penalty_matrix = [list(map(int, line.rstrip().split())) for line in lines[:num_chars]]

    penalty_pairs = defaultdict(tuple)
    for i, char in enumerate(characters):
        for j, other_char in enumerate(characters):
            penalty_pairs[(char, other_char)] = penalty_matrix[i][j]

    # Skip num of queries, we use list slice instead.
    queries = [tuple(line.rstrip().split()) for line in lines[num_chars+1:]]
    
    return penalty_pairs, queries


def sequence_alignment(string_1, string_2, penalty_pairs, gap_penalty):
    """
    Construct dynamic programming matrix and then constructs two strings that are aligned. 

    :param string_1: First string to align with second.
    :param string_2: Second string to align with first.
    :param penalty_pairs: Dictionary with tuple of chars as keys and penalty value as value.
    :param gap_penalty: Penalty if character is missing.
    :return new_string_1: String one aligned with second.
    :return new_string_2: String two aligned with first.
    """

    # Construction of dynamic programming matrix.
    m, n = len(string_1), len(string_2)
    dp = [ [0 for _ in range(n+1)] for _ in range(m+1)]

    for i in range(m+1):
        dp[i][0] = i * gap_penalty

    for j in range(n+1):
        dp[0][j] = j * gap_penalty

    for i, char in enumerate(string_1, start=1):
        for j, other_char in enumerate(string_2, start=1):

            dp[i][j] = max(penalty_pairs[(char, other_char)] + dp[i-1][j-1], \
                                gap_penalty + dp[i][j-1], \
                                gap_penalty + dp[i-1][j])

    # Construction of aligned strings
    align = []
    i, j = m, n
    while i > 0 and j > 0:
    
        if dp[i][j] == penalty_pairs[(string_1[i-1], string_2[j-1])] + dp[i-1][j-1]:
            align.append( (string_1[i-1], string_2[j-1]) )
            i, j = i - 1, j - 1

        elif dp[i][j] == gap_penalty + dp[i-1][j]:
            align.append( (string_1[i-1], '*') )
            i -= 1
        

        else:
            align.append( ('*', string_2[j-1]) )
            j -= 1
            
            
    while i > 0:
        align.append( (string_1[i-1], '*') )
        i -= 1

    while j > 0:
        align.append( ('*', string_2[j-1]) )
        j -= 1
       
    
    align.reverse()
    new_string_1, new_string_2 = '', ''
    for a, b in align:
        new_string_1 += a
        new_string_2 += b

    return new_string_1, new_string_2


if __name__ == "__main__":
    penalty_pairs, queries = parse()
    for querie in queries:
        string_1, string_2 = sequence_alignment(querie[0], querie[1], penalty_pairs, -4)
        print(string_1 + " " + string_2)