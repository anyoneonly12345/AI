import random
import math
import copy
class Problem:
    def __init__(self, id, capacity, num_items, optimal_solution, items):
        self.id = id
        self.capacity = capacity
        self.num_items = num_items
        self.optimal_solution = optimal_solution
        self.items = items
class Item:
    def __init__(self, id, weight):
        self.id = id
        self.weight = weight
class Bin:
    def __init__(self,capacity):
        self.items = []
        self.cap_left = capacity
    def add_item(self, item):
        self.items.append(item)
        self.cap_left -= item.weight
    def can_fit(self, item):
        return item.weight <= self.cap_left
    def remove_item(self, item):
        self.items.remove(item)
        self.cap_left += item.weight
    def isempty(self):
        return len(self.items) == 0
class Solution:
    def __init__(self, problem, bins):
        self.problem= problem
        self.bins = bins
        self.bins_number = len(bins)
global best_solution
best_solution = None
        
def evaluate(solution):
    if solution.bins_number- solution.problem.optimal_solution == 0:
        return 1000
    elif solution.bins_number- solution.problem.optimal_solution == 1:
        return 100
    elif solution.bins_number- solution.problem.optimal_solution == 2:
        return 50
    elif solution.bins_number- solution.problem.optimal_solution == 3:
        return 20
    elif solution.bins_number- solution.problem.optimal_solution == 4:
        return 5
    elif solution.bins_number- solution.problem.optimal_solution == 5:
        return 2
    else:
        return 1
def repair(solution):

    packed_items = set()
    for bin in solution.bins:
        for item in bin.items:
            if item in packed_items:
                bin.remove_item(item)
            else:
                packed_items.add(item)
    solution.bins.sort(key=lambda bin: bin.cap_left, reverse=True)
    i = 0
    while i < len(solution.bins) - 1:
        bin1 = solution.bins[i]
        bin2 = solution.bins[i + 1]
        if bin1.cap_left + bin2.cap_left >= solution.problem.capacity:
            for item in bin2.items:
                bin1.add_item(item)
            solution.bins.remove(bin2)
        else:
            i += 1
    return solution 
population_size = 8
mutation_rate = 0.3
num_generations = 10
def crossover(parent1, parent2):
    spelit_point = random.randint(1, len(parent1.bins)-1)
    child1 =copy.deepcopy(parent1)
    child2 =copy.deepcopy(parent2)
    child1.bins =copy.deepcopy(parent1.bins) + copy.deepcopy(parent2.bins[spelit_point:])
    child2.bins =copy.deepcopy(parent2.bins) + copy.deepcopy(parent1.bins[spelit_point:])
    child1 = repair(child1)
    child2 = repair(child2) 
    return child1, child2
def mutate(solution, mutation_rate):
    if random.random() < mutation_rate:
        solution=swap_items(solution)
    return solution
def genetic_algorithm(solution,population_size, mutation_rate, num_generations):
    best_solution = solution
    population = [random_solution(solution) for _ in range(population_size-1)]+[solution]
    for _ in range(num_generations):
        fitnesses = [evaluate(solution) for solution in population]
        parents = random.choices(population, weights=fitnesses, k=population_size)
        offspring = []
        for i in range(0, population_size, 2):
            offspring1, offspring2 =crossover(parents[i], parents[i+1])
            if offspring1.bins_number < best_solution.bins_number:
                best_solution = offspring1
            if offspring2.bins_number < best_solution.bins_number:
                best_solution = offspring2
            offspring1 = mutate(offspring1, mutation_rate)
            offspring2 = mutate(offspring2, mutation_rate)
            offspring.append(offspring1)
            offspring.append(offspring2)
        population = offspring


    return best_solution
def greedy_search(problem):
    bins = []
    for item in sorted(problem.items, key=lambda x: x.weight, reverse=True):
        best_bin = None
        min_waste = float('inf')

        for bin in bins:
            if bin.can_fit(item):
                waste = bin.cap_left - item.weight
                if waste < min_waste:
                    min_waste = waste
                    best_bin = bin

        if best_bin is None:
            new_bin = Bin(problem.capacity)
            new_bin.add_item(item)
            bins.append(new_bin)
        else:
            best_bin.add_item(item)

    return Solution(problem, bins)


