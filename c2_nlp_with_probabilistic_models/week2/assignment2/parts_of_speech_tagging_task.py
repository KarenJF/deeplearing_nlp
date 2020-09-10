################################################################
# This script focus on skills in part-of-speech (POS) tagging, #
# the process of assigning a part-of-speech tag (Noun, Verb,   #
# Adjective...) to each word in an input text.                 #
#                                                              #
# It covers:                                                   #
# - Learn how parts-of-speech tagging works                    #
# - Compute the transition matrix A in a Hidden Markov Model   #
# - Compute the emission matrix B in a Hidden Markov Model     #
# - Compute the Viterbi algorithm                              #
# - Compute the accuracy of your own model                     #
################################################################

# Importing packages and loading in the data set 
from utils_pos import get_word_tag, preprocess  
import pandas as pd
from collections import defaultdict
import math
import numpy as np

#################################################################
# Step 1: Load the data set:                                    #
# - One data set (WSJ-2_21.pos) will be used for training.      #
# - The other (WSJ-24.pos) for testing.                         #
# - The tagged training data has been preprocessed to form a    #
#   vocabulary (hmm_vocab.txt).                                 #
# - The words in the vocabulary are words from the training set #
#   that were used two or more times.                           #
# - The vocabulary is augmented with a set of 'unknown word     #
#   tokens', such as  '--unk-verb--' or '--unk-noun--' to       #
#   replace the unknown words in both the training and test     #
#   corpus                                                      #
#################################################################

# load in the training corpus
with open("WSJ_02-21.pos", 'r') as f:
    training_corpus = f.readlines()
    
# read the vocabulary data, split by each line of text, and save the list
with open("hmm_vocab.txt", 'r') as f:
    voc_l = f.read().split('\n')

# vocab: dictionary that has the index of the corresponding words
vocab = {} 

# Get the index of the corresponding words. 
for i, word in enumerate(sorted(voc_l)): 
    vocab[word] = i  
    
# load in the test corpus
with open("WSJ_24.pos", 'r') as f:
    y = f.readlines()

# preprocess the test corpus, corpus without tags, preprocessed
_, prep = preprocess(vocab, "test.words")    

#########################################################################
# First Part of this script is to leverage transition, emission and tag # 
# dictionary to do a simple POS tagging task.                           #
#########################################################################

#######################################################################
# Part1A : Get Transition, Emission and Tag Dictionary                #
# - Transition Counts: computes the number of times each tag happened #
#   next to another tag. e.g: maps (prev_tag, tag) to the number of   #
#   times it has appeared.                                            #
# - Emission Counts: compute the probability of a word given its tag  #
#   e.g: maps (tag, word) to the number of times it happened.         #
# - Tag Counts: compute number of times each tag appeared.            #
#   e.g: maps (tag) to the number of times it has occured.            #
#######################################################################
def create_dictionaries(training_corpus, vocab):
    """
    Input: 
        training_corpus: a corpus where each line has a word followed by its tag.
        vocab: a dictionary where keys are words in vocabulary and value is an index
    Output: 
        emission_counts: a dictionary where the keys are (tag, word) and the values are the counts
        transition_counts: a dictionary where the keys are (prev_tag, tag) and the values are the counts
        tag_counts: a dictionary where the keys are the tags and the values are the counts
    """
    
    # initialize the dictionaries using defaultdict
    emission_counts = defaultdict(int)
    transition_counts = defaultdict(int)
    tag_counts = defaultdict(int)
    
    # Initialize "prev_tag" (previous tag) with the start state, denoted by '--s--'
    prev_tag = '--s--' 
    
    # use 'i' to track the line number in the corpus
    i = 0 
    
    # Each item in the training corpus contains a word and its POS tag
    # Go through each word and its tag in the training corpus
    for word_tag in training_corpus:
        
        # Increment the word_tag count
        i += 1
        
        # Every 50,000 words, print the word count
        if i % 50000 == 0:
            print(f"word count = {i}")
            
        # get the word and tag using the get_word_tag helper function (imported from utils_pos.py)
        word, tag = get_word_tag(word_tag, vocab)
        
        # Increment the transition count for the previous word and tag
        transition_counts[(prev_tag, tag)] += 1
        
        # Increment the emission count for the tag and word
        emission_counts[(tag, word)] += 1

        # Increment the tag count
        tag_counts[tag] += 1

        # Set the previous tag to this tag (for the next iteration of the loop)
        prev_tag = tag
        
    return emission_counts, transition_counts, tag_counts

