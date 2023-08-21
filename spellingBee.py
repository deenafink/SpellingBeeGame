#I hereby certify that this program is solely the result of my own work and is in compliance with the Academic Integrity policy of the course syllabus and the academic integrity policy of the CS department.
import Draw
import math
import random


# function to create a single hexagon 
def createHex(across, down, letter):
    # each side of the hexagon is 45
    # create a hexagon using the pythagorean theorem (with traingles inside hexagons)
    # a**2 + b**2 = c**2
    # a**2 + 22.5**2 = 45**2
    # find the length of a
    a = math.sqrt((45**2)-(22.5**2))
    # across = x coordinate of center of hexagon, down = y coordinate of hexagon
    x = down-a
    y = down+a
    g = across-22.5
    h = across+22.5
    # draw lines to create a hexagon with length 45 sides
    Draw.setColor(Draw.BLACK)
    Draw.line(g, y, h, y)
    Draw.line(h, y, across+45, down)
    Draw.line(across+45, down, h, x)
    Draw.line(h, x, g, x)
    Draw.line(g, x, across-45, down)
    Draw.line(across-45, down, g, y)
     
    # Adding the letter variable into the hexagon
    # using these variables to center the letters
    xAxis = 7
    yAxis = 8
    Draw.string(letter, across-xAxis, down-yAxis)

# function to create the whole board
def DrawBoard(hexagons, score, guess, level, doneWords, reason, doneWords2, genius):   
    Draw.clear()     
    Draw.setFontFamily('Courier')
    Draw.setFontSize(25)
    #draw each cell with the 2D list of points and letter
    for row in range(len(hexagons)):
        for col in range(len(hexagons[0])-2):
            # call CreateHex with each set of points and letter
            createHex(hexagons[row][col], hexagons[row][col+1], hexagons[row][col+2])
    

    Draw.setFontSize(12)
    # draw the backgrounds for the buttons
    # Delete
    Draw.filledRect(305, 700, 50, 50)
    # New Game
    Draw.filledRect(375, 700, 50, 50)
    # Enter
    Draw.filledRect(445, 700, 50, 50)
    
    # Backgrounds for the score and level
    Draw.filledRect(100, 100, 115, 25)
    Draw.filledRect(100, 150, 115, 25)
    # textbox
    Draw.filledRect(340, 575, 120, 50)
    
    #Display the words correctly guessed
    Draw.string('Guessed Words:', 100, 230)
    
    # loop through doneWords
    for i in range(len(doneWords)):
        Draw.string(doneWords[i], 100, 250 + i*20)
    # if need to go to next column loop through doneWords2
    for i in range(len(doneWords2)):
        Draw.string(doneWords2[i], 200, 250 + i*20)
    
    # draw the title    
    Draw.setFontSize(45)
    Draw.string('Spelling Bee', 270, 45)
    
    
    # Draw the reason why the guess is wrong
    Draw.setFontSize(14)
    Draw.string(reason, 340, 550)
    
    # Draw if reached genius or not
    Draw.string(genius, 290, 115)
    
    Draw.setFontSize(12)
    Draw.setColor(Draw.WHITE)
    
    Draw.string('Delete', 309, 720)
    Draw.string('New\nGame', 385, 715)
    Draw.string('Enter', 452, 720)
    
    # draw the level and score variables
    Draw.string("Score: " + str(score), 100, 105)
    Draw.string("Level: " + level, 100, 155)
    
    # Display the guess
    Draw.setColor(Draw.WHITE)
    Draw.string(guess, 360, 592)
    Draw.show()

# returns a list of validWords
def loadDictionary(allWords):
    # add the word to validWords if is at least 4 letters
    validWords=[]
    for line in allWords:
        # account for the extra space at the end of the words
        if len(line)>=5:
            validWords+=[line[0:-1]]
    return validWords

#returns the candidates list    
def buildCandidates(validWords):
    candidates=[]
    for i in validWords:
        
        # if there are 7 letters
        if len(i)==7:
            multiple = False
            # check that there are 7 different letters
            d = {}
            for char in i:
                # if that letter is already in the word
                if char in d:
                    multiple = True
                else:
                    d[char] = 1
            # if there are 7 different letters multiple will still be False
            if multiple == False:
                candidates.append(i)
    
    return candidates

