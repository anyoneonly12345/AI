
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
        elif type <= 0.1:
            self.type = "Tiny"
        else:
            self.type = "Small"
    def show(self):
        print("BIN: ",self.id,self.weight,self.type)
class Problem:
    
    def __init__(self,title,cap,itemNum,bestNum):
        """
        title: the title of problem
        cap: the cap of the problem
        itemNum: the total item number
        bestNUm: the best solution number
        """
        self.title = title
        self.cap = int(cap )
        self.itemNum = int(itemNum )
        self.bestNum = int(bestNum)
        self.items = []
        self.VLargeitems = []
        self.Largeitems = []
        self.Miditems = []
        self.Smallitems = []
        self.Tinyitems = []
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
            self.Smallitems.append(item)
        elif item.type == "Tiny":
            self.Tinyitems.append(item)
    def throwEmpty(self):
        toRemove = []
        for bin in self.extrabins:
            if bin.left_cap == self.cap and bin.cur_weight == 0:
                toRemove.append(bin)
        for bin in toRemove:
            self.extrabins.remove(bin)
    def resetbins(self):
        """
        reset the bins and the extra bins
        """
        allBins = []
        for bin in self.bins:
            if bin.left_cap != self.cap and bin.cur_weight != 0:
                allBins.append(bin)
        for bin in self.extrabins:
            if bin.left_cap != self.cap and bin.cur_weight != 0:
                allBins.append(bin)
        allC = []
        allC = copy.copy(allBins)
        allC.sort(key = lambda x:x.left_cap, reverse= False)
        self.bins = []
        self.extrabins = []
        toRemove = []
        for bin in allC:
            if bin.left_cap == self.cap and bin.cur_weight == 0:
                toRemove.append(bin)
        for bin in toRemove:
            allC.remove(bin)
        
        for i in range(len(allC) ):
            if i < self.bestNum:
                self.bins.append(allC[i])
            else:
                if bin.left_cap != self.cap and bin.cur_weight != 0:
                    self.extrabins.append(allC[i])
                    # print("Extra", bin.left_cap, bin.cur_weight)
        self.throwEmpty()
        # print(self.extrabins)
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
        SmallItemlist = []
        TinyItemlist = []
        self.dict = {"VLarge":VLargeItemlist,"Large":LargeItemlist,"Mid":MidItemlist,
            "Small":SmallItemlist,"Tiny":TinyItemlist}
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
        
    def show(self):
        print("Show bin ","cur weight = ", self.cur_weight,"left weight = ", self.left_cap)
def readfile(filename):
    """ 
    read the file and build the problem class
    """
    f = open(filename,"r")
    problem_num = f.readline()
    problemlist = []
    for i in range(int(problem_num)):
        title = f.readline()
        title = title.strip('\n')
        title = title.strip(" ")
        info = f.readline()
        temp_t = info.split(" ")
        if temp_t[0] == "":
            temp_t.pop(0)
        for item in temp_t:
            item = item.strip(" ")
            item = int(item)
        problem = Problem(title,temp_t[0],temp_t[1],temp_t[2])
        for j in range(int(temp_t[2])):
            problem.bins.append(Bin(problem.cap))
        
        for j in range (int(temp_t[1])):
            itemc = f.readline()
            # print("itemc = ",itemc)
            itemtype = int(itemc)/problem.cap
            item = Item(j,int(itemc),itemtype)
            problem.items.append(item)
            problem.classifyItems(item)
        problemlist.append(problem)
    return problemlist
def bestFit(problem:Problem):
    """
    bestfit method to solve the problem
    """
    problem.items.sort(key=lambda x:x.weight, reverse=True)
    tempitems = copy.copy(problem.items)
    for bin in problem.bins:
        toReomveItems = []
        for item in tempitems:
            if bin.left_cap >= item.weight:
                bin.addItem(item)
                toReomveItems.append(item)
        for item in toReomveItems:
            tempitems.remove(item)
    bin = Bin(problem.cap)
    cid = 0
    addBinList = [bin]
    while(len(tempitems) != 0):
        toReomveItems = []
        bin = addBinList[cid]
        for item in tempitems:
            if bin.left_cap >= item.weight:
                bin.addItem(item)
                toReomveItems.append(item)
        for item in toReomveItems:
            tempitems.remove(item)
        if len(tempitems) != 0:
            cid += 1
            bin = Bin(problem.cap)
            addBinList.append(bin)
    for bin in addBinList:
        problem.extrabins.append(bin)
    print("Add num",len(addBinList))
