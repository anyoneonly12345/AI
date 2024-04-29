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
    def __init__(self, problem,bins):
        self.problem= problem
        self.bins = bins
        self.bins_number = 0
def emptybin_check(solution:Solution):
    for bin in solution.bins:
        if bin.isempty():
            solution.bins.remove(bin)
    return solution
def ShiftStrategy(solution:Solution):
    sorted_bins = [Bin(solution.problem.capacity)]
    sorted_bins = copy.deepcopy(solution.bins)
    sorted_bins = sorted(sorted_bins,key=lambda bin: bin.cap_left)  # sort bins from small left capacity to big left capacity
    for item in sorted_bins[-1].items:
        for bin in sorted_bins:
            if bin.can_fit(item):
                bin.add_item(item)
                sorted_bins[-1].remove_item(item)
                bin.items.sort(key=lambda item: item.weight)
                break
            if sorted_bins[-1].isempty():
                sorted_bins.pop()
                break
    solution.bins = copy.deepcopy(sorted_bins)
    solution.bins_number = len(solution.bins)
    emptybin_check(solution)   #check the empty bin
    return solution
def SplitStrategy(solution:Solution):
    avg_num_item = solution.problem.num_items // len(solution.bins)
    for bin in solution.bins:
        if len(bin.items) > avg_num_item:
            num_split = len(bin.items) // 2
            random.shuffle(bin.items)
            new_bin = Bin(solution.problem.capacity)
            for item in bin.items[:num_split]:
                new_bin.add_item(item)
                bin.remove_item(item)
            bin.items.sort(key=lambda item: item.weight)
            new_bin.items.sort(key=lambda item: item.weight)
            solution.bins.append(new_bin)
    solution.bins_number = len(solution.bins)
    return solution
def Exchange_LBLI(solution:Solution):
    emptybin_check(solution)  # check the empty bin
    flag = False  # successfully exchanged flag
    sorted_bins = copy.deepcopy(solution.bins)
    sorted_bins.sort(key=lambda bin: bin.cap_left)  # sort bins from small left capacity to big left capacity
    unfull_index = []
    for i in range(1, len(sorted_bins)):
        if sorted_bins[i].cap_left > 0:
            unfull_index.append(i)
    target_index = random.choice(unfull_index)
    target_items = []
    target_indexes = []
    can_exchange1 = False
    can_exchange2 = False
    sorted_bins[0].items.sort(key=lambda item: item.weight, reverse=True)
    current_size = sorted_bins[0].items[0].weight
    sum_size = 0
    for i in range(len(sorted_bins[target_index].items)):
        if sorted_bins[target_index].items[i].weight + sum_size <= current_size + sorted_bins[0].cap_left:
            target_items.append(sorted_bins[target_index].items[i])
            target_indexes.append(i)
            sum_size += sorted_bins[target_index].items[i].weight
            can_exchange1 = True
    if sum_size + sorted_bins[target_index].cap_left >= current_size:
        for i in range(len(target_indexes)):
            sorted_bins[target_index].remove_item(sorted_bins[target_index].items[target_indexes[i] - i])
        can_exchange2 = True
    if can_exchange1 and can_exchange2:
        sorted_bins[target_index].add_item(sorted_bins[0].items[0])
        sorted_bins[target_index].items.sort(key=lambda item: item.weight, reverse=True)
        sorted_bins[0].remove_item(sorted_bins[0].items[0])
        for item in target_items:
            sorted_bins[0].add_item(item)
        flag = True
    solution.bins =copy.deepcopy(sorted_bins)
    solution.bins_number = len(solution.bins)
    return solution
