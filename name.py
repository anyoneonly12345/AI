
import copy
from random import randint
import re
import sys
import time

class Bin:
    
    def __init__(self,id,v,type = 0):
        """
        id: the bin id 
        v: the v of bin
        type : the bin type 
        """
        self.id = id
        self.v = v
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
        print("BIN: ",self.id,self.v,self.type)
class Prob:
    
    def __init__(self,title,cap,binNum,bestNum):
        """
        title: the title of prob
        cap: the cap of the prob
        binNum: the total bin number
        bestNUm: the best solution number
        """
        self.title = title
        self.cap = int(cap )
        self.binNum = int(binNum )
        self.bestNum = int(bestNum)
        self.bins = []
        self.VLargebins = []
        self.Largebins = []
        self.Midbins = []
        self.Smallbins = []
        self.Tinybins = []
        self.containers = []
        self.extracontainers = []
        self.allcontainers = []
    def classifyBins(self,bin:Bin):
        if bin.type == "VLarge":
            self.VLargebins.append(bin)
        elif bin.type == "Large":
            self.Largebins.append(bin)
        elif bin.type == "Mid":
            self.Midbins.append(bin)
        elif bin.type == "Small":
            self.Smallbins.append(bin)
        elif bin.type == "Tiny":
            self.Tinybins.append(bin)
    def throwEmpty(self):
        toRemove = []
        for container in self.extracontainers:
            if container.left_v == self.cap and container.cur_v == 0:
                toRemove.append(container)
        for container in toRemove:
            self.extracontainers.remove(container)
    def resetcontainers(self):
        """
        reset the containers and the extra containers
        """
        allContainers = []
        for container in self.containers:
            if container.left_v != self.cap and container.cur_v != 0:
                allContainers.append(container)
        for container in self.extracontainers:
            if container.left_v != self.cap and container.cur_v != 0:
                allContainers.append(container)
        allC = []
        allC = copy.copy(allContainers)
        allC.sort(key = lambda x:x.left_v, reverse= False)
        self.containers = []
        self.extracontainers = []
        toRemove = []
        for container in allC:
            if container.left_v == self.cap and container.cur_v == 0:
                toRemove.append(container)
        for container in toRemove:
            allC.remove(container)
        
        for i in range(len(allC) ):
            if i < self.bestNum:
                self.containers.append(allC[i])
            else:
                if container.left_v != self.cap and container.cur_v != 0:
                    self.extracontainers.append(allC[i])
                    # print("Extra", container.left_v, container.cur_v)
        self.throwEmpty()
        # print(self.extracontainers)
        bestfitExtra(self)
class Container:
    def __init__(self,cap):
        """
        cap : the cap of the container
        """
        self.cap = cap
        self.inputbin = []
        self.cur_v = 0
        self.left_v = cap
        LargeBinlist=[]
        VLargeBinlist=[]
        MidBinlist = []
        SmallBinlist = []
        TinyBinlist = []
        self.dict = {"VLarge":VLargeBinlist,"Large":LargeBinlist,"Mid":MidBinlist,
            "Small":SmallBinlist,"Tiny":TinyBinlist}
    def addBin(self,bin:Bin):
        """
        bin: the bin to add 
        """
        self.inputbin.append(bin)
        self.cur_v += bin.v
        self.left_v -= bin.v
        self.dict[bin.type].append(bin)
    def removeBin(self,bin:Bin):
        """
        bin: the bin to remove
        """
        self.inputbin.remove(bin)
        self.cur_v -= bin.v
        self.left_v += bin.v
        self.dict[bin.type].remove(bin)
    def show(self):
        print("Show container ","cur v = ", self.cur_v,"left v = ", self.left_v)
