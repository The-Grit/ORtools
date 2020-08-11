#!/usr/bin/env python
# coding: utf-8



# 一个使用了两阶段单纯形法的类
# 适合求解的问题特征为：最大化或最小化问题；约束条件可等于/大等于/小等于（暂不支持大于或小于）；变量非负
# 程序的缺陷：不支持解决循环；不支持变量为负（需手动进行变量间的线性变换，使得变换后的变量非负），不支持列出多个最优解（即使是无穷多最优解，也只会列出一个最优解）




import numpy as np
import copy

def guidance():
    	syntax = 'The format is "instance=simplex.solver(goal,cost,coefficient,constant,relation)".\n'
    	goal = 'The parameter goal equals to 0 when minimization is required.If not, goal equals to 1.\n'
    	cost = 'The parameter cost is a list recording target factor.\n'
    	coefficient = 'The parameter coefficient is a multi-dimension list recording constraint coefficient.\n'
    	constant = 'The parameter constant is a list recording constraint item.\n'
    	relation = 'The parameter relation is a list consisting of 0,1 or 2 for less than,equal to and greater than respectively.\n'
    	solve = 'The solving of solver class is done by a method instance.solve()\n'
    	query = 'The query of solving result can be done by member variables instance.value,instance.solution and instance.status.'
    	print(syntax+goal+cost+coefficient+constant+relation+solve+query)
        
