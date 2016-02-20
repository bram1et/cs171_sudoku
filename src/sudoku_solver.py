from __future__ import print_function

import copy
import time

from src.sudoku_pieces import Block
from src.sudoku_pieces import Cell
from src.sudoku_pieces import Column
from src.sudoku_pieces import Row

try:
    import Queue as que  # ver. < 3.0
except ImportError:
    import queue as que

from pqdict import pqdict, minpq, maxpq

class SudokuSolver:
    def __init__(self, N, P, Q, board_values, input_tokens):
        self.n = N
        self.p = P
        self.q = Q
        self.rows = []
        self.columns = []
        self.blocks = []
        self.board_values = board_values
        self.num_cells = self.n * self. n
        self.cells_solved = 0
        self.solved = False
        self.start_time = None
        self.time_out_limit = None
        self.input_tokens = input_tokens
        self.nodes_created = 0
        self.times_backtracked = 0
        # self.cell_queue = que.PriorityQueue()
        self.test_queue = minpq()
        self.domain = self.get_domain()
        self.check_board_params()
        self.initialize_board()



    def get_block_num(self, row, col):
        return (int(row/self.p) + int(col/self.q)) + (self.p - 1) * int(row/self.p)

    def check_update(self, row_num, column_num, block_num):
        row_check = self.rows[row_num].check_row(row_num)
        column_check = self.columns[column_num].check_column(column_num)
        block_check = self.blocks[block_num].check_block(block_num)

        return row_check, column_check, block_check

    def update_domains(self, row_num, column_num, block_num):
        row_changes = self.rows[row_num].update_domains()
        col_changes = self.columns[column_num].update_domains()
        block_changes = self.blocks[block_num].update_domains()
        return row_changes, col_changes, block_changes


#        print('Row Changes', end=" ")
#        print(row_changes)
#        print('Column Changes', end=" ")
#        print(col_changes)
#        print('Block Changes', end=" ")
#        print(block_changes)

