#!/usr/bin/python
import copy
import random
import sys

from file_reader import FileReader
from sudoku_pieces import Block
from sudoku_pieces import Cell
from sudoku_pieces import Column
from sudoku_pieces import Row

from src.file_writer import FileWriter


class SudokuBoardGenerator:
    def __init__(self, M, N, P, Q):
        self.m = M
        self.n = N
        self.p = P
        self.q = Q
        self.rows = []
        self.columns = []
        self.blocks = []
        self.domain = self.get_domain()
        self.check_board_params()

    def get_domain(self):
        domain = []
        for i in range(self.n):
            if i < 9:
                domain.append(i + 1)
            else:
                domain.append(chr((i - 9) + 65))
        return domain

    def check_board_params(self):
        if self.n > 35:
            print('Number of tokens cannot excede 35')
            quit()
        if self.p <= 0 or self.q <= 0 or self.n <= 0:
            print('All values must be greater than 0')
            quit()
        if self.p * self.q != self.n:
            print('N must equal P * Q')
            quit()
        if self.m > self.n**2:
            print('M must less than N^2')
            quit()
#        if len(board) != self.n:
#            raise ValueError('Number of rows in board must equal N')
        return True

    def get_block_num(self, row, col):
        return (int(row/self.p) + int(col/self.q)) + (row//self.p)

    def create_empty_board(self):
        self.rows = []
        self.columns = []
        self.blocks = []

        for count in range(self.n):
            self.rows.append(Row(self.n))
            self.columns.append(Column(self.n))
            self.blocks.append(Block(self.p, self.q))

        for row in range(self.n):
            for col in range(self.n):
                new_cell = Cell(copy.copy(self.domain), 0)
                self.rows[row].add_to_row(new_cell)
                self.columns[col].add_to_column(new_cell)
                block_num = self.get_block_num(row, col)
                self.blocks[block_num].add_to_block(new_cell)


    def generate_board(self):
        self.create_empty_board()
        count = 0
        while(count < self.m):
#            print(count)
#            self.print_board()
#            print()
            for i in range(self.n**2):
                row = i // self.n
                col = i % self.n
                percent_Filled = self.m / float(self.n ** 2)
                if random.random() < percent_Filled:
                    domain = self.rows[row].cells[col].domain
                    if len(domain) > 0 and not self.rows[row].cells[col].set:
                        count += 1
                        self.rows[row].cells[col].value = random.choice(domain)
                        self.rows[row].cells[col].set = True

                        self.rows[row].update_domains()
                        self.columns[col].update_domains()
                        self.blocks[self.get_block_num(row, col)].update_domains()

                        self.rows[row].check_row(row)
                        self.columns[col].check_column(col)
                        self.blocks[self.get_block_num(row, col)].check_block(self.get_block_num(row, col))

                        if count == self.m:
                            break
                    elif len(domain) == 0:
                        # self.print_board()
                        # print(count)
                        count = 0
                        self.create_empty_board()

#        print(count)

    def print_board(self):
        for row in self.rows:
            row.print_row()

    def convert_board_to_list(self):
        board_list = []
        for row in self.rows:
            row_list = []
            for cell in row.cells:
                row_list.append(cell.value)
            board_list.append(row_list)
        return board_list



# if __name__ == '__main__':
#     if len(sys.argv) != 3:
#         print('Must specify input file and output file only')
#         quit()
#
#     else:
#         input_file_str = sys.argv[1]
#         output_file_str = sys.argv[2]
#
#     try:
#         input_file = open(input_file_str, 'r')
#         output_file = open(output_file_str, 'w')
#     except:
#         print('Error opening file')
#         quit()
#
#     fileReader = FileReader(input_file)
#     fileWriter = FileWriter(output_file)
#     M, N, P, Q = fileReader.get_params_generator()
#
#     sudoku_board =  SudokuBoardGenerator(M, N, P, Q)
#     sudoku_board.generate_board()
#     board_as_lists = sudoku_board.convert_board_to_list()
#     fileWriter.write_generated_board_to_file(N, P, Q, board_as_lists)

