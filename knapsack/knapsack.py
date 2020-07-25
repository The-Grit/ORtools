class Knapsack():
    def __init__(self,params):   
        self.value=params[0]
        self.n=len(self.value)
        
        self.cap=params[1]
        self.weight=params[2]
        self.m=len(self.cap)
        
        self.collection=set()
        self.maxIncome=None
        
        self.choose={}
        self.memory={}
        
    def compress(self,remainObj):
        num=0
        for i in remainObj:
            num+=1<<i
        return num
    
    def dynamicRecursion(self,cap,remainObj):
        if not remainObj:
            return 0
        compressNum=self.compress(remainObj)
        if compressNum in self.memory:
            return self.memory[compressNum]
        maxV=float('-inf')
        bestObj=-1
        allOverWeight=True
        for obj in remainObj:
            overWeight=False
            cap2=cap[:]
            for i in range(self.m):
                if self.weight[i][obj]>cap[i]:
                    overWeight=True
                    break
                else:
                    cap2[i]=cap2[i]-self.weight[i][obj]
            if overWeight:
                continue  
            allOverWeight=False
            remainObj2=remainObj[:]
            remainObj2.remove(obj)
            Value=self.value[obj]+self.dynamicRecursion(cap2,remainObj2)
            if Value>maxV:
                maxV=Value
                bestObj=obj  
        if allOverWeight:
            return 0
        self.memory[compressNum]=maxV
        self.choose[compressNum]=bestObj              
        return maxV
                       
    def retro(self):
        remainObj=[i for i in range(self.n)]
        while True:
            compressNum=self.compress(remainObj)
            obj=self.choose.get(compressNum,-1)
            if obj==-1:
                break
            self.collection.add(obj)
            remainObj.remove(obj)
               
    def solve(self):
        cap=self.cap[:]
        remainObj=[i for i in range(self.n)]
        self.maxIncome=self.dynamicRecursion(cap,remainObj)
        self.retro()