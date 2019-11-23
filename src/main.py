from src.classes.selector import Selector
from src.classes.comparison_functions import comparison_using_importance


def main():
    # create a selector class
    comparison_parameters = [1, 1, 1]
    learning_rate = 0.05
    weight = 0.1
    model = Selector(comparison_using_importance, comparison_parameters, learning_rate, weight)


if __name__ == '__main__':
    main()
