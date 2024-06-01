import pygame as pg
from handUtil import checkHand
import random
pg.font.init()
BACKGROUND_IMAGE = "assets//wallpaper.jpg"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 200, 200)
GREEN = (100, 200, 50)
MAIN_FONT = pg.font.SysFont("ariel", 44)

DISCARD_LIMIT = 3
HANDS_LIMIT = 4
HANDS_PLAYED = 0
DISCARDS_USED = 0
DECK_LENGTH = 52
TARGET_SCORE = 50

SUITS = ['Hearts', "Clubs", "Diamonds", "Spades"]
RANKS = ['A', 2, 3, 4, 5, 6, 9, 9, 10, 10, 10, 'Q', 'K' ]

HAND_ARRAY = []  #hand that player plays or discards (up to 5 cards)
CARDS_DEALT = [] #cards removed from the deck 
DECK = [] #main deck with 52 cards       
DISCARD_PILE = [] #cards that are submitted or discarded 
CARDS_SELECTED = 0
CARDS_SELECTED_STORAGE = []
MULT = {'Straight Flush': 5, 'Full House': 3.5, 'Four of a Kind': 4,'Flush': 3, 'Straight':2.5, 'Three of a Kind': 2, 'Two Pair': 1.4, 'One Pair': 1.2, 'High Card': 1, "Select Cards": 0}
BEST_HAND = ""
TOTAL_SCORE = 0

def changeImageCard(rank, suit):
    fileName = str(rank) + '_of_' + str(suit) + '.png'
    cardImage = pg.image.load("assets//PNGcards//" + fileName)
    return pg.transform.scale(cardImage, (50, 80))

def addToCardsTable(selectedCard):
    global CARDS_DEALT
    CARDS_DEALT.append(selectedCard)
    #print( len(CARDS_DEALT))

def removeCardsFromTable(selectedCard):
    global CARDS_DEALT
    CARDS_DEALT.remove(selectedCard)