def Exchange_randomBin_Reshuffle(solution:Solution):
    emptybin_check(solution)  # check the empty bin
    sorted_bins = sorted(solution.bins, key=lambda bin: bin.cap_left, reverse=True)  # sort bins from big left capacity to small left capacity
    exchangeBin_index1 = 0
    exchangeBin_index2 = 1
    flag = False  # valid exchangeBin_index1 and exchangeBin_index2
    sum_cap_left = 0
    for bin in sorted_bins:
        sum_cap_left += bin.cap_left
    while not flag:
        random_pointer1 = random.randint(1, sum_cap_left)  # the random number is from 1 to sum_cap_left
        random_pointer2 = random.randint(1, sum_cap_left)  # the random number is from 1 to sum_cap_left
        for i in range(len(sorted_bins)):
            random_pointer1 -= sorted_bins[i].cap_left
            if random_pointer1 <= 0:
                exchangeBin_index1 = i
                break
        for i in range(len(sorted_bins)):
            random_pointer2 -= sorted_bins[i].cap_left
            if random_pointer2 <= 0:
                exchangeBin_index2 = i
                break
        if exchangeBin_index1 != exchangeBin_index2:  # If the indexes of the two exchanged Bin are the same, randomly choose two again
            flag = True
    shuffle_count = 200
    whole_items = []
    for item in solution.bins[exchangeBin_index1].items:
        whole_items.append(item)
    for item in solution.bins[exchangeBin_index2].items:
        whole_items.append(item)
    best_exchangeBin1 = Bin(solution.problem.capacity)
    best_exchangeBin2 = Bin(solution.problem.capacity)
    for i in range(shuffle_count):
        exchangeBin1 = Bin(solution.problem.capacity)
        exchangeBin2 = Bin(solution.problem.capacity)
        random.shuffle(whole_items)
        for j in range(len(whole_items)):
            if whole_items[j].weight <= exchangeBin1.cap_left:
                exchangeBin1.add_item(whole_items[j])
            else:
                exchangeBin2.add_item(whole_items[j])
            if exchangeBin1.cap_left < best_exchangeBin1.cap_left and exchangeBin1.cap_left>=0 and exchangeBin2.cap_left>=0:
                best_exchangeBin1 = copy.deepcopy(exchangeBin1);
                best_exchangeBin2 = copy.deepcopy(exchangeBin2);
            
    solution.bins[exchangeBin_index1] = copy.deepcopy(best_exchangeBin1)
    solution.bins[exchangeBin_index2] = copy.deepcopy(best_exchangeBin2) 

    return solution
def Neighbourhood(nb_space, solution:Solution):
    if nb_space == 1:
        # 200 neighbourhood1 solutions space with LBLI, RandomBin_Reshuffule and shift heuristics
        neighbour_count = 100
        local_best_solution = copy.deepcopy(solution)
        for i in range(neighbour_count):
            local_best_solution = Exchange_LBLI(local_best_solution)
            local_best_solution = Exchange_randomBin_Reshuffle(local_best_solution)
            local_best_solution = ShiftStrategy(local_best_solution)
            local_best_solution = ShiftStrategy(local_best_solution)
            print(local_best_solution.bins_number, solution.bins_number)
            if local_best_solution.bins_number < solution.bins_number:
                solution = copy.deepcopy(local_best_solution)
    elif nb_space == 2:
        # 200 neighbourhood2 solutions space with Split, LBLI and shift heuristics
        neighbour_count = 50
        local_best_solution = copy.deepcopy(solution)
        for i in range(neighbour_count):
            local_best_solution = SplitStrategy(local_best_solution)
            local_best_solution = Exchange_LBLI(local_best_solution)
            local_best_solution = ShiftStrategy(local_best_solution)
            local_best_solution = ShiftStrategy(local_best_solution)
            if local_best_solution.bins_number < solution.bins_number:
                solution = copy.deepcopy(local_best_solution)
    elif nb_space == 3:
        # 200 neighbourhood3 solutions space with hybrid heuristics
        neighbour_count = 10
        local_best_solution = copy.deepcopy(solution)
        for i in range(neighbour_count):
            local_best_solution = Exchange_LBLI(local_best_solution)
            local_best_solution = Exchange_randomBin_Reshuffle(local_best_solution)
            local_best_solution = Exchange_randomBin_Reshuffle(local_best_solution)
            local_best_solution = SplitStrategy(local_best_solution)
            local_best_solution = Exchange_LBLI(local_best_solution)
            local_best_solution = Exchange_randomBin_Reshuffle(local_best_solution)
            local_best_solution = Exchange_randomBin_Reshuffle(local_best_solution)
            local_best_solution = SplitStrategy(local_best_solution)
            local_best_solution = Exchange_LBLI(local_best_solution)
            local_best_solution = Exchange_LBLI(local_best_solution)
            local_best_solution = Exchange_randomBin_Reshuffle(local_best_solution)
            local_best_solution = Exchange_randomBin_Reshuffle(local_best_solution)
            local_best_solution = ShiftStrategy(local_best_solution)
            local_best_solution = ShiftStrategy(local_best_solution)
            local_best_solution = ShiftStrategy(local_best_solution)
            local_best_solution = ShiftStrategy(local_best_solution)
            local_best_solution = ShiftStrategy(local_best_solution)
            local_best_solution = ShiftStrategy(local_best_solution)
            local_best_solution = ShiftStrategy(local_best_solution)
            local_best_solution = ShiftStrategy(local_best_solution)
            if local_best_solution.bins_number < solution.bins_number:
                solution = copy.deepcopy(local_best_solution)
    else:
        print("Bad nb_space!")

    return solution

