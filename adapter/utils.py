from typing import List


def get_string_between_delimiters(text, start_delim, end_delim):
    if start_delim not in text or end_delim not in text:
        return None
    start = text.split(start_delim, 1)[1]
    return start.split(end_delim, 1)[0]


def remove_string_between_delimiters(string, delimiters):
    """
    Removes the substring and delimiters from the string.

    Args:
    string (str): The input string.
    delimiters (set of tuple): A set of tuples where each tuple contains a pair of delimiters.

    Returns:
    str: The string with the substring and delimiters removed.
    """
    for delim in delimiters:
        start_delim, end_delim = delim
        if start_delim in string and end_delim in string:
            start_index = string.index(start_delim)
            end_index = string.index(end_delim, start_index) + len(end_delim)
            return string[:start_index] + string[end_index:]
    return string


def extractStringInList_GivenListOfDelimiters(inputList, delimiters) -> List[str]:
    """
    Extracts substrings between given delimiters from a list of strings.

    Args:
    input_list (list of str): The list of input strings.
    delimiters (set of tuple): A set of tuples where each tuple contains a pair of delimiters.

    Returns:
    list of str: A list of substrings found between the delimiters.
    """
    results = []

    for string in inputList:
        for delimiter in delimiters:
            firstDelimiter, secondDelimiter = delimiter
            substring = get_string_between_delimiters(string, firstDelimiter, secondDelimiter)
            if substring is not None:
                results.append(substring)
                break
    return results


class Predicate:
    def __init__(self, predicate, *predicateArgs):
        self.predicate = predicate
        self.predicateArgs = predicateArgs

    def __call__(self, *args):
        return self.predicate(*self.predicateArgs, *args)


def merge(collectionFirst, collectionSecond, predicate: Predicate = None):
    """
    Merge the second collection into the first collection based on some provided predicate.
    Note that the order of the collection is important as elements from the second collection will be checked against the predicate then added to the first.
    :param collectionFirst:
    :param collectionSecond:
    :param predicate:
    :return:
    """
    if predicate is None:
        predicate = Predicate(lambda x: True)
    for item in collectionSecond:
        if predicate(item):
            collectionFirst.add(item)
    return collectionFirst
