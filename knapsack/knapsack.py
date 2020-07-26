import numpy as np

class Knapsack():
    def __init__(self,param1,param2,param3):   
        self.value=param1
        self.m=len(self.value)
        
        self.cap=param2
        self.weight=param3
        self.dim=tuple([self.m]+[i+1 for i in self.cap])
        self.n=len(self.cap)
        
        self.collection=set()
        self.maxIncome=None
        
        self.state=np.zeros(self.dim)
        
    def recursiveFor(self,i,nowd,cap):
        if nowd==self.n+1:
            cap2=cap[:]
            overWeight=False
            for j in range(self.n):
                cap2[j]=cap[j]-self.weight[i][j]
                if self.weight[i][j]>cap[j]:
                    overWeight=True
                    break
            ind1=tuple([i]+cap)
            ind2=tuple([i-1]+cap)
            ind3=tuple([i-1]+cap2)
            if overWeight:
                if i==0:
                    self.state[ind1]=0
                else:
                    self.state[ind1]=self.state[ind2]
            else:
                if i==0:
                    self.state[ind1]=self.value[i]
                else:                    
                    self.state[ind1]=max(self.state[ind2],self.state[ind3]+self.value[i])           
        else:
            for k in range(self.dim[nowd]):
                self.recursiveFor(i,nowd+1,cap+[k])
                
    def retro(self):
        cap=self.cap[:]
        self.maxIncome=self.state[tuple([self.m-1]+cap)]
        for i in range(self.m-1,-1,-1):
            ind1=tuple([i]+cap)
            ind2=tuple([i-1]+cap)
            if i==0:
                if self.state[ind1]!=0:
                    self.collection.add(i)
            else:
                if self.state[ind1]!=self.state[ind2]:
                    self.collection.add(i)
                    for j in range(self.n):
                        cap[j]-=self.weight[i][j]
                
    def solve(self):
        nowd=1
        cap=[]
        for i in range(self.m):
            self.recursiveFor(i,nowd,cap)
        self.retro()
