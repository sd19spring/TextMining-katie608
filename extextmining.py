"""
Example class for downloading and storing text files.

Uses a local file cache to avoid repeatedly downloading

>>> moby = Text("http://www.gutenberg.org/files/2701/2701-0.txt") # doctest: +ELLIPSIS
INFO: 'http://www.gutenberg.org/files/2701/2701-0.txt' found in ...
>>> print(moby.text[27802:27818])
Call me Ishmael.
"""

# In your code you can try using a database or pickle instead of saving files
# This example does not do any processing or cleaning on the text data
# (but you should)

import os
import requests
import sys
import time

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


def run_example():
    """
    Return a dictionary with key: book title, value: Text objects for books.
    """
    import time

    urls = { "MLK": "https://www.americanrhetoric.com/speeches/mlkihaveadream.htm",
             "JFK": "https://www.americanrhetoric.com/speeches/jfkinaugural.htm",
             "FDR": "https://www.americanrhetoric.com/speeches/fdrfirstinaugural.html"
           }

    texts = {}
    for title, url in urls.items():
        t = Text(url)
        texts[title] = t

    return texts


if __name__ == '__main__':
    #import doctest
    #doctest.testmod()

    from pprint import pprint   # "Pretty-print" dictionary
    books = run_example()
    pprint(books)
    #for title, book in books.items():
    #    print(book.text[2000:2010])import sys
