"""
Project 3 Text Miner Assignment
"""

import math

def get_lines(filename):
    """
    Read all lines from `filename` and return a list of strings,
    one per line, with whitespace stripped from the ends.

    >>> lines_list = get_lines("Macbeth.txt")
    >>> print(lines_list[0:2])
    ['Tomorrow, and tomorrow, and tomorrow,', 'Creeps in this petty pace from day to day,']
    """
    lines = []
    with open(filename) as fp:
        for line in fp:
            # Remove whitespace (or do whatever other processing you like)
            processed_line = line.strip()
            lines.append(processed_line)
    return lines



def get_words(lines_list):
    """
    Takes in lines_list and returns a list of strings as words,
    with whitespace and punctuation stripped from the ends.

    >>> words_list = get_words(get_lines("Macbeth.txt"))
    >>> print(words_list[4:14])
    ['tomorrow', 'creeps', 'in', 'this', 'petty', 'pace', 'from', 'day', 'to', 'day']
    """
    words_list = []
    for line in lines_list:
        line = line + " "
        processed_line = line.strip('#$%&()*+-/:;""''<=>@[\]^_`{|}~')
        i = 0
        j = 0
        while i < len(processed_line):
            if processed_line[i] == " ":
                word = processed_line[j:i]
                word = word.strip('!#$%&()*+,-./:;""''<=>?@[\]^_`{|}~ ')
                word = word.lower()
                if word != "":
                    words_list.append(word)
                    j = i
                i += 1
            else:
                i += 1
    return words_list



# Run this code when called from the command line
if __name__ == "__main__":
    import doctest


    # Test get_words helper function
    # words_list = get_words(get_lines("Macbeth.txt"))
    # print(words_list)


    # Run all doctests in this file
    doctest.testmod()
