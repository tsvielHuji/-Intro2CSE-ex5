#################################################################
# FILE : wordsearch.py
# WRITER : TSVIEL ZAIKMAN , Tsviel , 208241133
# EXERCISE : intro2cs ex5 2020
# DESCRIPTION: The Program search for words in matrix and returns the
# instances for different given direction
# NOTES:
#################################################################

import sys
import re
import os

# Error Messages
NOT_A_STRING = "Your input is not valid. Recheck it please"
INVALID_DIRECTION_MESSAGE = "You had entered an Invalid Direction"
DIRECTION_MORE_THAN_ONCE = "The same direction had been entered more than once"
OPEN_WORD_FILE_FAIL = "Couldn't open the word file. Please make sure it " \
                      "exists and that you had entered its exact name and " \
                      "extension"
OPEN_MATRIX_FILE_FAIL = "Couldn't open the Matrix file. Please make sure it " \
                        "exists and that you had entered its exact name and " \
                        "extension"
LACK_OF_PARAMETERS = "An invalid amount of Parametrs, make sure you had " \
                     "entered exactly 4 parameters "

# Useful Constants
VALID_DIRECTIONS = ["u", "d", "r", "l", "w", "x", "y", "z"]
INITIATE_COUNTER = 0
EMPTY_RESULTS = [[]]
EMPTY_FILE_CONTENT = ""
# Direction Constants
LEFT_TO_RIGHT = "r"
RIGHT_TO_LEFT = "l"
TOP_TO_BOTTOM = "d"
BOTTOM_TO_TOP = "u"
BOTTOM_TO_TOP_RIGHT = "w"
BOTTOM_TO_TOP_LEFT = "x"
TOP_TO_BOTTOM_RIGHT = "y"
TOP_TO_BOTTOM_LEFT = "z"


def read_wordlist(filename):
    """
    The function opens the file containing the list of words we are looking
    for inside the Matrix, and appends them to a list of strings
    :param filename: A string which contains the name of a file
    containing list of words we are looking for in the Matrix
    :return: A list of the words which were read from the file by the function
    """
    output = []
    with open(filename) as file:
        word_list = file.read().splitlines()
    for word in word_list:
        output.append(word)
    return output


def read_matrix(filename):
    """
    The function reads the file containing the letters for the matrix
    :param filename: A string which contains the name of the file
    containing a list of letters presented in the Matrix
    :return: A two dimentional list of the letters of the matrix, which is
    in fact a list consisting of multiple sub-lists.
    Each sublist represents a ROW the matrix
    the matrix
    """
    with open(filename) as file:
        letter_list = file.read().splitlines()
        matrix = []
        for row in letter_list:
            # Append each of the rows list into the Matrix List
            sliced_list = list(row)
            matrix.append(sliced_list[0::2])
    return matrix


def diagonal(matrix):
    """
    prints given matrix in diagonal order
    :param matrix: a 2 dimensional list of letters
    :return: diagonal matrix represented in 2 dimensional list
    """
    # There will be row+col-1 lines in the output
    row = len(matrix)
    col = len(matrix[0])
    main_list = []
    for line in range(1, (row + col)):
        # Get column index of the first element
        # in this line of output. The index is 0
        # for first row lines and line - row for
        # remaining lines
        start_col = max(0, line - row)
        # Get count of elements in this line.
        # The count of elements is equal to
        # minimum of line number, col-start_col and row
        count = min(line, (col - start_col), row)
        sub_lists = []
        # Print elements of this line
        for j in range(0, count):
            sub_lists.append(matrix[min(row, line) - j - 1][start_col + j])

        main_list.append("".join(sub_lists))

    return main_list


def transpose(mtx):
    """

    :param mtx:
    :return: transposed matrix using list comprehension
    """
    return [[row[i] for row in mtx] for i in range(len(mtx[0]))]


def mirror(matrix):
    """
    :param matrix: a matrix of letters (lists of lists of strings)
    :return: a mirror matrix (each row of the original matrix is reversed)
    """
    return [list(reversed(reversed_row)) for reversed_row in matrix]


def count_single_word_in_single_row(word, row):
    """
    The function counts how many times a word occured in a single row of the
    matrix. It appends the value to a list along with the word, convert it
    into tuple which is appended to a list(output) which we return
    :param word: the word we are looking for (a string)
    :param row: A list of the letters in the row we are checking
    :return: A list of tuples (output) containing the word we had checked,
    and its
    occurrences
    """
    matches = re.findall(rf'(?=({re.escape(word)}))', "".join(row))
    occurrences = len(matches)
    return occurrences


