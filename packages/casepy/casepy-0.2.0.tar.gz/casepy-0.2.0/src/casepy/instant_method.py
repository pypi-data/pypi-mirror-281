from .permutation_generator import *
from .combination_generator import *


# def total_n_permutation(in_list: list, in_number_of_select: int) -> int:
#     """
#     Return the total number of permutations of the list.

#     .. _total_n_permutation:

#     Args:
#         in_list (list): The list to be permuted.
#         in_number_of_select (int): The number of elements to be selected.

#     Returns:
#         int: The total number of permutations of the list.

#     Examples:
#         >>> result = total_permutation([1, 2, 3, 3], 2)
#         >>> print(result)
#         7
#     """
#     instance = PermutationGenerator()
#     instance.set_parameters(in_list, in_number_of_select)
#     return instance.possible_cases()


def all_permutations(in_list: list, in_number_of_select: int) -> list:
    """
    Return all permutations of the list.

    .. _all_permutations:

    Args:
        in_list (list): The list to be permuted.
        in_number_of_select (int): The number of elements to be selected.

    Returns:
        list: All permutations of the list.

    Examples:
        >>> result = all_permutation([1, 2, 3, 3], 2)
        >>> print(result)
        [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2], [3, 3]]
    """
    instance = PermutationGenerator()
    instance.set_parameters(in_list, in_number_of_select)

    return instance.all_cases()


def n_th_permutation(in_iterator: int, in_list: list, in_number_of_select: int) -> list:
    """
    Return the n-th permutation of the list.

    .. _n_th_permutation:

    Args:
        in_iterator (int): Iterator n indicates the n-th permutation.
        in_list (list): The list to be permuted.
        in_number_of_select (int): The number of elements to be selected.

    Returns:
        list: The n-th permutation of the list.

    Examples:
        >>> result = n_th_permutation(3, [1, 2, 3, 3], 2)
        >>> print(result)
        [2, 3]

    """
    instance = PermutationGenerator()
    instance.set_parameters(in_list, in_number_of_select)

    return instance.n_th_case(in_iterator)


def n_to_m_th_permutations(
    in_n_iterator: int, in_m_iterator: int, in_list: list, in_number_of_select: int
) -> list:
    """
    Return list of permutations from n-th to m-th.

    .. _n_to_m_th_permutations:

    Args:
        in_n_iterator (int): Iterator n indicates the n-th permutation.
        in_m_iterator (int): Iterator m indicates the m-th permutation.
        in_list (list): The list to be permuted.
        in_number_of_select (int): The number of elements to be selected.

    Returns:
        list: List of permutation from n-th to m-th.

    Examples:
        >>> result = n_to_m_th_permutation(2, 4, [1, 2, 3, 3], 2)
        >>> print(result)
        [[2,1],[2,3],[3,1]]
    """
    instance = PermutationGenerator()
    instance.set_parameters(in_list, in_number_of_select)

    return instance.n_to_m_th_cases(in_n_iterator, in_m_iterator)


# def total_n_combination(in_list: list, in_number_of_select: int) -> int:
#     """
#     Return the total number of combinations of the list.

#     .. _total_n_combination:

#     Args:
#         in_list (list): The list to be combined.
#         in_number_of_select (int): The number of elements to be selected.

#     Returns:
#         int: The total number of combinations of the list.

#     Examples:
#         >>> result = total_combination([1, 2, 3, 3], 2)
#         >>> print(result)
#         6
#     """
#     instance = CombinationGenerator()
#     instance.set_parameters(in_number_of_select, in_list)
#     return instance.possible_cases()


def all_combinations(in_list: list, in_number_of_select: int) -> list:
    """
    Return all combinations of the list.

    .. _all_combinations:

    Args:
        in_list (list): The list to be combined.
        in_number_of_select (int): The number of elements to be selected.

    Returns:
        list: All combinations of the list.

    Examples:
        >>> result = all_combination([1, 2, 3, 3], 2)
        >>> print(result)
        [[1, 2], [1, 3], [2, 3]]
    """
    instance = CombinationGenerator()
    instance.set_parameters(in_number_of_select, in_list)

    return instance.all_cases()


def n_th_combination(in_iterator: int, in_list: list, in_number_of_select: int) -> list:
    """
    Return the n-th combination of the list.

    .. _n_th_combination:

    Args:
        in_iterator (int): Iterator n indicates the n-th combination.
        in_list (list): The list to be combined.
        in_number_of_select (int): The number of elements to be selected.

    Returns:
        list: The n-th combination of the list.

    Examples:
        >>> result = n_th_combination(2, [1, 2, 3, 3], 2)
        >>> print(result)
        [2, 3]
    """
    instance = CombinationGenerator()
    instance.set_parameters(in_number_of_select, in_list)

    return instance.n_th_case(in_iterator)


def n_to_m_th_combinations(
    in_n_iterator: int, in_m_iterator: int, in_list: list, in_number_of_select: int
) -> list:
    """
    Return list of combinations from n-th to m-th.

    .. _n_to_m_th_combinations:

    Args:
        in_n_iterator (int): Iterator n indicates the n-th combination.
        in_m_iterator (int): Iterator m indicates the m-th combination.
        in_list (list): The list to be combined.
        in_number_of_select (int): The number of elements to be selected.

    Returns:
        list: List of combination from n-th to m-th.

    Examples:
        >>> result = n_to_m_th_combinations(2, 4, [1, 2, 3, 3], 2)
        >>> print(result)
        [[2, 3], [3, 1], [3, 2]]
    """
    instance = CombinationGenerator()
    instance.set_parameters(in_number_of_select, in_list)

    return instance.n_to_m_th_cases(in_n_iterator, in_m_iterator)
