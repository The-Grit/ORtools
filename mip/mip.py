import simplex
import math
import numpy as np
import copy

def guidance():
	syntax='You need a goal,n,cost vector,coefficient matrix,constant vector,relation vector,intmark,binmark.\n'
	detail='goal means whether you want to maximize the problem;n means the total number of variables;intmark means whether a varible is a integer;binmark means whether a variable is a 0-1.\n'
	defualt='binmark is defaulted to [[],[]]\n'
	easyuse='You can use [[index list],[coefficient list]] to place [coefficient list]\n'
	solve='You can create a solver by entering ins=mip.solver(params) and solve it by entering ins.solve()\n'
	print(syntax+detail+default+easyuse)
class solver():
    def __init__(self,goal,n,cost,coefficient,constant,relation,intmark,binmark=[[],[]],gap=0.001):
        self.upperbound=float('inf')
        self.lowerbound=float('-inf')
        self.goal=goal
        self.n=n
        cost,coefficient,constant,relation,self.intmark,self.binmark=self.termGenerate(cost,coefficient,constant,relation,intmark,binmark)
        self.cost=np.array(cost)
        self.coefficient=((np.array(coefficient)).astype('float')).reshape((len(relation),len(cost)))
        self.constant=constant
        self.relation=relation
        #self.intmark=intmark # intmark is a list recording which variable is integer
        self.nodes=[]
        
        self.value=float('inf')
        self.solution=None
        self.status='Unknown'
        self.gap=gap
        self.finalgap=float('inf')
        
        self.goalchange=False
        self.standTran()
        
    def termGenerate(self,cost,coefficient,constant,relation,intmark,binmark):
        if type(cost[0])==list:
            p1=[0 for i in range(self.n)]
            for i in range(len(cost[0])):
                p1[cost[0][i]]=cost[1][i]
        else:
            p1=cost
        
        p2=[]  
        for row in coefficient:
            if type(row[0])==list:           
                temp=[0 for i in range(self.n)]
                for i in range(len(row[0])):
                    temp[row[0][i]]=row[1][i]
                p2.append(temp)
            else:
                p2.append(row)
                
        if type(constant[0])==list:
            p3=[0 for i in range(len(coefficient))]
            for i in range(len(constant[0])):
                p3[constant[0][i]]=constant[1][i]
        else:
            p3=constant
            
        if type(relation[0])==list:
            p4=[0 for i in range(len(coefficient))]
            for i in range(len(relation[0])):
                p4[relation[0][i]]=relation[1][i]
        else:
            p4=relation
            
        if type(intmark[0])==list:
            p5=[0 for i in range(self.n)]
            for i in range(len(intmark[0])):
                p5[intmark[0][i]]=intmark[1][i]
        else:
            p5=intmark
            
        if type(binmark[0])==list:
            p6=[0 for i in range(self.n)]
            for i in range(len(binmark[0])):
                p6[binmark[0][i]]=binmark[1][i]
        else:
            p6=binmark
            
        for i in range(len(binmark)):
            if binmark[i]:
                temp=[0 for j in range(self.n)]
                temp[i]=1
                p2.append(temp)
                p3.append(1)
                p4.append(0)
            
        return p1,p2,p3,p4,p5,p6 

    def standTran(self): # min问题转换为max问题
        if self.goal==0:
            self.cost = -1*self.cost
            self.goalchange=True
            self.goal=1
        
    def initnode(self):
        isint=True
        ins=simplex.solver(self.goal,self.cost,self.coefficient,self.constant,self.relation)
        ins.solve()
        if ins.status=='Unbounded':
            return 'Unbounded',None,None
        if ins.status=='Infeasible':
            return 'Infeasible',None,None
        node1=[ins.value]
        node2=[ins.value]
        for i in range(len(ins.solution)):
            v=ins.solution[i]
            if self.intmark[i] and round(v,0)!=v:
                node1.append([i,0,math.floor(v)])
                node2.append([i,2,math.floor(v)+1])
                isint=False
                break        
        if isint:
            self.lowerbound=ins.value
            self.upperbound=ins.value
            self.finalgap=0
            return 'Optimal',ins.value,ins.solution
        else:
            self.nodes.append(node1)
            self.nodes.append(node2)
            return 'Feasible',None,None
    
    def solve(self):
        status,value,solution=self.initnode()
        if status=='Unbounded':
            self.solution='Unbounded Solution'
            self.status=status
            self.value=float('-inf') if self.goalchange else float('inf')
            
        elif status=='Infeasible':
            self.solution='No feasible solution'
            self.status = status
            self.value='No feasible value'
            
        elif status=='Optimal':
            self.solution=solution
            self.status=status
            self.value=-value if self.goalchange else value
        else:           
            while self.nodes: 
                self.nodes.sort(reverse=True)               
                now=self.nodes[0][0]
                if now<self.lowerbound:
                    now=self.lowerbound
                self.upperbound=now
                self.finalgap=(self.upperbound-self.lowerbound)/self.lowerbound
                if not (math.isnan(self.finalgap) or self.finalgap>self.gap):
                    break               
                node=self.nodes.pop(0)
                coefficient=copy.deepcopy(self.coefficient)
                relation=copy.deepcopy(self.relation)
                constant=copy.deepcopy(self.constant)
                
                for combi in node[1:]:
                    coeff=[(1 if i==combi[0] else 0) for i in range(len(self.cost))]
                    relat=combi[1]
                    const=combi[2]

                    coefficient=np.row_stack((coefficient,coeff))
                    relation.append(relat)
                    constant.append(const)   
                    
                ins=simplex.solver(self.goal,self.cost,coefficient,constant,relation)
                ins.solve()
                if ins.status=='Infeasible' or ins.status=='Unbounded':
                    continue
                if ins.value<self.lowerbound:
                    continue  
                isint=True
                node1=copy.deepcopy(node)
                node1[0]=ins.value
                node2=copy.deepcopy(node)
                node2[0]=ins.value
                
                for i in range(len(ins.solution)):
                    v=ins.solution[i]
                    if self.intmark[i] and round(v,0)!=v:
                        node1.append([i,0,math.floor(v)])
                        node2.append([i,2,math.floor(v)+1])
                        isint=False
                        break
                if isint:
                    if ins.value>self.lowerbound:
                        self.lowerbound=ins.value
                        self.value=ins.value
                        self.solution=ins.solution
                else:
                    self.nodes.append(node1)
                    self.nodes.append(node2)
            self.status='Optimal'  
            self.finalgap=(self.upperbound-self.lowerbound)/self.lowerbound
            if self.goalchange:
            	self.value*=(-1)
            if not self.nodes:
                self.upperbound=self.lowerbound
                self.finalgap=0   