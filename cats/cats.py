"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    # END PROBLEM 1
    pointer=0
    for item in paragraphs:
        if select(item)==True and pointer==k:
            return item
        elif select(item)==True:
            pointer+=1

    return ''


def about(subject):
    """Return a select function that returns whether
    a paragraph contains one of the words in SUBJECT.

    Arguments:
        subject: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in subject]), 'subjects should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"

    def inner(s):
        finale=split(lower(remove_punctuation(s)))
        for i in subject:
            for j in finale:
                if i==j:
                    return True
        return False

    return inner
    # END PROBLEM 2


def accuracy(typed, source):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of SOURCE that was typed.

    Arguments:
        typed: a string that may contain typos
        source: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    source_words = split(source)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    accuracy_count=0

    if len(typed_words)==0 and len(source_words)==0:
        return 100.0
    
    if len(typed_words)==0 and len(source_words)!=0:
        return 0.0
    
    if len(typed_words)!=0 and len(source_words)==0:
        return 0.0
    
    if len(typed_words)<=len(source_words):
        for i in range(0, len(typed_words)):
            if typed_words[i]==source_words[i]:
                accuracy_count+=1
        
        percent=accuracy_count/len(typed_words)

    elif len(typed_words)>len(source_words):
        for i in range(0, len(source_words)):
            if typed_words[i]==source_words[i]:
                accuracy_count+=1
        
        percent=accuracy_count/len(typed_words)
    
    return percent*100.0

    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    # END PROBLEM 4
    return len(typed)/5/(elapsed/60)


############
# Phase 2A #
############


def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD. If multiple words are tied for the smallest difference,
    return the one that appears closest to the front of WORD_LIST. If the
    difference is greater than LIMIT, instead return TYPED_WORD.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing source words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    for i in word_list:
        if typed_word==i:
            return typed_word
        
    smallest_gap=10000
    smallest_index=0

    for i in range(0, len(word_list)):
        if diff_function(typed_word, word_list[i], limit)<smallest_gap:
            smallest_gap=diff_function(typed_word, word_list[i], limit)
            smallest_index=i
    
    if smallest_gap<=limit:
        return word_list[smallest_index]
    else:
        return typed_word
        
    
    # END PROBLEM 5


def feline_fixes(typed, source, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create SOURCE, then adds the difference in
    their lengths and returns the result.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> feline_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> feline_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> feline_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> feline_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> feline_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    if limit==0 and typed!=source:
        return 1
    
    if len(typed)==0 or len(source)==0:
        if limit-abs(len(typed)-len(source))>=0:
            return abs(len(typed)-len(source))
        else:
            return abs(len(typed)-len(source))+1
    
    if typed[0]!=source[0]:
            return 1+feline_fixes(typed[1:], source[1:], limit-1)
        
    return feline_fixes(typed[1:], source[1:], limit)
        
    


    

    


    
    '''out_limit=limit+1
    passin_limit=limit
    def inner(typed, source, limit):

        if limit-1==0 and passin_limit!=1 and passin_limit!=2 and passin_limit!=3:
            return out_limit

        if len(typed)==0 or len(source)==0:
            if limit-abs(len(typed)-len(source))>=0:
                return abs(len(typed)-len(source))
            else:
                return out_limit

        if typed[0]!=source[0]:
            return 1+inner(typed[1:], source[1:], limit-1)
        
        return inner(typed[1:], source[1:], limit)
    
    value=inner(typed, source, limit)

    return value'''

    # END PROBLEM 6


############
# Phase 2B #
############


def minimum_mewtations(typed, source, limit):
    """A diff function that computes the edit distance from TYPED to SOURCE.
    This function takes in a string TYPED, a string SOURCE, and a number LIMIT.
    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of edits
    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    if typed!=source and limit==0: # Base cases should go here, you may add more base cases as needed.
        # BEGIN
        "*** YOUR CODE HERE ***"
        return 1
    
    if typed==source:
        return 0
    
    if len(typed)==0 or len(source)==0:
        return abs(len(typed)-len(source))
        # END
    
    # Recursive cases should go below here
    if typed[0]==source[0]: # Feel free to remove or add additional cases
        # BEGIN
        "*** YOUR CODE HERE ***"
        return minimum_mewtations(typed[1:], source[1:], limit)
        # END
    else:
        add = 1+minimum_mewtations(typed, source[1:], limit-1)
        remove = 1+minimum_mewtations(typed[1:], source, limit-1)
        substitute = 1+minimum_mewtations(typed[1:], source[1:], limit-1)

        return min(add, remove, substitute)
        # BEGIN
        "*** YOUR CODE HERE ***"
        # END


