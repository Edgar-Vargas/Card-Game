import pygame as pg
from handUtil import checkHand, checkForStraight, checkForFlush
pg.font.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 200, 200)
GREEN = (100, 200, 50)
MAIN_FONT = pg.font.SysFont("comicsans", 44)

DISCARD_LIMIT = 3
HANDS_LIMIT = 4

SUITS = ['Hearts', "Clubs", "Diamonds", "Spades"]
RANKS = ['A', 2, 3, 4, 5, 6, 9, 9, 10, 10, 10, 'Q', 'K' ]

HAND_ARRAY = []
CARDS_DEALT = []
DECK = []
DISCARD_PILE = []
CARDS_SELECTED = 0
MULT = {'Straight Flush': 5, 'Full House': 3.5, 'Four of a Kind': 4,'Flush': 3, 'Straight':2.5, 'Three of a Kind': 2, 'Two Pair': 1.4, 'One Pair': 1.2, 'High Card': 1, "Select Cards": 0}
BEST_HAND = ""

def changeImageCard(rank, suit):
    fileName = str(rank) + '_of_' + str(suit) + '.png'
    cardImage = pg.image.load("assets//PNGcards//" + fileName)
    return pg.transform.scale(cardImage, (50, 80))

def addToCardsTable(selectedCard):
    global CARDS_DEALT
    CARDS_DEALT.append(selectedCard)
    print( len(CARDS_DEALT))

def removeCardsFromTable(selectedCard):
    global CARDS_DEALT
    CARDS_DEALT.remove(selectedCard)

class Card(pg.sprite.Sprite):
    def __init__(self, game, position, number, suit, rank):
        super().__init__(game.all_sprites)
        self.game = game
        self.image = pg.Surface((50, 80))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.number = number

        self.original_pos = position
        self.is_selected = False
        self.suit = suit
        self.value = rank      
        self.compareRank = rank
        self.tablePos = position

        self.width, self.height = 50, 80  # Original size
        self.hover_width = 70  # Width when hovered

        self.hover_offset = -15  # Offset to move up by 15 pixels when hovered
        self.is_hovered = False  # Track hover state

        #used for back end caomparisons (different from visual rank)
        self.rank = rank
        if self.compareRank == 'A':
            self.compareRank = 1
            self.value = 14
        elif self.compareRank == 'J':
            self.compareRank = 11
            self.value = 11
        elif self.compareRank == 'Q':
            self.compareRank = 12
            self.value = 12
        elif self.compareRank == 'K':
            self.compareRank = 13
            self.value = 13

        #self.update_image()
    def update_image(self):
        card_image = changeImageCard(self.rank, self.suit)
        self.image = pg.transform.scale(card_image, (50, 80))
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def update(self):
        global CARDS_SELECTED

        if self.mouse_clicked():
            # When selected card is selected again, return to its original position
            if self.is_selected:
                self.is_selected = False
                HAND_ARRAY.remove(self)
                CARDS_SELECTED -= 1
                addToCardsTable(self)
                self.rect.topleft = self.original_pos
            # If card is being selected, move to selection area
            else:
                # Checks if max hand limit(5) is reached
                if CARDS_SELECTED >= 5:
                    return
                # Only allows user to select from cards on table or hand (not deck)
                if self in HAND_ARRAY or (self in CARDS_DEALT):
                    HAND_ARRAY.append(self)
                    CARDS_SELECTED += 1
                    self.is_selected = True
                    self.rect.topleft = (200 + (CARDS_SELECTED - 1) * 65, 100)

        # Adjust position when mouse is over
        if self.mouse_over() and not self.is_selected:
            if not self.is_hovered:
                self.rect.move_ip(0, self.hover_offset)
                self.is_hovered = True
        elif self.is_hovered and not self.is_selected:
            if self in HAND_ARRAY:
                self.rect.topleft = (200 + HAND_ARRAY.index(self) * 65, 100)
            else:
                self.rect.topleft = self.original_pos
            self.is_hovered = False

        # Ensure the position is correct when the card is selected
        if self.is_selected:
            #check if hand array is empty
            if not HAND_ARRAY: return
            self.rect.topleft = (200 + HAND_ARRAY.index(self) * 65, 100)
            self.update_image()

        if self in CARDS_DEALT or self in HAND_ARRAY:
            self.update_image()
        else:
            self.image.fill(RED)

    def mouse_over(self):
        return self.rect.collidepoint(self.game.mouse_pos)
        
    def mouse_clicked(self):
        return self.mouse_over() and self.game.mouse_pressed == 1
    

    #adjust the value score of a card 
    def upgradeCard(self, multFactor = 1, addFactor = 0):
         if multFactor != 1:
             self.value = self.value * multFactor
         if addFactor != 0:
             self.value += addFactor
    
