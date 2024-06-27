def factorial(in_target_number: int) -> int:
    result = 1
    for i in range(1, in_target_number + 1):
        result *= i
    return result


def combination_total(in_number_of_elements: int, in_number_of_select: int) -> int:
    if in_number_of_elements == in_number_of_select:
        return 1
    if in_number_of_elements < in_number_of_select:
        return 0

    return (int)(
        factorial(in_number_of_elements)
        / (
            factorial(in_number_of_elements - in_number_of_select)
            * factorial(in_number_of_select)
        )
    )


def all_combinations_unique_elements(
    in_number_of_selection: int, in_elements: list
) -> list:
    """
    Return all combinations of the given number of selections from a list that has unique elements only.

    Args:
        in_number_of_selection (int): The number of selections.
        in_elements (list): The list of elements.

    Returns:
        list: All combinations of the given number.
    """
    result = []

    # Check if the number of selection is valid.
    if len(in_elements) < in_number_of_selection or in_number_of_selection < 1:
        return []
    if len(in_elements) == in_number_of_selection:
        return [in_elements]

    # If the number of selection is 1, return the list of elements.
    if in_number_of_selection == 1:
        for i in in_elements:
            result.append([i])
        return result

    # If the number of selection is larger than 1, do the following.
    # Cut the first element
    first, rest = in_elements[0], in_elements[1:]

    result = list(
        map(
            lambda x: [first] + x,
            all_combinations_unique_elements(in_number_of_selection - 1, rest),
        )
    ) + all_combinations_unique_elements(in_number_of_selection, rest)
    return result


def permutation_total(in_number_of_elements: int, in_number_of_select: int) -> int:
    """
    Return the number of all possible permutation cases (tranditional method).

    Args:
        in_number_of_elements (int): The number of elements.
        in_number_of_select (int): The number of selections.

    Returns:
        int: The number of all possible permutation cases.
    """
    if in_number_of_elements == in_number_of_select:
        return factorial(in_number_of_elements)
    if in_number_of_elements < in_number_of_select:
        return 0

    return (int)(
        factorial(in_number_of_elements)
        / factorial(in_number_of_elements - in_number_of_select)
    )