def readfile(filename):
    """ 
    read the file and build the problem class
    """
    f = open(filename,"r")
    pro_num = f.readline()
    problist = []
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
        prob = Prob(title,temp_t[0],temp_t[1],temp_t[2])
        for j in range(int(temp_t[2])):
            prob.containers.append(Container(prob.cap))
        
        for j in range (int(temp_t[1])):
            binc = f.readline()
            # print("binc = ",binc)
            bintype = int(binc)/prob.cap
            bin = Bin(j,int(binc),bintype)
            prob.bins.append(bin)
            prob.classifyBins(bin)
        problist.append(prob)
    return problist
def bestFit(prob:Prob):
    """
    bestfit method to solve the problem
    """
    prob.bins.sort(key=lambda x:x.v, reverse=True)
    tempbins = copy.copy(prob.bins)
    for container in prob.containers:
        toReomveBins = []
        for bin in tempbins:
            if container.left_v >= bin.v:
                container.addBin(bin)
                toReomveBins.append(bin)
        for bin in toReomveBins:
            tempbins.remove(bin)
    container = Container(prob.cap)
    cid = 0
    addContainerList = [container]
    while(len(tempbins) != 0):
        toReomveBins = []
        container = addContainerList[cid]
        for bin in tempbins:
            if container.left_v >= bin.v:
                container.addBin(bin)
                toReomveBins.append(bin)
        for bin in toReomveBins:
            tempbins.remove(bin)
        if len(tempbins) != 0:
            cid += 1
            container = Container(prob.cap)
            addContainerList.append(container)
    for container in addContainerList:
        prob.extracontainers.append(container)
    print("Add num",len(addContainerList))
def checker(prob:Prob):
    """
    check if the solution is right 
    """
    bins = copy.copy(prob.bins)
    for container in prob.containers:
        cap = prob.cap
        for bin in container.inputbin:
            bins.remove(bin)
            cap -= bin.v
            if cap == prob.cap:
                print("WARNING :empty")
            if cap < 0:
                print("ERROR: overload")
    for container in prob.extracontainers:
        cap = prob.cap
        for bin in container.inputbin:
            # bin.show()
            bins.remove(bin)
            cap -= bin.v
            if cap < 0:
                print("extra ERROR: overload")
    # print("len bins ",len(bins))
    for bin in bins:
        print("Miss bin", bin.show())

def output(problist:list,filename):
    """
    get the solution and print it to the file
    """
    outfile = open(filename,'w')
    print(len(problist),file = outfile)
    for prob in problist:
        prob.resetcontainers()
        prob.throwEmpty()
        # checker(prob)
        print(prob.title,file = outfile)
        print(prob.title)
        print(prob.extracontainers)
        num = len(prob.containers) + len(prob.extracontainers)
        print(" obj=  ",num, num- prob.bestNum,file = outfile)
        for container in prob.containers:
            for bin in container.inputbin:
                print(bin.id, end=" ",file = outfile)
            print(file = outfile)
        for container in prob.extracontainers:
            if container.left_v != prob.cap and container.cur_v != 0:
                # allContainers.append(container)
                for bin in container.inputbin:
                    print(bin.id, end=" ",file = outfile)
                print(file = outfile)
            container.show()

def getUnfillContainers(prob:Prob):
    """
    get the containers not full 
    :bins: the bins for the containers
    :containers: the containers that not full
    :prob_c: prob after remove the containers and bins
    """
    bins = []
    containers = []
    prob_c = copy.copy(prob)
    for container in prob.containers:
        if container.cur_v != prob.cap and container.left_v != 0:
            containers.append(container)
            for bin in container.inputbin:
                bins.append(bin)
    for container in containers:
        prob_c.containers.remove(container)
    for container in prob.extracontainers:
        if container.cur_v != prob.cap and container.left_v != 0:
            containers.append(container)
            for bin in container.inputbin:
                bins.append(bin)
        prob_c.extracontainers = []
    return bins,containers,prob_c

