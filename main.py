import itertools
import time
from dataclasses import dataclass
from typing import List, Tuple, Set, Dict
from collections import deque


class PizzaIngredientConverter(object):
    def __init__(self):
        self.__pizza_ingredients: Dict[str, int] = {}

    def pizza_ingredient_to_number(self, ingredient: str) -> int:
        if not self.__pizza_ingredients.__contains__(ingredient):
            self.__pizza_ingredients[ingredient] = len(self.__pizza_ingredients)
        return self.__pizza_ingredients[ingredient]


@dataclass
class ProblemDefinition:
    # For each pizza configuration (ingredients in each pizza), store the ids of the pizza (its len is the number
    # of repetitions)
    pizzas_configuration: List[Tuple[frozenset[int], frozenset[int]]]

    # For each team configuration (members in each team), store the number of repetitions
    teams_configuration: Dict[int, int]


@dataclass
class ProblemOutput:
    # For each team with delivered pizza, store the number of members of the team and the pizzas delivered
    delivered_pizzas: List[Tuple[int, Set[int]]]


def load_input(input_path: str) -> ProblemDefinition:
    """
    Load the input
    :param input_path: path to the input
    :return: input loaded
    """

    local_pizza_configuration: Dict[frozenset[int], Set[int]] = {}

    local_teams_configuration: Dict[int, int] = {}

    pizza_ingredient_converter = PizzaIngredientConverter()

    with open(input_path) as file:
        for line_index, line in enumerate(file):
            actual_line = line.split()
            if line_index == 0:
                local_teams_configuration = {
                    2: int(actual_line[1]),
                    3: int(actual_line[2]),
                    4: int(actual_line[3])
                }
            else:
                actual_pizza_set = frozenset(
                    pizza_ingredient_converter.pizza_ingredient_to_number(i) for i in actual_line[1:])
                if not local_pizza_configuration.__contains__(actual_pizza_set):
                    local_pizza_configuration[actual_pizza_set] = set()

                # Add actual pizza
                local_pizza_configuration[actual_pizza_set].add(line_index - 1)

    return ProblemDefinition([(i, frozenset(j)) for i, j in local_pizza_configuration.items()],
                             local_teams_configuration)


def save_output(output_path: str, solution: ProblemOutput):
    """
    Save the output
    :param output_path: path to the output
    :param solution: solution
    """
    separator_same_line = " "
    separator_new_line = "\n"
    output_string = separator_new_line.join(
        separator_same_line.join(str(k) for k in [i] + list(j)) for i, j in solution.delivered_pizzas)

    output_string_complete = f"{len(solution.delivered_pizzas)}\n" + output_string

    with open(output_path, "w") as file:
        file.write(output_string_complete)


def check_output_validity(problem_definition: ProblemDefinition, solution: ProblemOutput) -> bool:
    """
    Return true if the solution is valid
    :param problem_definition: Problem input
    :param solution: solution
    :return: true if the solution is valid
    """
    pizza_set: Set[int] = set().union(*[j for i, j in problem_definition.pizzas_configuration])
    selected_pizzas = list(itertools.chain(*[list(j) for i, j in solution.delivered_pizzas]))
    selected_pizzas_set = set(selected_pizzas)

    return len(selected_pizzas_set) == len(selected_pizzas) \
           and len(selected_pizzas_set.difference(pizza_set)) == 0 \
           and all(i == len(j) for i, j in solution.delivered_pizzas)


def check_output_score(problem_definition: ProblemDefinition, solution: ProblemOutput) -> int:
    """
    Return the score of the solution
    :param problem_definition: Problem input
    :param solution: solution
    :return: true if the solution is valid
    """
    indexed_pizzas: Dict[int, frozenset[int]] = {}
    for i, j in problem_definition.pizzas_configuration:
        indexed_pizzas.update({k: i for k in j})

    return sum(len(set().union(*[indexed_pizzas[k] for k in j])) ** 2 for _, j in solution.delivered_pizzas)


