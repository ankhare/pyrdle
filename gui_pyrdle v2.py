from tkinter import *
from tkinter import messagebox
import random

#pick word from word bank,  get its puzzle number and put results into dictionary
def pickWord():
    
    with open('shuffled_word_bank.txt', 'r') as f: 

        s = f.read()

    five_letter_bank = s.split()

    puzzle_word = random.choice(five_letter_bank)

    puzzle_number = five_letter_bank.index(puzzle_word) + 1
    
    return {'puzzle word':puzzle_word, 'puzzle number': puzzle_number }

#validate word by seeing if it is in word bank file
def isAValidWord(s):
    
    result = False

    with open('input_word_bank.txt', 'r') as f:   

        t = f.read()    

    input_word_bank = t.split()

    if s in input_word_bank:

        result = True

    return result


GREEN = '#00a603'
YELLOW = '#dbce0d'
WHITE = '#FFFFFF'
GRAY = '#cccccc'
RED = '#ff2a17'

#create window
window = Tk()
window.geometry('480x900')
window.title('Pyrdle 1.0')


#create game grid
for n in range(5):
    for m in range(1,7):
        gameLabel = Label(window, relief='ridge')
        gameLabel.grid(row=m, column=n*2, pady=10, columnspan=2)
        gameLabel.configure(width=5, height=3)

#create word entry box
wordEntry = Entry(window)
wordEntry.grid(row=8, column=0, pady=10, padx=10, columnspan=7)
wordEntry.configure(width=35)

#create keyboard buttons that can be used to input text in entry box
def onKeyClick(keybutton):
    wordEntry.insert(END, keybutton)
    
keys1 = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
for i in range(10):

    letter = keys1[i].upper()
    
    keybutton = Button(window, text=letter, command=lambda name=letter:onKeyClick(name))
    keybutton.grid(row=9, column=i, columnspan=1)
    keybutton.configure(height= 2)

keys2 = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']
for i in range(9):

    letter = keys2[i].upper()
    
    keybutton = Button(window, text=letter, command=lambda name=letter:onKeyClick(name))    
    keybutton.grid(row=10, column=i, columnspan=2)    
    keybutton.configure(height=2)

keys3 = ['z', 'x', 'c', 'v', 'b', 'n', 'm']
for i in range(7):

    letter = keys3[i].upper()    

    keybutton = Button(window, text=letter, command=lambda name=letter:onKeyClick(name))
    keybutton.grid(row=11, column=i, columnspan=3)
    keybutton.configure(height=2)
     
#create backspace key
def onBackspaceClick():
    s = wordEntry.get()
    
    n = len(s) - 1
    
    wordEntry.delete(n, END)
    
backspaceButton = Button(window, text='⌫', command=onBackspaceClick)
backspaceButton.grid(row=11, column=7, columnspan=3)
backspaceButton.configure(height=2)

###create clear key
##def onClearClick():
##    
##    wordEntry.delete(0, END)
##
##
##clearButton = Button(window, text='🗑', command=onClearClick)
##
##clearButton.grid(row=11, column=0)
##
##clearButton.configure(height=2)


#call functions and create global variables

a = pickWord()

secret_word = a['puzzle word']

puzzle_number = a['puzzle number']

attempt_number = 0

result_for_sharing = ''

game = 'on'

##print(secret_word)

