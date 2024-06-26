"""Decorators for testing"""
from .utils import capture_io

def add_points(points: float):

    def decorator(test_function: callable):
        setattr(test_function, 'points_increment', points)
        return test_function

    return decorator


def run_solution(inputs: list):

    def decorator(test_function: callable):

        def wrapper(class_self):
            from .globals import testing_script_path
            outputs = capture_io(testing_script_path, inputs)
            return test_function(class_self, outputs)

        return wrapper

    return decorator
