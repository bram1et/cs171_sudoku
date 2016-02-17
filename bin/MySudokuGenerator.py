import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from src.file_reader import FileReader
from src.sudoku_generator import SudokuBoardGenerator

from src.file_writer import FileWriter

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Must specify input file and output file only')
        quit()

    else:
        input_file_str = sys.argv[1]
        output_file_str = sys.argv[2]

    try:
        input_file = open(input_file_str, 'r')
        output_file = open(output_file_str, 'w')
    except:
        print('Error opening file')
        quit()

    fileReader = FileReader(input_file)
    fileWriter = FileWriter(output_file)
    M, N, P, Q = fileReader.get_params_generator()

    sudoku_board =  SudokuBoardGenerator(M, N, P, Q)
    sudoku_board.generate_board()
    board_as_lists = sudoku_board.convert_board_to_list()
    fileWriter.write_generated_board_to_file(N, P, Q, board_as_lists)