def checker(problem:Problem):
    """
    check if the solution is right 
    """
    items = copy.copy(problem.items)
    for bin in problem.bins:
        cap = problem.cap
        for item in bin.inputitem:
            items.remove(item)
            cap -= item.weight
            if cap == problem.cap:
                print("WARNING :empty")
            if cap < 0:
                print("ERROR: overload")
    for bin in problem.extrabins:
        cap = problem.cap
        for item in bin.inputitem:
            # item.show()
            items.remove(item)
            cap -= item.weight
            if cap < 0:
                print("extra ERROR: overload")
    # print("len items ",len(items))
    for item in items:
        print("Miss item", item.show())

def output(problemlist:list,filename):
    """
    get the solution and print it to the file
    """
    outfile = open(filename,'w')
    print(len(problemlist),file = outfile)
    for problem in problemlist:
        problem.resetbins()
        problem.throwEmpty()
        # checker(problem)
        print(problem.title,file = outfile)
        print(problem.title)
        print(problem.extrabins)
        num = len(problem.bins) + len(problem.extrabins)
        print(" obj=  ",num, num- problem.bestNum,file = outfile)
        for bin in problem.bins:
            for item in bin.inputitem:
                print(item.id, end=" ",file = outfile)
            print(file = outfile)
        for bin in problem.extrabins:
            if bin.left_cap != problem.cap and bin.cur_weight != 0:
                # allBins.append(bin)
                for item in bin.inputitem:
                    print(item.id, end=" ",file = outfile)
                print(file = outfile)
            bin.show()

def getUnfillBins(problem:Problem):
    """
    get the bins not full 
    :items: the items for the bins
    :bins: the bins that not full
    :problem_c: problem after remove the bins and items
    """
    items = []
    bins = []
    problem_c = copy.copy(problem)
    for bin in problem.bins:
        if bin.cur_weight != problem.cap and bin.left_cap != 0:
            bins.append(bin)
            for item in bin.inputitem:
                items.append(item)
    for bin in bins:
        problem_c.bins.remove(bin)
    for bin in problem.extrabins:
        if bin.cur_weight != problem.cap and bin.left_cap != 0:
            bins.append(bin)
            for item in bin.inputitem:
                items.append(item)
        problem_c.extrabins = []
    return items,bins,problem_c

def shaking(problem:Problem):
    """
    shake the problem that the non filled bins use bestfit to choose
    """
    unfillitems,unfillbins,problem_c = getUnfillBins(problem)
    unfillitems.sort(key = lambda x:x.weight,reverse= True)
    bin = Bin(problem_c.cap)
    cid = 0
    addBinList = [bin]
    while(len(unfillitems) != 0):
        toReomveItems = []
        bin = addBinList[cid]
        for item in unfillitems:
            if bin.left_cap >= item.weight:
                bin.addItem(item)
                toReomveItems.append(item)
        for item in toReomveItems:
            unfillitems.remove(item)
        if len(unfillitems) != 0:
            cid += 1
            bin = Bin(problem.cap)
            addBinList.append(bin)
    for bin in addBinList:
        problem_c.bins.append(bin)
    problem_c.resetbins()
    problem = problem_c
    return problem   

def dpAns(space,items:list):
    """
    dynamic programming to get the best solution
    items should no more than 30
    """
    list = []
    dp = []
    for i in range(len(items)):
        dict = {}
        list.append(dict)
    for j in range(space + 1):
        dp.append(0)
    for i in range(0,len(items),1):
        for j in range(space,-1,-1):
            list[i][j] = False
            if ( j>= items[i].weight ) :
                if ( dp[j] <= dp[j-items[i].weight]+ items[i].weight ): 
                    dp[j] = dp[j-items[i].weight]+items[i].weight
                    list[i][j] = True
    changeItems = []
    j = space
    for i in range(len(items),0,-1):
        if list[i - 1][j] == True:
            changeItems.append(items[i - 1])
            j -= items[i - 1].weight
    return changeItems,dp[space]

def dfs( cap, num,items,Min,c_list):
    """
    deep first search to get a local solution for 
    single bin item packing
    """
    Min = min(Min,cap)
    if (num == len(items)) :
        return
    if (cap-items[num].weight < 0) :
        dfs(cap,num+1,items,Min,c_list)
    else:
        c_list.append(items[num])
        dfs(cap-items[num].weight ,num+1,items,Min,c_list)

