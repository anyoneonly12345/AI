
import copy
from random import randint
import re
import sys
import time
import random
import math
class Item:
    
    def __init__(self,id,weight,type = 0):
        """
        id: the item id 
        weight: the weight of item
        type : the item type 
        """
        self.id = id
        self.weight = weight
        self.type = None
        if type > 0.5:
            self.type = "VLarge"
        elif type > 0.35:
            self.type = "Large"
        elif type > 0.25:
            self.type = "Mid"
        else:
            self.type = "Small"
class Problem:
    
    def __init__(self,title,cap,itemNum,bestbin_number):
        """
        title: the title of problem
        cap: the cap of the problem
        itemNum: the total item number
        bestbin_number: the best solution number
        """
        self.title = title
        self.cap = int(cap )
        self.itemNum = int(itemNum )
        self.bestbin_number = int(bestbin_number)
        self.items = []
        self.VLargeitems = []
        self.Largeitems = []
        self.Miditems = []
        self.Smalless_items = []
        self.bins = []
        self.extrabins = []
        self.allbins = []
    def classifyItems(self,item:Item):
        if item.type == "VLarge":
            self.VLargeitems.append(item)
        elif item.type == "Large":
            self.Largeitems.append(item)
        elif item.type == "Mid":
            self.Miditems.append(item)
        elif item.type == "Small":
            self.Smalless_items.append(item)

    def throwEmpty(self):
        toRemove = []
        for bin in self.extrabins:
            if bin.isEmpty():
                toRemove.append(bin)
        for bin in toRemove:
            self.extrabins.remove(bin)
    def resetbins(self):
        """
        reset the bins and the extra bins
        """
        all_bins = [bin for bin in self.bins + self.extrabins if not bin.isEmpty()]
        all_bins.sort(key=lambda x: x.left_cap)
        self.bins = [bin for i, bin in enumerate(all_bins) if i < self.bestbin_number and not bin.isEmpty()]
        self.extrabins = [bin for i, bin in enumerate(all_bins) if i >= self.bestbin_number and not bin.isEmpty()]
        self.throwEmpty()
        bestfitExtra(self)
class Bin:
    def __init__(self,cap):
        """
        cap : the cap of the bin
        """
        self.cap = cap
        self.inputitem = []
        self.cur_weight = 0
        self.left_cap = cap
        LargeItemlist=[]
        VLargeItemlist=[]
        MidItemlist = []
        Smalless_itemlist = []
        self.dict = {"VLarge":VLargeItemlist,"Large":LargeItemlist,"Mid":MidItemlist,
            "Small":Smalless_itemlist,}
    def addItem(self,item:Item):
        """
        item: the item to add 
        """
        self.inputitem.append(item)
        self.cur_weight += item.weight
        self.left_cap -= item.weight
        self.dict[item.type].append(item)
    def removeItem(self,item:Item):
        """
        item: the item to remove
        """
        self.inputitem.remove(item)
        self.cur_weight -= item.weight
        self.left_cap += item.weight
        self.dict[item.type].remove(item)
    def isEmpty(self):
        """
        check if the bin is empty
        """
        if self.cur_weight == 0:
            return True
        else:
            return False
    def isFull(self):
        """
        check if the bin is full
        """
        if self.left_cap == 0:
            return True
        else:
            return False
    def canfit(self,item:Item):
        """
        check if the item can fit into the bin
        """
        if self.left_cap >= item.weight:
            return True
        else:
            return False
def readfile(filename):
    """
    read the file and return the problem list
    """
    with open(filename, "r") as file:
        problem_count = int(file.readline())
        problems = []
        for _ in range(problem_count):
            title = file.readline().strip('\n').strip(" ")
            info = file.readline().split(" ")
            cap, itemNum, bestbin_number = [int(item.strip(" ")) for item in info if item != ""]
            problem = Problem(title, cap, itemNum, bestbin_number)
            for _ in range(bestbin_number):
             problem.bins.append(Bin(cap))
            for _ in range(itemNum):
                item_weight = int(file.readline())
                item_type = item_weight / cap
                item = Item(_, item_weight, item_type)
                problem.items.append(item)
                problem.classifyItems(item)
            problems.append(problem)
        return problems
