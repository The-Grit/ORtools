This is a solver that can solve multi-dimensional 0-1 knapsack problem.

You can create a knapsack problem solver by entering code:
	**ins=Knapsack([param1,param2,param3])**

param1 is the value of items;the data structure is a list like [1,2,3].

param2 is the capability of knapsack;the data structure is a list like [4,5],4 can mean the max weight knapsack can hold and 5 can mean the max volume knapsack can hold.If your knapsack problem has multi-dimensional capabilities more than weight and volume,this solver can success as well.

param3 is the weight,volume or other attributes of items;the data structure is a 2-dimensional list like [[1,1],[2,2],[3,3]],means the first item has an occupancy list [1,1] and the second item has a occupancy list [2,2].

You can solve this problem by function:
	**ins.solve()**

You can query outcome by field:
	**ins.maxIncome** means the optimal value.
	**ins.collection** means the optimal choice of items,the data structure is set,the element of this set is the index of items.

An example:

![image](https://github.com/aitexia/ORtools/blob/master/image/knapsack.PNG)

which means:

1.There are three items,the value of items is [7,8,9]

2.The knapsack has 3-D capabilities(weight,volume and another attribute),the list is [4,5,6]

3.The first item has an occupancy list [1,2,3].The second and the third item are as the same as the first. 

4.The optimal value is 16(=7+9).The optimal choice is choosing the items indexed 0 and 2,which mean the first and the third items.