class Card(pg.sprite.Sprite):
    #cardback attribute for deck
    card_back_image = pg.image.load("assets/cardback.jpg")
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
        global CARDS_SELECTED_STORAGE

        if self.mouse_clicked():
            # When selected card is selected again, return to its original position
            if self.is_selected: #when selected attribute is true, change it false from click 
                self.is_selected = False
                HAND_ARRAY.remove(self)
                CARDS_SELECTED -= 1
                CARDS_SELECTED_STORAGE.remove(self)
                addToCardsTable(self)
                self.rect.topleft = self.original_pos
            # If card is being selected, move to selection area
            else:
                # Checks if max hand limit(5) is reached
                if CARDS_SELECTED >= 5:
                    return
                # Only allows user to select from cards on table or hand (not deck)
                if self in HAND_ARRAY or (self in CARDS_DEALT):
                    self.is_selected = True
                    HAND_ARRAY.append(self)
                    CARDS_SELECTED_STORAGE.append(self)
                    CARDS_SELECTED += 1
                    self.rect.topleft = (200 + (CARDS_SELECTED - 1) * 65, 100)

        # Adjust position when mouse is over
        if self.mouse_over() :
            if not self.is_hovered or self in CARDS_SELECTED_STORAGE:
                self.rect.move_ip(0, self.hover_offset)
                self.is_hovered = True
                #self.rect.move_ip(0, -15)  # Increase height position by 15 pixels
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
            self.rect.topleft = (250 + HAND_ARRAY.index(self) * 65, 100) #position of selected cards 
            self.update_image()

        if self in CARDS_DEALT or self in HAND_ARRAY:
            self.update_image()
            
        else:
            self.image = pg.transform.scale(Card.card_back_image, (50, 80))
            #self.image.fill(RED)
             

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
        self.fps = 30       
        self.last_click_time = 0 
        self.game_over = False

         # Load the background image
        self.background_image = pg.image.load(BACKGROUND_IMAGE)
        self.background_image = pg.transform.scale(self.background_image, self.screen.get_size())
        self.all_sprites = pg.sprite.Group()    
       
        # create cards
        self.create_deck()
        random.shuffle(DECK)
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
            #create cards for the player hand 
            newCard = Card(self, pos, i, drawnCard.suit, drawnCard.rank)
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
        self.discard_button = Button(self, width, height, "Discard", self.discard_pressed, self.discard_button_image, self.discard_button_rect, self.discard_button_rect.center)

    def events(self):
        self.mouse_pressed = 0
        self.mouse_pos = pg.mouse.get_pos()
        current_time = pg.time.get_ticks()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if current_time - self.last_click_time > 200:  # Check the cooldown of half a second in between clicks 
                    self.last_click_time = current_time  # Reset the cooldown timer
                    self.last_button_click_time = 0  # Button-specific cooldown timer
                    self.mouse_pressed = event.button
            elif event.type == pg.KEYDOWN :
                print("testtesttesttest")
                self.game_over = False
                self.reset_game_state()
   
    def update(self):
        self.all_sprites.update()
    
    def draw(self):
        global BEST_HAND
        self.screen.blit(self.background_image, (0, 0))  # Blit the background image
        #self.screen.fill(GREEN)
        self.all_sprites.draw(self.screen) 
        BEST_HAND = checkHand(HAND_ARRAY)
        self.blit_text_center(self.screen, MAIN_FONT, BEST_HAND)
        self.draw_score()  # Draw the score in the top left corner
        self.render_deck_count()  # render deck count
        self.render_limits() #hands/discards left
        pg.display.update()
    
   
    def blit_text_center(self, win, font, text):
        render = font.render(text, 1, (200,200,200))
        #get half the text width to adjust for centering
        win.blit(render, (win.get_width()/2 - render.get_width() /
                      2, win.get_height()/2 - render.get_height()/2))
        
    def submit_hand(self):
        global CARDS_SELECTED
        global HANDS_PLAYED 
        
        HANDS_PLAYED += 1  
        self.score_cards()
        self.discard_cards() # Remove cards from hand and add to discard pile
        self.check_score()

        #blit_text_center(WIN, MAIN_FONT, f"Press Any Key To Start Level {game_info.level} ")
        #pg.display.update()
        #for event in pg.event.get():
            #if event.type == pg.QUIT:
                #pg.quit()
                #break
            
            #if event.type == pg.KEYDOWN:
                #self.reset_game_state()
        if HANDS_PLAYED >= 999999:
            self.game_over = True
            print("game over")
            self.reset_game_state()
            self.show_game_over_screen()
            return
            
        pg.display.update()
        #HAND_ARRAY.clear()
        print(len(DECK))
    
    def draw_score(self):
        score_text = f"Score: {TOTAL_SCORE} / {TARGET_SCORE}"
        score_surface = MAIN_FONT.render(score_text, True, WHITE)
        self.screen.blit(score_surface, (10, 10))

    def render_deck_count(self):
        deck_count_text = f"{len(DECK)} / {DECK_LENGTH}"
        font = pg.font.SysFont("Ariel", 24)
        text_surface = font.render(deck_count_text, True, WHITE)
        self.screen.blit(text_surface, (100, 470))  # Adjust the position as needed

    def render_limits(self):
        hands_limit_text = f"Hands Left: {HANDS_LIMIT -HANDS_PLAYED}"
        discard_limit_text = f"Discards Left: {DISCARD_LIMIT - DISCARDS_USED}"
        font = pg.font.SysFont("Ariel", 28)

        hands_limit_surface = font.render(hands_limit_text, True, WHITE)
        discard_limit_surface = font.render(discard_limit_text, True, WHITE)

        hands_limit_rect = hands_limit_surface.get_rect(topright=(self.screen.get_width() - 20, 10))
        discard_limit_rect = discard_limit_surface.get_rect(topright=(self.screen.get_width() - 20, 60))

        self.screen.blit(hands_limit_surface, hands_limit_rect)
        self.screen.blit(discard_limit_surface, discard_limit_rect)
   
    def score_cards(self):
        global TOTAL_SCORE
        totalScore = 0
        multi = MULT.get(BEST_HAND)
        #print("mult is " + str(multi))
        for card in HAND_ARRAY:
            TOTAL_SCORE += card.value 
       
        totalScore *= multi    
    def check_score(self):
        global TOTAL_SCORE, TARGET_SCORE

        if TOTAL_SCORE >= TARGET_SCORE:
            self.reset_game_state()
       

    def reset_game_state(self):
        global HANDS_PLAYED, DISCARDS_USED, TOTAL_SCORE, DECK, HAND_ARRAY, CARDS_DEALT, DISCARD_PILE, CARDS_SELECTED, CARDS_SELECTED_STORAGE, BEST_HAND
        #reset game vars
        HANDS_PLAYED = 0
        DISCARDS_USED = 0
        TOTAL_SCORE = 0
        HAND_ARRAY = []
        CARDS_DEALT = []
        DISCARD_PILE = []
        CARDS_SELECTED = 0
        CARDS_SELECTED_STORAGE = []
        BEST_HAND = ""

        # Recreate and shuffle the deck
        DECK = []
        self.create_deck()
        #DECK = DISCARD_PILE + HAND_ARRAY + CARDS_DEALT + DECK
        random.shuffle(DECK)

        # Clear the sprite group and recreate the cards
        self.all_sprites.empty()
        self.deal_cards()
        self.createButtons()

    def show_game_over_screen(self):
        print("in game over function")
        self.screen.fill(BLACK)
        game_over_text = "Game Over"
        prompt_text = "Press any key to continue"
        font = pg.font.SysFont("Ariel", 64)
        prompt_font = pg.font.SysFont("Ariel", 32)

        game_over_surf = font.render(game_over_text, True, WHITE)
        prompt_surf = prompt_font.render(prompt_text, True, WHITE)

        game_over_rect = game_over_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        prompt_rect = prompt_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))

        self.screen.blit(game_over_surf, game_over_rect)
        self.screen.blit(prompt_surf, prompt_rect)
        
        pg.display.update()
    
    def discard_pressed(self):
        global DISCARDS_USED

        if DISCARDS_USED >= DISCARD_LIMIT : return
        DISCARDS_USED += 1
        self.discard_cards()
         
    def discard_cards(self):
         global CARDS_SELECTED 
         global DISCARDS_USED

         for card in HAND_ARRAY:
            DISCARD_PILE.append(card)
            
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
            if HANDS_PLAYED >= HANDS_LIMIT:
                print("in break")
                self.show_game_over_screen()
                #self.reset_game_state()
                self.events()
                continue
                #self.draw()
            self.clock.tick(self.fps)
            self.events()        
            self.update()
            
            


            self.draw()        
        pg.quit() 