# returns true is every character in a can be found in b
# to use for compiling a list of words that only use the letters of the chosen word
def all_in(a, b):
    for i in a:
        if i not in b:
            return False
    return True

# returns a list of all possible solution words with that candidateWord
def getSolutionWords(candidateWord, validWords):
    solutions = []
    
    for i in validWords:
        # if the word's letters are only ones in the candidateWord
        if all_in(i, candidateWord):
            solutions.append(i)
    return solutions

# returns which letter appears the most throughout the solution words (to put in the middle)
def mostPopLetter(solutionWords):
    d = {}
    
    # loop through each word in solutionWords
    for word in solutionWords:
        # for each letter in the word
        for char in word:
            # tally how many times each letter is used
            if char in d:
                d[char]+=1
            else:
                d[char]=1
    
    # variables to find the most frequent letter
    largest = 0
    popLetter=""
    
    # Find the most frequent letter
    for key in d:
        # if encounter a letter with a higher tally make that letter the popLetter
        if d[key]>largest:
            largest=d[key]
            popLetter=key
    
    return popLetter

# fill the hexagons with letters
def fillLayout(hexagons, popLetter, candidateWord):
    # fill the middle hexagon with the most popLetter
    hexagons[-1][-1] = popLetter
    
    
    #remove popLetter from the candidateWord
    withoutPopLetter = ""
    for n in candidateWord:
        if n != popLetter:
            withoutPopLetter+=n
    
    # use the remaining letters in the words to fill the other hexagons
    # loop through the rows of the first 6 hexagons (not the last/middle one) and assign a letter to each
    for i in range(len(hexagons)-1):
        hexagons[i][-1] = withoutPopLetter[i]
    
# get the click 
def getClick(hexagons):
    # same pythagorean statement as before
    a = math.sqrt((45**2)-(22.5**2))
    
    while True:
        if Draw.mousePressed():
                newX = Draw.mouseX()
                newY = Draw.mouseY()
                
                # if the click was within the Delete button return "Delete"
                if newX >= 305 and newX <= 355 and newY >= 700 and newY <= 750:
                    return "Delete"
                
                # if the click was within the new game button return "New Game"
                elif newX >= 375 and newX <= 425 and newY >= 700 and newY <=750:
                    return "New Game"
                
                # if the click was within the Enter button return "Button"
                elif newX >= 445 and newX <= 495 and newY >=700 and newY <=750:
                    return "Enter"
                
                else:
                    #check if click was in a hexagon and return that associated letter- using circles
                    for row in range(len(hexagons)):
                        # use the points for the center of the hexagons as centers for the circles
                        across = hexagons[row][0]
                        down = hexagons[row][1]
                        # use the distance formula
                        # if the distance between the center and the newX,Y is smaller than the radius
                        radius = math.sqrt((across-(across-45))**2+(down-down)**2)
                        distance = math.sqrt((newX-across)**2+(newY-down)**2)
                        if distance < radius:
                            return hexagons[row][-1]
                            

