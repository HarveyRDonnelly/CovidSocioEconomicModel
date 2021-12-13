"""
Module Title: Regression Module
Source Path: modules/regression.py

Description:

The Regression Module contains the classes representing the Linear and Exponential regression
models used within this project. An instance of a LinearRegressionModel will contain the gradient
and the y-intercept of the best-fitting linear function for an inputted set of coordinates. This is
determined using the residual-squared linear regression method.

An instance of an ExponentialRegressionModel will contain the constants a and b of the best fitting
exponential function in the form of y = a * b^x. This is calculated by taking the natural logarithm
of all y-coordinates and then applying a linear regression model to the ln(y) points against the
x-coordinates. The gradient of the linear function represents ln(b) and the y_intercept represents
ln(a).

Please note, the linear and exponential regression methods in this class were written from scratch
using only an abstract understanding of residual-squared regression. No external code was used.


===============================

CSC110 Final Project:

"Virus of Inequality: The Socio-Economic Disparity of COVID-19 Cases
in the City of Toronto"

This file is Copyright (c) 2021 Harvey Ronan Donnelly and Ewan Robert Jordan.

"""
import math


class LinearRegressionModel:
    """
    Class representing a linear regression model.

    Instance Attributes:
        - coordinates: a list of tuples representing the coordinates that will be used as training
        data for the regression model.
        - angle: the angle interval for each rotation of the linear function.
        - angle_divisor: the number of divisions of the angle between the x and y axis that the
        linear function will be rotated.
        - gradient: the gradient m of the best fitting linear function such that y = mx + c.
        - y_intercept: the y-intercept c of the best fitting linear function such that y = mx + c.
        - r_squared: the residual-squared value for the best fitting linear function.

    Representation Invariants:
        - self.angle_divisor >= 1
        - 0 < self.angle < math.pi / 2

    >>> example_coords = [(0.0,1.0), (1.0,2.0), (2.0,3.0), (3.0,4.0)]
    >>> model = LinearRegressionModel(example_coords, 100)
    >>> math.isclose(model.gradient, 1.0)
    True
    >>> math.isclose(model.y_intercept, 1.0)
    True

    """

    coordinates: list[tuple[float, float]]
    angle: float
    angle_divisor: int
    gradient: float
    y_intercept: float
    r_squared: float

    def __init__(self, coordinates: list[tuple[float, float]], angle_divisor: int) -> None:
        self.coordinates = coordinates
        self.angle_divisor = angle_divisor
        self.angle = math.pi / angle_divisor
        self.gradient, self.y_intercept, self.r_squared = self.estimate_fit(coordinates)

    def estimate_fit(self, coordinates: list[tuple[float, float]]) -> tuple[float, float, float]:
        """
        Returns the constant coefficient m, the constant c and the residual-squared value
        for a fitted linear function of the coordinates such that y = mx + c.
        """

        iterations = self.angle_divisor
        mean_coord = self.calculate_mean_coordinate(coordinates)
        r_squared_so_far = {}

        for angle_multiplier in range(iterations):
            positive_m = math.tan(angle_multiplier * self.angle)

            positive_c = self.calculate_y_intercept(positive_m, mean_coord)
            positive_r_squared = self.sum_residuals_squared(coordinates, positive_m, positive_c)

            negative_m = math.tan(angle_multiplier * self.angle * -1)

            negative_c = self.calculate_y_intercept(negative_m, mean_coord)
            negative_r_squared = self.sum_residuals_squared(coordinates, negative_m, negative_c)

            r_squared_so_far[positive_r_squared] = (positive_m, positive_c)
            r_squared_so_far[negative_r_squared] = (negative_m, negative_c)

        min_r_squared = min(r_squared_so_far.keys())

        coefficient_m, constant_c = r_squared_so_far[min_r_squared]

        return (coefficient_m, constant_c, min_r_squared)

    def sum_residuals_squared(self, coordinates: list[tuple[float, float]], coefficient_m: float,
                              constant_c: float) -> float:
        """
        Sum the squared residuals of coordinates compared to a linear function defined as
        y = coefficient_m * x + constant_c.
        """

        residuals_squared_so_far = 0
        for coord in coordinates:
            line = coefficient_m * coord[0] + constant_c
            residual_difference = abs(line - coord[1])
            residuals_squared_so_far += residual_difference ** 2

        return residuals_squared_so_far

    def calculate_mean_coordinate(self, coordinates: list[tuple[float, float]]) \
            -> tuple[float, float]:
        """
        Returns the mean coordinate for the training data.

        >>> example_coords = [(0.0,0.0), (1.0,1.0), (2.0,2.0)]
        >>> model = LinearRegressionModel(example_coords, 100)
        >>> model.calculate_mean_coordinate(example_coords)
        (1.0, 1.0)

        """
        x_values = [coord[0] for coord in coordinates]
        y_values = [coord[1] for coord in coordinates]

        mean_x = sum(x_values) / len(x_values)
        mean_y = sum(y_values) / len(y_values)

        return (mean_x, mean_y)

    def calculate_y_intercept(self, coefficient_m: float, coordinate: tuple[float, float]) -> float:
        """
        Returns the y-intercept of a linear function from the gradient coefficient_m and an
        intercepted coordinate.

        >>> example_coords = [(0.0,0.0), (1.0,1.0), (2.0,2.0)]
        >>> model = LinearRegressionModel(example_coords, 100)
        >>> model.calculate_y_intercept(1.0, (2.0, 3.0))
        1.0

        """
        return coordinate[1] - (coefficient_m * coordinate[0])


class ExponentialRegressionModel(LinearRegressionModel):
    """
    Class representing an exponential regression model.
    """

    a: float
    b: float
    log_coordinates: list[tuple[float, float]]

    def __init__(self, coordinates: list[tuple[float, float]], angle_divisor: int):
        super().__init__(coordinates, angle_divisor)

        self.log_coordinates = self.calculate_log_coordinates(coordinates)

        self.gradient, self.y_intercept, self.r_squared = self.estimate_fit(self.log_coordinates)

        self.a = math.e ** self.gradient
        self.b = math.e ** self.y_intercept

    def calculate_log_coordinates(self, coordinates: list[tuple[float, float]]) \
            -> list[tuple[float, float]]:
        """
        Returns the coordinates for ln(y) vs x. Excludes any y-coordinates that are zero in order
        to avoid a logarithm domain error.
        """

        return [(coord[0], math.log(coord[1])) for coord in coordinates if coord[1] > 0]


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': [math],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
