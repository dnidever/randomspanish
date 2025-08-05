import os
import numpy as np
from . import utils

DATA = np.load(utils.datadir()+'spanish_database_5000words.npy')

def pickoptions(data,randomword,noptions=5):
    # Get random options
    done = False
    numpicked = 0
    optdata = []
    pickcount = 0
    while (done==False):
        optdata1 = np.random.choice(data)
        optnum = optdata1['number']
        if (optnum != randomword[-1]) and (optnum not in [o['number'] for o in optdata]): 
            optdata.append(optdata1)
            numpicked += 1
        if numpicked >= noptions:
            done = True
        pickcount += 1
    return optdata

def randomword(noptions=4,maxattempts=10,top=500):
    """
    Random word
    """

    if top is not None:
        si = np.argsort([d[-1] for d in DATA])
        data = DATA[si][:top]
    else:
        data = DATA
    
    flag = False
    count = 0
    history = []
    while (flag==False):

        # Pick the next word
        #  done repeat words
        randomword = np.random.choice(data)
        
        # Get random options
        optdata = pickoptions(data,randomword,noptions=noptions)
        
        # Stick the correct number in a random location
        correctposition = np.random.randint(noptions+1)
        alldata = optdata.copy()
        alldata.insert(correctposition,randomword)
            
        # Print them out
        print(randomword['word'])
        for i in range(len(alldata)):
            print('{:2d} {:s}'.format(i+1,alldata[i]['engdef']))
            
        # Solve attempts
        solvedone = False
        solved = False
        solvecount = 0
        while (solvedone==False):
            # Read answer
            guess = input('What is the correct definition? ')
            if guess.lower() == 'q':
                return
            if guess.isnumeric()==False:
                print(' ')
                print('Not a number')
                print(' ')
                solvecount += 1
                continue
            guess = int(guess)
            if guess != correctposition+1:
                print(' ')
                print('Incorrect')
                print(' ')
                solvecount += 1
                continue
            else:
                print(' ')
                print('Correct!')
                print(' ')
                solved = True
                solvecount += 1
            if solved or solvecount >= maxattempts:
                solvedone = True
        
        
        # Save what happened
        hist = [randomword,optdata,solved,solvecount]
        history.append(hist)
        
        count += 1

class RandomWordizer():

    def __init__(self,noptions=4,maxattempts=10,top=500):
        if top is not None:
            si = np.argsort([d[-1] for d in DATA])
            self.data = DATA[si][:top]
        else:
            self.data = DATA.copy()
        self.noptions = noptions
        self.maxattempts = maxattempts
        self.top = top
        self.randomword = []
        self.history = []
        self.correctposition = None
        self.alldata = []
        
    def __call__(self):
        flag = False
        count = 0
        while (flag==False):

            # Pick the next word
            #  done repeat words
            self.pickone()
        
            # Get random options
            self.pickoptions()
        
            # Stick the correct number in a random location
            correctposition = np.random.randint(self.noptions+1)
            self.correctposition = correctposition
            alldata = self.optdata.copy()
            alldata.insert(correctposition,self.randomword)
            self.alldata = alldata
            
            # Print them out
            self.printquestion()
            
            # Solve attempts
            solvedone = False
            solved = False
            solvecount = 0
            while (solvedone==False):
                # Read answer
                guess = input('What is the correct definition? ')
                # quit
                if guess.lower() == 'q':
                    return
                # no idea
                elif guess.lower() == '?':
                    solvedone = True
                    print()
                    print('The correct answer is '+str(correctposition+1)+' >>'+self.randomword['engdef']+'<<')
                    print()
                # not a number
                elif guess.isnumeric()==False:
                    print(' ')
                    print('Not a number')
                    print(' ')
                    solvecount += 1
                    continue
                # correctly formatted guess
                elif guess.isnumeric()==True:
                    guess = int(guess)
                    if guess != correctposition+1:
                        print(' ')
                        print('Incorrect')
                        print(' ')
                        solvecount += 1
                        continue
                    else:
                        print(' ')
                        print('Correct!')
                        print(' ')
                        solved = True
                        solvecount += 1
                if solved or solvecount >= self.maxattempts:
                    solvedone = True
        
            # Save what happened
            hist = [self.randomword,self.optdata,solved,solvecount]
            self.history.append(hist)

            print('{:d} words, {:d} correct'.format(self.nwords,self.ncorrect))
            print()
            
            count += 1

    @property
    def nwords(self):
        return len(self.history)

    @property
    def ncorrect(self):
        return int(np.sum([d[2] for d in self.history]))
            
    def pastwords(self,number=None):
        if len(self.history)>0:
            pwords = [d[0]['word'] for d in self.history]
            if number is not None:
                pwords = list(np.array(pwords)[-number:])
        else:
            pwords = []
        return pwords
        
    def pickone(self,norepeat=100):
        pwords = self.pastwords(norepeat)
        done = False
        while (done==False):
            newrandomword = np.random.choice(self.data)
            if newrandomword['word'] != pwords:
                done = True
        self.randomword = newrandomword

    def pickoptions(self,number=4):
        # Get random options
        optdata = pickoptions(self.data,self.randomword,
                              noptions=self.noptions)
        self.optdata = optdata

    def printquestion(self):
        # Print them out
        print('Random Word #{:d}: {:s}'.format(self.nwords+1,
                                              self.randomword['word']))
        for i in range(len(self.alldata)):
            print('{:2d} {:s}'.format(i+1,self.alldata[i]['engdef']))