def bestFit(problem:Problem):
    """
    best fit algorithm
    """
    problem.items.sort(key=lambda x:x.weight, reverse=True)
    tempitems = copy.copy(problem.items)
    for bin in problem.bins:
        toReomveItems = []
        for item in tempitems:
            if bin.canfit(item):
                bin.addItem(item)
                toReomveItems.append(item)
        for item in toReomveItems:
            tempitems.remove(item)
    bin = Bin(problem.cap)
    bins_id = 0
    addBinList = [bin]
    """
    best_bins_number is not enough, add result to the extra bins
    """
    while(len(tempitems) != 0):
        toReomveItems = []
        bin = addBinList[bins_id]
        for item in tempitems:
            if bin.canfit(item):
                bin.addItem(item)
                toReomveItems.append(item)
        for item in toReomveItems:
            tempitems.remove(item)
        if len(tempitems) != 0:
            bins_id += 1
            bin = Bin(problem.cap)
            addBinList.append(bin)
    for bin in addBinList:
        problem.extrabins.append(bin)
def output(problemlist:list,filename):
    """
    output the result to the file
    """
    with open(filename, 'w') as outfile:
        print(len(problemlist), file=outfile)
        for problem in problemlist:
            problem.resetbins()
            problem.throwEmpty()
            print(problem.title, file=outfile)
            print(problem.title)
            print(problem.extrabins)
            num = len(problem.bins) + len(problem.extrabins)
            print(" obj=  ", num, num - problem.bestbin_number, file=outfile)
            for bin in problem.bins + problem.extrabins:
                if not bin.isEmpty():
                    print(' '.join(str(item.id) for item in bin.inputitem), file=outfile)
def getUnfillBins(problem:Problem):
    """
    get the unfill bins and the items in the unfill bins
    """
    items = []
    bins = []
    copy_problem = copy.copy(problem)
    for bin in problem.bins:
        if not bin.isFull() and not bin.isEmpty():
            bins.append(bin)
            for item in bin.inputitem:
                items.append(item)
    for bin in bins:
        copy_problem.bins.remove(bin)
    for bin in problem.extrabins:
        if not bin.isFull() and not bin.isEmpty():
            bins.append(bin)
            for item in bin.inputitem:
                items.append(item)
        copy_problem.extrabins = []
    return items,copy_problem

def shaking(problem:Problem):
    """
    shaking algorithm
    shake bins with unfill items to get a new problem
    """
    unfilled_items, updated_problem = getUnfillBins(problem)
    unfilled_items.sort(key=lambda x: x.weight, reverse=True)
    bin_id = 0
    new_bin = Bin(updated_problem.cap)
    new_bins_list = [new_bin]
    while unfilled_items:
        items_to_remove = []
        current_bin = new_bins_list[bin_id]
        for item in unfilled_items:
            if current_bin.canfit(item):
                current_bin.addItem(item)
                items_to_remove.append(item)
        for item in items_to_remove:
            unfilled_items.remove(item)
        if unfilled_items:
            bin_id += 1
            new_bin = Bin(updated_problem.cap)
            new_bins_list.append(new_bin)
    for bin in new_bins_list:
        updated_problem.bins.append(bin)
    updated_problem.resetbins()
    problem = updated_problem
    
    return problem 

