from __future__ import print_function
import copy

class Row:
    def __init__(self, size):
        self.size = size
        self.cells = []

    def add_to_row(self, cell):
        self.cells.append(cell)

    def print_row(self):
        for cell in range(len(self.cells)):
            print(self.cells[cell].value, end=' ')
        print()

    def check_row(self, row_num):
        cell_values = []
        for cell in self.cells:
            if cell.value != 0:
                cell_values.append(cell.value)
        if len(set(cell_values)) != len(cell_values):
#            self.print_row()
#            raise ValueError('There is an error in row {}'.format(row_num))
            return False
        return True

    def update_domains(self):
        values_to_remove = []
        changes = dict()
        for this_cell in self.cells:
            if this_cell.value != 0:
                values_to_remove.append(this_cell.value)
        for this_cell in self.cells:
            changes[self.cells.index(this_cell)] = []
            if not this_cell.set:
                for value_to_remove in values_to_remove:
                    if this_cell.check_if_in_domain(value_to_remove):
                        this_cell.remove_from_domain(value_to_remove)
                        changes[self.cells.index(this_cell)].append(value_to_remove)
        return changes

    def add_to_domains(self, row_changes):
        for cell in row_changes.keys():
            if len(row_changes[cell]) > 0 and self.cells[cell].set == False:
                self.cells[cell].domain += row_changes[cell]

    def get_degree_cell(self, a_cell):
        degree = 0
        for other_cell in self.cells:
            if not other_cell.set:
                degree += 1
        return degree

class Column:
    def __init__(self, size):
        self.size = size
        self.cells = []

    def add_to_column(self, cell):
        self.cells.append(cell)

    def print_column(self):
        for cell in self.cells:
            print(cell.value, end='\n')

    def check_column(self, col_num):
        cell_values = []
        for cell in self.cells:
            if cell.value != 0:
                cell_values.append(cell.value)
        if len(set(cell_values)) != len(cell_values):
#            self.print_column()
#            raise ValueError('There is an error in column {}'.format(col_num))
            return False
        return True

    def update_domains(self):
        changes = dict()
        values_to_remove = []
        for this_cell in self.cells:
            if this_cell.value != 0:
                values_to_remove.append(this_cell.value)
        for this_cell in self.cells:
            changes[self.cells.index(this_cell)] = []
            if not this_cell.set:
                for value_to_remove in values_to_remove:
                    if this_cell.check_if_in_domain(value_to_remove):
                        this_cell.remove_from_domain(value_to_remove)
                        changes[self.cells.index(this_cell)].append(value_to_remove)
        return changes

    def add_to_domains(self, col_changes):
        for cell in col_changes.keys():
            if len(col_changes[cell]) > 0 and self.cells[cell].set == False:
                self.cells[cell].domain += col_changes[cell]

    def get_degree_cell(self, a_cell):
        degree = 0
        for other_cell in self.cells:
            if not other_cell.set:
                degree += 1
        return degree


class Block:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = []

    def add_to_block(self, cell):
        self.cells.append(cell)

    def print_block(self):
        break_point = self.cols
        for num_cells in range(len(self.cells)):
            print(self.cells[num_cells].value, end=' ')
            break_point -= 1
            if break_point == 0:
                print()
                break_point = self.cols

    def check_block(self, block_num):
        cell_values = []
        for cell in self.cells:
            if cell.value != 0:
                cell_values.append(cell.value)
        if len(set(cell_values)) != len(cell_values):
#            self.print_block()
#            raise ValueError('There is an error in block {}'.format(block_num))
            return False
        return True

    def update_domains(self):
        values_to_remove = []
        changes = dict()

        for this_cell in self.cells:
            if this_cell.value != 0:
                values_to_remove.append(this_cell.value)

        for this_cell in self.cells:
            changes[self.cells.index(this_cell)] = []
            if not this_cell.set:
                for value_to_remove in values_to_remove:
                    if this_cell.check_if_in_domain(value_to_remove):
                        this_cell.remove_from_domain(value_to_remove)
                        changes[self.cells.index(this_cell)].append(value_to_remove)
        return changes

    def add_to_domains(self, block_changes):
        for cell in block_changes.keys():
            if len(block_changes[cell]) > 0 and self.cells[cell].set == False:
                self.cells[cell].domain += block_changes[cell]

    def get_degree_cell(self, a_cell):
        degree = 0
        for other_cell in self.cells:
            if not other_cell.set:
                degree += 1
        return degree


class Cell:
    def __init__(self, domain, row, column, cell_number, input_tokens, value=0):
        self.value = value
        self.domain = [value] if value != 0 else domain
        self.set = True if value != 0 else False
        self.row = row
        self.column = column
        self.cell_number = cell_number
        self.degree = 0
        self.input_tokens = input_tokens
        # self.mode = 'FC'

    def get_priority(self):
        priority = [0, 0, self.cell_number]
        if self.input_tokens['MRV']:
            priority[0] = len(self.domain)
        if self.input_tokens['DH']:
            priority[1] = -1 * self.degree
        return tuple(priority)


    def __cmp__(self, other):
        return self.cell_number - other.cell_number

    def __lt__(self, other):
        return other.cell_number > self.cell_number

    def remove_from_domain(self, value):
        self.domain.remove(value)

    def is_domain_empty(self):
        return len(self.domain) == 0

    def check_if_in_domain(self, value):
        return value in self.domain