def changeItems(morebin,lessbin):
    """
    change one item from more bin to another bin make the space more
    """
    clist = []
    c_sum = 0
    for item in morebin.inputitem:
        if item.type == "VLarge" :
            continue
        c_space = morebin.left_cap + item.weight
        if c_space <= 20000 and len(lessbin.inputitem) <= 25:
            items = lessbin.inputitem
            clist, c_sum= dpAns(c_space,items)
            # print(clist, c_sum)
        else:
            cap = morebin.cap
            c_list = []
            c_sum = c_space
            items = lessbin.inputitem
            dfs(cap,0,items,c_sum,c_list)
            c_sum = c_space - c_sum
        if c_sum >= item.weight:
            return c_sum,clist,item
    return None,None,None
def changeItemswithType(morebin,lessbin,type):
    """
    change one item from more bin to another bin make the space more
    """
    clist = []
    c_sum = 0
    for item in morebin.inputitem:
        if item.type == type :
            c_space = morebin.left_cap + item.weight
            if c_space <= 20000 and len(morebin.inputitem) <= 25:
                items = lessbin.inputitem
                clist, c_sum= dpAns(c_space,items)
            else:
                cap = morebin.cap
                c_list = []
                c_sum = c_space
                items = lessbin.inputitem
                dfs(cap,0,items,c_sum,c_list)
                c_sum = c_space - c_sum
            if c_sum >= item.weight:
                return c_sum,clist,item
    return None,None,None
def split(problem:Problem):
    """
    random choose one bin and split it's items to 2 bin
    """
    randid = randint(0,problem.bestNum - 1)
    bin = problem.bins[randid]
    nbin = Bin(problem.cap)
    items = []
    for i in range(int(len(bin.inputitem)/2)):
        items.append(bin.inputitem[i])
    for item in items:
        bin.removeItem(item)
        nbin.addItem(item)
    problem.extrabins.append(nbin)
    return problem

def swap(morebin,lessbin):
    """
    swap one item from more bin to another bin make the space more
    """
    morebin1 = copy.copy(morebin)
    lessbin1 = copy.copy(lessbin)
    lessbin1.inputitem.sort(key = lambda x:x.weight,reverse = False)
    morebin1.inputitem.sort(key = lambda x:x.weight,reverse = False)
    for mitem in morebin1.inputitem:
        for litem in lessbin1.inputitem:
            if litem.weight < mitem.weight:
                break 
            if mitem.weight < litem.weight and mitem.weight+morebin1.left_cap >=litem.weight:
                return litem,mitem
    return None

def randomShake(problem:Problem):
    """
    choose 2 bin to shake randomly
    """
    problem.resetbins()
    problem_copy = copy.copy(problem)
    all_bins = []
    for bin in problem_copy.bins:
        all_bins.append(bin)
    for bin in problem_copy.extrabins:
        all_bins.append(bin)
    bin_num = len(all_bins)
    randBin1 = randint(0,bin_num - 1)
    randBin2 = randint(0,bin_num - 1)
    if randBin1 == randBin2:
        randBin2 +=1 
        randBin2 %= bin_num
    bin1 = all_bins[randBin1]
    bin2 = all_bins[randBin2]
    if bin1.left_cap > bin2.left_cap:
        bin_T = bin1 
        bin1 =  bin2 
        bin2 = bin_T
    solution = swap(bin1,bin2) # 2 have more left space
    if solution != None:
            bin1.removeItem(solution[1])
            bin2.removeItem(solution[0])
            bin1.addItem(solution[0])
            bin2.addItem(solution[1])

     
    problem = copy.copy(problem_copy)
    problem.resetbins()

    return problem



def chooseTwoType(problem:Problem,type1,type2):
    """
    for the item type choose 2 Type of bins
    """
    problem_copy = copy.copy(problem)
    Type1 = []
    Type2 = []       
    for bin in problem_copy.bins:
        if bin.left_cap == 0:
            continue
        flagL = False
        for item in bin.inputitem:
            if item.type == type1 :
                flagL = True
        if flagL == False:
            Type1.append(bin)
        else:
            Type2.append(bin)
        Type1,Type2 = TypeChange(Type1,Type2,type2)
    problem = problem_copy
    return problem