def count_single_word_in_matrix(word, matrix):
    """
    The function counts the occurrences of a given word
    :param word: a string representing a single word
    :param matrix: a matrix (list os lists of strings)
    :return: how many times the word occurs in the given matrix
    """
    occurrences = INITIATE_COUNTER  # Initiate occurrences counter

    for row in matrix:
        occurrences += count_single_word_in_single_row(word, row)
    return occurrences


def generate_matrices_to_search_list(matrix, directions):
    """
    :param matrix: a matrix (list os lists of strings)
    :param directions: a string consisting of the valid directions
    :return: transposed, mirrored and diagonal matrices based on matrix
    variable, thus running search for the word for all given directions
    """
    matrices_to_search = []
    if LEFT_TO_RIGHT in directions:
        matrices_to_search.append(matrix)
    if RIGHT_TO_LEFT in directions:
        matrices_to_search.append(mirror(matrix))
    if TOP_TO_BOTTOM in directions:
        matrices_to_search.append(transpose(matrix))
    if BOTTOM_TO_TOP in directions:
        matrices_to_search.append(mirror(transpose(matrix)))
    if BOTTOM_TO_TOP_RIGHT in directions:
        matrices_to_search.append(diagonal(matrix))
    if BOTTOM_TO_TOP_LEFT in directions:
        matrices_to_search.append(diagonal(mirror(matrix)))
    if TOP_TO_BOTTOM_RIGHT in directions:
        matrices_to_search.append(mirror(diagonal(matrix)))
    if TOP_TO_BOTTOM_LEFT in directions:
        matrices_to_search.append(mirror(diagonal(mirror(matrix))))
    return matrices_to_search


def find_words(word_list, matrix, directions):
    # Caching list
    search_results_list = []
    # Generate a list of matrices to check based on search directions
    matrices_to_search = generate_matrices_to_search_list(matrix, directions)

    for word in word_list:
        occurrences = INITIATE_COUNTER
        for matrix in matrices_to_search:
                occurrences += count_single_word_in_matrix(word, matrix)
        if occurrences > 0:
            search_results_list.append((word, occurrences))
    return search_results_list


def write_output(results, output_filename):
    """
    This function generates txt file (or overwrite an existing one) named as
    the string provided in the output_filename parameter.
    It writes the search result of the words in the Matrix in accordance to
    the format presented in the example files provided for this exercise.
    The function must keep the order of the words as it was provided in the
    list of outputs
    :param results: A list of tuples (word,count) as received in the return
    value of the find_words_in_file function.
    :param output_filename: The name which will be used from the generated
    txt file.
    """
    f = open(output_filename, "w+")
    if results == EMPTY_FILE_CONTENT:
        f.write("")
        f.close()
        return
    for i in results:
        f.write(str(i[0] + "," + str(i[1])))
        f.write('\n')
    f.close()
    return


def draw_matrix(matrix):
    """Function Draws a matrix"""
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in matrix]))
    print('\n')


def check_input_args(args):
    """
    The function checks each of the strings contained in the received list
    (args argument)
    :param args: A list of strings which are the parameters
    received from the Console
    :return: If it finds an error in one of the parameters,
    the function should return an appropriate message(without print)
    otherwise return None
    """
    try:
        open(args[1])
    except IOError:
        return OPEN_WORD_FILE_FAIL
    try:  # Try to open the Matrix file list to check if it exists
        open(args[2])
    except IOError:
        return OPEN_MATRIX_FILE_FAIL
    if len(args) != 5:  # Tests for the amount of the putted parameters
        return LACK_OF_PARAMETERS
    directions = list(args[4])  # A list of the directions
    for direction in directions:
        if direction not in VALID_DIRECTIONS:
            return INVALID_DIRECTION_MESSAGE
    pass


def no_result(results):
    """

    :param results:
    :return: True if no results, false if there is results
    """
    return sum([result[1] for result in results]) == 0


def is_empty_file(file):
    """True if empty, False if not"""
    if os.stat(file).st_size == 0:
        return True
    return False


def main():
    """
    This is the main function of the program which calls and combines all the
    functions of the program.
    This function of the program handles its integrity.
    :return:
    """
    args = sys.argv
    validate_parameters = check_input_args(args)
    if validate_parameters is not None:
        print(check_input_args(args))
    else:
        # Assign the sys.argv to local vars
        words_file, matrix_file = args[1], args[2]
        output_file, directions = args[3], args[4]
        # If one of the files are empty, exit from main
        if is_empty_file(words_file) or is_empty_file(matrix_file):
            write_output("", output_file)  # Create an empty file
            return
        # Build the word list from the words file
        word_list = read_wordlist(words_file)
        matrix = read_matrix(matrix_file)
        # Run the search and write to file
        results = find_words(word_list, matrix, directions)
        if no_result(results):
            write_output("", output_file)
            return
        else:
            write_output(results, output_file)


if __name__ == '__main__':
    main()
