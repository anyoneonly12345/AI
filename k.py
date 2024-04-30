import copy
class Problem:
    def __init__(self, n):
        self.n = n
        self.k = []

def start(problem):
    problem.k.append(1)
    return problem
def simulate(problem):
    current_problem = copy.copy(problem)
    current_problem.k.append(2)
    
    return problem
def main():
    n = 5
    problem = Problem(n)
    problem = start(problem)
    problem = simulate(problem)
    print(problem.k)
main()