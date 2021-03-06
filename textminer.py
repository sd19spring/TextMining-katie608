"""
Project 3 Text Miner Assignment
Katie Foster

Source for speeches:
https://www.americanrhetoric.com/top100speechesall.html
"""
import math
import os
import requests
import sys
import time
import urllib.request
from bs4 import BeautifulSoup
import requests

url_list = ["https://www.americanrhetoric.com/speeches/mlkihaveadream.htm",
"https://www.americanrhetoric.com/speeches/jfkinaugural.htm",
"https://www.americanrhetoric.com/speeches/fdrpearlharbor.htm",
"https://www.americanrhetoric.com/speeches/barbarajordan1976dnc.html",
"https://www.americanrhetoric.com/speeches/richardnixoncheckers.html",
"https://www.americanrhetoric.com/speeches/ronaldreaganchallenger.htm",
"https://www.americanrhetoric.com/speeches/jfkhoustonministers.html",
"https://www.americanrhetoric.com/speeches/lbjweshallovercome.htm",
"https://www.americanrhetoric.com/speeches/mariocuomo1984dnc.htm",
"https://www.americanrhetoric.com/speeches/jessejackson1984dnc.htm",
"https://www.americanrhetoric.com/speeches/barbarajordanjudiciarystatement.htm",
"https://www.americanrhetoric.com/speeches/douglasmacarthurfarewelladdress.htm",
"https://www.americanrhetoric.com/speeches/mlkivebeentothemountaintop.htm",
"https://www.americanrhetoric.com/speeches/teddyrooseveltmuckrake.htm",
"https://www.americanrhetoric.com/speeches/rfkonmlkdeath.html",
"https://www.americanrhetoric.com/speeches/dwightdeisenhowerfarewell.html",
"https://www.americanrhetoric.com/speeches/wilsonwarmessage.htm",
"https://www.americanrhetoric.com/speeches/douglasmacarthurthayeraward.html",
"https://www.americanrhetoric.com/speeches/richardnixongreatsilentmajority.html",
"https://www.americanrhetoric.com/speeches/jfkberliner.html",
"https://www.americanrhetoric.com/speeches/cdarrowpleaformercy.htm",
"https://www.americanrhetoric.com/speeches/rconwellacresofdiamonds.htm",
"https://www.americanrhetoric.com/speeches/ronaldreaganatimeforchoosing.htm"
]

"""DOWNLOADING AND FORMATTING"""

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

def get_extracted_speech(url):
    """Takes in url, then downloads the html from the url and strips the html
    and creates a file with the extracted speech
    Not a fruitful function so no doctests possible
    """
    # Set file title to the shortened title from the html
    file_title = requests.get(url).text
    file_title = file_title.replace("American Rhetoric","")
    file_title = file_title.replace(": ","")
    print(file_title)

    html = BeautifulSoup(file_title, 'html.parser') # gets file from the url and sets it to html
    fout = open(os.path.join("cache", html.title.text), "w") # makes or opens a file with title of html

    # returns only the text with font Verdana or Droid Sans
    speech = html.find_all(face="Verdana")
    speech2 = html.find_all(face="Droid Sans")

    # Writes the text from the html to a file as plain text
    for line in speech:
        fout.write(line.text)
    for line in speech2:
        fout.write(line.text)
    fout.close()

def get_all_speeches(list):
    """Takes in a list of URLs and rus get_extracted_speech for each of them
    Not a fruitful function so no doctests possible
    """
    i = 0
    for url in url_list:
        get_extracted_speech(url_list[i])
        i+=1
        time.sleep(2)


"""ANALYSIS"""
def get_lines(filename):
    """
    Read all lines from `filename` and return a list of strings,
    one per line, with whitespace stripped from the ends.

    >>> lines_list = get_lines("Macbeth.txt")
    Macbeth.txt
    >>> print(lines_list[0:2])
    ['Tomorrow, and tomorrow, and tomorrow,', 'Creeps in this petty pace from day to day,']
    """
    print(filename)
    lines = []
    with open(filename) as fp:
        for line in fp:
            processed_line = line.strip()
            lines.append(processed_line)
    return lines

