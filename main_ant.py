from random import randint
import pygame
from fourmi import Fourmi
from ville import Town


def update_screen(itinerary):
    """given an itinerary this pocedure draws a possible solution starting from the first town (all_towns[0]), can be upgraded to analyse better the data it is feeded

    Args:
        itinerary (list): the towns in the order the computer should go through
    """
    for town_indice in range(len(itinerary)-1):
        pygame.draw.circle(screen, (150,150,150), (itinerary[town_indice].x , itinerary[town_indice].y ), RADIUS, 2)
        pygame.draw.line(screen, (100,100,100), (itinerary[town_indice].x , itinerary[town_indice].y ), (itinerary[town_indice + 1].x , itinerary[town_indice + 1].y ), width = 2)
    pygame.draw.circle(screen, (150,150,150), (itinerary[-1].x , itinerary[-1].y ), RADIUS, 2)
    pygame.draw.line(screen, (100,100,100), (itinerary[-1].x , itinerary[-1].y ), (itinerary[0].x , itinerary[0].y ), width = 2)
    # print("done")

    
def next_screen():
    """
    determines a not to bad itinerary
    """
    itinerary = [all_towns[0]]
    for i in range(TOWN_NUMBER - 1):
        # print(itinerary)
        future = itinerary[-1].most_phero()
        i = 0
        while future[i] in itinerary:
            i += 1
        itinerary.append(future[i])
    update_screen(itinerary)

    
pygame.init()

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1 * SCREEN_HEIGHT
RADIUS = 6

SPEED = 10
TOWN_NUMBER = 20
all_towns = []
ANT_NUMBER = 100000
all_ants = []
total_pheromone = 0

# we create the towns
for town in range(TOWN_NUMBER):
    all_towns.append(Town(town, TOWN_NUMBER, RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH, []))

for town in all_towns:
    # we update the all_towns attribute, so that every town can have access to all of the towns
    town.all_towns = all_towns

# we create the ants
for ant in range(ANT_NUMBER):
    all_ants.append(Fourmi(ant, all_towns[randint(0, TOWN_NUMBER - 1)], TOWN_NUMBER, SPEED))
    

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))

background = pygame.image.load('carte0.jpg')

launched = True

while launched:
    # show the background
    screen.blit(background, (-200, -200))

    # we update the screen
    next_screen()
    pygame.display.flip()
    
    # we move the ants
    for fourmi in all_ants:
        fourmi.move()
       
    # total_pheromone is a counter to determine when the program is to stop by itself
    total_pheromone += 10
    
    if total_pheromone > 1000000:
        launched = False
        
    for event in pygame.event.get():
        # if the event if closing the window
        if event.type == pygame.QUIT:
            launched = False
            pygame.quit()
            print("Fermeture du prgm 1 ")
            