def best_item_combine(space,items:list):
    """
    return the best combination of items and the max weight of the combination
    """
    item_inclusion_list = []    #initialize the item inclusion list and max weight list
    max_weight_list = []
    for i in range(len(items)):
        item_inclusion_dict = {}
        item_inclusion_list.append(item_inclusion_dict)
    for j in range(space + 1):
        max_weight_list.append(0)
    """
    calculate the max item weight of each space
    """
    for i in range(len(items)):
        for j in range(space, -1, -1):
            item_inclusion_list[i][j] = False
            if ( j>= items[i].weight ) :
                if ( max_weight_list[j] <= max_weight_list[j-items[i].weight]+ items[i].weight ): 
                    max_weight_list[j] = max_weight_list[j-items[i].weight]+items[i].weight
                    item_inclusion_list[i][j] = True
    """
     find the best combination of items 
    """
    selected_items = []
    remaining_space = space
    for i in range(len(items), 0, -1):
        if item_inclusion_list[i - 1][remaining_space] == True:
            selected_items.append(items[i - 1])
            remaining_space -= items[i - 1].weight
    
    return selected_items, max_weight_list[space]

def minimal_cap_left( cap, num,items,min_weight,selected_items):
    """
    find the minimal cap left
    """
    if min_weight > cap:
        min_weight = cap
    if (num == len(items)) :
        return
    if (cap-items[num].weight < 0) :
        minimal_cap_left(cap,num+1,items,min_weight,selected_items)
    else:
        selected_items.append(items[num])
        minimal_cap_left(cap-items[num].weight ,num+1,items,min_weight,selected_items)

def changeItems(morebin,lessbin):
    """
    change items between two bins
    return a better result of the two bins
    """
    selected_items = []
    selected_weight = 0
    MAXSPACE = 20000
    MAXITEM = 25
    for item in morebin.inputitem:
        if item.type == "VLarge" :
            continue
        selected_space = morebin.left_cap + item.weight#the space after adding the item
        if selected_space <= MAXSPACE and len(lessbin.inputitem) <= MAXITEM: #if the space is less than the max space and the number of items is less than the max item number
            items = lessbin.inputitem
            selected_items, selected_weight= best_item_combine(selected_space,items)#find the best combination of items
        else:#if the space is larger than the max space or the number of items is larger than the max item number
            cap = morebin.cap 
            selected_items = [] 
            selected_weight = selected_space 
            items = lessbin.inputitem
            minimal_cap_left(cap,0,items,selected_weight,selected_items)#find the minimal cap left
            selected_weight = selected_space - selected_weight
        if selected_weight >= item.weight:
            #if the selected weight is larger than the item weight, return the selected weight, selected items and the item
            return selected_weight,selected_items,item
    return None,None,None
def changeItemswithType(morebin,lessbin,type):
    """
    change items between two bins with the same type
    return a better result of the two bins
    """
    selected_items = []
    selected_weight = 0
    MAXSPACE = 20000
    MAXITEM = 25
    for item in morebin.inputitem:
        if item.type == type :
            selected_space = morebin.left_cap + item.weight
            if selected_space <= MAXSPACE and len(morebin.inputitem) <= MAXITEM:
                items = lessbin.inputitem
                selected_items, selected_weight= best_item_combine(selected_space,items)
            else:
                cap = morebin.cap
                selected_items = []
                selected_weight = selected_space
                items = lessbin.inputitem
                minimal_cap_left(cap,0,items,selected_weight,selected_items)
                selected_weight = selected_space - selected_weight
            if selected_weight >= item.weight:
                return selected_weight,selected_items,item
    return None,None,None
def swap(morebin,lessbin):
    """
    swap the items between two bins
    return the best combination of two bins
    """
    morebin1 = copy.copy(morebin)
    lessbin1 = copy.copy(lessbin)
    lessbin1.inputitem.sort(key = lambda x:x.weight)
    morebin1.inputitem.sort(key = lambda x:x.weight)
    for more_item in morebin1.inputitem:
        for less_item in lessbin1.inputitem:
            if less_item.weight < more_item.weight:
                break 
            if more_item.weight < less_item.weight and more_item.weight+morebin1.left_cap >=less_item.weight:
                return less_item,more_item
    return None

