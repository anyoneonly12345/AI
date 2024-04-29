
import copy
import random
import re
import sys
import time
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
    def show(self):
        print("item: ",self.id,self.weight,self.type)
class Problem:
    
    def __init__(self,title,cap,itemNum,bestNum):
        """
        title: the title of problem
        cap: the cap of the problem
        itemNum: the total item number
        bestNUm: the best problem number
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
        self.bins = []
        self.extrabins = []
        self.allbins = []
    def classifyitems(self,item:Item):
        if item.type == "VLarge":
            self.VLargeitems.append(item)
        elif item.type == "Large":
            self.Largeitems.append(item)
        elif item.type == "Mid":
            self.Miditems.append(item)
        elif item.type == "Small":
            self.Smallitems.append(item)
    def throwEmpty(self):
        toRemove = []
        for bin in self.extrabins:
            if bin.left_cap == self.cap and bin.cur_weight== 0:
                toRemove.append(bin)
        for bin in toRemove:
            self.extrabins.remove(bin)
    def resetbins(self):
        """
        reset the bins and the extra bins
        """
        allbins = []
        for bin in self.bins:
            if bin.left_cap != self.cap and bin.cur_weight!= 0:
                allbins.append(bin)
        for bin in self.extrabins:
            if bin.left_cap != self.cap and bin.cur_weight!= 0:
                allbins.append(bin)
        allC = []
        allC = copy.copy(allbins)
        allC.sort(key = lambda x:x.left_cap, reverse= False)
        self.bins = []
        self.extrabins = []
        toRemove = []
        for bin in allC:
            if bin.left_cap == self.cap and bin.cur_weight== 0:
                toRemove.append(bin)
        for bin in toRemove:
            allC.remove(bin)
        
        for i in range(len(allC) ):
            if i < self.bestNum:
                self.bins.append(allC[i])
            else:
                if bin.left_cap != self.cap and bin.cur_weight!= 0:
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
        self.cur_weight= 0
        self.left_cap = cap
        Largeitemlist=[]
        VLargeitemlist=[]
        Miditemlist = []
        Smallitemlist = []
        self.dict = {"VLarge":VLargeitemlist,"Large":Largeitemlist,"Mid":Miditemlist,
            "Small":Smallitemlist}
    def additem(self,item:Item):
        """
        item: the item to add 
        """
        self.inputitem.append(item)
        self.cur_weight+= item.weight
        self.left_cap -= item.weight
        self.dict[item.type].append(item)
    def removeitem(self,item:Item):
        """
        item: the item to remove
        """
        self.inputitem.remove(item)
        self.cur_weight-= item.weight
        self.left_cap += item.weight
        self.dict[item.type].remove(item)
    def canfit(self,item:Item):
        """
        item: the item to check
        """
        if self.left_cap >= item.weight:
            return True
        return False
def readfile(filename):
    """ 
    read the file and build the problem class
    """
    f = open(filename,"r")
    pro_num = f.readline()
    problemlist = []
    for i in range(int(pro_num)):
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
            itemtype = int(itemc)/problem.cap
            item = Item(j,int(itemc),itemtype)
            problem.items.append(item)
            problem.classifyitems(item)
        problemlist.append(problem)
    return problemlist

    
def bestFit(problem:Problem):
    """
    bestfit method to solve the problem
    """
    problem.items.sort(key=lambda x:x.weight, reverse=True)
    tempitems = copy.copy(problem.items)
    for bin in problem.bins:
        toReomveitems = []
        for item in tempitems:
            if bin.canfit(item):
                bin.additem(item)
                toReomveitems.append(item)
        for item in toReomveitems:
            tempitems.remove(item)
    bin = Bin(problem.cap)
    bid = 0
    addbinList = [bin]
    while(len(tempitems) != 0):
        toReomveitems = []
        bin = addbinList[bid]
        for item in tempitems:
            if bin.canfit(item):
                bin.additem(item)
                toReomveitems.append(item)
        for item in toReomveitems:
            tempitems.remove(item)
        if len(tempitems) != 0:
            bid += 1
            bin = Bin(problem.cap)
            addbinList.append(bin)
    for bin in addbinList:
        problem.extrabins.append(bin)
    print("Add num",len(addbinList))
def output(problemlist:list,filename):
    """
    get the problem and print it to the file
    """
    outfile = open(filename,'w')
    print(len(problemlist),file = outfile)
    for problem in problemlist:
        problem.resetbins()
        problem.throwEmpty()
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
            if bin.left_cap != problem.cap and bin.cur_weight!= 0:
                for item in bin.inputitem:
                    print(item.id, end=" ",file = outfile)
                print(file = outfile)

def getUnfillbins(problem:Problem):
    """
    get the bins not full 
    :items: the items for the bins
    :bins: the bins that not full
    :copy_problem: problem after remove the bins and items
    """
    items = []
    bins = []
    copy_problem = copy.copy(problem)
    for bin in problem.bins:
        if bin.cur_weight!= problem.cap and bin.left_cap != 0:
            bins.append(bin)
            for item in bin.inputitem:
                items.append(item)
    for bin in bins:
        copy_problem.bins.remove(bin)
    for bin in problem.extrabins:
        if bin.cur_weight!= problem.cap and bin.left_cap != 0:
            bins.append(bin)
            for item in bin.inputitem:
                items.append(item)
        copy_problem.extrabins = []
    return items,copy_problem

def shaking(problem:Problem):
    """
    shake the problem that the non filled bins use bestfit to choose
    """
    unfillitems,copy_problem = getUnfillbins(problem)
    unfillitems.sort(key = lambda x:x.weight,reverse= True)
    bin = Bin(copy_problem.cap)
    bid = 0
    addbinList = [bin]
    while(len(unfillitems) != 0):
        toReomveitems = []
        bin = addbinList[bid]
        for item in unfillitems:
            if bin.canfit(item):
                bin.additem(item)
                toReomveitems.append(item)
        for item in toReomveitems:
            unfillitems.remove(item)
        if len(unfillitems) != 0:
            bid += 1
            bin = Bin(problem.cap)
            addbinList.append(bin)
    for bin in addbinList:
        copy_problem.bins.append(bin)
    copy_problem.resetbins()
    problem = copy_problem
    return problem   

def find_best_item_combine(space,items:list):
    list = []
    binweight = []
    for i in range(len(items)):
        dict = {}
        list.append(dict)
    for j in range(space + 1):
        binweight.append(0)
    for i in range(0,len(items),1):
        for j in range(space,-1,-1):
            list[i][j] = False
            if ( j>= items[i].weight ) :
                if ( binweight[j] <= binweight[j-items[i].weight]+ items[i].weight ): 
                    binweight[j] = binweight[j-items[i].weight]+items[i].weight
                    list[i][j] = True
    select_item_to_change = []
    j = space
    for i in range(len(items),0,-1):
        if list[i - 1][j] == True:
            select_item_to_change.append(items[i - 1])
            j -= items[i - 1].weight
    return select_item_to_change,binweight[space]

def local_search( cap, num,items,Min,c_list):
    """
    deep first search to get a local problem for 
    single bin item packing
    """
    if Min>cap:
        Min = cap
    if (num == len(items)) :
        return
    if (cap-items[num].weight >= 0) :
        c_list.append(items[num])
        local_search(cap-items[num].weight ,num+1,items,Min,c_list)
    else:
        local_search(cap,num+1,items,Min,c_list)
def select_item_to_change(morebin,lessbin):
    """
    change one item from more bin to another bin make the space more
    """
    clist = []
    c_sum = 0
    for item in morebin.inputitem:
        if item.type == "VLarge" :
            continue
        c_space = morebin.left_cap + item.weight
        if c_space <= 20000 :
            items = lessbin.inputitem
            clist, c_sum= find_best_item_combine(c_space,items)
            # print(clist, c_sum)
        else:
            cap = morebin.cap
            c_list = []
            c_sum = c_space
            items = lessbin.inputitem
            local_search(cap,0,items,c_sum,c_list)
            c_sum = c_space - c_sum
        if c_sum >= item.weight:
            return c_sum,clist,item
    return None,None,None

def split(problem:Problem):
    """
    random choose one bin and split it's items to 2 bin
    """
    randid = random.randint(0,len(problem.bins) - 1)
    bin = problem.bins[randid]
    nbin = Bin(problem.cap)
    items = []
    for i in range(int(len(bin.inputitem)/2)):
        items.append(bin.inputitem[i])
    for item in items:
        bin.removeitem(item)
        nbin.additem(item)
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
    return None,None

def randomShake(problem:Problem):
    """
    choose 2 bin to shake randomly
    """
    problem.resetbins()
    copy_problemopy = copy.copy(problem)
    all_bins = []
    for bin in copy_problemopy.bins:
        all_bins.append(bin)
    for bin in copy_problemopy.extrabins:
        all_bins.append(bin)
    bin_num = len(all_bins)
    randbin1 = random.randint(0,bin_num - 1)
    randbin2 = random.randint(0,bin_num - 1)
    while(randbin1 == randbin2):
        randbin2 = random.randint(0,bin_num - 1)
    bin1 = all_bins[randbin1]
    bin2 = all_bins[randbin2]
    if bin1.left_cap > bin2.left_cap:
        bin_T = bin1 
        bin1 =  bin2 
        bin2 = bin_T
    item1,item2 = swap(bin1,bin2) 
    if item1 != None:
            bin1.removeitem(item2)
            bin2.removeitem(item1)
            bin1.additem(item1)
            bin2.additem(item2) 
    problem = copy.copy(copy_problemopy)
    problem.resetbins()

    return problem

def Getmorecapleft(morebin,lessbin,type):
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
                clist, c_sum= find_best_item_combine(c_space,items)
            else:
                cap = morebin.cap
                c_list = []
                c_sum = c_space
                items = lessbin.inputitem
                local_search(cap,0,items,c_sum,c_list)
                c_sum = c_space - c_sum
            if c_sum >= item.weight:
                return c_sum,clist,item
    return None,None,None

def chooseTwoType(problem:Problem,type1,type2):
    """
    for the item type choose 2 Type of bins
    """
    copy_problemopy = copy.copy(problem)
    Type1 = []
    Type2 = []       
    for bin in copy_problemopy.bins:
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
    problem = copy_problemopy
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
            c_sum,clist,item = Getmorecapleft(morebin,lessbin,type)
            if c_sum == None:
                continue
            else:
                morebin.removeitem(item)
                lessbin.additem(item)
                for item in clist:
                    morebin.additem(item)
                    lessbin.removeitem(item)
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
    bid = 0
    addbinList = [bin]
    while(len(tempitems) != 0):
        toReomveitems = []
        bin = addbinList[bid]
        for item in tempitems:
            if bin.canfit(item):
                bin.additem(item)
                toReomveitems.append(item)
        for item in toReomveitems:
            tempitems.remove(item)
        if len(tempitems) != 0:
            bid += 1
            bin = Bin(problem.cap)
            addbinList.append(bin)
    problem.extrabins = []
    for bin in addbinList:
        problem.extrabins.append(bin)
    return problem

def dealExtra(problem:Problem):  
    """
    try to put the items in extra to the other bins
    """
    for morebin in problem.bins:
        toRemove = []
        for lessbin in problem.extrabins:
            c_sum,clist,item = select_item_to_change(morebin,lessbin)
            if c_sum == None:
                continue
            else:
                morebin.removeitem(item)
                lessbin.additem(item)
                for item in clist:
                    morebin.additem(item)
                    lessbin.removeitem(item)
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
            if bin.canfit(item):
                bin.additem(item)
                toRemove.append(bin)
                break
    for item in toRemove:
        for bin in problem.extrabins:
                bin.removeitem(item)
    problem.resetbins()
    return problem

def checkResult(problem1:Problem,problem2:Problem):
    if len(problem1.extrabins) < len(problem2.extrabins):
        return problem1
    elif len(problem1.extrabins) > len(problem2.extrabins):
        return problem2
    else:
        sum1 = 0
        sum2 = 0
        for bin in problem1.extrabins:
            sum1 += bin.left_cap
        for bin in problem2.extrabins:
            sum2 += bin.left_cap
        if sum1 > sum2:
            return problem1
        else:
            return problem2
def variable_neibourhood_search(problem, best_problem):
    shaking_time = 30
    problem = shaking(problem)
    for i in range(shaking_time):
        problem,best_problem= neighbourhood(problem, best_problem)
        if len(best_problem.extrabins) <= 1:
            break
        if i >0:
            problem = shaking(problem)
    return problem, best_problem
def neighbourhood(problem, best_problem):
    problem = chooseTwoType(problem,"VLarge","Large")
    problem = dealExtra(problem)
    problem = bffExtra(problem)
    problem = bestfitExtra(problem)
    best_problem = checkResult(problem,best_problem)
    return problem, best_problem
def neighbourhood2(problem, best_problem):
    problem = chooseTwoType(problem,"Large","Mid")
    problem = dealExtra(problem)
    problem = chooseTwoType(problem,"VLarge","Large")
    problem = bffExtra(problem)
    best_problem = checkResult(problem,best_problem)
    return problem, best_problem
def mutiple_randomshake(problem):
    for t in range(300):
        problem = randomShake(problem)
    return problem
def process_problem2(problem, best_problem):
    problem = mutiple_randomshake(problem)
    problem,best_problem = neighbourhood2(problem, best_problem)
    return problem, best_problem
def process_problem3(problem, best_problem):
    for i in range(20):
        if i%3 == 0:
            problem  = split(problem)
        mutiple_randomshake(problem)
        problem,best_problem = neighbourhood2(problem, best_problem)
        if len(best_problem.extrabins) <= 1:
            break
    return problem, best_problem
def simulated_annealing(problem,best_problem,temperature=100, cooling_rate=0.8,end_temperature=20):
    currentproblem = copy.deepcopy(problem)
    newproblem = copy.deepcopy(problem)
    while temperature > end_temperature:
        print("Temperature",temperature)
        newproblem,best_problem= process_problem2(newproblem, best_problem)
        if len(best_problem.extrabins) <= 1:
            break
        delta = len(newproblem.extrabins) - len(currentproblem.extrabins)
        if delta > 0:
            best_problem = copy.deepcopy(currentproblem)
        else:
            if random.random() < math.exp(delta / temperature):
                newproblem = copy.deepcopy(currentproblem)
        temperature *= cooling_rate

    return problem,best_problem
def main():
    totaltime = 0
    filename = sys.argv[2]
    problemlist = readfile(filename)
    problemslnlist = []
    for problem in problemlist:
        startT = time.time()
        bestFit(problem)
        best_problem = copy.copy(problem)
        problem.resetbins()
        problem, best_problem = variable_neibourhood_search(problem, best_problem)
        if len(best_problem.extrabins) <= 1:
            best_problem = bestfitExtra(best_problem)
            problemslnlist.append(best_problem)
            continue
        problem, best_problem = simulated_annealing(problem, best_problem)
        #problem, best_problem = process_problem2(problem, best_problem)
        if len(best_problem.extrabins) <= 1:
            best_problem = bestfitExtra(best_problem)
            problemslnlist.append(best_problem)
            continue

        """ problem, best_problem = process_problem3(problem, best_problem)
        if len(best_problem.extrabins) <= 1:
            best_problem = bestfitExtra(best_problem)
            problemslnlist.append(best_problem)
            continue """
        best_problem = bestfitExtra(best_problem)
        endT = time.time()
        print("Running time ",endT - startT)
        totaltime += (endT - startT)
        problemslnlist.append(problem)
    output(problemslnlist,sys.argv[4])
    print(totaltime)
if __name__ == "__main__":
    main()