#    def add_back_to_domain(self, row_num, column_num, block_num, value):
#        self.rows[row_num].add_to_domains(value)
#        self.columns[column_num].add_to_domains(value)
#        self.blocks[block_num].add_to_domains(value)

    def initialize_board(self):
        cell_count = 1
        for count in range(self.n):
            self.rows.append(Row(self.n))
            self.columns.append(Column(self.n))
            self.blocks.append(Block(self.p, self.q))

        for row in range(self.n):
            for col in range(self.n):
                block_num = self.get_block_num(row, col)
                cell_value = self.board_values[row][col]
                if cell_value != 0:
                    self.cells_solved += 1
                new_cell = Cell(copy.copy(self.domain), row, col, cell_count, self.input_tokens, cell_value)
                if not new_cell.set:
                    # self.cell_queue.put(new_cell)
                    self.test_queue.additem(new_cell, new_cell.get_priority())
                self.rows[row].add_to_row(new_cell)
                self.columns[col].add_to_column(new_cell)
                self.blocks[block_num].add_to_block(new_cell)
                cell_count += 1

        for index in range(self.n):
            self.check_update(index, index, index)
            if self.input_tokens['FC']:
                self.update_domains(index, index, index)
                for key in self.test_queue.keys():
                    self.test_queue.updateitem(key, key.get_priority())
            if self.input_tokens['MRV']:
                self.update_domains(index, index, index)
                for key in self.test_queue.keys():
                    self.test_queue.updateitem(key, key.get_priority())
            if self.input_tokens['DH']:
                for cell in self.test_queue.keys():
                    row_num = cell.row
                    col_num = cell.column
                    block_num = self.get_block_num(row_num, col_num)
                    cell.row_degree = self.rows[row_num].get_degree_cell(cell)
                    cell.col_degree = self.columns[col_num].get_degree_cell(cell)
                    cell.block_degree = self.blocks[block_num].get_degree_cell(cell)
                    # cell.degree = row_degree + col_degree + block_degree
                    self.test_queue.updateitem(cell, cell.get_priority())

    def print_board(self):
        for row in self.rows:
            row.print_row()

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
        # if len(board) != self.n:
        #     raise ValueError('Number of rows in board must equal N')
        for row in self.board_values:
            if len(row) != self.n:
                print('Number of columns in board must equal N')
                quit()
            for cell in row:
                if cell not in self.domain and cell != 0:
                    # print(self.domain, cell)
                    print('Value of a cell is not in domain')
                    quit()
        return True

    def print_domains(self):
        for row in self.rows:
            for col in range(self.n):
                print(row.cells[col].domain, end=" ")
            print()

    def check_changes(self, row_changes, col_changes, block_changes, row_num, col_num, block_num):
        for cell in row_changes.keys():
            if len(row_changes[cell]) > 0:
                if self.rows[row_num].cells[cell].is_domain_empty():
                    return False
        for cell in col_changes.keys():
            if len(col_changes[cell]) > 0:
                if self.columns[col_num].cells[cell].is_domain_empty():
                    return False
        for cell in block_changes.keys():
            if len(block_changes[cell]) > 0:
                if self.blocks[block_num].cells[cell].is_domain_empty():
                    return False
        return True

    def calculate_domain_heuristic(self, row_num, col_num, block_num):
        cells_in_this_row = self.rows[row_num].cells
        for cell_in_row in cells_in_this_row:
            if not cell_in_row.set and cell_in_row in self.test_queue:
                old_degree = cell_in_row.degree
                row_num_dh = cell_in_row.row
                col_num_dh = cell_in_row.column
                block_num_dh = self.get_block_num(row_num_dh, col_num_dh)
                row_degree = self.rows[row_num_dh].get_degree_cell(cell_in_row)
                col_degree = self.columns[col_num_dh].get_degree_cell(cell_in_row)
                block_degree = self.blocks[block_num_dh].get_degree_cell(cell_in_row)
                cell_in_row.degree = row_degree + col_degree + block_degree
                print("row: ", end="")
                print(cell_in_row.degree - old_degree)
                self.test_queue.updateitem(cell_in_row, cell_in_row.get_priority())

        cells_in_this_col = self.columns[col_num].cells
        for cell_in_col in cells_in_this_col:
            if not cell_in_col.set and cell_in_col in self.test_queue:
                old_degree = cell_in_col.degree
                row_num_dh = cell_in_col.row
                col_num_dh = cell_in_col.column
                block_num_dh = self.get_block_num(row_num_dh, col_num_dh)
                row_degree = self.rows[row_num_dh].get_degree_cell(cell_in_col)
                col_degree = self.columns[col_num_dh].get_degree_cell(cell_in_col)
                block_degree = self.blocks[block_num_dh].get_degree_cell(cell_in_col)
                cell_in_col.degree = row_degree + col_degree + block_degree
                print("column: ", end="")
                print(cell_in_col.degree - old_degree)
                self.test_queue.updateitem(cell_in_col, cell_in_col.get_priority())

        cells_in_this_block = self.blocks[block_num].cells
        for cell_in_block in cells_in_this_block:
            if not cell_in_block.set and cell_in_block in self.test_queue:
                old_degree = cell_in_block.degree
                row_num_dh = cell_in_block.row
                col_num_dh = cell_in_block.column
                block_num_dh = self.get_block_num(row_num_dh, col_num_dh)
                row_degree = self.rows[row_num_dh].get_degree_cell(cell_in_block)
                col_degree = self.columns[col_num_dh].get_degree_cell(cell_in_block)
                block_degree = self.blocks[block_num_dh].get_degree_cell(cell_in_block)
                cell_in_block.degree = row_degree + col_degree + block_degree
                print("block: ", end="")
                print(cell_in_block.degree - old_degree)
                self.test_queue.updateitem(cell_in_block, cell_in_block.get_priority())

    def calculate_domain_heuristic_test(self, row_num, col_num, block_num, modifier):

        changed_cells = set()

        cells_in_this_row = self.rows[row_num].cells
        for cell_in_row in cells_in_this_row:
            if not cell_in_row.set and cell_in_row in self.test_queue:
                cell_in_row.row_degree += modifier
                changed_cells.add(cell_in_row)

        cells_in_this_col = self.columns[col_num].cells
        for cell_in_col in cells_in_this_col:
            if not cell_in_col.set and cell_in_col in self.test_queue:
                cell_in_col.column_degree += modifier
                changed_cells.add(cell_in_col)

        cells_in_this_block = self.blocks[block_num].cells
        for cell_in_block in cells_in_this_block:
            if not cell_in_block.set and cell_in_block in self.test_queue:
                cell_in_block.block_degree += modifier
                changed_cells.add(cell_in_block)

        for changed_cell in changed_cells:
            self.test_queue.updateitem(changed_cell, changed_cell.get_priority())



    def solve_board(self, start_row=0, start_col=0):
        # print()
        # self.print_board()
        # print()
        self.nodes_created += 1
        time_elapsed = time.time() - self.start_time
        if time_elapsed > self.time_out_limit:
            return self

        if self.cells_solved == (self.n * self.n):
            self.solved = True
            return self
        else:
            for row_num in range(start_row, self.n):
                for col_num in range(start_col, self.n):
                    this_cell = self.rows[row_num].cells[col_num]
                    if not this_cell.set and len(this_cell.domain) > 0:
                        # for value in self.domain: //commenting out for FC testing purposes
                        for value in this_cell.domain:
                            this_cell.value = value