def randomShake(problem:Problem):
    """
    random shake algorithm
    return a new problem after shaking
    """
    problem.resetbins()
    problem_copy = copy.copy(problem)

    all_bins = problem_copy.bins + problem_copy.extrabins
    bin_count = len(all_bins)

    bin_index1, bin_index2 = random.sample(range(bin_count), 2)
    bin1, bin2 = all_bins[bin_index1], all_bins[bin_index2]

    if bin1.left_cap > bin2.left_cap:
        bin1, bin2 = bin2, bin1

    solution = swap(bin1, bin2)  # bin2 has more left space
    if solution is not None:
        bin1.removeItem(solution[1])
        bin2.removeItem(solution[0])
        bin1.addItem(solution[0])
        bin2.addItem(solution[1])

    problem = copy.copy(problem_copy)
    problem.resetbins()

    return problem



def chooseTwoType(problem:Problem,type1,type2):
    """
    choose two types of items and change the items between the bins
    """
    copy_problemopy = copy.copy(problem)
    bins_without_type1 = []
    bins_with_type1 = []       
    
    for bin in copy_problemopy.bins:
        if bin.isFull():
            continue
        has_type1_item = any(item.type == type1 for item in bin.inputitem)
        if has_type1_item:
            bins_with_type1.append(bin)
        else:
            bins_without_type1.append(bin)
    
    bins_without_type1, bins_with_type1 = TypeChange(bins_without_type1, bins_with_type1, type2)
    problem = copy_problemopy
    
    return problem

def TypeChange(Type1:list,Type2:list,type):
    """
    change the items between the two types of bins
    
    """
    Type1_c = copy.copy(Type1)
    Type2_c = copy.copy(Type2)
    for morebin in Type1_c:
        toRemove = []
        for lessbin in Type2_c:
            selected_weight,selected_items,item = changeItemswithType(morebin,lessbin,type)
            if selected_weight == None:
                continue
            else:
                morebin.removeItem(item)
                lessbin.addItem(item)
                for item in selected_items:
                    morebin.addItem(item)
                    lessbin.removeItem(item)
                break
        for bin in toRemove:
            Type2_c.remove(bin)
    return Type1_c,Type2_c

def bestfitExtra(problem:Problem):
    """
    best fit the extra items
    """
    temp_items = [item for bin in problem.extrabins for item in bin.inputitem]
    add_bin_list = [Bin(problem.cap)]

    while temp_items:
        to_remove_items = []
        current_bin = add_bin_list[-1]
        for item in temp_items:
            if current_bin.canfit(item):
                current_bin.addItem(item)
                to_remove_items.append(item)
        temp_items = [item for item in temp_items if item not in to_remove_items]

        if temp_items:
            add_bin_list.append(Bin(problem.cap))

    problem.extrabins = add_bin_list
    return problem
def maintain_extra_bins(problem:Problem): 
    """
    maintain the extra bins items
    """
     
    for morebin in problem.bins:
        for lessbin in problem.extrabins:
            selected_weight, selected_items, item = changeItems(morebin, lessbin)
            if selected_weight is not None:
                morebin.removeItem(item)
                lessbin.addItem(item)
                for item in selected_items:
                    morebin.addItem(item)
                    lessbin.removeItem(item)
                break
    problem.extrabins = [bin for bin in problem.extrabins if not bin.isEmpty()]
    problem.resetbins()

    return problem

def fit_extraitem(problem:Problem):
    """
    fit the extra items
    """
      
    extraitems = []
    for bin in problem.extrabins:
        for item in bin.inputitem:
            extraitems.append(item)
    extraitems.sort(key = lambda x:x.weight,reverse= True)
    toRemove = []
    for item in extraitems:
        for bin in problem.bins:
            if bin.canfit(item):
                bin.addItem(item)
                toRemove.append(bin)
                break
    for item in toRemove:
        for bin in problem.extrabins:
            try:
                bin.removeItem(item)
            except:
                pass
    problem.resetbins()
    return problem

