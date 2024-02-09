import re

number = 1 #  '123'
symbol = 2 # 'LOOP', 'END'
operation = 3 #  = ; ( ) @ + - & | !
error = 4 

class Detector(object):
    """
    Uses regular expressions to detect Numbers, Symbols and Operations.
    """
    
    _number_re = r'\d+'
    _symbol_start_re = r'\w_.$:'
    _symbol_re = '[' + _symbol_start_re + '][' + _symbol_start_re + r'\d]*'
    _operation_re = r'[=;()@+\-&|!]'
    _word = re.compile(_number_re + '|' + _symbol_re + '|' + _operation_re)
    _comment = re.compile('//.*$')

    def __init__(self, asm_file_name):
        """
        Initializes the Detector with a given assembly file.
        """
        file = open(asm_file_name, 'r')
        self._lines = file.read()
        self._tokens = self._tokenize(self._lines.split('\n'))
        # List of tokens 
        self.curr_instr_tokens = []
        # Current token 
        self.curr_token = (error, 0)

    def _is_operation(self, word):
        """
        Checks if a word is an operation token.
        """
        return self._is_match(self._operation_re, word)

    def _is_number(self, word):
        """
        Checks if a word is a number token.
        """
        return self._is_match(self._number_re, word)

    def _is_symbol(self, word):
        """
        Checks if a word is a symbol token.
        """
        return self._is_match(self._symbol_re, word)

    def _is_match(self, re_str, word):
        """
        Checks if a word matches a given regular expression.
        """
        return re.match(re_str, word) is not None

    def _tokenize(self, lines):
        """
        Tokenizes each line of the assembly code.
        """
        return [t for t in [self._tokenize_line(l) for l in lines] if t]

    def _tokenize_line(self, line):
        """
        Tokenizes a single line of assembly code.
        """
        return [self._token(word) for word in self._split(self._remove_comment(line))]

    def _remove_comment(self, line):
        """
        Removes comments from a line of assembly code.
        """
        return self._comment.sub('', line)

    def _split(self, line):
        """
        Splits a line into individual tokens.
        """
        return self._word.findall(line)

    def _token(self, word):
        """
        Categorizes a word into a specific token type.
        """
        if self._is_number(word):
            return number, word
        elif self._is_symbol(word):
            return symbol, word
        elif self._is_operation(word):
            return operation, word
        else:
            return error, word

    def has_more_instructions(self):
        """
        Checks if there are more instructions to process.
        """
        return self._tokens != []

    def next_instruction(self):
        """
        Gets the next instruction from the token list.
        """
        self.curr_instr_tokens = self._tokens.pop(0)
        self.next_token()
        return self.curr_instr_tokens

    def has_next_token(self):
        """
        Checks if there are more tokens in the current instruction.
        """
        return self.curr_instr_tokens != []

    def next_token(self):
        """
        Gets the next token from the current instruction.
        """
        if self.has_next_token():
            self.curr_token = self.curr_instr_tokens.pop(0)
        else:
            self.curr_token = error, 0
        return self.curr_token

    def peek_token(self):
        """
        Peeks at the next token without removing it from the current instruction.
        """
        if self.has_next_token():
            return self.curr_instr_tokens[0]
        else:
            return error, 0