class solver():
    # 初始化线性系统的要素：目标函数极大或极小/目标函数系数/约束系数矩阵/右端常数项向量/约束关系向量
    def __init__(self,goal,costVector,coefficientMatrix,constantVector,relationVector,bigM=99999999): 
        self.bigM=bigM
        self.art = 0 # 记录是否需要设置人工变量
        self.variableQuantity = len(costVector)
        self.subjectQuantity = len(relationVector)
        self.relationVector = np.array(relationVector)
        self.coefficientMatrix = (np.array(coefficientMatrix)).astype('float').reshape((self.subjectQuantity,self.variableQuantity))
        self.variableType = np.array([0 for i in range(self.variableQuantity)]) # 决策变量的标号为0
        self.constantVector = (np.array(constantVector)).astype('float')
        self.costVector = (np.array(costVector)).astype('float')
        self.goal = goal
        self.goalChange = 0
        self.basicVarIndex = {i:-1 for i in range(self.variableQuantity)}# 记录各个变量是否为基变量,是则为对应的约束索引，否则为-1
        self.subVar = {i:-1 for i in range(self.subjectQuantity)} # 记录各行常数项对应的基变量
        self.status='Unknown status'
        self.value ='No value'
        self.solution = 'No solution'
        self.itera=0
        self.StandTran() # 转换为右端常数项非负、最大化的模型
        self.canonical() # 生成规范型   
        
    # 将初始的右端常数项转换为右端常数项非负的模型；将最小化问题统统转换为最大化问题
    def StandTran(self):
        for i in range(self.subjectQuantity):
            if self.constantVector[i]<0:             
                self.coefficientMatrix[i] = -1*self.coefficientMatrix[i]
                self.constantVector[i] = -1*self.constantVector[i]
                if self.relationVector[i] == 0:
                    self.relationVector[i] = 2
                    continue
                if self.relationVector[i] == 2:
                    self.relationVector[i] = 0
        if self.goal == 0:
            self.costVector = -1*self.costVector
            self.goalChange = 1
     
    # 返回一个线性规划的规范型，并标记松弛/剩余/人工变量;对应的标号分别为1,2,3 
    def canonical(self):       
        n=self.variableQuantity
        for i in range(self.subjectQuantity):
            if self.relationVector[i] == 0: # relation为0/1/2分别对应小等于/等式/大等于
                col=np.array([1 if j==i else 0 for j in range(self.subjectQuantity)])
                self.coefficientMatrix=np.column_stack((self.coefficientMatrix,col))
                self.variableType=np.append(self.variableType,1)
                self.costVector=np.append(self.costVector,0)
                self.relationVector[i]=1
                n+=1
                self.basicVarIndex[n-1]=i
                self.subVar[i]=n-1
                continue

            if self.relationVector[i] == 1:
                col=np.array([1 if j==i else 0 for j in range(self.subjectQuantity)])
                self.coefficientMatrix=np.column_stack((self.coefficientMatrix,col))
                self.variableType=np.append(self.variableType,3)
                self.costVector=np.append(self.costVector,-self.bigM)
                n+=1
                self.basicVarIndex[n-1]=i
                self.subVar[i]=n-1
                self.art=1
                continue
                
            if self.relationVector[i] == 2:
                col=np.array([-1 if j==i else 0 for j in range(self.subjectQuantity)])
                self.coefficientMatrix=np.column_stack((self.coefficientMatrix,col))
                self.variableType=np.append(self.variableType,2)
                self.costVector=np.append(self.costVector,0)                
                n+=1
                self.basicVarIndex[n-1]=-1
                
                    
                col=np.array([1 if j==i else 0 for j in range(self.subjectQuantity)])
                self.coefficientMatrix=np.column_stack((self.coefficientMatrix,col))
                self.variableType=np.append(self.variableType,3)
                self.costVector=np.append(self.costVector,-self.bigM)  
                self.relationVector[i]=1
                n+=1
                self.basicVarIndex[n-1]=i
                self.subVar[i]=n-1
                self.art=1
    
    # 返回清除人工变量的规范型
    def clearArtificial(self): 
        artindex=[]    
        n=len(self.costVector)
        m=n
        k=0
        for i in range(n):
            if self.variableType[i] ==3 and self.basicVarIndex[k]==-1:
                if i==n-1:
                    self.basicVarIndex.pop(k)
                for j in range(k+1,m):
                    self.basicVarIndex[j-1]=self.basicVarIndex.pop(j)
                for key in self.subVar:
                    if self.subVar[key]>k:
                        self.subVar[key]=self.subVar[key]-1
                m-=1
                artindex.append(i)
            else:
                k+=1
        self.costVector=np.delete(self.costVector,artindex)  
        self.variableType=np.delete(self.variableType,artindex)
        self.coefficientMatrix=np.delete(self.coefficientMatrix,artindex,axis=1)
    
    # 返回一个规范型中各变量的检验数
    def reducedCost(self,costVector): 
        reducedCostList=[]
        basicCost = []  
        for i in range(self.subjectQuantity):               
            basicCost.append(costVector[self.subVar[i]])
        for i in range(len(costVector)):
            Col=self.coefficientMatrix[:,i]
            reducedCost=costVector[i]-np.dot(basicCost,Col)
            reducedCostList.append(reducedCost)    
        return reducedCostList
    
    # 生成规范型的初始基可行解，使基变量中不包含人工变量
    def pahseI(self):
        if self.art:
            # 如果需要添加人工变量，那么需要先求解一个线性规划问题来决定是否有可行解
            tempcostVector=copy.deepcopy(self.costVector)
            for i in range(len(self.variableType)):
                if self.variableType[i] != 3:
                    tempcostVector[i]=0
                else:
                    tempcostVector[i]=-1
            outcome,status = self.phaseII(tempcostVector)
            if outcome<0: # 一阶段问题是最大化问题，如果最优值outcome不为0，那么说明问题无可行解
                outcome = "No feasible solution"
                return outcome,None,None
            else: # 如果最优值outcome为0，那么说明问题有可行解，清除规范型中的人工变量
                print("Feasible! Artificial variables can be eliminated!")
                self.clearArtificial()
                outcome,status=self.phaseII(self.costVector)
                solution=[0 for i in range(self.variableQuantity)]
                for i in range(self.variableQuantity):
                    if self.basicVarIndex[i]==-1:
                        continue
                    solution[i]=self.constantVector[self.basicVarIndex[i]]
                return outcome,status,solution
        else: # 如果不需要添加人工变量，那么不需要清除人工变量，直接返回规范型即可
            outcome,status=self.phaseII(self.costVector)
            solution=[0 for i in range(self.variableQuantity)]
            for i in range(self.variableQuantity):
                if self.basicVarIndex[i]==-1:
                    continue
                solution[i]=(self.constantVector[self.basicVarIndex[i]])
            return outcome,status,solution
    
    def phaseII(self,costVector): # 对于有初始基可行解的规范型，进行单纯形算法迭代，以最大化为目标
        optimality = 0 # 唯一最优解的id
        infiniteOpt = 1 # 无穷多最优解的id
        unBounded = 2 # 无界解的id
        
        countOpt = 0
        countInfOpt = 0
        countUnbounded = 0
        
        reducedCostList = self.reducedCost(costVector)
        for i in range(len(reducedCostList)):          
            checkNumber=reducedCostList[i]
            if checkNumber < 0:
                countOpt += 1
                continue
            if checkNumber == 0:
                countOpt += 1
                countInfOpt += 1
                continue
            if checkNumber > 0:
                if self.coefficientMatrix[:,i].all()<=0: # 检验一个检验数为负的系数列是否全非正 
                    unBounded = 1
                    continue       
        
        if countOpt == len(costVector):
            if (countInfOpt-self.subjectQuantity)>0:
                return self.outcome(costVector),infiniteOpt
            else:
                return self.outcome(costVector),optimality
        else:
            if countUnbounded:
                return self.outcome(costVector),unBounded
            else:
                self.iterate(reducedCostList)               
                return self.phaseII(costVector)
    
    def outcome(self,costVector): # 计算基可行解的目标函数值
        outcome = 0
        for i in self.subVar:
            outcome+=self.constantVector[i]*costVector[self.subVar[i]]
        return outcome
      
    # 对于一个规范型进行出基进基、更新系数矩阵和右端常数项
    def iterate(self,reducedCostList): 
        self.itera+=1
        
        inbasis = reducedCostList.index(max(reducedCostList))
        basisCol = self.coefficientMatrix[:,inbasis]
        
        ratio=float('inf')
        outbasis = -1   
        j=-1
        for i in range(self.subjectQuantity):
            if self.coefficientMatrix[i][inbasis]<=0:
                continue
            if self.constantVector[i]/self.coefficientMatrix[i][inbasis]<ratio:
                ratio=self.constantVector[i]/self.coefficientMatrix[i][inbasis]
                outbasis = self.subVar[i]
                j=i
                
        self.basicVarIndex[inbasis]=self.basicVarIndex[outbasis]      
        self.basicVarIndex[outbasis]=-1
        self.subVar[j]=inbasis
        
        # 进行方程组的同解变换
        matrix=copy.deepcopy(self.coefficientMatrix)
        constant=copy.deepcopy(self.constantVector)
        
        pivotVal = self.coefficientMatrix[j][inbasis]     
        for i in range(self.subjectQuantity):
            if i == j:
                matrix[i] = self.coefficientMatrix[i]/pivotVal
                constant[i] = self.constantVector[i]/pivotVal
            else:
                for k in range(len(self.costVector)):
                    matrix[i][k] = self.coefficientMatrix[i][k]-self.coefficientMatrix[i][inbasis]*self.coefficientMatrix[j][k]/pivotVal
                constant[i] = self.constantVector[i]-self.coefficientMatrix[i][inbasis]*self.constantVector[j]/pivotVal
        self.coefficientMatrix=matrix  
        self.constantVector=constant
    
    def solve(self):
        # 检验问题是否无可行解
        outcome,status,solution = self.pahseI()
        if outcome == "No feasible solution":
            self.value = 'No feasible value'
            self.solution = outcome
            self.status = 'Infeasible'
        else:
            solution = [round(i,2) for i in solution]
            formatoutcome=round(outcome,2)
            # 如果问题有可行解，则只会有唯一最优解、无穷多最优解以及无界解三种情况
            if status == 0:
                self.status='Only Optimal'
                self.solution=solution
                self.value=-formatoutcome if self.goalChange else formatoutcome
            if status == 1:
                self.status='Infinite Optimal'
                self.solution=solution
                self.value=-formatoutcome if self.goalChange else formatoutcome
            if status == 2:
                self.status='Unbounded'
                self.solution='Unbounded Solution'
                self.value=float('inf') if self.goal == 1 else float('-inf')
        print('Iterate %s times.'%self.itera)
        print('Status is %s'%self.status)
