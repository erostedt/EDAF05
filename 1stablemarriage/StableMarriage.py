import sys


def load_file():
    """
    Loads input file and converts it to two lists of women and men.
    :return: One list of women and one list of men.
    """
    #x = input('Directory and file to read from: ')

    lines = sys.stdin.readlines()
    #lines = open(x, 'r')
    lines = [line.strip() for line in lines]

    for x in range(len(lines)):
        lines[x] = lines[x].ljust(len(lines[x]) + 1, ' ')

    # removes first number (number of pairs)
    nbr_women = int(lines.pop(0))
    lines = ''.join(lines)

    lines = lines.split()
    persons = []

    for x in range(nbr_women * 2):
        persons.append(lines[x * (nbr_women + 1):x * (nbr_women + 1) + nbr_women + 1])

    persons = [list(map(int, person)) for person in persons]
    persons = sort_people(persons)

    men = persons[1::2]
    women_ineffective = persons[::2]
    women = []
    
    for i, person in enumerate(women_ineffective):
        women.append(invert_list(person, nbr_women))

    for line in women:
        line.insert(0, 0)

    return women, men


def invert_list(person, nbr_person):
    pref_list = [0]*nbr_person
    for i, pref in enumerate(person[1:], start=1):
        pref_list[pref-1] = i
    return [person[0]] + pref_list


def sort_people(unsorted_list):
    """
    Bundles all men and all women together.
    :param unsorted_list: File containing unsorted people.
    :return: Sorted list.
    """

    return_list = sorted(unsorted_list, key=lambda x: x[0])

    return return_list


def prefers_new_man(w, m):
    """
    Checks if woman w prefers a new man m over her current man.
    :param w: Woman w.
    :param m: Man m.
    :return: True if woman prefers new man, False else.
    """
    curr_man = w[0]
    new_man = m[0]
    w_preflist = w[2:]
    if w_preflist[new_man-1] < w_preflist[curr_man-1]:
        return True
    else:
        return False


def get_old_man(w, pairs):
    """
    Finds woman w's current man (not just name/index but also preference list).
    :param w: Woman w.
    :param pairs: list of all current pairs.
    :return: Old man with preference list.
    """
    for pair in pairs:
        if w in pair:
            return pair[1]


def final_pairs(pairs):
    """
    Transforms the pairs list with preferences to a pairs list with only names/indicies.
    Sorted after women, i.e final pairs = [(1, a), (2, b) ...]
    :param pairs: All pairs (as list of lists)
    """
    final_pairs = []
    for pair in pairs:
        w = pair[0]
        m = pair[1]
        final_pairs.append((w[1], m[0]))
    return sorted(final_pairs, key=lambda pair: pair[0])


def get_single_women(W):
    """
    Returns all girls that do not have a partner.
    :param W: Women W.
    :return: All the single women
    """
    return [w[1] for w in W if w[0] == 0]


def output(pairs):
    """
    Prints out the man associated with woman with number i at i:th position
    :param pairs: Sorted pairs.
    """
    for pair in pairs:
        print(pair[1])


def GS(W, M):
    """
    Finds stable match between Women and Men (stored as list of lists).

    Storage info:
    Women
    A specific woman w has her information stored as following:
    index 0 holds the number of her man (0 if she is single).
    index 1 holds her own number.
    index 2- holds her preference list.

    Men
    A specific man m has his information stored as following:
    index 0 holds his own number.
    index 1- holds his preference list.

    :param W: Women W sorted by their own number.
    :param M: Men M sorted by their own number.
    :return pairs, women_no_partner, men_no_partner: Stable pairs, women who did not find a partner, men who did not find partner.
    """
    pairs = []
    men_no_partner = []
    while M:
        m = M[0]
        del M[0]
        # Due to indexing for the people starts as 1 but python starts list at 0 we need to shift by one.
        w = W[m[1] - 1]
        del m[1]
        if w[0] == 0:
            pairs.append((w, m))
            w[0] = m[0]
        elif prefers_new_man(w, m):
            old_man = get_old_man(w, pairs)
            pairs.remove((w, old_man))
            pairs.append((w, m))
            M.append(old_man)
            w[0] = m[0]
        else:
            M.append(m)
    women_no_partner = get_single_women(W)
    pairs = final_pairs(pairs)
    return pairs, women_no_partner, men_no_partner


if __name__ == '__main__':
    W, M = load_file()
    pairs, _, _ = GS(W, M)
    output(pairs)
