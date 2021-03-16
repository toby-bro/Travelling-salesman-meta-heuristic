from random import randint

class Town:
    def __init__(self, number, TOWN_NUMBER, RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH, all_towns):
        self.ID = number
        self.all_towns = all_towns
        self.TOWN_NUMBER = TOWN_NUMBER
        self.neighbours_pheromone = [1] * TOWN_NUMBER
        self.neighbours_pheromone[self.ID] = -1
        self.x = randint(RADIUS, SCREEN_WIDTH - RADIUS)
        self.y = randint(RADIUS, SCREEN_HEIGHT - RADIUS)
        self.total_destination_pheromone = 0
    
    def sub_total_phero(self, fourmi):
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
        L, possible_towns = self.sub_total_phero(fourmi)
        phero_chosen = randint(1, L[-1] + len(possible_towns))
        if phero_chosen - L[-1] > 0:
            return self.all_towns[possible_towns[phero_chosen - L[-1] - 1]]
        # print('ph', phero_chosen)
        i = 0
        imax = len(L)
        # print(fourmi.iD, self.ID, L, possible_towns)
        while phero_chosen > L[i]:
            if i < imax:
                i += 1
        # # total_pheromone += 1
        # self.neighbours_pheromone[possible_towns[i]] += 1
        # all_towns[possible_towns[i]].neighbours_pheromone[self.ID] += 1
        return self.all_towns[possible_towns[i]]

    def dist(self, othertown):
        return ((self.x - othertown.x)**2 + (self.y - othertown.y)**2)**(0.5)
    
    def most_phero(self):
        # indice = self.neighbours_pheromone.index(max(self.neighbours_pheromone))
        # L = []
        
        # return all_towns[indice]
        L = []
        for i in self.neighbours_pheromone:
            L.append(i)
        
        i = 1
        town_order = self.all_towns[:]
        town_order.pop(self.ID)
        L.pop(self.ID)
        # print(len(L), len(town_order))
        while i < len(L):
            if i == 0:
                i += 1
            elif L[i] > L[i -1]:
                L[i], L[i-1] = L[i-1], L[i]
                town_order[i], town_order[i-1] = town_order[i-1], town_order[i]
                i -= 1
            else:
                i+=1
        # choise = [self.neighbours_pheromone[a.ID] for a in town_order]
        # for a in town_order:
        #     print(self.neighbours_pheromone[a.ID])
        # print(choise)
        return town_order