def algorithm_many_ingredients(problem_definition: ProblemDefinition) -> ProblemOutput:
    """
    Return an output for testing purposes
    :param problem_definition:
    :return:
    """
    pizzas_configurations = {[r for r in j][0]: i for i, j in problem_definition.pizzas_configuration}

    delivered_pizzas: deque[Tuple[int, Set[int]]] = deque()

    union_multiplier = 2
    intersection_multiplier = 1

    # Obtain for four people
    for i in range(problem_definition.teams_configuration[4]):
        print(f"Team {i}/{problem_definition.teams_configuration[4]}")
        # Obtain pizza with max ingredients
        pizza_max_ingredients_id, pizza_max_ingredients_ingredients = max(pizzas_configurations.items(),
                                                                          key=lambda x: len(x[1]))
        pizzas_configurations.pop(pizza_max_ingredients_id)

        # Obtain the pizza with min intersection member 2
        pizza_min_ingredients_id_1, pizza_min_ingredients_ingredients_1 = max(pizzas_configurations.items(),
                                                                              key=lambda x: union_multiplier * len(frozenset.union(
                                                                                  pizza_max_ingredients_ingredients,
                                                                                  x[1])) - intersection_multiplier * len(frozenset.intersection(
                                                                                  pizza_max_ingredients_ingredients,
                                                                                  x[1])))
        pizzas_configurations.pop(pizza_min_ingredients_id_1)

        # Obtain the pizza with min intersection member 3
        pizza_min_ingredients_id_2, pizza_min_ingredients_ingredients_2 = max(pizzas_configurations.items(),
                                                                              key=lambda x: union_multiplier * len(frozenset.union(
                                                                                  pizza_max_ingredients_ingredients,
                                                                                  pizza_min_ingredients_ingredients_1,
                                                                                  x[1]))+ intersection_multiplier* len(frozenset.intersection(
                                                                                  pizza_max_ingredients_ingredients,
                                                                                  pizza_min_ingredients_ingredients_1,
                                                                                  x[1])))
        pizzas_configurations.pop(pizza_min_ingredients_id_2)

        # Obtain the pizza with min intersection member 4
        pizza_min_ingredients_id_3, _ = max(pizzas_configurations.items(),
                                            key=lambda x: union_multiplier *  len(frozenset.union(
                                                pizza_max_ingredients_ingredients,
                                                pizza_min_ingredients_ingredients_1,
                                                pizza_min_ingredients_ingredients_2,
                                                x[1])) - intersection_multiplier* len(frozenset.intersection(
                                                pizza_max_ingredients_ingredients,
                                                pizza_min_ingredients_ingredients_1,
                                                pizza_min_ingredients_ingredients_2,
                                                x[1])))
        pizzas_configurations.pop(pizza_min_ingredients_id_3)

        delivered_pizzas.append(
            (4, {pizza_max_ingredients_id, pizza_min_ingredients_id_1, pizza_min_ingredients_id_2,
                 pizza_min_ingredients_id_3}))

    # Obtain for three people
    for i in range(problem_definition.teams_configuration[3]):
        print(f"Team {i}/{problem_definition.teams_configuration[3]}")
        # Obtain pizza with max ingredients
        pizza_max_ingredients_id, pizza_max_ingredients_ingredients = max(pizzas_configurations.items(),
                                                                          key=lambda x: len(x[1]))
        pizzas_configurations.pop(pizza_max_ingredients_id)

        # Obtain the pizza with min intersection member 2
        pizza_min_ingredients_id_1, pizza_min_ingredients_ingredients_1 = max(pizzas_configurations.items(),
                                                                              key=lambda x: union_multiplier * len(frozenset.union(
                                                                                  pizza_max_ingredients_ingredients,
                                                                                  x[1]))- intersection_multiplier* len(frozenset.intersection(
                                                                                  pizza_max_ingredients_ingredients,
                                                                                  x[1])))
        pizzas_configurations.pop(pizza_min_ingredients_id_1)

        # Obtain the pizza with min intersection member 3
        pizza_min_ingredients_id_2, _ = max(pizzas_configurations.items(),
                                            key=lambda x: union_multiplier * len(frozenset.union(
                                                pizza_max_ingredients_ingredients,
                                                pizza_min_ingredients_ingredients_1,
                                                x[1])) - intersection_multiplier * len(frozenset.intersection(
                                                pizza_max_ingredients_ingredients,
                                                pizza_min_ingredients_ingredients_1,
                                                x[1])))
        pizzas_configurations.pop(pizza_min_ingredients_id_2)

        delivered_pizzas.append(
            (3, {pizza_max_ingredients_id, pizza_min_ingredients_id_1, pizza_min_ingredients_id_2}))

    # Obtain for two people
    for i in range(problem_definition.teams_configuration[2]):
        print(f"Team {i}/{problem_definition.teams_configuration[2]}")
        # Obtain pizza with max ingredients
        pizza_max_ingredients_id, pizza_max_ingredients_ingredients = max(pizzas_configurations.items(),
                                                                          key=lambda x: len(x[1]))
        pizzas_configurations.pop(pizza_max_ingredients_id)

        # Obtain the pizza with min intersection
        pizza_min_ingredients_id, _ = max(pizzas_configurations.items(),
                                          key=lambda x: union_multiplier * len(
                                              frozenset.union(pizza_max_ingredients_ingredients, x[1])) - intersection_multiplier * len(
                                              frozenset.intersection(pizza_max_ingredients_ingredients, x[1])))
        pizzas_configurations.pop(pizza_min_ingredients_id)

        delivered_pizzas.append((2, {pizza_max_ingredients_id, pizza_min_ingredients_id}))

    return ProblemOutput(list(delivered_pizzas))


