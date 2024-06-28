import random

from amazed.maze import Maze
from amazed.builder.Builder import Builder
from amazed.solver import flood_fill

class GeneticAlgorithm(Builder):
    
    def __init__(self, maze: Maze, seed: int = None, gif: bool = False, parameters:dict = None, autorun:bool=True) -> None:
        '''
        Class that uses a genetic algorithm to evolve a maze. It heavy relies on the @parameters dictionary, so make
        sure that all values are correct.
        @parameters : {
            "GENERATIONS" : int,
            "INITIAL_POPULATION" : [],
            "INITIAL_POPULATION_MUTATION_CHANCE" : float,
            "POP_SIZE" : int,
            "MUTATION_CHANCE" : float,
            "CROSSOVER_CHANCE" : float,
            "K_ELITISM" : int
        }
        '''
        super().__init__(maze, seed, gif)
        self.gif = gif

        if parameters is None:
            raise RuntimeError(f"[GeneticAlgorithm] You forgot to specify the parameters.")
        
        self.GENERATIONS = parameters["GENERATIONS"]
        self.POPULATION = self.create_population(
            parameters["INITIAL_POPULATION"], 
            parameters["INITIAL_POPULATION_MUTATION_CHANCE"],
            parameters["POP_SIZE"]
        )
        self.POP_SIZE = parameters["POP_SIZE"]
        self.CHROMOSOME_LENGTH = self.maze.rows * (self.maze.columns - 1) + self.maze.columns * (self.maze.rows - 1)
        self.MUTATION_CHANCE = parameters["MUTATION_CHANCE"]
        self.CROSSOVER_CHANCE = parameters["CROSSOVER_CHANCE"]
        self.K_ELITISM = parameters["K_ELITISM"]

        if autorun:
            self.run()
        
    def run(self):
        '''
        Runs the GA algorithm. If needed, this function can be overridden.
        '''

        self.best_individual_all = ''
        self.best_score_all = 0
        self.gen_change = 0

        for gen in range(1, self.GENERATIONS):
            print(f"[ GeneticAlgorithm ][ run ] Generation: {gen} / {self.GENERATIONS+1}")
            scores = []

            for index in range(self.POP_SIZE):
                individual = self.POPULATION[index]
                assert isinstance(individual, list), f"Individual is of type {type(individual)}"
                
                scores.append((index, self.fitness(individual)))

            self.sorted_scores = sorted(scores, key=lambda item: item[1])

            best_current_index = self.sorted_scores[-1][0]
            best_current_score = self.sorted_scores[-1][1]
            best_individual = self.POPULATION[best_current_index]

            if self.best_score_all <= best_current_score:
                self.best_score_all = best_current_score
                self.best_individual_all = best_individual
                self.gen_change = gen

            # Clear previously best population
            self.new_population = []

            self.selection()

            self.crossover()

            self.mutation()

            self.elitism()
                
            if len(self.new_population) != len(self.POPULATION):
                print(*self.new_population, sep="\n")
                raise RuntimeError(f"how did you??")

            self.POPULATION = self.new_population
            if self.gif:
                self.add_frame

        self.maze.reset()
        self.maze.set_wall_bitstring(self.best_individual_all)

    def create_population(self, initial_population:list, mutation_chance:float, pop_size:int) -> list:
        
        # Population is given
        if len(initial_population) > 0:
            if isinstance(initial_population[0], list):
                return initial_population
            else:
                raise RuntimeError(f"[ GeneticAlgorithm ][ create_population ] Individuals from a population must be list objects.")
        
        # No population given, randomly create one based on the bitstring of the maze
        if len(initial_population) == 0:
            population = []
            bitstring = self.maze.get_wall_bitstring()
            bitstring = "".join(bitstring)
            for i in range(pop_size):
                new_bitstring = []
                for j in bitstring:
                    if random.random() < mutation_chance:
                        new_bitstring.append("0") if j == "1" else new_bitstring.append("1")
                    else:
                        new_bitstring.append(j)
                population.append(new_bitstring)
            
            return population
        
        raise RuntimeError(f"[GeneticAlgorithm] Something went wrong with population creation. Population: {population}")

    def fitness(self, idv=list):
        # In the future, this process could be optimized
        # to use only the bitstring without creating a new maze.
        new_maze = Maze(self.maze.rows, self.maze.columns)

        new_maze.set_wall_bitstring(idv)

        intersection_score = 0
        for i in range(new_maze.rows):
            for j in range(new_maze.columns):
                walls = 0
                for wall in (Maze.NORTH, Maze.EAST, Maze.SOUTH, Maze.WEST):
                    if new_maze.data[i][j].walls[wall]:
                        walls += 1
                if walls == 0:
                    intersection_score += -0.1
                if walls == 1:
                    intersection_score += 0.1
                if walls == 2:
                    intersection_score += 0.4
                if walls == 3:
                    intersection_score += 0.2
                if walls == 4:
                    intersection_score += -1

        # M_3
        curr_score = intersection_score / (new_maze.rows * new_maze.columns)
        areas = flood_fill(new_maze)

        # M_5
        curr_score = curr_score + 1 / areas

        return curr_score

    def selection(self):
        total_fitness = sum(_[1] for _ in self.sorted_scores)
        probabilities = [f / total_fitness for _, f in self.sorted_scores]

        cumulative_probabilities = [0]
        cumulative_sum = 0
        for p in probabilities:
            cumulative_sum += p
            cumulative_probabilities.append(cumulative_sum)

        # Selection using roulette wheel
        for i in range(self.POP_SIZE):
            spin = random.random()
            for j in range(self.POP_SIZE):
                if cumulative_probabilities[j] <= spin and spin < cumulative_probabilities[j+1]:
                    self.new_population.append(self.POPULATION[j])
                    break

    def crossover(self):
        for i in range(0, self.POP_SIZE, 2):
            if random.random() < self.CROSSOVER_CHANCE:
                crossover_point = random.randint(1, self.CHROMOSOME_LENGTH-1)

                x = self.new_population[i][:crossover_point] + self.new_population[i+1][crossover_point:]
                y = self.new_population[i+1][:crossover_point] + self.new_population[i][crossover_point:]

                self.new_population[i] = x
                self.new_population[i+1] = y

    def mutation(self):
        for i in range(self.POP_SIZE):
            for j in range(self.CHROMOSOME_LENGTH):
                if random.random() < self.MUTATION_CHANCE:
                    if self.new_population[i][j] == "0":
                        self.new_population[i][j] = "1"
                    elif self.new_population[i][j] == "1":
                        self.new_population[i][j] = "0"
                    else:
                        raise ValueError(f"[ GA ] What :keklmao: {self.new_population[i][j]}")

    def elitism(self):
        for k in range(self.K_ELITISM):
            idv_index = self.sorted_scores[-k][0]
            self.new_population[-k] = self.POPULATION[idv_index]

    def add_frame(self):
        frame = self.maze.export(show=False)
        self.frames.append(frame)