def TypeChange(Type1:list,Type2:list,type):
    """
    Change the items in bins of different Types
    
    """
    Type1_c = copy.copy(Type1)
    Type2_c = copy.copy(Type2)
    for morebin in Type1_c:
        toRemove = []
        for lessbin in Type2_c:
            c_sum,clist,item = changeItemswithType(morebin,lessbin,type)
            if c_sum == None:
                continue
            else:
                morebin.removeItem(item)
                lessbin.addItem(item)
                for item in clist:
                    morebin.addItem(item)
                    lessbin.removeItem(item)
                break
        for bin in toRemove:
            Type2_c.remove(bin)
    return Type1_c,Type2_c

def bestfitExtra(problem:Problem):
    extras = problem.extrabins
    tempitems = []
    for bin in extras:
        for item in bin.inputitem:
            tempitems.append(item)
    bin = Bin(problem.cap)
    cid = 0
    addBinList = [bin]
    while(len(tempitems) != 0):
        toReomveItems = []
        bin = addBinList[cid]
        for item in tempitems:
            if bin.left_cap >= item.weight:
                bin.addItem(item)
                toReomveItems.append(item)
        for item in toReomveItems:
            tempitems.remove(item)
        if len(tempitems) != 0:
            cid += 1
            bin = Bin(problem.cap)
            addBinList.append(bin)
    problem.extrabins = []
    for bin in addBinList:
        problem.extrabins.append(bin)
    return problem

def dealExtra(problem:Problem):  
    """
    try to put the items in extra to the other bins
    """
    for morebin in problem.bins:
        toRemove = []
        for lessbin in problem.extrabins:
            c_sum,clist,item = changeItems(morebin,lessbin)
            if c_sum == None:
                continue
            else:
                morebin.removeItem(item)
                lessbin.addItem(item)
                for item in clist:
                    morebin.addItem(item)
                    lessbin.removeItem(item)
                break
        for bin in toRemove:
            problem.extrabins.remove(bin)
    problem.resetbins()
    return problem

def bffExtra(problem:Problem):  
    """
    try to put the items in extra to the other bins
    """
    extraitems = []
    for bin in problem.extrabins:
        for item in bin.inputitem:
            extraitems.append(item)
    extraitems.sort(key = lambda x:x.weight,reverse= True)
    toRemove = []
    for item in extraitems:
        for bin in problem.bins:
            if bin.left_cap >= item.weight:
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
    Compare the problem result return the better one
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
def process(problem:Problem,best_problem:Problem):
    for i in range(30):
        if i != 0:
            problem = shaking(problem)
        problem,best_problem = neighbourhood(problem,best_problem)
        if len(best_problem.extrabins) == 0:
            break  
    return problem, best_problem
def variable_neibourhood_search(problem, best_problem):
    shaking_time = 30
    for i in range(shaking_time):
        if i != 0:
            problem = shaking(problem)
        problem,best_problem= neighbourhood(problem, best_problem)
        if len(best_problem.extrabins) <= 1:
            break
    return problem, best_problem
def neighbourhood(problem:Problem,best_problem:Problem):
            problem = chooseTwoType(problem,"VLarge","Large")
            problem = dealExtra(problem)
            problem = bffExtra(problem)
            problem = bestfitExtra(problem)
            best_problem = checkResult(problem,best_problem)
            best_problem = bestfitExtra(best_problem)
            return problem,best_problem
def mutipule_randomShake(problem:Problem):
    for i in range(300):
        problem = randomShake(problem)
    return problem

def process1(problem:Problem,best_problem:Problem):
    problem = mutipule_randomShake(problem)
    problem,best_problem = neighbourhood2(problem,best_problem)
    return problem, best_problem
def simulated_annealing(problem, best_problem, temperature=100, cooling_rate=0.8, end_temperature=1):
    current_problem = problem
    new_problem = problem
    while temperature > end_temperature:
        new_problem, best_problem = process1(new_problem, best_problem)
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
def neighbourhood2(problem, best_problem):
    problem = chooseTwoType(problem,"Large","Mid")
    problem = dealExtra(problem)
    problem = chooseTwoType(problem,"VLarge","Large")
    problem = bffExtra(problem)
    best_problem = checkResult(problem,best_problem)
    best_problem = bestfitExtra(best_problem)
    return problem, best_problem
def process2(problem,best_problem):
     for i in range(20):
            if i%3 == 0:
                problem  = split(problem)
            for t in range(300):
                problem = randomShake(problem)
            problem,best_problem = neighbourhood2(problem,best_problem)
            if len(best_problem.extrabins) == 0:
                break
     return problem, best_problem
def HyperHeuristic(problem:Problem,best_problem:Problem):
    for i in range(6):
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
        

 
main()