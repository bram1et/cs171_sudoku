class RunInfo:

    def __init__(self):
        self.total_start = None
        self.preprocessing_start = None
        self.preprocessing_done = None
        self.search_start = None
        self.search_done = None
        self.solution_time = None
        self.status_types = {"s": "success",
                             "t": "timeout",
                             "e": "error"}
        self.status = None
        self.solution = None
        self.count_nodes = 0
        self.count_deadends = 0

    def generate_empty_board(self, N):
        output_string = "("
        for i in range(N * N):
            output_string += "0,"

        output_string = output_string[:-1]
        output_string += ")"
        return  output_string
