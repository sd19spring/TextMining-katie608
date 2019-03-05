"""
Project 3 Text Miner Assignment
Ideas
-Compare text from the 1500s on every 50 years and look at word freqency
    -"translate" something from one era's dialect to another's? If possible
-compare certain works or famous speeches to different reading levels examples
-different dialects of english, maybe different parts of US
-famous speeches and what made them great? Make something like a famous speech from that?
-company mottos or their very vauge descriptions
-famous speeches and find most commonly repeated phrases and how often
 they are repeated vs non-famous speeches?
 https://www.americanrhetoric.com/top100speechesall.html
 https://www.americanrhetoric.com/speechbankm-r.htm
 https://www.bartleby.com/268/
 http://www.historyplace.com/speeches/previous.htm
"""
import math
import os
import requests
import sys
import time

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

def strip_scheme(url):
    """
    Return 'url' without scheme part (e.g. "http://")

    >>> strip_scheme("https://www.example.com")
    'www.example.com'
    >>> strip_scheme("http://www.gutenberg.org/files/2701/2701-0.txt")
    'www.gutenberg.org/files/2701/2701-0.txt'
    """
    # TODO: This ad-hoc implementation is fairly fragile
    # and doesn't support e.g. URL parameters (e.g. ?sort=reverse&lang=fr)
    # For a more robust implementation, consider using
    # https://docs.python.org/3/library/urllib.parse.html
    scheme, remainder = url.split("://")
    return remainder

class Text:
    """
    Text class holds text-based information downloaded from the web
    It uses local file caching to avoid downloading a given file multiple times,
    even across multiple runs of the programself.
    """
    def __init__(self, url, file_cache=os.path.join(sys.path[0], "cache")):
        """
        Given 'url' of a text file, create a new instance with the
        text attribute set by either downloading the URL or retrieving
        it from local text cache.

        Optional 'file_cache' argument specifies where text cache should be
        stored (default: same directory as the script in a "cache" folder)
        """
        self.url = url
        self.local_fn = os.path.join(file_cache, strip_scheme(url))

        # First see if file is already in local file cache
        if self.is_cached():
            print("INFO: {url!r} found in local file cache, reading".format(url=self.url))
            self.read_cache()

        # If not found, download (and write to local file cache)
        else:
            print("INFO: {url!r} not found in local file cache, downloading".format(url=self.url))
            self.download()
            self.write_cache()

    def __repr__(self):
        return "Text({url!r})".format(url=self.url)

    def is_cached(self):
        """Return True if file is already in local file cache"""
        return os.path.exists(self.local_fn)

    def download(self):
        """Download URL and save to .text attribute"""
        self.text = requests.get(self.url).text     # TODO: Exception handling
        # Wait 2 seconds to avoid stressing data source and rate-limiting
        # You don't need to do this here (only has to happen between requests),
        # but you should have it somewhere in your code
        time.sleep(2)

    def write_cache(self):
        """Save current .text attribute to text cache"""
        # Create directory if it doesn't exist
        directory = os.path.dirname(self.local_fn)
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Write text to local file cache
        with open(self.local_fn, 'w') as fp:
            fp.write(self.text)

    def read_cache(self):
        """Read from text cache (file must exist) and save to .text attribute"""
        with open(self.local_fn, 'r') as fp:
            self.text = fp.read()


# Run this code when called from the command line
if __name__ == "__main__":
    import doctest

    # Test get_words helper function
    # words_list = get_words(get_lines("Macbeth.txt"))
    # print(words_list)

    # Run all doctests in this file
    doctest.testmod()
