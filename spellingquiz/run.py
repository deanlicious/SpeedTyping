import pygame
from spellingquiz.apilogin import *
import random
import time
import cv2
import sys
import datetime
from pygame.locals import *
import os
import json
import pathlib

pygame.init()

FPS = 30
FramePerSec = pygame.time.Clock()
cap0 = cv2.VideoCapture(0)
#cap1 = cv2.VideoCapture(1)


#create a
completedTests = 0

newpath = str(pathlib.Path(__file__).parent.absolute()) + r'\data\testing'
while os.path.exists(newpath + str(completedTests) ):
    completedTests += 1
newpath = newpath + str(completedTests)
os.makedirs(newpath)


WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

color = pygame.Color('dodgerblue2')
fontSize = 32
font = pygame.font.Font(None, fontSize)

DisplayWidth = 600
DisplayHeight = 600

DISPLAYSURF = pygame.display.set_mode((DisplayWidth, DisplayHeight), pygame.RESIZABLE)
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption('Spelling Game')

def reddit_scrapper(reddit):
    subreddit = reddit.subreddit('python')
    reddittitles = []
    hot_python = subreddit.hot()
    for submission in hot_python:
        if not submission.stickied:
            removeNonString = ''.join([i if ord(i) < 128 else ' ' for i in submission.title])
            reddittitles.append(removeNonString)
    return  reddittitles



allRedditTexts = reddit_scrapper(reddit)



def fresh_game(completedTests, reddit, allRedditTexts):
    #set all variable back to normal
    newpath = str(pathlib.Path(__file__).parent.absolute()) + r'\data\typingtest'
    i = 0
    while os.path.exists(newpath + str(completedTests)):
        completedTests += 1
    newpath = newpath + str(completedTests)
    os.makedirs(newpath)
    currentUserLocation = 0
    logger = ''
    longtext = random.choice(allRedditTexts)
    jsonData = {
        'text': longtext,
        'datetime': datetime.datetime.now(),
        'typeData': []
    }
    start = datetime.datetime.now()
    text = ''
    typeDataWord = []
    filename = newpath + '/spellingQuiz-' + datetime.datetime.now().strftime("%Y-%m-%d@%H#%M#%S") + '.txt'

    freshgame = {
        'newpath' : newpath,
        'currentUserLocation': currentUserLocation,
        'logger' : logger,
        'jsonData' : jsonData,
        'typeDataWord' : typeDataWord,
        'start' : start,
        'filename' : filename,
        'longtext' : longtext,
        'i' : i,
        'text' : text
    }
    return freshgame

class gameClass():
    #class to hold all of the game data and allow you to refresh the game
    pass



def blit_text(surface, text, pos, font, currentuserlocation, color=pygame.Color('green')):
    #https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    upto = 0
    currentword = []
    for line in words:
        for word in line:
            upto += 1
            if upto > currentuserlocation:
                currentword.append(word)
                color = pygame.Color('black')

            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
    if currentword:
        return currentword[0]
    else:
        return ''



currentUserLocation = 0
logger = ''


typeDataWord = []

filename = newpath + '/spellingQuiz-'+ datetime.datetime.now().strftime("%Y-%m-%d@%H#%M#%S") + '.txt'
startgame = True

rectangle = [[50, 50], [200, 200]]

while startgame:
    ret, frame = cap0.read()
    cv2.rectangle(frame, (rectangle[0][0], rectangle[0][1]), (rectangle[1][0], rectangle[1][1]), (255, 0, 0), 4)
    cv2.imshow('setup', frame)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                cv2.destroyAllWindows()

                startgame = False
            if event.key == pygame.K_w:
                #move box up
                rectangle[0][1] -= 10
                rectangle[1][1] -= 10
            if event.key == pygame.K_s:
                # move box down
                rectangle[0][1] += 10
                rectangle[1][1] += 10
            if event.key == pygame.K_a:
                # move box left
                rectangle[0][0] -= 10
                rectangle[1][0] -= 10
            if event.key == pygame.K_d:
                # move box right
                rectangle[0][0] += 10
                rectangle[1][0] += 10
            if event.key == pygame.K_q:
                # make box taller
                rectangle[0][0] -= 10
            if event.key == pygame.K_z:
                # make box shorter
                rectangle[0][0] += 10
            if event.key == pygame.K_e:
                # make box wider
                rectangle[1][1] -= 10
            if event.key == pygame.K_c:
                # make box thinner
                rectangle[1][1] += 10





start = datetime.datetime.now()
text = ''

refreshgame = fresh_game(completedTests, reddit, allRedditTexts)

jsonData = {
    'text' : refreshgame['longtext'],
    'datetime' : datetime.datetime.now(),
    'keyboard_location' : rectangle,
    'typeData' : []
}

def build():
    '''this function is currently a stopgap,
    eventually to be turned into building spellingquiz'''
    pass

while True:  # making a loop
    ret, frame = cap0.read()
    #ret, frame = cap1.read()


    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:


            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                print(text , currentWord)


                if text == currentWord:
                    jsonData['typeData'].append(typeDataWord)
                    refreshgame['currentUserLocation'] += 1
                    text = ''
                    logger = ''
                    typeDataWord = []


            elif event.key ==  pygame.K_BACKSPACE:
                if len(text)>0:
                    start = refreshgame['start']
                    logger += f'[{datetime.datetime.now()-start},DELETE]\t'
                    typeDataWord.append([datetime.datetime.now() - start, 'DELETE'])
                    text = text[0:-1]

            else:
                ret0, frame0 = cap0.read()
                #ret1, frame1 = cap1.read()
                if ret0 == True:
                    newpath = refreshgame['newpath']
                    img_name = f"{newpath}/{int(round(time.time() * 1000))}{event.unicode}"
                    img_name0 = img_name +'.png'
                    #img_name1 = img_name + 'b.png'
                    cv2.imwrite(img_name0, frame0)
                    #scv2.imwrite(img_name1, frame1)


                logger += f'[{datetime.datetime.now()-start}, {event.unicode}]\t'
                typeDataWord.append([datetime.datetime.now()-start, event.unicode])
                text += event.unicode


    DISPLAYSURF.fill((WHITE))
    currentWord = blit_text(DISPLAYSURF, refreshgame['longtext'], (20,20),font,refreshgame['currentUserLocation'])
    txt_current = font.render(text, True, color)
    txt_spell_word = font.render(currentWord,True,color)


    DISPLAYSURF.blit(txt_current,(DisplayWidth//2,5*DisplayHeight//6))
    DISPLAYSURF.blit(txt_spell_word, (DisplayWidth // 2, 2*DisplayHeight // 3))

    pygame.display.flip()
    FramePerSec.tick(FPS)

    if currentWord == '':
        print(f'total time: {datetime.datetime.now()-start}')
        with open(newpath+r'\dataSet' +  '.json','w+', encoding='utf-8' ) as f:
            jsonData['text'] = refreshgame['longtext']
            jsonData['datetime'] = datetime.datetime.now()
            json.dump(jsonData, f, ensure_ascii=False, indent=4 , default=str)
            jsonData['typeData'] = []
        refreshgame = fresh_game(completedTests, reddit, allRedditTexts)





pygame.quit()
sys.exit()
cap0.release()
out.release()
cv2.destroyAllWindows()