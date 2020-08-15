这是一个混合整数规划求解器，使用了分支定界法

支持：最大化或最小化；不等号、等号约束

***需要注意导入的库***：需要下载simplex.py，该文件的路径为ORtools/simplex.py

使用语法为（举例说明）：

goal=1 # goal为1表示为最大化，为表示为最小化
 
n=10 # n表示变量数

cost=[36,40,50,22,20,30,25,48,58,61] # cost表示每个变量在目标函数中的系数

coefficient=[[100,120,150,80,70,90,80,140,160,180],

[1,1,1,0,0,0,0,0,0,0],

[0,0,0,1,1,0,0,0,0,0],

[0,0,0,0,0,1,1,0,0,0],

[0,0,0,0,0,0,0,1,1,1]] # coefficient表示每行约束中，每个变量的系数。不需要手动将约束化为等式，但如果变量在某行的系数为0，则需要将0加入约束矩阵中
            
constant=[720,2,1,1,2] # constant表示右端常数项
 
relation=[0,0,2,2,2] # relation表示每行的约束关系，0表示小于等于，1表示等于，2表示大于等于

intmark=[1,1,1,1,1,1,1,1,1,1] # intmark标记哪些变量属于整数变量。intmark[i]=1表示变量i限定为整数变量，反之则不然

binmark=[1,1,1,1,1,1,1,1,1,1] # binmark标记哪些变量属于0-1变量。binmark[i]=1表示变量i限定为0-1变量，反之则不然

gap=0.01 # gap表示当分支定界法求出上界与下界的百分比差距小于gap时，算法结束，返回最优值和最优解

ins=mip.solver(goal,n,cost,coefficient,constant,relation,intmark,binmark,gap)  # 生成mip求解器实例
ins.solve() # solve（）函数开始求解
ins.status # 解的状态：最优解、无界解、无可行解
ins.value # 最优解的值
ins.solution # 最优解
ins.lowerbound # 下界
ins.upperbound # 上界