def Shaking(solution:Solution):
    # reshuffle non-full bins
    reshuffle_bins = []
    reshuffle_items = []
    sorted_bins1 = copy.deepcopy(solution.bins)
    sorted_bins1.sort(key=lambda bin: bin.cap_left)  # sort bins from small left capacity to big left capacity
    for bin in sorted_bins1:
        if bin.cap_left == 0:
            reshuffle_bins.append(bin)
        else:
            for item in bin.items:
                reshuffle_items.append(item)
    random.shuffle(reshuffle_items)
    bin_capacity = solution.problem.capacity
    flag_newBin = False
    current_bin = Bin(bin_capacity)
    # First Fit
    current_bin.add_item(reshuffle_items[0])
    reshuffle_bins.append(current_bin)
    for i in range(1, len(reshuffle_items)):
        for k in range(len(reshuffle_bins)):
            # Search the first fitted bin for this item
            if reshuffle_items[i].weight < reshuffle_bins[k].cap_left:
                reshuffle_bins[k].add_item(reshuffle_items[i])
                flag_newBin = False
                break
            flag_newBin = True
        if flag_newBin:
            # If there is no fitted bin before, then push a new bin to take the item.
            bin = Bin(bin_capacity)
            current_bin = bin
            current_bin.add_item(reshuffle_items[i])
            reshuffle_bins.append(current_bin)
    solution.bins = copy.deepcopy(reshuffle_bins)
    # choose two bins randomly, reshuffle the items of them and pack them randomly
    exchangeBin_index1 = random.randint(0, len(solution.bins) - 1)
    exchangeBin_index2 = random.randint(0, len(solution.bins) - 1)
    emptybin_check(solution)  # check the empty bin
    sorted_bins = copy.deepcopy(solution.bins)
    sorted_bins.sort(key=lambda bin: bin.cap_left, reverse=True)  # sort bins from big left capacity to small left capacity
    # store the whole items needed to be packed
    whole_items = []
    for item in sorted_bins[exchangeBin_index1].items:
        whole_items.append(item)
    for item in sorted_bins[exchangeBin_index2].items:
        whole_items.append(item)
    # check the random packing is valid
    flag_valid_randomPack = False
    while not flag_valid_randomPack:
        exchangeBin1 = Bin(bin_capacity)
        exchangeBin2 = Bin(bin_capacity)
        random.shuffle(whole_items)
        for j in range(len(whole_items)):
            if whole_items[j].weight <= exchangeBin1.cap_left:
                exchangeBin1.add_item(whole_items[j])
            else:
                exchangeBin2.add_item(whole_items[j])
        if exchangeBin1.cap_left >= 0 and exchangeBin2.cap_left >= 0:
            solution.bins[exchangeBin_index1] = copy.deepcopy(exchangeBin1)
            solution.bins[exchangeBin_index2] = copy.deepcopy(exchangeBin2)
            flag_valid_randomPack = True
    # exchange randomly two items which is the largest item in each bin
    flag = True
    while flag:
        exchangeBin_index1 = random.randint(0, len(solution.bins) - 1)
        exchangeBin_index2 = random.randint(0, len(solution.bins) - 1)
        while exchangeBin_index1 == exchangeBin_index2:
            exchangeBin_index2 = random.randint(0, len(solution.bins) - 1)
        can_exchange1 = (solution.bins[exchangeBin_index1].items[0].weight + solution.bins[exchangeBin_index1].cap_left) > solution.bins[exchangeBin_index2].items[0].weight
        can_exchange2 = (solution.bins[exchangeBin_index2].items[0].weight + solution.bins[exchangeBin_index2].cap_left) > solution.bins[exchangeBin_index1].items[0].weight
        if can_exchange1 and can_exchange2:
            item1 = solution.bins[exchangeBin_index1].items[0]
            item2 = solution.bins[exchangeBin_index2].items[0]
            solution.bins[exchangeBin_index1].remove_item(item1)
            solution.bins[exchangeBin_index2].remove_item(item2)
            solution.bins[exchangeBin_index1].add_item(item2)
            solution.bins[exchangeBin_index2].add_item(item1)
            solution.bins[exchangeBin_index1].items.sort(key=lambda item: item.weight, reverse=True)
            solution.bins[exchangeBin_index2].items.sort(key=lambda item: item.weight, reverse=True)
            flag = False
    return solution
