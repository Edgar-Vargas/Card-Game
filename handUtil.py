import pygame
#straight flush
#four of a kind
#full house
#flush
#straight
#three of a kind 
#two pair
#pair
#high card
pygame.font.init()

MAIN_FONT = pygame.font.SysFont("comicsans", 44)

def checkHand(card_list):
    if  len(card_list) == 0:
        return 'Select Cards'
    flush = False
    straight = False
    handText = checkForPairs(card_list)
    #if flush and straight:
        
    return handText

def calcScore(card_list):


    return 111

def blit_text_center(win, font, text):
    render = font.render(text, 1, (200,200,200))
    text_rect = render.get_rect()
    text_rect.center = (300, 300)
    win.blit(render, text_rect)

def checkForStraight(card_list):
    cardsToScore = []
    #sort list by comparison rank value 
    sorted_list = sorted(card_list, key=lambda card: card.compareRank)
    straightCount = 0
    #cant be straight with less than 5 cards selected
    if len(sorted_list) < 5 :
        return False
    for i in range(5):
        currentCard = sorted_list[i]
        #print(currentCard.compareRank)
        #first iteration needs no comparison since its the start of the straight
        if i == 0:
            previous = currentCard.compareRank
            cardsToScore.append(currentCard)
            #print("previous card is " + str(previous))
            straightCount += 1
            continue
        #else:
        #since list is always sorted, value diff should always be 1
        if currentCard.compareRank - previous == 1 or currentCard.compareRank - previous == -1 :
            straightCount += 1
            cardsToScore.append(currentCard)
            previous = currentCard.compareRank

    if straightCount >= 5:
        #print("straight!")
        return True
        #return {True, cardsToScore}
    else:
        return False

def checkForFlush(card_list):
    #cardsToScore = []
    if len(card_list) < 5 :
        return False
    flushCount = 0
    for i in range(5):
        currentCard = card_list[i]
        if i == 0:
            #cardsToScore.update(currentCard)
            previousSuit = currentCard.suit
            flushCount += 1
            continue
        else:
            if currentCard.suit == previousSuit:
                #cardsToScore.update(currentCard)
                flushCount += 1
                previousSuit = currentCard.suit
                continue
            else:
                return False
            
    if flushCount >= 5:
        #print("FLUSH!")
        return True
        #return {True, cardsToScore}

#RETURNS string of best hand
def checkForPairs(card_list):
    cardsToScore = {}
    pair_set = dict()
    pairCount = 0
    noPair = True

    onePair = False
    twoPair = False
    threeOfKind = False
    fourOfKind = False
    fullHouse = False

    for currentCard in card_list:
        #adds card rank to dict while it doesnt exist
        if currentCard.rank not in pair_set:
            pair_set.update({currentCard.rank : 1})
        #iterates existing key value by 1
        else:
            pair_set[currentCard.rank] += 1

        if pair_set[currentCard.rank] == 2:
            onePair = True
            noPair = False
            pairCount += 1
            
        elif pair_set[currentCard.rank] == 3:
            threeOfKind = True
        elif pair_set[currentCard.rank] == 4:
            fourOfKind = True
   
    if pairCount == 2: twoPair = True
    #check for fullhouse, twoPair must be true so threeOfKind doesnt get recognized as a full house by itself
    if threeOfKind and onePair and twoPair : fullHouse = True
    
    straight = checkForStraight(card_list)
    #straight = False
    #flush = False
    flush = checkForFlush(card_list)
    
    straightFlush = straight and flush
    prioList = {'straightFlush': straightFlush, 'fourOfKind': fourOfKind, 'fullHouse': fullHouse, 'flush': flush, 'straight': straight,  'threeOfKind': threeOfKind, 'twoPair': twoPair, 'onePair': onePair, 'noPair': noPair}
    highestPrio = get_prio(prioList)
    #print(highestPrio)
    return formatHandText(highestPrio)
def get_prio(prioList): 
    for prio in prioList:
        if prioList.get(prio) is True: return prio

#hand format helper for displaying to user; since hand types will stay the same 
def formatHandText(handType):
     if handType == "onePair" : return "One Pair"
     elif handType == "noPair" : return "High Card"
     elif handType == "twoPair" : return "Two Pair"
     elif handType == "threeOfKind" : return "Three of a Kind"
     elif handType == "flush" : return "Flush"
     elif handType == "straightFlush" : return "Straight Flush"
     elif handType == "fourOfKind" : return "Four of a Kind"
     elif handType == "fullHouse" : return "Full House"