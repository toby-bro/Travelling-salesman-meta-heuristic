"""
Travelling Sales-man problem
"""

from random import randint
from numpy import exp
import pygame

class Town(pygame.sprite.Sprite):
    def __init__(self, father =  None):
        super().__init__()
        self.son = None
        self.father = father
        self.x = randint(RADIUS, SCREEN_WIDTH - RADIUS)
        self.y = randint(RADIUS, SCREEN_HEIGHT - RADIUS)
    
    def update(self):
        # pygame.draw.line(screen, (100,100,100), (self.x, self.y), (self.son.x, self.son.y), width = 2)
        pygame.draw.circle(screen, (150,150,150), (self.x, self.y), RADIUS, 2)
    

def exchange_path(town_order, first, last):
    if first > last:
        first, last = last, first
    if first == 0 and last == len(town_order):
        town_order[:] = town_order[:: -1]
    elif first == 0:
        town_order[: last + 1] = town_order[last :: -1]
    elif last == len(town_order):
        town_order[first :] = town_order[-1: first - 1 : -1]
    else:
        town_order[first : last + 1] = town_order[last : first - 1 : -1]
    return town_order

def update_screen():
    for town_indice in range(len(order)-1):
        pygame.draw.circle(screen, (150,150,150), (towns[order[town_indice]].x, towns[order[town_indice]].y), RADIUS, 2)
        pygame.draw.line(screen, (100,100,100), (towns[order[town_indice]].x, towns[order[town_indice]].y), (towns[order[town_indice + 1]].x, towns[order[town_indice + 1]].y), width = 2)
    pygame.draw.circle(screen, (150,150,150), (towns[order[-1]].x, towns[order[-1]].y), RADIUS, 2)
    pygame.draw.line(screen, (100,100,100), (towns[order[-1]].x, towns[order[-1]].y), (towns[order[0]].x, towns[order[0]].y), width = 2)

def dist(town1, town2):
    return ((town1.x-town2.x)**2 + (town1.y-town2.y)**2 )**(0.5)

def total_distance_pile():
    total_distance = 0
    for town in towns:
        total_distance += dist(town, town.son)
    return total_distance

def total_distance_orders(town_order, towns):
    total_distance = 0
    for town_indice in range(len(town_order) - 1):
        total_distance += dist(towns[town_order[town_indice]], towns[town_order[town_indice + 1]])
    total_distance += dist(towns[town_order[-1]], towns[town_order[0]])
    return total_distance
    
def heuristic(order, towns):
    first_order = order[:]
    for i in range(1, len(order)-1):
        for j in range(len(order)):
            new_order = order[:]
            new_order[i], new_order[j] = new_order[j], new_order[i]
            if total_distance_orders(new_order, towns) < total_distance_orders(order, towns):
                order = new_order
    if first_order == order:
        print('we are done')
        global test
        test = False
    return order

def meta_heuristic(order, towns, tolerance=0):
    count = 0
    first_order = order[:]
    old_order = order[:]
    for i in range(1, len(order)-1):
        for j in range(len(order)):
            new_order = order[:]
            new_order[i], new_order[j] = new_order[j], new_order[i]
            tot1, tot2 = total_distance_orders(new_order, towns), total_distance_orders(old_order, towns)
            if total_distance_orders(new_order, towns) < total_distance_orders(old_order, towns):
                order = new_order[:]
                count = 0
            elif count == 0 and tot1 < (1 + exp(-tolerance / (NUMBER_OF_TOWNS**2 * 10**5))) * tot2:
                old_order = order[:]
                order = new_order[:]
                count += 1
            else:
                order = old_order[:]
                count = 0
    if first_order == order:
        print('we are done')
        global test
        test = False
    return order

def meta_heuristic2(order, towns, tolerance=0):
    count = 0
    global number_of_tests
    old_order = order[:]
    first_order = order[:]
    for i in range(1, len(order)-1):
        for j in range(len(order)):
            number_of_tests += 1
            new_order = order[:]
            new_order = exchange_path(new_order, i, j)
            tot1, tot2 = total_distance_orders(new_order, towns), total_distance_orders(old_order, towns)
            if total_distance_orders(new_order, towns) < total_distance_orders(old_order, towns):
                order = new_order[:]
                count = 0
            elif count == 0 and tot1 < (1 + exp(-tolerance / (NUMBER_OF_TOWNS**2 * 10**5))) * tot2:
                old_order = order[:]
                order = new_order[:]
                count += 1
            else:
                order = old_order[:]
                count = 0
                
    if first_order == order:
        print('we are done')
        global test
        test = False
        return order
    return order

pygame.init()

NUMBER_OF_TOWNS = 100

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1 * SCREEN_HEIGHT
RADIUS = 6


towns =[Town()]
order = [0]

for town in range(NUMBER_OF_TOWNS - 1):
    towns.append(Town(towns[-1]))
    towns[-2].son = towns[-1]
    order.append(order[-1]+1)

towns[0].father = towns[-1]
towns[-1].son = towns[0]

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))

background = pygame.image.load('carte0.jpg')

running = True
initial_order = order[:]

tolerance = 0
test = True
while running:

    # appliquer l'arrière-plan du jeu
    screen.blit(background, (-200, -200))

    update_screen()
    # mettre à jour l'écran
    pygame.display.flip()
    if test == True:
        order = heuristic(order, towns)
    
    # si je joueur ferme cette fenêtre
    for event in pygame.event.get():
        # que l'evenement est fermeture de fenetre
        if event.type == pygame.QUIT:
            running = False
            # pygame.quit()
            print("Fermeture du prgm 1 ")
    

    
running = True
test = True
order = initial_order[:]
number_of_tests = 0
# on résout le problème avec une méthode meta-heuristique
while running:
    # appliquer l'arrière-plan du jeu
    screen.blit(background, (-200, -200))

    update_screen()
    # mettre à jour l'écran
    pygame.display.flip()
    # order = heuristic(order, towns)
    tolerance += 1
    if test == True:
        order = meta_heuristic2(order, towns, tolerance)
    # si je joueur ferme cette fenêtre
    for event in pygame.event.get():
        # que l'evenement est fermeture de fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture du prgm 3")
    
print(number_of_tests)
        
