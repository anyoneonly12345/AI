MAX_TIME = 30  # the maximum running time for each problem instance

import random
import time
import sys
class Item:
    def __init__(self, size, index):
        self.item_size = size
        self.item_index = index

    def get_item_size(self):
        return self.item_size

    def get_item_index(self):
        return self.item_index


class Bin:
    def __init__(self, capacity):
        self.capacity_left = capacity
        self.items = []


class Problem:
    def __init__(self):
        self.items = []
        self.name = ""
        self.item_number = 0
        self.bin_capacity = 0
        self.best_objective = 0.0


class Solution:
    def __init__(self):
        self.problem = Problem()
        self.objective = 0.0
        self.feasibility = 0
        self.bins = []


class MyProblems:
    def __init__(self):
        self.my_problems = []
        self.my_solutions = []
        self.problem_number = 0

    def initial_problems(self, problem_number):
        self.problem_number = problem_number
        for _ in range(problem_number):
            problem = Problem()
            self.my_problems.append(problem)

    def load_problems(self, data_file):
        try:
            with open(data_file, 'r') as openfile:
                lines = openfile.readlines()
                self.problem_number = int(lines[0].strip())
                self.initial_problems(self.problem_number)

                line_index = 1
                for i in range(self.problem_number):
                    problem = self.my_problems[i]
                    problem.name = lines[line_index].strip()
                    line_index += 1
                    problem.bin_capacity = int(lines[line_index].strip())
                    line_index += 1
                    problem.item_number = int(lines[line_index].strip())
                    line_index += 1
                    problem.best_objective = float(lines[line_index].strip())
                    line_index += 1

                    for j in range(problem.item_number):
                        item_size = int(lines[line_index].strip())
                        item = Item(item_size, j)
                        problem.items.append(item)
                        line_index += 1

        except FileNotFoundError:
            print(f"Data file {data_file} does not exist. Please check!")
            exit(2)

    @staticmethod
    def item_cmp(item1, item2):
        return item1.get_item_size() > item2.get_item_size()

    @staticmethod
    def bin_cmp(bin1, bin2):
        return bin1.capacity_left < bin2.capacity_left

    def empty_bin_checker(self, solution):
        solution.bins = [bin for bin in solution.bins if bin.items]
        
    def shift_strategy(self, solution):
        sorted_bins = sorted(solution.bins, key=lambda bin: bin.capacity_left)
        sorted_bins.reverse()
        
        for item in sorted_bins[-1].items[:]:
            for bin in sorted_bins[:-1]:
                if item.get_item_size() <= bin.capacity_left:
                    bin.items.append(item)
                    bin.capacity_left -= item.get_item_size()
                    sorted_bins[-1].items.remove(item)
                    if not sorted_bins[-1].items:
                        sorted_bins.pop()
                    break

        solution.bins = sorted_bins
        solution.objective = len(solution.bins)
        self.empty_bin_checker(solution)

    def split_strategy(self, solution):
        avg_num_item = solution.problem.item_number // len(solution.bins)
        
        for bin in solution.bins[:]:
            if len(bin.items) > avg_num_item:
                num_split = len(bin.items) // 2
                random.shuffle(bin.items)
                
                new_bin = Bin(solution.problem.bin_capacity)
                for item in bin.items[:num_split]:
                    new_bin.items.append(item)
                    bin.capacity_left += item.get_item_size()
                    new_bin.capacity_left -= item.get_item_size()
                
                bin.items = bin.items[num_split:]
                bin.items.sort(key=lambda item: item.get_item_size(), reverse=True)
                new_bin.items.sort(key=lambda item: item.get_item_size(), reverse=True)
                solution.bins.append(new_bin)
        
        solution.objective = len(solution.bins)

    def exchange_lbli(self, solution):
        self.empty_bin_checker(solution)
        sorted_bins = sorted(solution.bins, key=lambda bin: bin.capacity_left)
        unfull_bins = [i for i in range(1, len(sorted_bins)) if sorted_bins[i].capacity_left > 0]
        
        if not unfull_bins:
            return
        
        target_index = random.choice(unfull_bins)
        target_bin = sorted_bins[target_index]
        largest_bin = sorted_bins[0]
        
        target_items = []
        sum_size = 0
        
        largest_bin.items.sort(key=lambda item: item.get_item_size(), reverse=True)
        
        for item in target_bin.items[:]:
            if item.get_item_size() + sum_size <= largest_bin.capacity_left:
                target_items.append(item)
                sum_size += item.get_item_size()
        
        if sum_size + target_bin.capacity_left >= largest_bin.capacity_left:
            for item in target_items:
                target_bin.capacity_left += item.get_item_size()
                target_bin.items.remove(item)
            
            for item in target_items:
                largest_bin.items.append(item)
                largest_bin.capacity_left -= item.get_item_size()
            
            largest_bin.items.sort(key=lambda item: item.get_item_size(), reverse=True)
            target_bin.items.sort(key=lambda item: item.get_item_size(), reverse=True)
            
        solution.bins = sorted_bins
        solution.objective = len(solution.bins)
        self.empty_bin_checker(solution)

    def variable_neighbourhood_search(self, problem_index, max_time):
        solution = Solution()
        problem = self.my_problems[problem_index]

        solution.problem = problem
        solution.feasibility = 1
        start_time = time.time()
        
        bin_capacity = problem.bin_capacity
        item_number = problem.item_number

        items = [Item(random.randint(1, bin_capacity // 2), i) for i in range(item_number)]
        items.sort(key=lambda item: item.get_item_size(), reverse=True)

        bin_capacity_left = bin_capacity
        bins = []

        for item in items:
            if item.get_item_size() <= bin_capacity_left:
                bin_capacity_left -= item.get_item_size()
            else:
                bins.append(Bin(bin_capacity))
                bin_capacity_left = bin_capacity - item.get_item_size()

            bins[-1].items.append(item)

        solution.bins = bins
        solution.objective = len(bins)

        methods = [self.shift_strategy, self.split_strategy, self.exchange_lbli]
        while time.time() - start_time < max_time:
            method = random.choice(methods)
            method(solution)

        return solution
def main(argv):
    data_file = ""
    solution_file = ""
    MAX_TIME = 0

    if len(argv) > 7:
        print("Too many arguments.")
        return 1
    elif len(argv) != 7:
        print("Insufficient arguments. Please use the following options:\n   -s data_file (compulsory)\n   -o solution_file (compulsory)\n   -t max_time (in sec)")
        return 2
    else:
        i = 1
        while i < len(argv):
            if argv[i] == "-s":
                data_file = argv[i + 1]
            elif argv[i] == "-o":
                solution_file = argv[i + 1]
            elif argv[i] == "-t":
                MAX_TIME = int(argv[i + 1])
            i += 2

    my_problems = MyProblems()
    my_problems.load_problems(data_file)

    for i in range(len(my_problems.my_problems)):
        my_problems.variable_neighbourhood_search(i, MAX_TIME)

    my_problems.output_solutions(solution_file)

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python main.py -s data_file -o solution_file -t max_time")
        sys.exit(1)
    else:
        main(sys.argv)