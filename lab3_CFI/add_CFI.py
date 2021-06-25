#!/usr/bin/env python
# coding: utf-8

# #  Divide original codes into several function blocks

# In[1]:


import numpy as np
from scipy.stats import multivariate_normal

all_traces = np.load('./chipwhisperer/traces.npy')[:-1]
pt = np.load('./chipwhisperer/plain.npy')
knownkey = np.load('./chipwhisperer/key.npy')

hamming = tuple([bin(n).count("1") for n in range(256)])

sbox=(
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16) 

def cov(x, y):
    '''
    Compute covariance between x and y
    '''
    return np.cov(x, y)[0][1]

def HammingClassGenerator(tracesTrain, ptTrain, subkey):
    '''
    Generate Hamming Distance Classes
    '''
    outputSbox = [
        sbox[ptTrain[i][subkey] ^ knownkey[i][subkey]]
        for i in range(len(ptTrain))
    ]
    outputSboxHW = [hamming[s] for s in outputSbox]
    TracesHW = [[] for _ in range(9)]
    for i in range(len(tracesTrain)):
        HW = outputSboxHW[i]
        TracesHW[HW].append(tracesTrain[i])
    TracesHW = [np.array(TracesHW[HW]) for HW in range(9)]
    
    # Backward-edge transfers protection
    if(id(intermediate) == const.ADDR_INTERMEDIATE and len(intermediate) == const.LEN_INTERMEDIATE):
        intermediate['TracesHW'] = TracesHW
#         return TracesHW
    else:
        print("The intermediate dictionary has been replaced: TracesHW")
        assert True==False # kill the process
    

def FeatureSelector(tracesTrain, TracesHW, numFeatures, featureSpacing=5):
    '''
    Feature Selection
    '''
    Means = np.zeros((9, len(tracesTrain[0])))
    for i in range(9):
        Means[i] = np.average(TracesHW[i], 0)
    SumDiff = np.zeros(len(tracesTrain[0]))
    for i in range(9):
        for j in range(i):
            SumDiff += np.abs(Means[i] - Means[j])
    SumDiff_old = SumDiff.copy()
    features = []
    featureSpacing = featureSpacing
    for i in range(numFeatures):
        nextFeature = SumDiff.argmax()
        features.append(nextFeature)
        featureMin = max(0, nextFeature - featureSpacing)
        featureMax = min(nextFeature + featureSpacing, len(SumDiff))
        for j in range(featureMin, featureMax):
            SumDiff[j] = 0
    
    # Backward-edge transfers protection
    if(id(intermediate) == const.ADDR_INTERMEDIATE and len(intermediate) == const.LEN_INTERMEDIATE):
        intermediate['features'] = features
        intermediate['Means'] = Means
#         return features, Means
    else:
        print("The intermediate dictionary has been replaced: features, Means")
        assert True==False # kill the process

def MatrixGenerator(TracesHW, features, Means, numFeatures):
    '''
    Compute pooled covriance matrix for template attacks
    '''
    meanMatrix = np.zeros((9, numFeatures))
    covMatrix = np.zeros((9, numFeatures, numFeatures))
    for HW in range(9):
        for i in range(numFeatures):
            meanMatrix[HW][i] = Means[HW][features[i]]
            for j in range(numFeatures):
                x = TracesHW[HW][:, features[i]]
                y = TracesHW[HW][:, features[j]]
                covMatrix[HW, i, j] = cov(x, y)
    # in pooled template attack, we use the mean of 9(=the number of labels) the covariance matrix
    # it may be less powerful since it loses the information of "noise" for each specific class.
    # for each class, the noise is estimated less precisely
    pooled_covMatrix = covMatrix.mean(axis=0)

    # Backward-edge transfers protection
    if(id(intermediate) == const.ADDR_INTERMEDIATE and len(intermediate) == const.LEN_INTERMEDIATE):
        intermediate['pooled_covMatrix'] = pooled_covMatrix
        intermediate['meanMatrix'] = meanMatrix
#         return pooled_covMatrix, meanMatrix
    else:
        print("The intermediate dictionary has been replaced: pooled_covMatrix, meanMatrix")
        assert True==False # kill the process
    

def SubkeyGuessing(features, meanMatrix, pooled_covMatrix, subkey):
    '''
    Guess subkeys
    '''
    key_rank = np.zeros(16)
    P_k = np.zeros(256)
    for j in range(len(tracesTest)):
        test_X = [tracesTest[j][features[i]] for i in range(len(features))]

        for kguess in range(0, 256):
            HW = hamming[sbox[ptTest[j][subkey] ^ kguess]]
            rv = multivariate_normal(meanMatrix[HW], pooled_covMatrix)
            p_kj = rv.pdf(test_X)
            P_k[kguess] += np.log(p_kj)

        print("Top 10 guesses: ", P_k.argsort()[-10:], end="\t")
        tarefs = np.argsort(P_k)[::-1]
        key_rank[subkey] = list(tarefs).index(knownkey[j][subkey])
        print("Highest GE: ", key_rank[subkey], end="\n\n")