def simple_algorithm(problem_definition: ProblemDefinition) -> ProblemOutput:
    """
    Return an output for testing purposes
    :param problem_definition:
    :return:
    """
    pizza_set: Set[int] = set().union(*[j for i, j in problem_definition.pizzas_configuration])

    delivered_pizzas: deque[Tuple[int, Set[int]]] = deque()

    for members_in_team, number_of_teams in problem_definition.teams_configuration.items():
        teams_to_assign = len(pizza_set) // members_in_team

        for _ in range(min(teams_to_assign, number_of_teams)):
            pizzas_in_team = [pizza_set.pop() for _ in range(members_in_team)]
            delivered_pizzas.append((members_in_team, set(pizzas_in_team)))

    return ProblemOutput(list(delivered_pizzas))


if __name__ == '__main__':
    # 9:49 -> Inicio
    # 10:25 -> Estructura inicial
    # 10:52 -> Input
    # 11:14 -> Simple solution
    # 11:25 -> Output
    # 11:43 -> Score
    # 11:46 -> First submission done: Break

    possible_inputs = {
        "a": "in/a_example.in",
        "b": "in/b_little_bit_of_everything.in",
        "c": "in/c_many_ingredients.in",
        "d": "in/d_many_pizzas.in",
        "e": "in/e_many_teams.in"
    }

    possible_outputs = {
        "a": "out/a_example.out",
        "b": "out/b_little_bit_of_everything.out",
        "c": "out/c_many_ingredients.out",
        "d": "out/d_many_pizzas.out",
        "e": "out/e_many_teams.out"
    }

    __main_input = "c"
    print("Loading input")
    __main_problem_definition = load_input(possible_inputs[__main_input])
    print("Running algorithm")
    __start_time = time.time()
    __main_problem_output = algorithm_many_ingredients(__main_problem_definition)
    __end_time = time.time()
    print(f"\t Running time: {__end_time - __start_time}")

    print("Checking validity")
    if check_output_validity(__main_problem_definition, __main_problem_output):
        print("Checking score")
        __main_score = check_output_score(__main_problem_definition, __main_problem_output)
        print(f"\t Score is: {__main_score}")
        print("Saving output")
        save_output(possible_outputs[__main_input], __main_problem_output)

    else:
        print("\t Solution is invalid")
