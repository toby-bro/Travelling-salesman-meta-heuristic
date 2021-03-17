from random import randint

class Town:
    
    def __init__(self, number, TOWN_NUMBER, RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH, all_towns):
        """creates a new Town

        Args:
            number (int): the town's position in the list all_towns
            TOWN_NUMBER (int): total number of Towns
            RADIUS (int): the width of the circles in the interface
            SCREEN_HEIGHT (int): the interface's height
            SCREEN_WIDTH (int): the interface's width
            all_towns (list): list of all the towns that never changes during the program
        """
        self.ID = number
        self.all_towns = all_towns
        self.TOWN_NUMBER = TOWN_NUMBER
        self.neighbours_pheromone = [1] * TOWN_NUMBER
        self.neighbours_pheromone[self.ID] = -1
        self.x = randint(RADIUS, SCREEN_WIDTH - RADIUS)
        self.y = randint(RADIUS, SCREEN_HEIGHT - RADIUS)
        self.total_destination_pheromone = 0
    
    def sub_total_phero(self, fourmi):
        """sends back the towns in which the ant can go next and the cumulated sum of all of the pheromone (L)
        which will be used to determine which is the town that the ant chose randomly

        Args:
            fourmi (Fourmi): the ant of whom we want to determine the next location

        Returns:
            (list): the cumulated sum of all the pheromones by town,
            (list): the different towns the ant can visit
        """
        s = 0
        L = []
        possible_towns = []
        for town_indice in range(self.TOWN_NUMBER):
            if self.all_towns[town_indice] not in (fourmi.memory or fourmi.location):
                s += self.neighbours_pheromone[town_indice]
                possible_towns.append(town_indice)
                L.append(s)
        return L, possible_towns
    
    def next_town(self, fourmi):
        """chooses the next town the ant (fourmi) will visit the

        Args:
            fourmi (Fourmi): the ant of whom we want to determine the next location

        Returns:
            Town: the next destination of the particular ant : fourmi
        """
        L, possible_towns = self.sub_total_phero(fourmi)
        # chooses randomly the next town
        phero_chosen = randint(1, L[-1] + len(possible_towns))
        if phero_chosen - L[-1] > 0:
            return self.all_towns[possible_towns[phero_chosen - L[-1] - 1]]
        i = 0
        imax = len(L)
        
        # procedure to find which town was chosen randomly (after applying the probabilities (determined by the amount of pheromone on the path)
        # of falling on each of the towns)
        while phero_chosen > L[i]:
            if i < imax:
                i += 1
        return self.all_towns[possible_towns[i]]

    def dist(self, othertown):
        """returns the total distance in pixels between two towns on the map
        """
        return ((self.x - othertown.x)**2 + (self.y - othertown.y)**2)**(0.5)
    
    def most_phero(self):
        """sorts out the neighbouring towns by the amount of pheromone on the path leading to them

        Returns:
            list: the towns sorted out by decreasing quantities of pheromones
        """
        # L will be the list of all of the towns pheromone with L[i] the quantity of pheromone leading to town_order[i] form the town (self)
        L = []
        for i in self.neighbours_pheromone:
            L.append(i)
        
        i = 1
        # we don't want an ant to travel to the town on which it is so we forbid the program of sorting the self town with the others
        town_order = self.all_towns[:]
        town_order.pop(self.ID)
        L.pop(self.ID)
        
        # the sorting algorithm
        while i < len(L):
            if i == 0:
                i += 1
            elif L[i] > L[i -1]:
                L[i], L[i-1] = L[i-1], L[i]
                town_order[i], town_order[i-1] = town_order[i-1], town_order[i]
                i -= 1
            else:
                i+=1
        # once the towns are sorted by decreasing quantity of pheromone we return the list that will determine the next most chosen destination from the self town
        return town_order
