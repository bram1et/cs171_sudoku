#!/usr/bin/python
class FileReader:
	def __init__(self, file):
		self.file = file
		self.N = -1
		self.P = -1
		self.Q = -1
		self.M = -1

	def get_params(self):
		try:
			self.N, self.P, self.Q = tuple(self.file.readline().strip().split(' '))
			self.N = int(self.N)
			self.P = int(self.P)
			self.Q = int(self.Q)
		except:
			print("Starting information provided is incorrect or error reading from file. Quiting...")
			quit()

		return self.N, self.P, self.Q

	def get_board(self):
		board = []
		if self.N == -1 or self.P == -1 or self.Q == -1:
			print('Must get parameters first via get_params(). Quitting...')
			quit()
		num_rows = self.P * self.Q
		for row_num in range(num_rows):
			row_str = self.file.readline().strip()
			if len(row_str) == 0:
				print("Starting information provided is incorrect. Quitting...")
				quit()
			row = [int(cell) if cell.isdigit() else cell for cell in row_str.split(' ')]
			board.append(row)
		return board


	def get_params_generator(self):
		try:
			self.M, self.N, self.P, self.Q = tuple(self.file.readline().strip().split(' '))
			self.M = int(self.M)
			self.N = int(self.N)
			self.P = int(self.P)
			self.Q = int(self.Q)
		except:
			print("Starting information provided is incorrect. Quitting...")
			quit()

		return self.M, self.N, self.P, self.Q