start_temperature = 100
end_temperature = 0.1
cooling_rate = 0.99



def simulated_annealing(solution):
    best_solution = solution
    current_solution = copy.deepcopy(solution)
    temperature = start_temperature

    while temperature > end_temperature :
        neighbor_solution = swap_items(current_solution)
        cost_diff =neighbor_solution.bins_number - current_solution.bins_number
        if cost_diff < 0:
            current_solution = neighbor_solution
            if neighbor_solution.bins_number < best_solution.bins_number:
                best_solution = neighbor_solution
        else:
            probability = math.exp(-cost_diff / temperature)
            if random.random() < probability:
                current_solution = neighbor_solution
        temperature *= cooling_rate
    return best_solution
def random_solution(solution):
    random.shuffle(solution.problem.items)
    new_solution = first_fit(solution.problem)
    return new_solution
def swap_items(solution):
    copy_solution = copy.deepcopy(solution)
    sorted_bins = sorted(copy_solution.bins, key=lambda bin: bin.cap_left,reverse=True)
    bin1 = sorted_bins[0]
    Itemlist = bin1.items
    copy_solution.bins.remove(bin1)
    sorted_bins.remove(bin1)
    selected_bins = sorted_bins[:10]
    bin2,bin3 = random.sample(selected_bins,2)
    if bin2.cap_left < bin3.cap_left:
        bin2,bin3 = bin3,bin2
    for item1 in bin2.items:
        for item2 in bin3.items:
            if item1.weight > item2.weight:
                bin2.remove_item(item1)
                bin3.remove_item(item2)
                if bin3.can_fit(item1) :
                    bin2.add_item(item2)
                    bin3.add_item(item1)
                    break
                else:
                    bin2.add_item(item1)
                    bin3.add_item(item2)
                    break
    for item in Itemlist:
        item_placed = False

        for bin in copy_solution.bins:
            if bin.can_fit(item):
                bin.add_item(item)
                item_placed = True
                break

        if not item_placed:
            new_bin = Bin(copy_solution.problem.capacity)
            new_bin.add_item(item)
            copy_solution.bins.append(new_bin)
        
    return copy_solution
    
def first_fit(problem):
    bins = []

    for item in problem.items:
        item_placed = False

        for bin in bins:
            if bin.can_fit(item):
                bin.add_item(item)
                item_placed = True
                break

        if not item_placed:
            new_bin = Bin(problem.capacity)
            new_bin.add_item(item)
            bins.append(new_bin)

    return Solution(problem, bins)


def best_fit(problem):
    bins = []

    for item in problem.items:
        best_bin = None
        min_waste = float('inf')

        for bin in bins:
            if bin.can_fit(item):
                waste = bin.cap_left - item.weight
                if waste < min_waste:
                    min_waste = waste
                    best_bin = bin

        if best_bin is None:
            new_bin = Bin(problem.capacity)
            new_bin.add_item(item)
            bins.append(new_bin)
        else:
            best_bin.add_item(item)

    return Solution(problem, bins)
    


def read_bin_packing_file(filename):
    with open(filename, 'r') as file:
        num_problems = int(file.readline())
        problems = []
        for _ in range(num_problems):
            problem_id = file.readline().strip()
            capacity, num_items, optimal_solution = map(int, file.readline().split())
            items = []
            for i in range(num_items):
                item= Item(i, int(file.readline().strip()))
                items.append(item)
            problem = Problem(problem_id, capacity, num_items, optimal_solution, items)
            problems.append(problem)
    return problems
def main():
    problems = read_bin_packing_file(r"C:\Users\scyth1\Desktop\AI method\binpack1.txt")
    for problem in problems:
        
        print(problem.id)
        #best_solution = first_fit(problem)
        best_solution = greedy_search(problem)
        best_solution= genetic_algorithm(best_solution,population_size, mutation_rate, num_generations)
        #best_solution = simulated_annealing(best_solution)
        print(best_solution.bins_number)
        print(problem.optimal_solution- best_solution.bins_number)
        #for bin in best_solution.bins:
            #print(bin.cap_left)
            #print([item for item in bin.items])
            #print(' '.join(str(item.weight) for item in bin.items))
if __name__ == '__main__':
    main()