""" ngrams.py """

""" USAGE: python ngrams.py test """

import os
import sys

unsmoothUniENG = {}
unsmoothUniGER = {}
unsmoothUniSPA = {}

unsmoothBiENG = {}
unsmoothBiGER = {}
unsmoothBiSPA = {}

unsmoothTriENG = {}
unsmoothTriGER = {}
unsmoothTriSPA = {}

laplaceENG = {}
laplaceGER = {}
laplaceSPA = {}

interpolatedENG = {}
interpolatedGER = {}
interpolatedSPA = {}

lambda1 = 0.3333333333333
lambda2 = 0.3333333333333
lambda3 = 0.3333333333333

trainingDocs = ['training.en', 'training.de', 'training.es']

os.system('cls')
print "Analyzing Training Data"

for doc in trainingDocs:

    uni = {}
    bi = {}
    tri = {}

    uniProb = {}
    biProb  = {}
    triProb = {}

    totChars = 0

    last = ['', '']

    with open(doc) as f:
      while True:
        char = f.read(1)
        if not char:
            break
        curBi  = last[0] + char
        curTri = last[1] + last[0] + char
        if not uni.has_key(char):
            uni.update({char:1})
        else:
            uni[char] = uni.get(char) + 1

        if len(curBi) == 2:
            if not bi.has_key(curBi):
                bi.update({curBi:1})
            else:
                bi[curBi] = bi.get(curBi) + 1

        if len(curTri) == 3:
            if not tri.has_key(curTri):
                tri.update({curTri:1})
            else:
                tri[curTri] = tri.get(curTri) + 1

        if not last[0] == '': last[1] = last[0]
        last[0] = char

    for key in uni:
        totChars += uni[key]

    for key in uni:
        uniProb.update({key:1. * uni.get(key) / totChars})

    for key in bi:
        biProb.update({key:1. * bi.get(key) / uni.get(key[:1])})

    for key in tri:
        triProb.update({key:1. * tri.get(key) / bi.get(key[:2])})

    if   doc == 'training.en':
        uniENG = uni
        biENG = bi
        triENG = tri
    elif doc == 'training.de':
        uniGER = uni
        biGER = bi
        triGER = tri
    else:
        uniSPA = uni
        biSPA = bi
        triSPA = tri

    for i in uni:
        for j in uni:
            if not bi.has_key(i + j): bi.update({i+j:0})
    
    for i in uni:
        for j in uni:
            for k in uni:
                if not tri.has_key(i+j+k): tri.update({i+j+k:0})

print "Building N-Gram Models"

totUniENG = 0
totUniGER = 0
totUniSPA = 0

for i in uniENG:
    totUniENG = totUniENG + uniENG[i]

for i in uniGER:
    totUniGER = totUniGER + uniGER[i]

for i in uniSPA:
    totUniSPA = totUniSPA + uniSPA[i]


for i in uniENG:
    unsmoothUniENG.update({i:(uniENG[i] * 1.0) / (totUniENG * 1.0)})
    for j in uniENG:
        if uniENG[j] > 0:
            unsmoothBiENG.update({i+j:(biENG[i+j] * 1.0)/(uniENG[i] * 1.0)})
        else:
            unsmoothBiENG.update({i+j:0})
        for k in uniENG:
            if biENG[i+j] > 0:
                unsmoothTriENG.update({i+j+k: (triENG[i+j+k] * 1.0)/(biENG[i+j] * 1.0)})
            else:
                unsmoothTriENG.update({i+j+k:0})

for i in uniGER:
    unsmoothUniGER.update({i:(uniGER[i] * 1.0) / (totUniGER * 1.0)})
    for j in uniGER:
        if uniGER[j] > 0:
            unsmoothBiGER.update({i+j:(biGER[i+j] * 1.0)/(uniGER[i] * 1.0)})
        else:
            unsmoothBiGER.update({i+j:0})
        for k in uniGER:
            if biGER[i+j] > 0:
                unsmoothTriGER.update({i+j+k: (triGER[i+j+k] * 1.0)/(biGER[i+j] * 1.0)})
            else:
                unsmoothTriGER.update({i+j+k:0})

for i in uniSPA:
    unsmoothUniSPA.update({i:(uniSPA[i] * 1.0) / (totUniSPA * 1.0)})
    for j in uniSPA:
        if uniSPA[j] > 0:
            unsmoothBiSPA.update({i+j:(biSPA[i+j] * 1.0)/(uniSPA[i] * 1.0)})
        else:
            unsmoothBiSPA.update({i+j:0})
        for k in uniSPA:
            if biSPA[i+j] > 0:
                unsmoothTriSPA.update({i+j+k: (triSPA[i+j+k] * 1.0)/(biSPA[i+j] * 1.0)})
            else:
                unsmoothTriSPA.update({i+j+k:0})