def shaking(prob:Prob):
    """
    shake the problem that the non filled containers use bestfit to choose
    """
    unfillbins,unfillcontainers,prob_c = getUnfillContainers(prob)
    unfillbins.sort(key = lambda x:x.v,reverse= True)
    container = Container(prob_c.cap)
    cid = 0
    addContainerList = [container]
    while(len(unfillbins) != 0):
        toReomveBins = []
        container = addContainerList[cid]
        for bin in unfillbins:
            if container.left_v >= bin.v:
                container.addBin(bin)
                toReomveBins.append(bin)
        for bin in toReomveBins:
            unfillbins.remove(bin)
        if len(unfillbins) != 0:
            cid += 1
            container = Container(prob.cap)
            addContainerList.append(container)
    for container in addContainerList:
        prob_c.containers.append(container)
    prob_c.resetcontainers()
    prob = prob_c
    return prob   

def dpAns(space,bins:list):
    """
    dynamic programming to get the best solution
    bins should no more than 30
    """
    list = []
    dp = []
    for i in range(len(bins)):
        dict = {}
        list.append(dict)
    for j in range(space + 1):
        dp.append(0)
    for i in range(0,len(bins),1):
        for j in range(space,-1,-1):
            list[i][j] = False
            if ( j>= bins[i].v ) :
                if ( dp[j] <= dp[j-bins[i].v]+ bins[i].v ): 
                    dp[j] = dp[j-bins[i].v]+bins[i].v
                    list[i][j] = True
    changeBins = []
    j = space
    for i in range(len(bins),0,-1):
        if list[i - 1][j] == True:
            changeBins.append(bins[i - 1])
            j -= bins[i - 1].v
    return changeBins,dp[space]

def dfs( cap, num,bins,Min,c_list):
    """
    deep first search to get a local solution for 
    single container bin packing
    """
    Min = min(Min,cap)
    if (num == len(bins)) :
        return
    if (cap-bins[num].v < 0) :
        dfs(cap,num+1,bins,Min,c_list)
    else:
        c_list.append(bins[num])
        dfs(cap-bins[num].v ,num+1,bins,Min,c_list)

def changeBins(morecontainer,lesscontainer):
    """
    change one bin from more container to another container make the space more
    """
    clist = []
    c_sum = 0
    for bin in morecontainer.inputbin:
        if bin.type == "VLarge" :
            continue
        c_space = morecontainer.left_v + bin.v
        if c_space <= 20000 and len(lesscontainer.inputbin) <= 25:
            bins = lesscontainer.inputbin
            clist, c_sum= dpAns(c_space,bins)
            # print(clist, c_sum)
        else:
            cap = morecontainer.cap
            c_list = []
            c_sum = c_space
            bins = lesscontainer.inputbin
            dfs(cap,0,bins,c_sum,c_list)
            c_sum = c_space - c_sum
        if c_sum >= bin.v:
            return c_sum,clist,bin
    return None,None,None

def split(prob:Prob):
    """
    random choose one container and split it's bins to 2 container
    """
    randid = randint(0,prob.bestNum - 1)
    container = prob.containers[randid]
    ncontainer = Container(prob.cap)
    bins = []
    for i in range(int(len(container.inputbin)/2)):
        bins.append(container.inputbin[i])
    for bin in bins:
        container.removeBin(bin)
        ncontainer.addBin(bin)
    prob.extracontainers.append(ncontainer)
    return prob

def swap(morecontainer,lesscontainer):
    """
    swap one bin from more container to another container make the space more
    """
    morecontainer1 = copy.copy(morecontainer)
    lesscontainer1 = copy.copy(lesscontainer)
    lesscontainer1.inputbin.sort(key = lambda x:x.v,reverse = False)
    morecontainer1.inputbin.sort(key = lambda x:x.v,reverse = False)
    for mbin in morecontainer1.inputbin:
        for lbin in lesscontainer1.inputbin:
            if lbin.v < mbin.v:
                break 
            if mbin.v < lbin.v and mbin.v+morecontainer1.left_v >=lbin.v:
                return lbin,mbin
    return None