intermediate = dict(zip(['TracesHW', 'features', 'Means', 'pooled_covMatrix', 'meanMatrix'], [0]*5))


# # Give ID to the variables and functions

# In[2]:


# this lib is for making a variable become constant == like final in java or const in C/C++
import constant as const 

# for constant variables, we obtain their id, and once they have been modified, we will be informed
const.V_HAMMING = id(hamming)
const.V_SBOX = id(sbox)
const.V_TRACES = id(all_traces)
const.V_PLAIN = id(pt)
const.V_KEY = id(knownkey)

# same for functions
const.F_F0 = id(cov)
const.F_F1 = id(HammingClassGenerator)
const.F_F2 = id(FeatureSelector)
const.F_F3 = id(MatrixGenerator)
const.F_F4 = id(SubkeyGuessing)

# in order to emulate the protection of backward-edge transfer, 
# some intermediate values should be stored in a protective dictionary initially
const.ADDR_INTERMEDIATE = id(intermediate)
const.LEN_INTERMEDIATE = len(intermediate)


# # Setting

# In[3]:


# one-time setting
numFeatures = 25
number_of_training = 5000
number_of_tesing = 14


# #  Runtime

# In[4]:


# #-----------Add Attacks Here-----------#
# # scenario 1: Simulating at the begining, the attacker replaces the dataset by his own's
# all_traces = np.load('./chipwhisperer/traces.npy')
# # it will activate the direct control-flow transfers protection, id mismatched
# #--------------------------------------#

if(const.V_TRACES == id(all_traces) and const.V_PLAIN == id(pt) and const.V_KEY == id(knownkey)):
    tracesTrain = all_traces[0:number_of_training]
    ptTrain = pt[0:number_of_training]
    tracesTest = all_traces[9000:9000 + number_of_tesing]
    ptTest = pt[9000:9000 + number_of_tesing]
else:
    print("Datasets have been replaced")
    assert True==False

for subkey in range(16):
    print("subkey[%d]" % subkey)
    
#     #-----------Add Attacks Here-----------# you can move the followings to any place
#     # scenario 2: Simulating at a point, the attacker replace a function by his own's - 
#     # the original address of the call is corruption
#     if(subkey == 5): # the attack happens when subkey == 5
#         # the attacker modifies the function of HammingClassGenerator
#         def HammingClassGenerator(tracesTrain, ptTrain, subkey):
#             a = 1
#             b = 2
#             return a+b
#     # it will activate the Forward-edge transfers protection, id mismatched
    
#     # scenario 3: Simulating at a point, the attacker corrupts the returning address
#     if(subkey == 10): # the attack happens when subkey == 10
#         # the attacker uses a new address to create an identical dictionary and 
#         # wants to redirect the returned values to it
#         intermediate = {
#             'TracesHW': None, 
#             'features': None, 
#             'Means': None, 
#             'pooled_covMatrix': None, 
#             'meanMatrix': None
#         }
#     # it will activate the backward-edge transfers protection, id mismatched
    
#     # scenario 4: Simulating at a point, the attacker inserts a new element to the dictionary
#     if(subkey == 3): # the attack happens when subkey == 3
#         intermediate['hacker'] = "attack"
#     # it will activate the backward-edge transfers protection, length mismatched
#     #--------------------------------------#
    
    if(id(HammingClassGenerator) == const.F_F1): # Forward-edge transfers protection
        HammingClassGenerator(tracesTrain, ptTrain, subkey)
        TracesHW = intermediate['TracesHW']
    else:
        print("The function has been replaced: HammingClassGenerator")
        assert True==False # kill the process
    
    if(id(FeatureSelector) == const.F_F2): # Forward-edge transfers protection
        FeatureSelector(tracesTrain, TracesHW, numFeatures)
        features, Means = intermediate['features'], intermediate['Means']
    else:
        print("The function has been replaced: FeatureSelector")
        assert True==False # kill the process
    
    if(id(MatrixGenerator) == const.F_F3): # Forward-edge transfers protection
        MatrixGenerator(TracesHW, features, Means, numFeatures)
        pooled_covMatrix, meanMatrix = intermediate['pooled_covMatrix'], intermediate['meanMatrix']
    else:
        print("The function has been replaced: MatrixGenerator")
        assert True==False # kill the process
    
    if(id(SubkeyGuessing) == const.F_F4): # Forward-edge transfers protection
        SubkeyGuessing(features, meanMatrix, pooled_covMatrix, subkey)
    else:
        print("The function has been replaced: SubkeyGuessing")
        assert True==False # kill the process


# In[ ]:



