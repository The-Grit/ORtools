This is a solver that can solve multi-dimensional 0-1 knapsack problem.

You can create a knapsack problem solver by entering code:
	<br>&emsp;&emsp;**```ins=Knapsack([param1,param2,param3])```**

param1 is the value of items.The data structure is a list like [1,2,3].

param2 is the capability of knapsack,which can be multi-dimensional.The data structure is a list like [4,5].4 can mean the max weight knapsack can hold and 5 can mean the max volume knapsack can hold.If your knapsack problem has multi-dimensional capabilities more than weight and volume,this solver can success as well.

param3 is the weight,volume or other attributes of items.The data structure is a list like [[1,1],[2,2],[3,3]],meaning the first item has an occupancy [1,1] and the second item has an occupancy [2,2].

You can solve this problem by function:
	<br>&emsp;&emsp;**```ins.solve()```**

You can query outcome by field:
	<br>&emsp;&emsp;**```ins.maxIncome```** means the optimal value.
	<br>&emsp;&emsp;**```ins.collection```** means the optimal choice of items,the data structure is set,the element of this set is the index of items.
An example:


![image](https://github.com/aitexia/ORtools/blob/master/image/knapsack2.PNG)
![image](https://github.com/aitexia/ORtools/blob/master/image/knapsack1.PNG)

which means:

1.There are 20 items,the value of items is x.

2.The knapsack has 2-D capabilities(may be weight and volume),the list is [100,100].

3.The first item has an occupancy [10, 6].The second has an occupancy [3, 9] and so on.

4.The optimal value is 39.The optimal choice is choosing the items indexed {3,4,5,7,8,9,11,12,16,18,19}.

(The first item is indexed 0 and so on.)
