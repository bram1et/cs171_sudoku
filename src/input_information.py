class InputInformation:
    def __init__(self, input_arguments):

        self.input_file = input_arguments[1]
        self.output_file = input_arguments[2]
        self.timeout_limit = input_arguments[3]
        if not self.timeout_limit.isdigit():
            print("Input timeout is not a number. Quitting...")
            quit()

        remaining_inputs = input_arguments[4:]
        self.tokens = {
            'FC' : True if 'FC' in remaining_inputs else False,
            'ACP' : True if 'ACP' in remaining_inputs else False,
            'MAC' : True if 'MAC' in remaining_inputs else False,
            'MRV' : True if 'MRV' in remaining_inputs else False,
            'DH' : True if 'DH' in remaining_inputs else False,
            'LCV' : True if 'LCV' in remaining_inputs else False
        }
        self.check_tokens(remaining_inputs)

    def check_tokens(self, input_tokens):
        allowed_tokens = ['FC', 'ACP', 'MAC', 'MRV', 'DH', 'LCV']
        for token in input_tokens:
            if token not in allowed_tokens:
                print("Found an incorrect token. Ignoring....")
                break








