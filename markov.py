#Bennett Summy / 261016707
import doctest
import random

def get_grams(text, k):
    ''' (string, int) -> dict
    Takes string text and positive integer k to return a dictionary of k grams (with values being the
    number of times a trailing character occurs the k-gram).
    
    >>> get_grams('lobwobdob', 2)
    {'lo': {'b': 1}, 'ob': {'w': 1, 'd': 1}, 'bw': {'o': 1}, 'wo': {'b': 1}, 'bd': {'o': 1}, 'do': {'b': 1}}
    
    >>> get_grams("LOL", 1)
    {'L': {'O': 1}, 'O': {'L': 1}}
    
    >>> get_grams("hello", 2)
    {'he': {'l': 1}, 'el': {'l': 1}, 'll': {'o': 1}}
    
    >>> get_grams("hello", 6)
    {}
    '''
    grams_dict = {}
    
    for index in range(len(text) - 1):
        if not (index + k >= len(text)): #preventing index error due to len(text)
            value = text[index : index + k] #isolating the k-gram
            
            if value not in grams_dict: #first instance seeing k-gram
                grams_dict[value] = {} 
                next_value = text[index + k]
                if next_value not in grams_dict[value]: #checking for new char trailing k-gram
                    grams_dict[value][next_value] = 1 
            
            else: #occurs if k-gram seen previously; checks char trailing k-gram
                next_value = text[index + k]
                if next_value not in grams_dict[value]: #checking for new char trailing k-gram
                    grams_dict[value][next_value] = 1
                else: #if char trailing k-gram isn't new
                    grams_dict[value][next_value] += 1
                
    return grams_dict

def combine_grams(grams1, grams2):
    ''' (dict, dict) -> dict
    Combines dictionary grams1, and dictionary grams2 into one dictionary, which is then returned.
    All inner values are combined, and grams1 & grams2 aren't impacted.
    
    >>> combine_grams({'a': {'b': 3, 'c': 9}, 'b': {'a': 10, 'c': 5}}, {'a': {'c' : 9},'b': {'a': 5, 'c': 5}, 'c': {'d': 4}})
    {'a': {'c': 18}, 'b': {'a': 15, 'c': 10}, 'c': {'d': 4}}
    
    >>> combine_grams({'a': {'a': 3, 'b': 3, 'c': 9}, 'c' : {'a' : 18}}, {'c': {'a': 16, 'd': 4}})
    {'a': {'a': 3, 'b': 3, 'c': 9}, 'c': {'a': 34, 'd': 4}}
    
    >>> combine_grams({'z': {'z':9}}, {'z': {'z':10, 'b': 34}})
    {'z': {'z': 19, 'b': 34}}
    '''
    
    combined_grams = {}
    
    for value in grams1: # shallow copy of grams1 into combined_grams
        combined_grams[value] = grams1.get(value)
   
    for outer_value in grams2: #add grams2 into combined grams
        if outer_value in combined_grams: #if a key is in grams1 and grams2
            inner_dict = {} #a new inner list is created to prevent altering the original dicts
            for inner_value in grams2[outer_value]: #running through inner keys of the outer key 
                if inner_value in combined_grams[outer_value]: #if the inner key exists already, adds the values
                    inner_dict[inner_value] = grams1[outer_value].get(inner_value) + grams2[outer_value].get(inner_value)
                else: #if inner key doesn't exist, adds it in
                    inner_dict[inner_value] = grams2[outer_value].get(inner_value)
            combined_grams[outer_value] = inner_dict #the inside list is added into combine_grams
        else: #if the key isn't in grams1, but is in grams2
            combined_grams[outer_value] = grams2[outer_value]
    return combined_grams

def get_grams_from_files(filenames, k):
    ''' (list, int) -> dict
    Takes a list filenames, which are strings corresponding to files. k tells how long each k-gram is.
    It reads the file and creates a k-grams dict for each file. Combines all k-grams dicts into one dict, which is returned.
    
    >>> grams = get_grams_from_files(['holmes.txt'], 1)
    >>> len(grams)
    96
    
    >>> grams = get_grams_from_files(['raven.txt'], 2)
    >>> len(grams)
    516
    
    >>> grams = get_grams_from_files(['raven.txt'], 1)
    >>> len(grams)
    57
    '''
    grams_dict = {}
    
    for filename in filenames: #each loop corresponds to one file
        filename_file_obj = open(filename, 'r', encoding = 'utf-8')
        file = ""
        for line in filename_file_obj: #adding each line into file as it occurs
            file = file + line
        filename_file_obj.close()
        grams_dict = combine_grams(grams_dict, get_grams(file, k)) #combines all previous files with this file
    
    return grams_dict
 
def generate_next_char(grams, cur_gram):
    ''' (dict, str) -> str
    Generates the next character after cur_gram, when given the k-gram dictionary grams.
    Returns the next character selected at random.
    
    >>> random.seed(15)
    >>> generate_next_char({'Dad': {' ': 10, 'd': 5}, 'Gran': {'d': 100}}, 'Dad')
    'd'
    >>> generate_next_char({'Dad': {' ': 10, 'd': 5}, 'Gran': {'d': 100}}, 'Dad')
    ' '
    
    >>> random.seed(1337)
    >>> grams = get_grams_from_files(['holmes.txt'], 1)
    >>> generate_next_char(grams, 'b')
    'y'
    
    >>> random.seed(1337)
    >>> grams = get_grams_from_files(['holmes.txt', 'raven.txt'], 1)
    >>> generate_next_char(grams, 'b')
    't'
    '''
    main_keys = list(grams.keys())
    
    #raising exceptions if input values are wrong
    if len(cur_gram) != len(main_keys[0]): #length of cur_gram isn't equal to the length of the k-grams
        raise AssertionError ("The length of the current gram does not match the length of keys in the grams dictionary!")
    if cur_gram not in grams: #if the current gram isn't in the grams dict - wouldn't have predicted following chars
        raise AssertionError ("The gram given is not in the grams dictionary!")
    
    #getting list of the k-grams in the dict for the population
    population_list = list(grams[cur_gram].keys())
    
    #counting the total instances of the k-gram by adding the trailing char instances
    total_occurances = 0
    for value in grams[cur_gram]:
        total_occurances = total_occurances + grams[cur_gram].get(value)
    
    #determining weights of each trailing char by dividing by the total_occurances
    weights_list = []
    for value in grams[cur_gram]:
        weights_list.append(grams[cur_gram].get(value) / total_occurances)
    
    #performs randon choices and returns
    #index at end removes it from a list and makes the char a str    
    return (random.choices(population_list, weights_list))[0]