#######################################################################
# Part1B : Get predicted POS and calculate accuracy of the model      #
#######################################################################
def predict_pos(prep, y, emission_counts, vocab, states):
    '''
    Input: 
        prep: a preprocessed version of 'y'. A list with the 'word' component of the tuples.                         
        y: a corpus composed of a list of tuples where each tuple consists of (word, POS)
        emission_counts: a dictionary where the keys are (tag,word) tuples and the value is the count
        vocab: a dictionary where keys are words in vocabulary and value is an index
        states: a sorted list of all possible tags for this assignment
    Output: 
        accuracy: Number of times you classified a word correctly
    '''
    
    # Initialize the number of correct predictions to zero
    num_correct = 0
    
    # Get the (tag, word) tuples, stored as a set
    all_words = set(emission_counts.keys())
    
    # Get the number of (word, POS) tuples in the corpus 'y'
    total = len(y)
    for word, y_tup in zip(prep, y): 

        # Split the (word, POS) string into a list of two items
        y_tup_l = y_tup.split()
        
        # Verify that y_tup contain both word and POS
        if len(y_tup_l) == 2:
            
            # Set the true POS label for this word
            true_label = y_tup_l[1]

        else:
            # If the y_tup didn't contain word and POS, go to next word
            continue
    
        count_final = 0
        pos_final = ''
        
        # If the word is in the vocabulary...
        if word in vocab:
            for pos in states:
                        
                # define the key as the tuple containing the POS and word
                key = (pos, word)

                # check if the (pos, word) key exists in the emission_counts dictionary
                if key in emission_counts: # complete this line

                # get the emission count of the (pos,word) tuple 
                    count = emission_counts[key]

                    # keep track of the POS with the largest count
                    if count > count_final: 

                        # update the final count (largest count)
                        count_final = count

                        # update the final POS
                        pos_final = pos

            # If the final POS (with the largest count) matches the true POS:
            if pos_final == true_label: # complete this line
                
                # Update the number of correct predictions
                num_correct += 1

    accuracy = num_correct / total
    
    return accuracy

#######################################################################
# Part2A : Hidden Markov Models for POS: implementing a Hidden Markov #
# Model (HMM) with a Viterbi decoder                                  #
# - In this case, the states are the parts-of-speech.                 #
# - A Markov Model utilizes a transition matrix, A.                   #
# - A Hidden Markov Model adds an observation or emission matrix B    #
#   which describes the probability of a visible observation when we  #
#   are in a particular state.                                        #
# - In this case, the emissions are the words in the corpus           #
# - The state, which is hidden, is the POS tag of that word.          #
#######################################################################

#######################################################################
# Creating the 'A' transition probabilities matrix                    #
# - Each cell in the 'A' transistion matrix tells the probability to  #
#   go from one part of speech to another.                            #
#######################################################################
def create_transition_matrix(alpha, tag_counts, transition_counts):
    ''' 
    Input: 
        alpha: number used for smoothing
        tag_counts: a dictionary mapping each tag to its respective count
        transition_counts: transition count for the previous word and tag
    Output:
        A: matrix of dimension (num_tags,num_tags)
    '''
    # Get a sorted list of unique POS tags
    all_tags = sorted(tag_counts.keys())
    
    # Count the number of unique POS tags
    num_tags = len(all_tags)
    
    # Initialize the transition matrix 'A'
    A = np.zeros((num_tags,num_tags))
    
    # Get the unique transition tuples (previous POS, current POS)
    trans_keys = set(transition_counts.keys())
    
    # Go through each row of the transition matrix A
    for i in range(num_tags):
        
        # Go through each column of the transition matrix A
        for j in range(num_tags):

            # Initialize the count of the (prev POS, current POS) to zero
            count = 0
        
            # Define the tuple (prev POS, current POS)
            # Get the tag at position i and tag at position j (from the all_tags list)
            key = (all_tags[i],all_tags[j])

            # Check if the (prev POS, current POS) tuple 
            # exists in the transition counts dictionary
            if key in transition_counts: #complete this line
                
                # Get count from the transition_counts dictionary 
                # for the (prev POS, current POS) tuple
                count = transition_counts[key]
                
            # Get the count of the previous tag (index position i) from tag_counts
            count_prev_tag = tag_counts[key[0]]
            
            # Apply smoothing using count of the tuple, alpha, 
            # count of previous tag, alpha, and total number of tags
            A[i,j] = (count + alpha)/(count_prev_tag + num_tags*alpha)

    ### END CODE HERE ###
    
    return A

