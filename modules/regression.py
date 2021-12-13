"""
DOCSTRING
"""
import math as m


class LinearRegressionModel:
    """
    Class representing a linear regression model.
    """

    coordinates: list[tuple[float, float]]
    angle: float
    angle_divisor: int
    gradient: float
    y_intercept: float

    def __init__(self, coordinates: list[tuple[float, float]], angle_divisor: int) -> None:
        self.coordinates = coordinates
        self.angle_divisor = angle_divisor
        self.angle = m.pi / angle_divisor
        self.gradient, self.y_intercept = self.estimate_fit(coordinates)

    def estimate_fit(self, coordinates: list[tuple[float, float]]) -> tuple[float, float]:
        """
        Returns the constant coefficient m and the constant c for a fitted linear function of the
        coordinates such that y = mx + c.
        """

        iterations = self.angle_divisor
        mean_coord = self.calculate_mean_coordinate(coordinates)
        r_squared_so_far = {}

        for angle_multiplier in range(iterations):
            positive_m = m.tan(angle_multiplier * self.angle)

            positive_c = self.calculate_y_intercept(positive_m, mean_coord)
            positive_r_squared = self.sum_residuals_squared(coordinates, positive_m, positive_c)

            negative_m = m.tan(angle_multiplier * self.angle * -1)

            negative_c = self.calculate_y_intercept(negative_m, mean_coord)
            negative_r_squared = self.sum_residuals_squared(coordinates, negative_m, negative_c)

            r_squared_so_far[positive_r_squared] = (positive_m, positive_c)
            r_squared_so_far[negative_r_squared] = (negative_m, negative_c)

        min_r_squared = min(r_squared_so_far.keys())

        return r_squared_so_far[min_r_squared]

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

        log_b, log_a = self.estimate_fit(self.log_coordinates)

        self.a = m.e ** log_a
        self.b = m.e ** log_b

    def calculate_log_coordinates(self, coordinates: list[tuple[float, float]]) \
            -> list[tuple[float, float]]:
        """
        Returns the coordinates for ln(y) vs x. Excludes any y-coordinates that are zero in order
        to avoid a logarithm domain error.
        """

        return [(coord[0], m.log(coord[1])) for coord in coordinates if coord[1] > 0]