def randomShake(prob:Prob):
    """
    choose 2 container to shake randomly
    """
    prob.resetcontainers()
    prob_copy = copy.copy(prob)
    all_containers = []
    for container in prob_copy.containers:
        all_containers.append(container)
    for container in prob_copy.extracontainers:
        all_containers.append(container)
    container_num = len(all_containers)
    randContainer1 = randint(0,container_num - 1)
    randContainer2 = randint(0,container_num - 1)
    if randContainer1 == randContainer2:
        randContainer2 +=1 
        randContainer2 %= container_num
    container1 = all_containers[randContainer1]
    container2 = all_containers[randContainer2]
    if container1.left_v > container2.left_v:
        container_T = container1 
        container1 =  container2 
        container2 = container_T
    sln = swap(container1,container2) # 2 have more left space
    if sln != None:
            container1.removeBin(sln[1])
            container2.removeBin(sln[0])
            container1.addBin(sln[0])
            container2.addBin(sln[1])

     
    prob = copy.copy(prob_copy)
    prob.resetcontainers()

    return prob

def changeBinswithType(morecontainer,lesscontainer,type):
    """
    change one bin from more container to another container make the space more
    """
    clist = []
    c_sum = 0
    for bin in morecontainer.inputbin:
        if bin.type == type :
            c_space = morecontainer.left_v + bin.v
            if c_space <= 20000 and len(morecontainer.inputbin) <= 25:
                bins = lesscontainer.inputbin
                clist, c_sum= dpAns(c_space,bins)
            else:
                cap = morecontainer.cap
                c_list = []
                c_sum = c_space
                bins = lesscontainer.inputbin
                dfs(cap,0,bins,c_sum,c_list)
                c_sum = c_space - c_sum
            if c_sum >= bin.v:
                return c_sum,clist,bin
    return None,None,None

def chooseTwoGroup(prob:Prob,type1,type2):
    """
    for the bin type choose 2 group of containers
    """
    prob_copy = copy.copy(prob)
    group1 = []
    group2 = []       
    for container in prob_copy.containers:
        if container.left_v == 0:
            continue
        flagL = False
        for bin in container.inputbin:
            if bin.type == type1 :
                flagL = True
        if flagL == False:
            group1.append(container)
        else:
            group2.append(container)
        group1,group2 = groupChange(group1,group2,type2)
    prob = prob_copy
    return prob

def groupChange(group1:list,group2:list,type):
    """
    Change the bins in containers of different groups
    
    """
    group1_c = copy.copy(group1)
    group2_c = copy.copy(group2)
    for morecontainer in group1_c:
        toRemove = []
        for lesscontainer in group2_c:
            c_sum,clist,bin = changeBinswithType(morecontainer,lesscontainer,type)
            if c_sum == None:
                continue
            else:
                morecontainer.removeBin(bin)
                lesscontainer.addBin(bin)
                for bin in clist:
                    morecontainer.addBin(bin)
                    lesscontainer.removeBin(bin)
                break
        for container in toRemove:
            group2_c.remove(container)
    return group1_c,group2_c

def bestfitExtra(prob:Prob):
    extras = prob.extracontainers
    tempbins = []
    for container in extras:
        for bin in container.inputbin:
            tempbins.append(bin)
    container = Container(prob.cap)
    cid = 0
    addContainerList = [container]
    while(len(tempbins) != 0):
        toReomveBins = []
        container = addContainerList[cid]
        for bin in tempbins:
            if container.left_v >= bin.v:
                container.addBin(bin)
                toReomveBins.append(bin)
        for bin in toReomveBins:
            tempbins.remove(bin)
        if len(tempbins) != 0:
            cid += 1
            container = Container(prob.cap)
            addContainerList.append(container)
    prob.extracontainers = []
    for container in addContainerList:
        prob.extracontainers.append(container)
    return prob