#######################################################################
# Create the 'B' emission probabilities matrix                        #
# - Each cell in the 'B' emission matrix tells the probability of a   #
#   word with that part of speech                                     #
#######################################################################
def create_emission_matrix(alpha, tag_counts, emission_counts, vocab):
    '''
    Input: 
        alpha: tuning parameter used in smoothing 
        tag_counts: a dictionary mapping each tag to its respective count
        emission_counts: a dictionary where the keys are (tag, word) and the values are the counts
        vocab: a dictionary where keys are words in vocabulary and value is an index.
               within the function it'll be treated as a list
    Output:
        B: a matrix of dimension (num_tags, len(vocab))
    '''
    
    # get the number of POS tag
    num_tags = len(tag_counts)
    
    # Get a list of all POS tags
    all_tags = sorted(tag_counts.keys())
    
    # Get the total number of unique words in the vocabulary
    num_words = len(vocab)
    
    # Initialize the emission matrix B with places for
    # tags in the rows and words in the columns
    B = np.zeros((num_tags, num_words))
    
    # Get a set of all (POS, word) tuples 
    # from the keys of the emission_counts dictionary
    emis_keys = set(list(emission_counts.keys()))
    
    ### START CODE HERE (Replace instances of 'None' with your code) ###
    
    # Go through each row (POS tags)
    for i in range(num_tags): # complete this line
        
        # Go through each column (words)
        for j in range(num_words): # complete this line

            # Initialize the emission count for the (POS tag, word) to zero
            count = 0
                    
            # Define the (POS tag, word) tuple for this row and column
            key =  (all_tags[i],vocab[j])

            # check if the (POS tag, word) tuple exists as a key in emission counts
            if key in emission_counts: # complete this line
        
                # Get the count of (POS tag, word) from the emission_counts d
                count = emission_counts[key]
                
            # Get the count of the POS tag
            count_tag = tag_counts[key[0]]
                
            # Apply smoothing and store the smoothed value 
            # into the emission matrix B for this row and column
            B[i,j] = (count + alpha)/(count_tag + alpha * num_words)

    ### END CODE HERE ###
    return B

#######################################################################
# Part 3: Viterbi Algorithm and Dynamic Programming                   #
# - Initialization: initialize the best_paths and best_probabilities  #
#   matrices that you will be populating in feed_forward.             #
# - Feed forward: At each step, you calculate the probability of each #
#   path happening and the best paths up to that point.               #
# - Feed backward: This allows you to find the best path with the     #
#   highest probabilities.                                            #
#######################################################################

#######################################################################
# Part 3.1 Initialization                                             #
# - best_probs: Each cell contains the probability of going from one  #
#   POS tag to a word in the corpus.                                  #
# - best_paths: A matrix that helps you trace through the best        #
#   possible path in the corpus.                                      #
#######################################################################
def initialize(states, tag_counts, A, B, corpus, vocab):
    '''
    Input: 
        states: a list of all possible parts-of-speech
        tag_counts: a dictionary mapping each tag to its respective count
        A: Transition Matrix of dimension (num_tags, num_tags)
        B: Emission Matrix of dimension (num_tags, len(vocab))
        corpus: a sequence of words whose POS is to be identified in a list 
        vocab: a dictionary where keys are words in vocabulary and value is an index
    Output:
        best_probs: matrix of dimension (num_tags, len(corpus)) of floats
        best_paths: matrix of dimension (num_tags, len(corpus)) of integers
    '''
    # Get the total number of unique POS tags
    num_tags = len(tag_counts)
    
    # Initialize best_probs matrix 
    # POS tags in the rows, number of words in the corpus as the columns
    best_probs = np.zeros((num_tags, len(corpus)))
    
    # Initialize best_paths matrix
    # POS tags in the rows, number of words in the corpus as columns
    best_paths = np.zeros((num_tags, len(corpus)), dtype=int)
    
    # Define the start token
    s_idx = states.index("--s--")
    
    # Go through each of the POS tags
    for i in range(num_tags): # complete this line
        
        # Handle the special case when the transition from start token to POS tag i is zero
        if A[s_idx,i]==0: # complete this line
            
            # Initialize best_probs at POS tag 'i', column 0, to negative infinity
            best_probs[i,0] = float('-inf')
        
        # For all other cases when transition from start token to POS tag i is non-zero:
        else:
            
            # Initialize best_probs at POS tag 'i', column 0
            # Check the formula in the instructions above
            best_probs[i,0] = math.log(A[s_idx,i]) + math.log(B[i,vocab[corpus[0]]])
                        
    return best_probs, best_paths