def checkResult(problem1:Problem,problem2:Problem):
    """
    check the result and return the best result
    """
    if len(problem1.extrabins) < len(problem2.extrabins):
        return problem1
    elif len(problem1.extrabins) > len(problem2.extrabins):
        return problem2
    else:
        sum1 = 0
        sum2 = 0
        for bin in problem1.extrabins:
            sum1 += bin.cur_weight
        for bin in problem2.extrabins:
            sum2 += bin.cur_weight
        if sum1 < sum2:
            return problem1
        else:
            return problem2
def neighbourhood(problem:Problem,best_problem:Problem):
    """
    neighbourhood search algorithm
    it is composed of low level function combine algorithm and best fit the extra items
    """
    problem = chooseTwoType(problem,"VLarge","Large")
    problem = maintain_extra_bins(problem)
    problem = fit_extraitem(problem)
    problem = bestfitExtra(problem)
    best_problem = checkResult(problem,best_problem)
    best_problem = bestfitExtra(best_problem)
    return problem,best_problem
def variable_neibourhood_search(problem, best_problem):
    """
    variable neighbourhood search algorithm
    """
    shaking_time = 35
    for i in range(shaking_time):
        if i != 0:
            problem = shaking(problem)
        problem,best_problem= neighbourhood(problem, best_problem)
        if len(best_problem.extrabins) <= 1:
            break
    return problem, best_problem

def lowlevelcombine(problem, best_problem):
    """
    low level function combine algorithm
    """
    problem = chooseTwoType(problem,"Large","Mid")
    problem = maintain_extra_bins(problem)
    problem = chooseTwoType(problem,"VLarge","Large")
    problem = fit_extraitem(problem)
    best_problem = checkResult(problem,best_problem)
    best_problem = bestfitExtra(best_problem)
    return problem, best_problem
def mutipule_randomShake(problem:Problem):
    """
    multiple random shake algorithm
    """
    for i in range(500):
        problem = randomShake(problem)
    return problem
def neighbourhood2(problem:Problem,best_problem:Problem):
    """
    neighbourhood search algorithm
    shake the bins with unfill items
    then use the low level function combine algorithm to get a better result
    """
    problem = mutipule_randomShake(problem)
    problem,best_problem = lowlevelcombine(problem,best_problem)
    return problem, best_problem
def simulated_annealing(problem, best_problem, temperature=100, cooling_rate=0.8, end_temperature=0.1):
    """
    simulated annealing algorithm
    
    """
    current_problem = problem
    new_problem = problem
    while temperature > end_temperature:
        new_problem, best_problem = neighbourhood2(new_problem, best_problem)
        if len(best_problem.extrabins) == 0:
            break
        delta = len(new_problem.extrabins) - len(current_problem.extrabins)
        if delta > 0:
            best_problem = current_problem
        else:
            if random.random() < math.exp(delta / temperature):
                current_problem = new_problem
        temperature *= cooling_rate
    return new_problem, best_problem
def HyperHeuristic(problem:Problem,best_problem:Problem):
    """
    selection hyper heuristic algorithm
    it is composed of simulated annealing and variable neighbourhood search
    depending on the number of extra bins, it will choose the best algorithm
    """
    for i in range(10):
        if len(best_problem.extrabins) >2:
            problem,best_problem = simulated_annealing(problem,best_problem)    
        else:
            problem,best_problem = variable_neibourhood_search(problem,best_problem)
        if len(best_problem.extrabins) == 0:
            break
    return problem,best_problem
def main():
    totaltime = 0
    filename = sys.argv[2]
    problemlist = readfile(filename)
    problemsolutionlist = []
    for problem in problemlist:
        startT = time.time()
        bestFit(problem)
        best_problem = copy.copy(problem)
        problem.resetbins()
        problem,best_problem = HyperHeuristic(problem,best_problem)
        best_problem = bestfitExtra(best_problem)
        endT = time.time()
        print("Running time ",endT - startT)
        totaltime += (endT - startT)
        problemsolutionlist.append(problem)
    output(problemsolutionlist,sys.argv[4])
    print(totaltime)
if __name__ == "__main__":
    main()