def playGame(candidateWord, solutionWords, popLetter, hexagons):  
    fillLayout(hexagons, popLetter, candidateWord)
    # set all variables to initial state
    doneWords = []
    doneWords2 = []
    guess = ""
    level = "Good"
    score = 0
    reason = ""
    genius = ""

    
    while True:
        
        DrawBoard(hexagons, score, guess, level, doneWords, reason, doneWords2, genius)
        
        # find what button was clicked
        returned = getClick(hexagons)
        
        # if New Game was clicked fall out of the loop
        if returned=="New Game":
            return
        
        # if Delete was pressed delete the last letter from the guess
        elif returned=="Delete":
            guess= guess[0:-1]
        
        # if Enter was pressed:    
        elif returned=="Enter":
            
            # if the guess is in solutionWords and has the popLetter and the word wasn't done yet
            if (guess in solutionWords) and (popLetter in guess) and (guess not in doneWords and guess not in doneWords2):
                # add 7 points for words with 7 or more letters
                if len(guess)>=7:
                    score+=7
    
                    # add to doneWords if there are 23 words to get max 24 in each column
                    if len(doneWords)<=23:
                        doneWords+=[guess]
                    
                    # add the second column words to the second list, doneWords2    
                    # make sure that the max number of words found is 48 to fit in board
                    elif len(doneWords)>23 and len(doneWords2) <=23:
                        doneWords2+=[guess]
                    
                    # set the guess and reason why wrong to empty strings    
                    guess=""
                    reason = ""                    
                
                # if the guess has less than 7 letters add one point to the score   
                elif len(guess)>=4 and len(guess) < 7:
                    score+=1
                    
                    # add first column words to doneWords                    
                    if len(doneWords)<=23:
                        doneWords+=[guess]
                        # add second column words to doneWords2
                    elif len(doneWords)>23 and len(doneWords2) <=23:
                        doneWords2+=[guess]
                    reason = ""
                    guess = ""                    
                    
            # add explanations for why wrong
            # if the word is too short
            elif len(guess)<4:
                reason = "Too short"
                guess = ""
            # if the guess isn't a word but uses popLetter
            elif guess not in solutionWords and popLetter in guess:
                reason = "Word not found"
                guess = ""
            # if the guess didn't have the middle letter
            elif popLetter not in guess:
                reason = "Need to use middle letter"
                guess = ""
            # if the guess was already guessed
            elif guess in doneWords or doneWords2:
                reason = "Word already found"
                guess = ""
                    
            # update the variables for the level based on the new score
            if score < 10:
                level = "Good"
            elif score >= 10 and score <20:
                level = "Excellent"
            elif score >= 20:
                level = "Genius!"
                # if hit level genius this variable will display
                genius = "Congrats! You're a Genius!"
        
        # if a letter was pressed add the letter to guess       
        else:
            # limit the guess to 10 letters so it doesn't go off the textbox
            if len(guess)<11:
                guess+=returned
            
        DrawBoard(hexagons, score, guess, level, doneWords, reason, doneWords2, genius)

def main():
    # set the canvas size and color
    Draw.setCanvasSize(800, 800)
    Draw.setBackground(Draw.YELLOW)
    
    # open the dictionary file
    fin = open("ospd.txt")
    # initiate a list to put all the words into
    allWords = []
    
    # add each line to a list of allWords
    line = fin.readline()
    while line:
        allWords+=[line.upper()]
        line = fin.readline()
    fin.close()
    
    # initiate a variable for the letter placeholder in hexagons
    letter = ""
    
    # 2D list of each hexagon with pre-caluculated points to use as centers
    hexagons=[[332.5, 361.0288568, letter],
              [400, 322.0577136, letter],
              [467.5, 361.028856, letter],
              [467.5, 438.9711432, letter],
              [400, 477.9422864, letter],
              [332.5, 438.9711432, letter],
              [400, 400, letter]]    
    
    score = 0  # initiate game score variable
    guess = "" # intitiate empty string for the guess
    level  = "Good"  # initiate the level to good
    doneWords = []   # list of doneWords
    doneWords2= []   # second list of done words if need to go to second column
    reason = ""      # initiate reason why guess was wrong string
    genius = ""      # empty string only filled if hit genius level
    
    validWords = loadDictionary(allWords)   # list of all words with at least 4 letters
    candidates = buildCandidates(validWords)  # list of seven letter words with seven different letters
    
    # shuffle the candidates list every time the game is played so different word every time
    random.shuffle(candidates)
    
    # forever loop through this - new iteration every time New Game is pressed
    while True:
        # choose a word for the seven letter word
        for i in range(len(candidates)):
            candidateWord = candidates[i]  # the seven letter word chosen is the next word in the newly shuffled list
            solutionWords = getSolutionWords(candidateWord, validWords)  # find the solutionWords for the candidate word
            popLetter = mostPopLetter(solutionWords)  # find the most popular letter
            playGame(candidateWord, solutionWords, popLetter, hexagons)
        
main()
    