def dealExtra(prob:Prob):  
    """
    try to put the bins in extra to the other containers
    """
    for morecontainer in prob.containers:
        toRemove = []
        for lesscontainer in prob.extracontainers:
            c_sum,clist,bin = changeBins(morecontainer,lesscontainer)
            if c_sum == None:
                continue
            else:
                morecontainer.removeBin(bin)
                lesscontainer.addBin(bin)
                for bin in clist:
                    morecontainer.addBin(bin)
                    lesscontainer.removeBin(bin)
                break
        for container in toRemove:
            prob.extracontainers.remove(container)
    prob.resetcontainers()
    return prob

def bffExtra(prob:Prob):  
    """
    try to put the bins in extra to the other containers
    """
    extrabins = []
    for container in prob.extracontainers:
        for bin in container.inputbin:
            extrabins.append(bin)
    extrabins.sort(key = lambda x:x.v,reverse= True)
    toRemove = []
    for bin in extrabins:
        for container in prob.containers:
            if container.left_v >= bin.v:
                container.addBin(bin)
                toRemove.append(container)
                break
    for bin in toRemove:
        for container in prob.extracontainers:
            try:
                container.removeBin(bin)
            except:
                pass
    prob.resetcontainers()
    return prob

def checkResult(prob1:Prob,prob2:Prob):
    """
    Compare the problem result return the better one
    """
    if len(prob1.extracontainers) < len(prob2.extracontainers):
        return prob1
    elif len(prob1.extracontainers) > len(prob2.extracontainers):
        return prob2
    else:
        sum1 = 0
        sum2 = 0
        for container in prob1.extracontainers:
            sum1 += container.cur_v
        for container in prob2.extracontainers:
            sum2 += container.cur_v
        if sum1 < sum2:
            return prob1
        else:
            return prob2

def main():
    totaltime = 0
    filename = sys.argv[2]
    problist = readfile(filename)
    probslnlist = []
    for prob in problist:
        flag = False
        startT = time.time()
        bestFit(prob)
        best_prob = copy.copy(prob)
        prob.resetcontainers()
        for i in range(30):
            if i != 0:
                prob = shaking(prob)
            prob = chooseTwoGroup(prob,"VLarge","Large")
            prob = dealExtra(prob)
            prob = bffExtra(prob)
            prob = bestfitExtra(prob)
            best_prob = checkResult(prob,best_prob)
            if len(best_prob.extracontainers) <= 1:
                flag = True
                break
        if flag == True:
            best_prob = bestfitExtra(best_prob)
            probslnlist.append(best_prob)
            continue
        for i in range(30):
            for t in range(200):
                prob = randomShake(prob)
            prob = chooseTwoGroup(prob,"Large","Mid")
            prob = dealExtra(prob)
            prob = chooseTwoGroup(prob,"VLarge","Large")
            prob = checkResult(bffExtra(prob),prob)
            best_prob = checkResult(prob,best_prob)
            if len(best_prob.extracontainers) <= 1:
                flag = True
                break
        if flag == True:
            best_prob = bestfitExtra(best_prob)
            probslnlist.append(best_prob)
            continue

        for i in range(20):
            if i%3 == 0:
                prob  = split(prob)
            for t in range(300):
                prob = randomShake(prob)
            prob = chooseTwoGroup(prob,"Large","Mid")
            prob = dealExtra(prob)
            prob = chooseTwoGroup(prob,"VLarge","Large")
            prob = checkResult(bffExtra(prob),prob)
            best_prob = checkResult(prob,best_prob)
            if len(best_prob.extracontainers) <= 1:
                flag = True
                break
        if flag == True:
            best_prob = bestfitExtra(best_prob)
            probslnlist.append(best_prob)
            continue
        best_prob = bestfitExtra(best_prob)
        endT = time.time()
        print("Running time ",endT - startT)
        totaltime += (endT - startT)
        probslnlist.append(prob)
        

    output(probslnlist,sys.argv[4])
    print(totaltime)
        

 
main()