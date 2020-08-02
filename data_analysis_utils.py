from collections import Counter
import string
import re

import nltk
from nltk.corpus import stopwords
from nltk.collocations import *

ENGLISH_STOPWORDS = stopwords.words('english')
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

def get_comments_from_obj(post_id, comments):
    if post_id in comments:
        return comments[post_id]
    else:
        return None

def giant_cleaned_string(series_of_list_of_comments):
    """Return string from Pandas Series of lists of strings.
    
    Combines multiple pandas rows with lists of strings into one giant string with URLs and punctuation removed.
    """
    comment_string = ' '.join(series_of_list_of_comments.apply(lambda x: ' '.join(x.split())))
    comment_string = re.sub('http://\S+|https://\S+', '', comment_string)

    chars_to_replace = string.punctuation[:6]+string.punctuation[7:]+'“”\n' # Don't remove single quotation mark
    whitespace_to_replace_with = len(chars_to_replace) * ' '

    comment_string = comment_string.lower().translate(str.maketrans(chars_to_replace, whitespace_to_replace_with))
    return comment_string

def acceptable_token(token):
    """ Return True if token is longer than one character and is not present in ENGLISH_STOPWORDS
    """
    return (len(token) > 1 and token not in ENGLISH_STOPWORDS)

def tokenize(giant_comment_string):
    """ Return list of word tokens from given string.
    """
    tokens = giant_comment_string.split(' ')
    return list(filter(acceptable_token, tokens))

def create_counter_object(giant_comment_string):
    """ Return Counter with word counters for given string.
    """
    word_counter = Counter(tokenize(giant_comment_string))
    return word_counter

def top_adjectives(giant_comment_string, num_of_words=10):
    """ Return list with most common adjectives in given string.
    """

    def find_adjectives(list_of_word_pos_tuple):
        return list_of_word_pos_tuple[1] == 'JJ'

    comment_words_POS = nltk.pos_tag(tokenize(giant_comment_string))
    comment_adj_counter = Counter([adj[0] for adj in list(filter(find_adjectives, comment_words_POS))])
    return comment_adj_counter.most_common(num_of_words)

# TODO: Determine association metric to use
# http://www.nltk.org/_modules/nltk/metrics/association.html
def top_ngrams(giant_comment_string, top_n=15, ngram=2):
    """ Return top-n sized list with most frequently appearing n-grams in given string.
    """

    if ngram == 2:
        finder = BigramCollocationFinder.from_words(tokenize(giant_comment_string))
        return finder.nbest(bigram_measures.likelihood_ratio, top_n)
    elif ngram == 3:
        finder = TrigramCollocationFinder.from_words(tokenize(giant_comment_string))
        return finder.nbest(trigram_measures.likelihood_ratio, top_n)
    else:
        return "Error: Only bi- and trigrams supported."