class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((800, 600))
        self.screen_rect = self.screen.get_rect()          
        self.fps = 5       
        self.all_sprites = pg.sprite.Group()    
        # create cards
        self.create_deck()
        self.deal_cards()
        self.createButtons()

    def create_deck(self):
        for s in SUITS:
            for r in RANKS:
                pos = (100, 500 )
                newCard = Card(self, pos, r, s, r)
                DECK.append(newCard)
    def deal_cards(self):            
        for i in range(7):
            pos = (200 + i * 65, 500)
            #remove top of deck list and add to player hand 
            drawnCard = DECK.pop()
            #print(newHandCard.rank)
            #create cards for the player hand 
            newCard = Card(self, pos, i, drawnCard.suit, drawnCard.rank)
            print(newCard.original_pos)
            newCard.tablePos = newCard.original_pos
            addToCardsTable(newCard)
            #add new card to sprite group for displaying 
            self.all_sprites.add(newCard)
  
    #pass over all self props and set them in the button object property vals
    def createButtons(self):
        width = 200
        height = 50
        surf = pg.display.get_surface()
        # Calculate position to center the button
        #screen_rect = game.screen.get_rect()
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        #position button relative to window size
        self.rect.center = (surf.get_width()//2, (surf.get_height() - surf.get_height()//3))
         #create the Submit Hand button
        self.submit_button = Button(self, 200, 50, "Submit Hand", self.submit_hand, self.image, self.rect, self.rect.center)
         # Discard button
        self.discard_button_image = pg.Surface((width, height))
        self.discard_button_rect = self.discard_button_image.get_rect()
        self.discard_button_rect.center = (surf.get_width()//2, surf.get_height()//12)
        self.discard_button = Button(self, width, height, "Discard", self.discard_cards, self.discard_button_image, self.discard_button_rect, self.discard_button_rect.center)

    def events(self):
        self.mouse_pressed = 0
        self.mouse_pos = pg.mouse.get_pos()        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_pressed = event.button
   
    def update(self):
        self.all_sprites.update()
    
    def draw(self):
        global BEST_HAND
        self.screen.fill(GREEN)
        self.all_sprites.draw(self.screen) 
        BEST_HAND = checkHand(HAND_ARRAY)
        self.blit_text_center(self.screen, MAIN_FONT, BEST_HAND)
      
        pg.display.update()
    
   
    def blit_text_center(self, win, font, text):
        render = font.render(text, 1, (200,200,200))
        #get half the text width to adjust for centering
        win.blit(render, (win.get_width()/2 - render.get_width() /
                      2, win.get_height()/2 - render.get_height()/2))
        
    def submit_hand(self):
        global CARDS_SELECTED  
        self.score_cards()
        # Remove cards from hand and add to discard pile
        self.discard_cards()
        #HAND_ARRAY.clear()
        print(len(DECK))

    def score_cards(self):
        totalScore = 0
        multi = MULT.get(BEST_HAND)
        print("mult is " + str(multi))
        for card in HAND_ARRAY:
            totalScore += card.value 
       
        totalScore *= multi    
        print("Score is " + str(totalScore))

    def discard_cards(self):
         global CARDS_SELECTED 
         for card in HAND_ARRAY:
            DISCARD_PILE.append(card)
            #testCount += 1
            #drawn card should replace the card's table position before it was played 
            pos = card.original_pos
            drawnCard = DECK.pop()
            newCard = Card(self, pos, drawnCard.number, drawnCard.suit, drawnCard.rank)
            addToCardsTable(newCard)
            self.all_sprites.add(newCard)
            card.kill()  # Remove the card sprite from the all_sprites group
         HAND_ARRAY.clear()
         CARDS_SELECTED = 0
                
    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(self.fps)
            self.events()        
            self.update()
            self.draw()        
        pg.quit() 

class Button(pg.sprite.Sprite):
    def __init__(self, game, width, height, text, callback, img, rect, center):
        super().__init__(game.all_sprites)
        self.game = game
        #change position of text
        self.width = width
        self.height = height 
        self.text = text
        self.callback = callback
        self.font = pg.font.SysFont("comicsans", 30)
        self.image = img
        self.rect = rect
        self.rect.center = center
        # Blue 
        self.color = (0, 0, 255)  
        self.render_text()
    
    def render_text(self):
        self.image.fill(self.color)
        text_surf = self.font.render(self.text, True, WHITE)
        # text pos
        text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surf, text_rect)
    
    def update(self):
        self.check_click()
    
    def check_click(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            self.callback()
        
if __name__ == '__main__':
    g = Game()
    g.run()