# Solution for practice problem Hash Code 2021

The statement of the problem is in the [problem](./problem) folder, and the input in the [in](./in) folder.

## Algorithm

### Many ingredients algorithm 
The algorithm for the many ingredients' dataset is located in the __
algorithm_little_bit_of_everything_union_intersection__ function.

This proposal assumes that the better solution is found when the priority in the pizza delivery is given based on the
number of team members.

To select the pizzas to deliver for each team, first is selected the pizza for the first member, that will be the
remaining pizza with more ingredients. For each of the remaining members of the team, is selected the pizza that
maximize the following formula:

- 3 * number of total ingredients in the team - 1 * repeated ingredients in all the pizzas of the team

### Example algorithm
The implementation is equal to the implementation of __Many ingredients algorithm__.

### Little bit of everything algorithm
The implementation is equal to the implementation of __Many ingredients algorithm__.

### Many pizzas algorithm
The implementation is equal to the implementation of __Many ingredients algorithm__.

### Many teams algorithm
The implementation is equal to the implementation of __Many ingredients algorithm__.

## Results

Score obtained:

| Dataset name | Score upper bound | Obtained score     | Execution time (s) | Algorithm name |
|--------------|-----------|-----------|--------------------|--------------------|
| a - example          | 148         | 61         |1                  | algorithm_little_bit_of_everything_union_intersection |
| b - little bit of everything           | 26270         |10279         | 1                  | algorithm_little_bit_of_everything_union_intersection |
| c - many ingredients           |754480357         | 706424419 | 806                | algorithm_many_ingredients |
| d - many pizzas           | 8307077         |7827075         | 2455                  | algorithm_many_pizzas_union_intersection |
| e - many teams           | 11233632         |10752356         | 4929                  | algorithm_many_teams_union_intersection |

The __Score upper bound__ is the theoretical maximum score that can be obtained. However, this is only a limit, there may not be a feasible solution with this score. 