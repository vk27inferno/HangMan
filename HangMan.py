class HangMan:
    
    font = ('Comic Sans MS', 20, 'bold')
    theme = 'Dark'
    allWords = []
    stages = None
    title = None    
    
    def __init__(self):
        self.tries = None
        self.pWord = None
        self.word = None
        self.used = []
        self.char = None

    def setup(self, path, stges, title="HangMan"):
        with open(path, 'r') as file:
            self.allWords = file.read().split()
        del file
        self.stages = stges
        self.title = title

    def play(self):
        
        def setTheme(theme, place):
            if theme == 'Dark':
                b = 'black'
                f = 'white'
            else:
                b = 'white'
                f = 'black'
                
            if place == 'askDiff':
                self.diffWindow.config(bg = b)
                self.diffFrame['bg'] = b
                i = [self.diffLabel, self.db1, self.db2, self.db3]
            elif place == 'Main':
                self.window.config(bg = b)
                inputEntry['insertbackground'] = f
                for i in [frame1, frame2]:
                    i['bg'] = b
                i = [wordLabel, themeButton, ph, inputEntry, triesLabel, usageLabel, logLabel]
            elif place == 'askReplay':
                self.replayWindow.config(bg = b)
                self.reFrame['bg'] = b
                i = [self.reLabel, self.reb1, self.reb2]

            for j in i:
                j['bg'] = b
                j['fg'] = f

        def changeTheme():
            if self.theme == 'Dark':
                self.theme = 'Light'
            else:
                self.theme = 'Dark'
                
            themeButton['text'] = self.theme
            setTheme(self.theme, 'Main')
            
        def replay():
            self.replayWindow.destroy()
            self.__init__()
            self.play()
            
        def askReplay(event):
            #Destroying the running game
            self.window.destroy()

            #Creating the replay Window
            self.replayWindow = Tk()
            self.replayWindow.title('Re-Experience?')

            self.reLabel = Label(master = self.replayWindow, font = self.font, text = "Wanna replay?\nSwear it'll be a different word...")
            self.reLabel.pack()
            self.reFrame = Frame(master = self.replayWindow)
            self.reFrame.pack()
            self.reb1 = Button(master = self.reFrame, font = self.font, text = 'Yup', command = replay)
            self.reb1.pack(side = 'left')
            self.reb2 = Button(master = self.reFrame, font = self.font, text = 'Later.', command = lambda: self.replayWindow.destroy())
            self.reb2.pack(side = 'left')

            setTheme(self.theme, 'askReplay')

            self.replayWindow.mainloop()
                
        def askDiff():
            def returnStage(num):
                nonlocal x
                x = num
                self.diffWindow.destroy()
            
            self.diffWindow = Tk()
            self.diffWindow.title('Difficulty')

            self.diffLabel = Label(master = self.diffWindow, font = self.font, text = 'Choose your level of difficulty: ')
            self.diffLabel.pack()

            self.diffFrame = Frame(master = self.diffWindow)
            self.diffFrame.pack()
            x=None
            self.db1 = Button(master = self.diffFrame, font = self.font, text = self.stages[0]['stage'], command = lambda: returnStage(0))
            self.db1.pack(side = 'left')
            self.db2 = Button(master = self.diffFrame, font = self.font, text = self.stages[1]['stage'], command = lambda: returnStage(1))
            self.db2.pack(side = 'left')
            self.db3 = Button(master = self.diffFrame, font = self.font, text = self.stages[2]['stage'], command = lambda: returnStage(2))
            self.db3.pack(side = 'left')

            setTheme(self.theme, 'askDiff')

            self.diffWindow.mainloop()
            return x

        def setDiff(i):
            from random import choice
                        
            wordLenRange = (self.stages[i]['wordLen']['min'], self.stages[i]['wordLen']['max'])
            
            possibleWords = []
            for j in self.allWords:
                if len(j) in range(wordLenRange[0], wordLenRange[1] + 1):
                    possibleWords.append(j)
                    
            self.word = list(choice(possibleWords).lower())
            self.pWord = ''.join(self.word)
            self.allWords.remove(self.pWord)
            self.tries = self.stages[i]['tries']

        def isValid(string):
            if len(string)==1 and string.isalpha():
                    return True
            else:
                return False

        def isUsed(string):
            if string in self.used or string in wordLabel['text']:
                return True
            else:
                return False

        def isRight(string):
            if string in self.word:
                return True
            else:
                return False

        def updateLog(x):
            if x == 'invalid input':
                logLabel['text'] = 'Enter a valid single alphabet'
            elif x == 'in word':
                logLabel['text'] = 'This letter is revealed'
            elif x == 'in used':
                logLabel['text'] = 'You have already used this letter'
            elif x == 'right':
                logLabel['text'] = 'Good Guess...'
            elif x == 'wrong':
                logLabel['text'] = 'You missed it.'
            elif x == 'win':
                logLabel['text'] += '\nYou Win...Press any key...'
            else:
                logLabel['text'] += '\nYou Lost...The word is revealed.\nPress any key...'

        def updateWord():
            txt = list(wordLabel['text'])
            while self.char in self.word:
                index = self.word.index(self.char)
                txt[index] = self.char
                self.word[index] = '*'
            txt = ''.join(txt)
            wordLabel['text'] = txt

        def updateTries():
            self.tries -= 1
            triesLabel['text'] = '{} Oops left'.format(self.tries)

        def updateUsage():
            self.used.append(self.char)
            usageLabel['text'] = 'Used Letters: {}'.format(', '.join(self.used))

        def processGame(event):
            self.char = inputEntry.get().strip()
            if isValid(self.char):
                self.char = self.char.lower()
                if isUsed(self.char):
                    if self.char in wordLabel['text']:
                        updateLog('in word')
                    else:
                        updateLog('in used')
                else:
                    if isRight(self.char):
                        updateWord()
                        updateLog('right')
                    else:
                        updateTries()
                        updateUsage()
                        updateLog('wrong')
            else:
                updateLog('invalid input')

            inputEntry.delete(0, 'end')
            
            if '*' not in wordLabel['text']:
                updateLog('win')
                inputEntry.bind('<Key>', askReplay)
                
            if self.tries == 0:
                updateLog('lost')
                wordLabel['text'] = self.pWord
                inputEntry.bind('<Key>', askReplay)
            
        
        ## GUI Design
        from tkinter import Tk, Label, Entry, Button, Frame

        #Diffficulty PopUp
        diff = askDiff()
        setDiff(diff)

        # Main Window
        self.window = Tk()
        self.window.title(self.title)

        # Frames and Buttons
        frame1 = Frame(master = self.window)
        frame1.pack(fill = 'x')
        wordLabel = Label(master = frame1, font = self.font, text = '*'*len(self.word))
        wordLabel.pack()
        themeButton = Button(master = frame1, font = ("Comic Sans MS", 12), text = self.theme, command = changeTheme)
        themeButton.pack(side = 'right')

        frame2 = Frame(master = self.window)
        frame2.pack()
        ph = Label(master = frame2, font = self.font, text = 'Guess a Letter: ')
        ph.pack(side = 'left')
        inputEntry = Entry(master = frame2, font = self.font, width = 5)
        inputEntry.focus_set()
        inputEntry.pack(side = 'left')
        triesLabel = Label(master = frame2, font = self.font, text = '{} Oops left'.format(self.tries))
        triesLabel.pack(side = 'left')

        usageLabel = Label(master = self.window, font = self.font, text = 'Used Letters: -')
        usageLabel.pack()

        logLabel = Label(master = self.window, font = self.font, text = "-:Log:-")
        logLabel.pack()

        setTheme(self.theme, 'Main')

        #Event Handler and MainLoop
        self.window.bind('<Return>', processGame)
        self.window.mainloop()

path = "words.txt"
stages = ({'stage': 'Cool', 'tries':10, 'wordLen':{'min':3, 'max':5}}, {'stage': 'Engaging', 'tries':6, 'wordLen':{'min':6, 'max':8}}, {'stage': 'Intense', 'tries': 4, 'wordLen': {'min': 9, 'max': 15}})

game1 = HangMan()
game1.setup(path, stages)
game1.play()
