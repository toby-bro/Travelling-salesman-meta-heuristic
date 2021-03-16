class Fourmi:
    def __init__(self, number, location, TOWN_NUMBER, SPEED):
        self.iD = number
        self.location = location
        self.destination = None
        self.moving = False
        self.speed = SPEED
        self.memory = [self.location] * int(TOWN_NUMBER**(0.5))
        self.memory = self.memory[:]
        self.travel_time = 0
        self.total_travel_time = 0
    
    def move(self):
        if self.moving:
            self.travel_time += 1
            if self.travel_time >= self.total_travel_time:
                self.moving = False
                
                self.location.neighbours_pheromone[self.destination.ID] += 1
                self.destination.neighbours_pheromone[self.location.ID] += 1
                self.location = self.destination
        else:
            # phero_chosen = randint(0, self.location.total_destination_pheromone)
            # total = 0
            # town_id = 0 
            # limit = self.location.total_destination_pheromone
            # while phero_chosen < total and phero_chosen < limit:
            #     total += self.location.neighbours_pheromone[town_id]
            #     town_id += 1
            # self.destination = all_towns[town_id]
            # total_pheromone += 1
            self.destination = self.location.next_town(self)
            self.total_travel_time = int(self.destination.dist(self.location))
            self.travel_time = 0
            self.moving = True
            self.update_memory(self.location)
    
    def update_memory(self, newtown):
        self.memory = self.memory[1:] + [newtown]