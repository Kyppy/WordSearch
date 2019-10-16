"""
This script was written by Kyppy Ngaira Simani and completed on October 3rd, 2019

PROBLEM STATEMENT:
Given a dictionary and a file containing a list of input words, write a
program that can generate all the words that can be formed using a subset of
characters from each input word.
"""

import collections
import itertools
import os
import time
import urllib.request


class Trie:
    """
    This class emulates the parent-child node structure of a trie
    """

    root = {}

    def add(self, word):
        """
        Creates a new chain of parent-child string nodes using nested dicts

        arguments:
            word(str): string of characters to add as nodes to trie

        returns:
            None
        """

        current_node = self.root
        for char in word:
            if char not in current_node:
                current_node[char] = {}
            current_node = current_node[char]

        # * denotes the trie has this word as an item
        # if * doesn't exist, trie doesn't have this word but is a path to longer word
        current_node['*'] = True

    def search(self, search_word):
        """
        Iterates through the characters of 'search_word' and the trie nodes
        and confirms if the given search word exists in the trie/dictionary

        arguments:
            search_word(str): word to search through the trie for

        returns:
            Boolean
        """

        current_node = self.root
        for char in search_word:
            if char not in current_node:
                return False
            current_node = current_node[char]

        if '*' in current_node:
            return True
        else:
            return False


def str_match(search_str, base_str):
    """
    Evaluates the set of characters in 'search_str' and 'base_str'
    to determine if the  characters in 'search_str' are a subset of characters in 'base_str'

    arguments:
        search_str(str): string of characters to compare against 'base_str'
        base_str(str): string of characters that 'search_str' is compared against

    returns:
        Boolean
    """

    # create a multiset-like dict of character counters from each string.
    search_set = collections.Counter(search_str)
    base_set = collections.Counter(base_str)

    # subtracts the 'base_set' character count from the 'search_set'.
    # 'search_str' is a subset of 'base_str' if the result of the subtraction
    # reduces all character counts in 'search_set' to at least zero
    search_set.subtract(base_set)
    result = list(search_set.elements())
    if any(result):
        return False
    else:
        return True


def word_search(dict_source, search_item):
    """
    Generates all the words that can be formed using a subset of
    characters from the input word and a given dictionary/list of acceptable words

    arguments:
        dict_source(str): name of the .txt file in the CWD to be used as reference dictionary
        search_item(str): input string used to generate character subset

    returns:
        results(list): list of acceptable words
    """

    results = []

    # strings longer than 9 characters cause unfeasible permutation calculation times
    # a relatively time-efficient alternative is used for strings greater than 9 characters
    if len(search_item) <= 9:
        for i in range(1, len(search_item) + 1):
            word_perm = itertools.permutations(search_item, i)
            words = (''.join(perm) for perm in word_perm)

            for my_word in words:
                if dictionary.search(my_word):
                    results.append(my_word)

        # eliminate duplicate strings by creating a dict
        # then invoke dict back into a list
        results = list(dict.fromkeys(results))
        return results
    else:
        with open(dict_source, 'r') as reader:
            for word in reader.read().splitlines():
                if len(word) > len(search_item):
                    continue
                else:
                    match = str_match(word, search_item)
                    if match:
                        results.append(word)
            return results


def download_dictionary(dict_url, dict_name):
    """
    Downloads a .txt file with the name 'dict_name'
    from the 'dict_url' into the CWD of this script.

    arguments:
        dict_url(str): a url that points to a .txt file
        dict_name(str): name assigned to the .txt file

    returns:
        filename(str): name of the .txt file as seen in the cwd
    """

    url = dict_url
    dir_path = os.getcwd()
    filename = '{}.txt'.format(dict_name)
    path = dir_path + '/{}'.format(filename)
    print("Beginning file download...")
    urllib.request.urlretrieve(url, path)
    print("Download of {} is complete".format(filename))
    return filename


start_time = time.time()

search_list = ['cat', 'dog', 'museum', 'photosynthesis', 'typewriter']
dictionary = Trie()

# NOTE: the following lines of code (145-150) may increase execution time only on the first run.
# It assumes the user does not already have a copy of the reference dictionary in their CWD.
# Subsequent runs will accurately reflect the execution time of the script.
url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'
dict_name = 'dictionary'
if not os.path.exists('{}.txt'.format(dict_name)):
    dict_source = download_dictionary(url, dict_name)
else:
    dict_source = '{}.txt'.format(dict_name)

with open(dict_source, 'r') as reader:
    for word in reader.read().splitlines():
        dictionary.add(word)

for item in search_list:
    print(word_search(dict_source, item))

print("Script execution time is: {:.4} seconds".format((time.time() - start_time)))