def Initial_solution(solution):
    bin_capacity = solution.problem.capacity
    flag_newBin = False
    # This is for sorting items
    sorted_items = copy.deepcopy(solution.problem.items)
    sorted_items.sort(key=lambda item: item.weight)  # sort items from small-size to large-size
    current_bin = Bin(bin_capacity)
    #first fit
    current_bin.add_item(sorted_items[0])
    solution.bins.append(current_bin)
    solution.bins_number += 1
    for i in range(1, len(sorted_items)):
        for k in range(len(solution.bins)):
            # Search the first fitted bin for this item
            if sorted_items[i].weight <= solution.bins[k].cap_left:
                solution.bins[k].add_item(sorted_items[i])
                flag_newBin = False
                break
            flag_newBin = True
        if flag_newBin:
            # If there is no fitted bin before, then push a new bin to take the item.
            bin = Bin(bin_capacity)
            current_bin = bin
            current_bin.add_item(sorted_items[i])
            solution.bins.append(current_bin)
            solution.bins_number += 1
    return solution

def Variable_Neighbourhood_Search(problem):
    current_solution = Solution(problem)
    current_solution = Initial_solution(current_solution)
    best_solution = copy.deepcopy(current_solution)
    nb_space = 1
    maxSpace = 2
    while nb_space < maxSpace + 1:
        n_best_solution = copy.deepcopy(best_solution)
        current_solution=Neighbourhood(nb_space, current_solution)
        if n_best_solution.bins_number <current_solution.bins_number:
            current_solution = copy.deepcopy(n_best_solution)
            nb_space = 1
        else:
            nb_space += 1
    if current_solution.bins_number < best_solution.bins_number:
        best_solution =copy.deepcopy(current_solution)
    current_solution=Shaking(current_solution)
    return best_solution      
""" def evaluate(solution):
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


    return best_solution """
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
    problems = read_bin_packing_file(r"C:\Users\scyth1\Desktop\AI method\AI\binpack1.txt")
    for problem in problems:
        
        print(problem.id)
        best_solution = greedy_search(problem)
        #best_solution = Variable_Neighbourhood_Search(problem)
        #best_solution= genetic_algorithm(best_solution,population_size, mutation_rate, num_generations)
        #best_solution = simulated_annealing(best_solution)
        print(best_solution.bins_number)
        print(problem.optimal_solution- best_solution.bins_number)
        #for bin in best_solution.bins:
            #print(bin.cap_left)
            #print([item for item in bin.items])
            #print(' '.join(str(item.weight) for item in bin.items))
if __name__ == '__main__':
    main()