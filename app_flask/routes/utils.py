'''
    Utils for all routes
'''
from typing import Tuple, Union, Optional, Any


def validate_and_convert_args(
        arg_name: str,
        arg_value: str,
        expected_type: type,
        conversion_func: Optional[callable] = None,
        *args,
        **kwargs) -> Tuple[bool, Union[str, Any]]:
    """
    Validates and converts the given argument value to the specified type.

    :param arg_value: The value of the argument to validate and convert.
    :type arg_value: str
    :param expected_type: The expected type of the argument value.
    :type expected_type: type
    :param conversion_func: A conversion function applied to the argument. Defaults to None.
    :type conversion_func: Optional[Callable]
    :param *args: Additional positional arguments to pass to the conversion function.
    :param **kwargs: Additional keyword arguments to pass to the conversion function.
    :return: tuple of a bool if passed, 
             and either the converted value (if successful) or an error message (if unsuccessful).
    :rtype: Tuple[bool, Union[str, Any]]

    :raises ValueError: If the argument value cannot be converted to the expected type.
    :raises Exception: If an unknown exception occurs during the validation and conversion process.
    """
    try:
        if conversion_func:
            converted_value = conversion_func(*args, **kwargs)
        else:
            converted_value = expected_type(arg_value)
        return True, converted_value
    except ValueError as e:
        return False, f"Invalid value for {arg_name}, passed value: {arg_value}. Expected type: {expected_type.__name__}. Error: {e}"
    except Exception as e:
        return False, f"Error converting {arg_name}, Error: {e}"