def final_diff(typed, source, limit):
    """A diff function that takes in a string TYPED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function.'

FINAL_DIFF_LIMIT = 6 # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(typed, source, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        typed: a list of the words typed so far
        source: a list of the words in the typing source
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> source = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, source, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], source, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    accuracy_count=0

    typed_words=typed
    source_words=source
    
    if len(typed_words)==0 and len(source_words)==0:
        percent=1.0
        dict={'id': user_id, 'progress': percent}
        upload(dict)
        return 1.0
    
    if len(typed_words)==0 and len(source_words)!=0:
        percent=0.0
        dict={'id': user_id, 'progress': percent}
        upload(dict)
        return 0.0
    
    if len(typed_words)!=0 and len(source_words)==0:
        percent=0.0
        dict={'id': user_id, 'progress': percent}
        upload(dict)
        return 0.0
    
    for i in range(0, len(typed_words)):
        if typed_words[i]==source_words[i]:
            accuracy_count+=1
        else:
            percent=accuracy_count/len(source_words)
            dict={'id': user_id, 'progress': percent}
            upload(dict)
            return percent
        
    
        
    
    percent=accuracy_count/len(source_words)
    dict={'id': user_id, 'progress': percent}
    upload(dict)
    return percent
        
   
    # END PROBLEM 8


def time_per_word(words, timestamps_per_player):
    """Given timing data, return a match data abstraction, which contains a
    list of words and the amount of time each player took to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        timestamps_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> get_all_words(match)
    ['collar', 'plush', 'blush', 'repute']
    >>> get_all_times(match)
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    total=[[]]

    for i in range(0, len(timestamps_per_player)):
        subtotal=[]
        for j in range(0, len(timestamps_per_player[i])-1):
            diff=timestamps_per_player[i][j+1]-timestamps_per_player[i][j]
            subtotal+=[diff]
        total+=[subtotal]
    
    total.pop(0)
    
    

    return match(words, total)
    # END PROBLEM 9


def fastest_words(match):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        match: a match data abstraction as returned by time_per_word.

    >>> p0 = [5, 1, 3] 
    >>> p1 = [4, 1, 6]
        p3 = [3, 4, 3]
        p4 = [1, 1, 1]
just               have         fun
[5, 4, 3, 1], [1, 1, 4, 1], [3, 6, 3, 1]
 p0 p1 p2 p3
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """ # contains an *index* for each player
       # contains an *index* for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"

    time_for_all=get_all_times(match)
    words_for_all=get_all_words(match)
    
    def reverselist(list):
        new=[[]]

        for i in range(0, len(time_for_all[0])):
            subtotal=[]
            for j in range(0, len(time_for_all)):
                subtotal+=[time_for_all[j][i]]
            
            new+=[subtotal]
        del new[0]
        return new

    new=[[] for x in range(len(get_all_times(match)))]

    list=reverselist(time_for_all)

    for i in range(0, len(list)):
        for j in range(0, len(list[0])):
            if min(list[i])==list[i][j]:
                new[j]=new[j]+[words_for_all[i]]
                break
    return new

      


    '''time_for_all=get_all_times(match)

    words_for_all=get_all_words(match)
    
    def reverselist(list):
        new=[[]]

        for i in range(0, len(time_for_all[0])):
            subtotal=[]
            for j in range(0, len(time_for_all)):
                subtotal+=[time_for_all[j][i]]
            
            new+=[subtotal]
        
        return new.pop(0)
    
    list=reverselist(time_for_all)

    strongest_at_each_word=[]

    for i in range(0, len(list)):
        fixeddex=0
        index=0
        for j in range(0, len(list[0])-1):
            if list[i][fixeddex]>list[i][j+1]:
                index+=1
                fixeddex+=1
        strongest_at_each_word+=[index]
    
    new=[[]]
    for i in range(0, len(strongest_at_each_word)+1):
        subtotal=[]
        if i in strongest_at_each_word:
            for j in range(0, len(strongest_at_each_word)):
                if strongest_at_each_word[j]==i:
                    subtotal+=[words_for_all[j]]
        new+=[subtotal]

    return new.pop(0)'''




    
        




            
            




    
        



    

    # END PROBLEM 10


def match(words, times):
    """A data abstraction containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return {"words": words, "times": times}


def get_word(match, word_index):
    """A utility function that gets the word with index word_index"""
    assert 0 <= word_index < len(get_all_words(match)), "word_index out of range of words"
    return get_all_words(match)[word_index]


def time(match, player_num, word_index):
    """A utility function for the time it took player_num to type the word at word_index"""
    assert word_index < len(get_all_words(match)), "word_index out of range of words"
    assert player_num < len(get_all_times(match)), "player_num out of range of players"
    return get_all_times(match)[player_num][word_index]

def get_all_words(match):
    """A selector function for all the words in the match"""
    return match["words"]

def get_all_times(match):
    """A selector function for all typing times for all players"""
    return match["times"]


def match_string(match):
    """A helper function that takes in a match data abstraction and returns a string representation of it"""
    return f"match({get_all_words(match)}, {get_all_times(match)})"

enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(source)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, source))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)