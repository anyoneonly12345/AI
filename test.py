
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
    def show(self):
        print("Show bin ","cur v = ", self.cur_weight,"left v = ", self.left_cap)
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
            # print("itemc = ",itemc)
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
            if bin.left_cap >= item.weight:
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
            if bin.left_cap >= item.weight:
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
            if bin.left_cap != problem.cap and bin.cur_weight!= 0:
                # allbins.append(bin)
                for item in bin.inputitem:
                    print(item.id, end=" ",file = outfile)
                print(file = outfile)
            bin.show()

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
            if bin.left_cap >= item.weight:
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

def dpAns(space,items:list):
    """
    dynamic programming to get the best problem
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
    changeitems = []
    j = space
    for i in range(len(items),0,-1):
        if list[i - 1][j] == True:
            changeitems.append(items[i - 1])
            j -= items[i - 1].weight
    return changeitems,dp[space]

def dfs( cap, num,items,Min,c_list):
    """
    deep first search to get a local problem for 
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

def changeitems(morebin,lessbin):
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
    return None

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
    if randbin1 == randbin2:
        randbin2 +=1 
        randbin2 %= bin_num
    bin1 = all_bins[randbin1]
    bin2 = all_bins[randbin2]
    if bin1.left_cap > bin2.left_cap:
        bin_T = bin1 
        bin1 =  bin2 
        bin2 = bin_T
    sln = swap(bin1,bin2) # 2 have more left space
    if sln != None:
            bin1.removeitem(sln[1])
            bin2.removeitem(sln[0])
            bin1.additem(sln[0])
            bin2.additem(sln[1])

     
    problem = copy.copy(copy_problemopy)
    problem.resetbins()

    return problem

def changeitemswithType(morebin,lessbin,type):
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

def chooseTwoGroup(problem:Problem,type1,type2):
    """
    for the item type choose 2 group of bins
    """
    copy_problemopy = copy.copy(problem)
    group1 = []
    group2 = []       
    for bin in copy_problemopy.bins:
        if bin.left_cap == 0:
            continue
        flagL = False
        for item in bin.inputitem:
            if item.type == type1 :
                flagL = True
        if flagL == False:
            group1.append(bin)
        else:
            group2.append(bin)
        group1,group2 = groupChange(group1,group2,type2)
    problem = copy_problemopy
    return problem

def groupChange(group1:list,group2:list,type):
    """
    Change the items in bins of different groups
    
    """
    group1_c = copy.copy(group1)
    group2_c = copy.copy(group2)
    for morebin in group1_c:
        toRemove = []
        for lessbin in group2_c:
            c_sum,clist,item = changeitemswithType(morebin,lessbin,type)
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
            group2_c.remove(bin)
    return group1_c,group2_c

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
            if bin.left_cap >= item.weight:
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
            c_sum,clist,item = changeitems(morebin,lessbin)
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
            if bin.left_cap >= item.weight:
                bin.additem(item)
                toRemove.append(bin)
                break
    for item in toRemove:
        for bin in problem.extrabins:
            try:
                bin.removeitem(item)
            except:
                pass
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
    problem = chooseTwoGroup(problem,"VLarge","Large")
    problem = dealExtra(problem)
    problem = bffExtra(problem)
    problem = bestfitExtra(problem)
    best_problem = checkResult(problem,best_problem)
    return problem, best_problem
def neighbourhood2(problem, best_problem):
    problem = chooseTwoGroup(problem,"Large","Mid")
    problem = dealExtra(problem)
    problem = chooseTwoGroup(problem,"VLarge","Large")
    problem = bffExtra(problem)
    best_problem = checkResult(problem,best_problem)
    return problem, best_problem
def mutiple_randomshake(problem):
    for t in range(300):
        problem = randomShake(problem)
    return problem
def process_problem2(problem, best_problem):
    for i in range(20):
        problem = mutiple_randomshake(problem)
        problem,best_problem = neighbourhood2(problem, best_problem)
        if len(best_problem.extrabins) <= 1:
            break
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
        problem, best_problem = process_problem2(problem, best_problem)
        if len(best_problem.extrabins) <= 1:
            best_problem = bestfitExtra(best_problem)
            problemslnlist.append(best_problem)
            continue

        problem, best_problem = process_problem3(problem, best_problem)
        if len(best_problem.extrabins) <= 1:
            best_problem = bestfitExtra(best_problem)
            problemslnlist.append(best_problem)
            continue
        best_problem = bestfitExtra(best_problem)
        endT = time.time()
        print("Running time ",endT - startT)
        totaltime += (endT - startT)
        problemslnlist.append(problem)
    output(problemslnlist,sys.argv[4])
    print(totaltime)
        

 
main()