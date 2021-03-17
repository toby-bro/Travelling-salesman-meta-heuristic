class Fourmi:
    def __init__(self, number, location, TOWN_NUMBER, SPEED):
        """creates an ant

        Args:
            number (int): ant's iD
            location (Town): place where the ant starts
            TOWN_NUMBER (int): total number of towns
            SPEED (int): the speed at which the ant moves across the map
        """
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
        """moves the ant, checks if it has reached it's destination or otherwise just moves the ant closer to it's destination
        """
        if self.moving:
            self.travel_time += 1
            # the ant moves closer to her destination
            if self.travel_time >= self.total_travel_time:
                # then the ant has reached it's destination
                self.moving = False
                # we add pheromone on the path the ant has just gone through
                self.location.neighbours_pheromone[self.destination.ID] += 1
                self.destination.neighbours_pheromone[self.location.ID] += 1
                self.location = self.destination
        else:
            # if the ant is not moving then we choose her next destination
            self.destination = self.location.next_town(self)
            self.total_travel_time = int(self.destination.dist(self.location))
            self.travel_time = 0
            self.moving = True
            self.update_memory(self.location)
    
    def update_memory(self, newtown):
        """adds newtown to the last towns the ant has visited, in order to forbid it from going to and fro between the same towns

        Args:
            newtown (Town): the last town the ant has been through
        """
        self.memory = self.memory[1:] + [newtown]