for i in uniENG:
    for j in uniENG:
        for k in uniENG:
            laplaceENG.update({i+j+k: 1. * (triENG[i+j+k] + 1)/(biENG[i+j] + len(uniENG))})

for i in uniGER:
    for j in uniGER:
        for k in uniGER:
            laplaceGER.update({i+j+k: 1. * (triGER[i+j+k] + 1)/(biGER[i+j] + len(uniGER))})

for i in uniSPA:
    for j in uniSPA:
        for k in uniSPA:
            laplaceSPA.update({i+j+k: 1. * (triSPA[i+j+k] + 1)/(biSPA[i+j] + len(uniSPA))})

for i in uniENG:
    for j in uniENG:
        for k in uniENG:
            interpolatedENG.update({i+j+k:(lambda1 * unsmoothTriENG[i+j+k] + lambda2 * unsmoothBiENG[j+k] + lambda3 * unsmoothUniENG[k])})

for i in uniGER:
    for j in uniGER:
        for k in uniGER:
            interpolatedGER.update({i+j+k:(lambda1 * unsmoothTriGER[i+j+k] + lambda2 * unsmoothBiGER[j+k] + lambda3 * unsmoothUniGER[k])})

lambda1 = 1.0/3
lambda2 = 1.0/3
lambda3 = 1.0/3

for i in uniSPA:
    for j in uniSPA:
        for k in uniSPA:
            interpolatedSPA.update({i+j+k:(lambda1 * unsmoothTriSPA[i+j+k] + lambda2 * unsmoothBiSPA[j+k] + lambda3 * unsmoothUniSPA[k])})

totChars = 0

last = ['', '']

source = sys.argv[1]

UEpp = 1.0
UGpp = 1.0
USpp = 1.0

LEpp = 1.0
LGpp = 1.0
LSpp = 1.0

IEpp = 1.0
IGpp = 1.0
ISpp = 1.0

UEUpp = 1.0
UEBpp = 1.0

print "Analyzing Test Data"

with open(source) as f:
  while True:
    char = f.read(1)
    if not char:
        break

    totChars = totChars + 1
    norm = -1.0 / totChars
   
with open(source) as f:
    while True:
        char = f.read(1)
        if not char:
            break

        curTri = last[1] + last[0] + char

        UEUpp = UEUpp * pow(unsmoothUniENG[char],norm)
        
        if len(curTri) >= 2:
            if unsmoothBiENG.get(curTri[:2]) > 0:
                UEBpp = UEBpp * pow(unsmoothBiENG.get(curTri[:2]),norm)
        
        if len(curTri) == 3:
            if unsmoothTriENG.get(curTri) > 0:
                UEpp = UEpp * pow(unsmoothTriENG[curTri],norm)
            if unsmoothTriGER.get(curTri) > 0:
                UGpp = UGpp * pow(unsmoothTriGER[curTri],norm)
            if unsmoothTriSPA.get(curTri) > 0:
                USpp = USpp * pow(unsmoothTriSPA[curTri],norm)
            if laplaceENG.has_key(curTri):
                LEpp = LEpp * pow(laplaceENG[curTri],norm)
            if laplaceGER.has_key(curTri):
                LGpp = LGpp * pow(laplaceGER[curTri],norm)
            if laplaceSPA.has_key(curTri):
                LSpp = LSpp * pow(laplaceSPA[curTri],norm)
            if interpolatedENG.has_key(curTri):
                IEpp = IEpp * pow(interpolatedENG[curTri],norm)
            if interpolatedGER.has_key(curTri):
                IGpp = IGpp * pow(interpolatedGER[curTri],norm)
            if interpolatedSPA.has_key(curTri):
                ISpp = ISpp * pow(interpolatedSPA[curTri],norm)
                
        last[1] = last[0]
        last[0] = char

os.system('cls')

print "Unsmoothed and Smoothed Trigram Model Perplexities:"

print "\nUnsmoothed English Perplexity:   ", UEpp
print "Laplace English Perplexity:      ", LEpp
print "Interpolated English Perplexity: ", IEpp

print "\nUnsmoothed German Perplexity:    ", UGpp
print "Laplace German Perplexity:       ", LGpp
print "Interpolated German Perplexity:  ", IGpp

print "\nUnsmoothed Spanish Perplexity:   ", USpp
print "Laplace Spanish Perplexity:      ", LSpp
print "Interpolated Spanish Perplexity: ", ISpp, "\n"

smoothENG = LEpp + IEpp
smoothGER = LGpp + IGpp
smoothSPA = LSpp + ISpp

if   smoothENG < smoothGER and smoothENG < smoothSPA: print "The document is probably written in English!"
elif smoothGER < smoothENG and smoothGER < smoothSPA: print "The document is probably written in German!"
elif smoothSPA < smoothENG and smoothSPA < smoothGER: print "The document is probably written in Spanish!"
else: print "The models were inconclusive in determining the language of the document."