########################################################################
# Part 3.2 Viterbi Forward                                             #
# Populuate the best_probs and best_paths                              #
# - Walk forward through the corpus.                                   #
# - For each word, compute a probability for each possible tag.        #
# - Unlike the previous algorithm predict_pos (the 'warm-up' exercise),# 
#   this will include the path up to that (word,tag) combination.      #
########################################################################
def viterbi_forward(A, B, test_corpus, best_probs, best_paths, vocab):
    '''
    Input: 
        A, B: The transition and emission matrices respectively
        test_corpus: a list containing a preprocessed corpus
        best_probs: an initilized matrix of dimension (num_tags, len(corpus))
        best_paths: an initilized matrix of dimension (num_tags, len(corpus))
        vocab: a dictionary where keys are words in vocabulary and value is an index 
    Output: 
        best_probs: a completed matrix of dimension (num_tags, len(corpus))
        best_paths: a completed matrix of dimension (num_tags, len(corpus))
    '''
    # Get the number of unique POS tags (which is the num of rows in best_probs)
    num_tags = best_probs.shape[0]
    
    # Go through every word in the corpus starting from word 1
    # Recall that word 0 was initialized in `initialize()`
    for i in range(1, len(test_corpus)): 
        
        # Print number of words processed, every 5000 words
        if i % 5000 == 0:
            print("Words processed: {:>8}".format(i))
            
        # For each unique POS tag that the current word can be
        for j in range(num_tags): # complete this line
            
            # Initialize best_prob for word i to negative infinity
            best_prob_i = float('-inf')
            
            # Initialize best_path for current word i to None
            best_path_i = None

            # For each POS tag that the previous word can be:
            for k in range(num_tags): # complete this line
            
                # Calculate the probability = 
                # best probs of POS tag k, previous word i-1 + 
                # log(prob of transition from POS k to POS j) + 
                # log(prob that emission of POS j is word i)
                prob = best_probs[k,i-1] + math.log(A[k,j])+math.log(B[j,vocab[test_corpus[i]]])

                # check if this path's probability is greater than
                # the best probability up to and before this point
                if prob > best_prob_i: # complete this line
                    
                    # Keep track of the best probability
                    best_prob_i = prob
                    
                    # keep track of the POS tag of the previous word
                    # that is part of the best path.  
                    # Save the index (integer) associated with 
                    # that previous word's POS tag
                    best_path_i = k

            # Save the best probability for the 
            # given current word's POS tag
            # and the position of the current word inside the corpus
            best_probs[j,i] = best_prob_i
            
            # Save the unique integer ID of the previous POS tag
            # into best_paths matrix, for the POS tag of the current word
            # and the position of the current word inside the corpus.
            best_paths[j,i] = best_path_i

        ### END CODE HERE ###
    return best_probs, best_paths

def viterbi_backward(best_probs, best_paths, corpus, states):
    '''
    This function returns the best path.
    
    '''
    # Get the number of words in the corpus
    # which is also the number of columns in best_probs, best_paths
    m = best_paths.shape[1] 
    
    # Initialize array z, same length as the corpus
    z = [None] * m
    
    # Get the number of unique POS tags
    num_tags = best_probs.shape[0]
    
    # Initialize the best probability for the last word
    best_prob_for_last_word = float('-inf')
    
    # Initialize pred array, same length as corpus
    pred = [None] * m
    
    ## Step 1 ##
    
    # Go through each POS tag for the last word (last column of best_probs)
    # in order to find the row (POS tag integer ID) 
    # with highest probability for the last word
    for k in range(num_tags): # complete this line

        # If the probability of POS tag at row k 
        # is better than the previously best probability for the last word:
        if best_probs[k,-1]>best_prob_for_last_word: # complete this line
            
            # Store the new best probability for the last word
            best_prob_for_last_word = best_probs[k,-1]
    
            # Store the unique integer ID of the POS tag
            # which is also the row number in best_probs
            z[m - 1] = k
            
    # Convert the last word's predicted POS tag
    # from its unique integer ID into the string representation
    # using the 'states' dictionary
    # store this in the 'pred' array for the last word
    pred[m - 1] = states[z[m - 1]]
    
    ## Step 2 ##
    # Find the best POS tags by walking backward through the best_paths
    # From the last word in the corpus to the 0th word in the corpus
    for i in range(m-1, 0, -1): # complete this line
        
        # Retrieve the unique integer ID of
        # the POS tag for the word at position 'i' in the corpus
        pos_tag_for_word_i = z[i]
        
        # In best_paths, go to the row representing the POS tag of word i
        # and the column representing the word's position in the corpus
        # to retrieve the predicted POS for the word at position i-1 in the corpus
        z[i - 1] = best_paths[pos_tag_for_word_i,i]
        
        # Get the previous word's POS tag in string form
        # Use the 'states' dictionary, 
        # where the key is the unique integer ID of the POS tag,
        # and the value is the string representation of that POS tag
        pred[i - 1] = states[z[i - 1]]
        
     ### END CODE HERE ###
    return pred

########################################################################
# Part 4: Predicting on a data set and calculate accuracy              #
########################################################################
def compute_accuracy(pred, y):
    '''
    Input: 
        pred: a list of the predicted parts-of-speech 
        y: a list of lines where each word is separated by a '\t' (i.e. word \t tag)
    Output: 
        
    '''
    num_correct = 0
    total = 0
    
    # Zip together the prediction and the labels
    for prediction, y in zip(pred, y):
        ### START CODE HERE (Replace instances of 'None' with your code) ###
        # Split the label into the word and the POS tag
        word_tag_tuple = y.split()
        
        # Check that there is actually a word and a tag
        # no more and no less than 2 items
        if len(word_tag_tuple)!=2: # complete this line
            continue 

        # store the word and tag separately
        word, tag = word_tag_tuple[0],word_tag_tuple[1]
        
        # Check if the POS tag label matches the prediction
        if prediction == tag: # complete this line
            
            # count the number of times that the prediction
            # and label match
            num_correct += 1
            
        # keep track of the total number of examples (that have valid labels)
        total += 1
        
        ### END CODE HERE ###
    return num_correct/total

if __name__ == '__main__':
    
    # Part 1 Get Transition, Emission and Tag count metrics: 
    print("Simple method: using Transition, Emission and Tags Matrix directly for POS ")
    emission_counts, transition_counts, tag_counts = create_dictionaries(training_corpus, vocab)
    states = sorted(tag_counts.keys())
    accuracy_predict_pos = predict_pos(prep, y, emission_counts, vocab, states)
    print(f"Accuracy of prediction using predict_pos is {accuracy_predict_pos:.4f}")
    
    # Part 2: Hidden Markov Models for POS
    # Part 2.1: Get 'A' Transistion Probability Matrix: 
    alpha = 0.001
    A = create_transition_matrix(alpha, tag_counts, transition_counts)
    # Testing your function
    #print(f"A at row 0, col 0: {A[0,0]:.9f}")
    #print(f"A at row 3, col 1: {A[3,1]:.4f}")

    #print("View a subset of transition matrix A")
    #A_sub = pd.DataFrame(A[30:35,30:35], index=states[30:35], columns = states[30:35] )
    #print(A_sub)
    
    # Part 2.2: Get 'B' emissio probability matrx: 
    B = create_emission_matrix(alpha, tag_counts, emission_counts, list(vocab))
    #print(f"View Matrix position at row 0, column 0: {B[0,0]:.9f}")
    #print(f"View Matrix position at row 3, column 1: {B[3,1]:.9f}")

    # Try viewing emissions for a few words in a sample dataframe
    #cidx  = ['725','adroitly','engineers', 'promoted', 'synergy']

    # Get the integer ID for each word
    #cols = [vocab[a] for a in cidx]

    # Choose POS tags to show in a sample dataframe
    #rvals =['CD','NN','NNS', 'VB','RB','RP']

    # For each POS tag, get the row number from the 'states' list
    #rows = [states.index(a) for a in rvals]

    # Get the emissions for the sample of words, and the sample of POS tags
    #B_sub = pd.DataFrame(B[np.ix_(rows,cols)], index=rvals, columns = cidx )
    #print(B_sub)
    
    # Part 3: Build Viterbi algorithm for Hidden Markov Models
    # viterbi algorithm 
    # initialize
    best_probs, best_paths = initialize(states, tag_counts, A, B, prep, vocab)
    # forward
    best_probs, best_paths = viterbi_forward(A, B, prep, best_probs, best_paths, vocab)
    # backward
    pred = viterbi_backward(best_probs, best_paths, prep, states)
    
    # Part 4: Prediction and mode accuracy
    # predict a POS: 
    print('The third word is:', prep[3])
    print('Your prediction is:', pred[3])
    print('Your corresponding label y is: ', y[3])
    
    print(f"Accuracy of the Viterbi algorithm is {compute_accuracy(pred, y):.4f}")