class Button(pg.sprite.Sprite):
    button_red = pg.image.load("assets/redBackground.jpg")
    def __init__(self, game, width, height, text, callback, img, rect, center):
        super().__init__(game.all_sprites)
        self.game = game
        #change position of text
        self.width = width
        self.height = height 
        self.text = text
        self.callback = callback
        self.font = pg.font.SysFont("Ariel", 30)
        self.image = img
        self.rect = rect
        self.rect.center = center
        # Blue 
        self.color = (0, 0, 255)  
        self.render_text()
    
    def render_text(self):
         # Blit the button background image
        background_image = pg.transform.scale(Button.button_red, (self.width, self.height))
        self.image.blit(background_image, (0, 0))
        
        text_surf = self.font.render(self.text, True, WHITE)
        # text pos
        text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surf, text_rect)
    
    def update(self):
        self.check_click()
    
    #added timer on button clicks since sumbit_hand() was being called multiple times on single button clicks 
    def check_click(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()
        current_time = pg.time.get_ticks()
        if self.rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            if current_time - self.game.last_button_click_time > 1000:  # check if over 1 second has elapsed since last button click 
                self.game.last_button_click_time = current_time  # Reset the button cooldown timer
                self.callback()
        
if __name__ == '__main__':
    g = Game()
    g.run()