#when the guess button is clicked:
def onButtonClick():

    global secret_word
    global attempt_number
    global result_for_sharing
    global game

    if game == 'on':

        #process user input
        your_guess = wordEntry.get()
        
        your_guess = your_guess.lower()

        if ' ' in your_guess:
            your_guess = your_guess.strip()
            
        wordEntry.delete(0, END)
        
        #reject invalid responses
        if len(your_guess) != 5:
            
            messagebox.showerror('Invalid Input', 'Use a 5 letter word')

        elif isAValidWord(your_guess) == False:
            
            messagebox.showerror('Invalid Input', 'Not in the word list')

        else:
            #accept attempt

            attempt_number += 1
                
            local_secret_word = list(secret_word)

            #start with all letters as incorrect
            your_result = ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️']

            #mark correct letters green and alter local secret word so that the same letter will not be used create a yellow in a different location as well
            for i in range(5):

                if your_guess[i] == local_secret_word[i]:

                    your_result[i] = '🟩'

                    local_secret_word[i] = '*'
                    
            #mark partially correct letters yellow and alter the letter marked yellow so that they will not be used to create additional yellows
            for i in range(5): 

                ch = your_guess[i]

                if your_guess[i] in local_secret_word and your_result[i] != '🟩':

                    your_result[i] = '🟨'

                    for i in range(5):

                        if ch == local_secret_word[i]:

                            local_secret_word[i] = '+'

                            break
                        
            #make used keys that are not in the word or have been guessed correctly white or green:            
            for i in range(5):

                ch = your_guess[i]

##                d = {1: ['keys1', 9, 1], 2:['keys2', 10, 2], 3:['keys3', 11, 3]}
                
                if ch not in secret_word or ch == secret_word[i]:
                    if ch in keys1:
                        c = keys1.index(ch)
                        r = 9
                        cs = 1                                        
                    elif ch in keys2:
                        c = keys2.index(ch)
                        r = 10
                        cs = 2
                    else:
                        c = keys3.index(ch)
                        r = 11
                        cs = 3
                        
                    letter = ch.upper()

                    keyButton = Button(window, text=letter, command=lambda name=letter:onKeyClick(name), bg=GRAY)
                    keyButton.grid(row=r, column=c, columnspan=cs)

                    if ch == secret_word[i]:
                        keyButton.configure(height=2, fg=GREEN)  
                    else:
                        keyButton.configure(height=2, fg=WHITE)

            #add result as string to sharing string
            result_for_sharing += ''.join(your_result) + '\n'

            #display result of attempt
            for i in range(5):

                gameLabel = Label(window, text=your_guess[i].upper())
                gameLabel.grid(row=attempt_number, column=i*2, pady=10, columnspan=2)
                gameLabel.configure(width=5, height=3)

                if your_result[i] != '🟩':
                    
                    if your_result[i] != '🟨':
                        gameLabel.configure(bg=GRAY, fg=WHITE)
                        
                    else:
                        gameLabel.configure(bg=YELLOW, fg=WHITE) 
                else: 
                    gameLabel.configure(bg=GREEN,fg=WHITE)
                    
            #if game is won:
            if your_result == ['🟩', '🟩', '🟩' , '🟩', '🟩']:

                game = 'over'

                d = {1:'Genius!', 2:'Magnificent!', 3:'Impressive!',\
                     4:'Splendid!', 5:'Nice!', 6:'Phew!'}

                message = d[attempt_number]
                   
            #if all 6 attempts are used:
            elif attempt_number == 6:

                game = 'over'

                message = 'The word was {}!'.format(secret_word)

                attempt_number = 'X'
                
            #if game is over, show final results: 
            if game == 'over':

                #index_remove = result_for_sharing.pop(-1)

                wordEntry.insert(0, 'Press Guess to Exit')
                wordEntry.configure(state=DISABLED)

                gameOverLabel = Label(window, text='\n \n {} \n \n Share your results:'.format(message))
                gameOverLabel.grid(row=14, column=0, columnspan=10)

                gameOverText = Text(window, height=8, width=15)
                gameOverText.grid(row=15, column=0, columnspan=10)
                gameOverText.insert(END, 'Pyrdle {} {}/6: \n{}'.format(puzzle_number, attempt_number, result_for_sharing))
    else:
        window.destroy()
        
                            
guessButton = Button(window, text='Guess', command=onButtonClick) 

guessButton.configure(width=10)

guessButton.grid(row=8, column=7, columnspan=3)

    
mainloop()