def get_words(lines_list):
    """
    Takes in lines_list and returns a list of strings as words,
    with whitespace and punctuation stripped from the ends.

    >>> words_list = get_words(get_lines("Macbeth.txt"))
    Macbeth.txt
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


def word_counter(words_list, num_entries):
    """Return a dictionary that counts occurrences of each word in words_list

    Examples:
    >>> word_counter(["word", "word", "notword"], 2)
    (('Number of different words used:', 2), ('Frequency:', [(2, 'word'), (1, 'notword')]))
    >>> word_counter(get_words(get_lines("Macbeth.txt")),4)
    Macbeth.txt
    (('Number of different words used:', 58), ('Frequency:', [(6, 'and'), (3, 'tomorrow'), (3, 'to'), (3, 'the')]))
    """
    d = dict()
    for word in words_list:
        d[word] = 1 + d.get(word,0)

    sorted_d = []
    for key, value in d.items():
        sorted_d.append((value, key))
    sorted_d.sort()
    sorted_d.reverse()
    return ("Number of different words used:",len(sorted_d)), ("Frequency:", sorted_d[0:num_entries])

def phrase_counter(words_list, num_entries):
    """Returns a dictionary that counts occurances of 2, 3 and 4 letter phrases in words_list
    >>> phrase_counter(get_words(get_lines("Macbeth.txt")),2)
    Macbeth.txt
    ('Frequency 2', [(2, 'tomorrow and'), (2, 'day to')], 'Frequency 3', [(2, 'tomorrow and tomorrow'), (1, 'yesterdays have lighted')], 'Freuquency 4', [(1, 'yesterdays have lighted fools'), (1, 'way to dusty death')])
    """
    phrase_list2 = []
    phrase_list3 = []
    phrase_list4 = []
    i = 0
    for i in range (len(words_list)-3): #subtracting 3 was not a great solution because it would exclude any 2 or 3 word phrases at the end of the doccument, but I could not think of a better way
        phrase_list2.append(words_list[i]+" "+words_list[i+1])
        phrase_list3.append(words_list[i]+" "+words_list[i+1]+" "+words_list[i+2])
        phrase_list4.append(words_list[i]+" "+words_list[i+1]+" "+words_list[i+2]+" "+words_list[i+3])

        d2 = dict()
        for phrase2 in phrase_list2:
            d2[phrase2] = 1 + d2.get(phrase2,0)

        d3 = dict()
        for phrase3 in phrase_list3:
            d3[phrase3] = 1 + d3.get(phrase3,0)

        d4 = dict()
        for phrase4 in phrase_list4:
            d4[phrase4] = 1 + d4.get(phrase4,0)

    sorted2 = sort_dictionary(d2, num_entries)
    sorted3 = sort_dictionary(d3, num_entries)
    sorted4 = sort_dictionary(d4, num_entries)
    return("Frequency 2", sorted2, "Frequency 3", sorted3, "Freuquency 4", sorted4)


def sort_dictionary(d, num_entries):
    """Sorts a dictionary and returns sorted dictionary as a list
    """
    sorted_d = []
    for key, value in d.items():
        sorted_d.append((value, key))
    sorted_d.sort()
    sorted_d.reverse()
    # return (len(sorted_d), sorted_d[0:num_entries])
    return sorted_d[0:num_entries]

def analyze_all_files(function, num_results):
    """Takes in an analysis function (like word counter) and performs it on all
    files in the cache directory
    Not a fruitful function so no doctest
    """
    fout = open("Final Results", "w")
    for speech_fn in os.listdir("cache"):
        analysis_list = []

        word_analysis = word_counter(get_words(get_lines(os.path.join("cache", speech_fn))), num_results)
        analysis_list.append(word_analysis)
        print(word_analysis)

        phrase_analysis = phrase_counter(get_words(get_lines(os.path.join("cache", speech_fn))), num_results)
        analysis_list.append(phrase_analysis)
        print(phrase_analysis)
        fout.write(str(speech_fn) +"\n"+ str(word_analysis) +"\n"+ str(phrase_analysis)+"\n \n")
    fout.close()


# Run this code when called from the command line
if __name__ == "__main__":
    import doctest

    # Uncomment this when you want to download all speeches from url list
    # get_all_speeches(url_list)

    # runs the entire analysis part of the program for all files in cache
    analyze_all_files(phrase_counter, 20)

    # Run all doctests in this file
    doctest.testmod()