def generate_text(grams, start_grams, k, n):
    ''' (dict, str, int, int) -> str
    This function takes in a k-gram dictionary grams, and integer k (for length of k-grams). It also takes the
    first gram to be used start_gram and generates a piece of text of length n.
    
    >>> random.seed(15)
    >>> grams = get_grams_from_files(['raven.txt'], 7)
    >>> print(generate_text(grams, "Quoth the", 7, 115))
    Quoth the Raven, sitting
    On the morrow;—vainly I had sought to borrow
        From my books surcease of sorrow—sorrow

    >>> random.seed(3005)
    >>> grams = get_grams_from_files(['raven.txt'], 9)
    >>> print(generate_text(grams, "Quoth the", 9, 115))
    Quoth the Raven “Nevermore.”
    <BLANKLINE>
        This I sat engaged in guessing, but no syllable expressing
    To the fowl whose
    
    >>> random.seed(3005)
    >>> grams = get_grams_from_files(['raven.txt', 'beowulf.txt'], 9)
    >>> print(generate_text(grams, "Quoth the", 9, 115))
    Quoth the Raven “Nevermore.”
    <BLANKLINE>
        This my earls that attend him,
    [70]      When the spirit one after all
    <BLANKLINE>
    
    >>> random.seed(3005)
    >>> grams = get_grams_from_files(['raven.txt'], 10)
    >>> print(generate_text(grams, "Quoth the", 10, 115))
    Traceback (most recent call last):
    AssertionError: The length of the current gram does not match the length of keys in the grams dictionary!
    '''
    #establishing local var
    cur_gram = start_grams
    last_whitespace_pos = 0
    
    #if the length of start_grams is longer than k, cuts off the start_grams so len(start_grams) == k
    #if len(start_grams) < k, error is raised, so don't need to worry about that here
    if len(start_grams) > k:
        cur_gram = start_grams[:k]

    #another local var created, but needs to be after cur_gram is adjusted (if needed)
    generated_text = cur_gram
    
    #loop to run and generate chars until len(generated_text) < n
    while len(generated_text) < n:
        next_char = generate_next_char(grams, cur_gram)
        generated_text += next_char
        cur_gram = cur_gram[1:] + next_char
        if next_char == ' ': #stores the last instance of a whitespace
            last_whitespace_pos = len(generated_text) - 1 
    
    #returns generated text at the most recent whitespace (don't want to end in the middle of a word)
    return generated_text[:last_whitespace_pos]

def repair_text(corrupted_text, error_char, grams, k):
    ''' (str, char, dict, int) -> str
    Takes a string of corrupted_text and an error_char, and uses a grams dictionary and k length to replace
    the error_chars with valid characters. This doesn't really do anything naturally.

    >>> random.seed(1029)
    >>> grams = get_grams_from_files(['beowulf.txt'], 5)
    >>> print(repair_text('It battle-waves ~~~~~, the ~~~~~~~~ fire-demon', '~', grams, 5))
    It battle-waves of da, the H.-So.)
     fire-demon
    
    >>> random.seed(15)
    >>> grams = get_grams_from_files(['beowulf.txt'], 5)
    >>> print(repair_text('It battle-waves ~~~~~, the ~~~~~~~~ fire-demon', '~', grams, 5))
    It battle-waves from
    , the eddies,  fire-demon
    
    >>> random.seed(1330)
    >>> grams = get_grams_from_files(['raven.txt', 'beowulf.txt'], 5)
    >>> print(repair_text('~~~~~s the bes~ of tim~s, i~ was ~he wo~st of~times', '~', grams, 5))
    ~~~~~s the best of times, in was phe worst offtimes
    
    >>> random.seed(1330)
    >>> grams = get_grams_from_files(['raven.txt', 'beowulf.txt'], 2)
    >>> print(repair_text('~~ ~a~ ~h~ bes~ of tim~s, i~ was ~he wo~st of~times', '~', grams, 2))
    ~~ ~a~ ~h~ bes  of tim s, in was che worst ofttimes
    '''
    #local var
    repaired_text = corrupted_text
    
    #add case for if cur_gram cannot be fit in the first part of k
    
    cur_gram = corrupted_text[:k]

    #runs through each value of repaired_text
    for index, value in enumerate(repaired_text):
        if value == error_char and index + 1 > k: #if the error_char is found at the value, and cur_gram is the right length
            cur_gram = repaired_text[index - k: index] #takes out the cur_gram from before the error_char
            if error_char in cur_gram: #for handling leaving in error_char
                continue
            next_char = generate_next_char(grams, cur_gram)
            repaired_text = repaired_text[:index] + next_char + repaired_text[index + 1:] #adds in the error_char replacement
    return repaired_text

if __name__ == "__main__": 
    doctest.testmod()