#                            print(value, row_num, col_num, self.cells_solved)
#                             print("Trying {0} at location ({1}, {2}). {3} Solved".format(value, row_num, col_num, self.cells_solved))
#                            self.print_board()
                            row_ok, col_ok, block_ok = self.check_update(row_num, col_num, self.get_block_num(row_num, col_num))
                            if row_ok and col_ok and block_ok:
                                this_cell.set = True
                                if self.input_tokens['FC']:
                                    row_changes, col_changes, block_changes = self.update_domains(row_num, col_num, self.get_block_num(row_num, col_num))
                                    if not self.check_changes(row_changes, col_changes, block_changes, row_num, col_num, self.get_block_num(row_num, col_num)):
                                        # print("A domain is empty")
                                        self.rows[row_num].add_to_domains(row_changes)
                                        self.columns[col_num].add_to_domains(col_changes)
                                        self.blocks[self.get_block_num(row_num, col_num)].add_to_domains(block_changes)
                                        this_cell.value = 0
                                        this_cell.set = False
                                        continue
                                self.cells_solved += 1
                                if col_num == self.n - 1:
                                    next_row = row_num + 1
                                    next_col = 0
                                else:
                                    next_row = row_num
                                    next_col = col_num + 1
                                solved_board = self.solve_board(next_row, next_col)
                                if solved_board != None:
                                    return solved_board
                                else:
                                    # print("Backtracking on {0} at location ({1}, {2})".format(value, row_num, col_num))
                                    this_cell.set = False
                                    self.times_backtracked += 1
                                    self.cells_solved -= 1
                                    if self.input_tokens['FC']:
                                        self.rows[row_num].add_to_domains(row_changes)
                                        self.columns[col_num].add_to_domains(col_changes)
                                        self.blocks[self.get_block_num(row_num, col_num)].add_to_domains(block_changes)
                            else:
                                this_cell.value = 0
                                this_cell.set = False
#                                self.cells_solved -= 1
                        this_cell.value = 0
                        this_cell.set = False
                        return None
                    else:
                        if col_num == self.n - 1:
                            row_num = row_num + 1
                            col_num = 0
                start_row = 0
                start_col = 0
        return None

    def solve_board_heap(self, print_progress=False, start_row=0, start_col=0):
        print_progress = False
        if print_progress == True:
            print()
            self.print_board()
            print()
        self.nodes_created += 1
        time_elapsed = time.time() - self.start_time
        if time_elapsed > self.time_out_limit:
            return self

        if self.cells_solved == (self.n * self.n):
            self.solved = True
            return self
        else:
            # while not self.cell_queue.empty():
            while self.test_queue:
                # this_cell= self.cell_queue.get()
                this_cell,_ = self.test_queue.popitem()
                row_num = this_cell.row
                col_num = this_cell.column
                block_num = self.get_block_num(row_num, col_num)
                if not this_cell.set and len(this_cell.domain) > 0:
                    for value in this_cell.domain:
                        this_cell.value = value
                        if print_progress == True:
                            print(value, row_num, col_num, self.cells_solved)
                            print("Trying {0} at location ({1}, {2}). {3} Solved".format(value, row_num, col_num, self.cells_solved))
                            self.print_board()
                        row_ok, col_ok, block_ok = self.check_update(row_num, col_num, self.get_block_num(row_num, col_num))
                        if row_ok and col_ok and block_ok:
                            this_cell.set = True
                            if self.input_tokens['FC']:
                                row_changes, col_changes, block_changes = self.update_domains(row_num, col_num, self.get_block_num(row_num, col_num))
                                if not self.check_changes(row_changes, col_changes, block_changes, row_num, col_num, self.get_block_num(row_num, col_num)):
                                    # print("A domain is empty")
                                    self.rows[row_num].add_to_domains(row_changes)
                                    self.columns[col_num].add_to_domains(col_changes)
                                    self.blocks[self.get_block_num(row_num, col_num)].add_to_domains(block_changes)
                                    this_cell.value = 0
                                    this_cell.set = False
                                    continue
                            if self.input_tokens['MRV'] and self.input_tokens['FC']:
                                for row_change in row_changes.keys():
                                    if len(row_changes[row_change]) > 0:
                                        update_cell = self.rows[row_num].cells[row_change]
                                        if update_cell in self.test_queue:
                                            self.test_queue.updateitem(update_cell, update_cell.get_priority())

                                for col_change in col_changes.keys():
                                    if len(col_changes[col_change]) > 0:
                                        update_cell = self.columns[col_num].cells[col_change]
                                        if update_cell in self.test_queue:
                                            self.test_queue.updateitem(update_cell, update_cell.get_priority())

                                for block_change in block_changes.keys():
                                    if len(block_changes[block_change]) > 0:
                                        update_cell = self.blocks[block_num].cells[block_change]
                                        if update_cell in self.test_queue:
                                            self.test_queue.updateitem(update_cell, update_cell.get_priority())

                            if self.input_tokens['DH']:
                                # self.calculate_domain_heuristic(row_num, col_num, block_num)
                                self.calculate_domain_heuristic_test(row_num, col_num, block_num, -1)

                            self.cells_solved += 1
                            if col_num == self.n - 1:
                                next_row = row_num + 1
                                next_col = 0
                            else:
                                next_row = row_num
                                next_col = col_num + 1
                            solved_board = self.solve_board_heap(next_row, next_col)
                            if solved_board != None:
                                return solved_board
                            else:
                                if print_progress == True:
                                    print("Backtracking on {0} at location ({1}, {2})".format(value, row_num, col_num))
                                this_cell.set = False
                                self.times_backtracked += 1
                                self.cells_solved -= 1
                                # self.cell_queue.put(this_cell)
                                if this_cell not in self.test_queue:
                                    self.test_queue.additem(this_cell, this_cell.get_priority())

                                if self.input_tokens['FC']:
                                    self.rows[row_num].add_to_domains(row_changes)
                                    self.columns[col_num].add_to_domains(col_changes)
                                    self.blocks[self.get_block_num(row_num, col_num)].add_to_domains(block_changes)

                                if self.input_tokens['MRV'] and self.input_tokens['FC']:
                                    for row_change in row_changes.keys():
                                        if len(row_changes[row_change]) > 0:
                                            update_cell = self.rows[row_num].cells[row_change]
                                            if update_cell in self.test_queue:
                                                self.test_queue.updateitem(update_cell, update_cell.get_priority())

                                    for col_change in col_changes.keys():
                                        if len(col_changes[col_change]) > 0:
                                            update_cell = self.columns[col_num].cells[col_change]
                                            if update_cell in self.test_queue:
                                                self.test_queue.updateitem(update_cell, update_cell.get_priority())

                                    for block_change in block_changes.keys():
                                        if len(block_changes[block_change]) > 0:
                                            update_cell = self.blocks[block_num].cells[block_change]
                                            if update_cell in self.test_queue:
                                                self.test_queue.updateitem(update_cell, update_cell.get_priority())

                                if self.input_tokens['DH']:
                                    self.calculate_domain_heuristic_test(row_num, col_num, block_num, +1)

                        else:
                            this_cell.value = 0
                            this_cell.set = False
                            # self.cell_queue.put(this_cell)
                            if this_cell not in self.test_queue:
                                self.test_queue.additem(this_cell, this_cell.get_priority())
#                                self.cells_solved -= 1
                    this_cell.value = 0
                    this_cell.set = False
                    # self.cell_queue.put(this_cell)
                    if this_cell not in self.test_queue:
                        self.test_queue.additem(this_cell, this_cell.get_priority())
                    return None
                else:
                    if col_num == self.n - 1:
                        row_num = row_num + 1
                        col_num = 0
            start_row = 0
            start_col = 0
        return None

    def heap_test(self):
        this_cell = self.rows[4].cells[4]
        # self.cell_queue.put(self.rows[4].cells[4])
        change = True
        print(this_cell in self.test_queue)
        # while self.test_queue:
        #     cell, priority = self.test_queue.popitem()
        #     print(cell.cell_number, cell.row, cell.column, (len(cell.domain), cell.degree, cell.cell_number))


    def board_to_output(self):
        output_string = "("
        for row in self.rows:
            for col in range(self.n):
                output_string += str(row.cells[col].value)
                output_string += ","
        output_string = output_string[:-1]
        output_string += ")"
        return output_string


