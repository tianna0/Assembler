import Detector


class Instruction:
    """
    Parses the assembly program by looking ahead one or two tokens to determine the type of instruction. 
    """
    
    a_instr = 0   # Addressing Instruction.
    c_instr = 1   # Computation Instruction.
    l_instr = 2   # Label-Declaration pseudo-Instruction.

    def __init__(self, file):
        self.lexer = Detector.Detector(file)
        self._init_instruction_info()

    def _init_instruction_info(self):
        """
        Initializes the instruction data stores.
        """
        self._instruction_type = -1
        self._symbol = ''
        self._dest = ''
        self._comp = ''
        self._jmp = ''

    def _a_instruction(self):
        """
        Addressing Instruction.
        """
        self._instruction_type = Instruction.a_instr
        tok_type, self._symbol = self.lexer.next_token()

    def _l_instruction(self):
        """
        Symbol Declaration instruction. 
        """
        self._instruction_type = Instruction.l_instr
        tok_type, self._symbol = self.lexer.next_token()

    def _c_instruction(self, token, value):
        """
        Computation instruction. 
        """
        self._instruction_type = Instruction.c_instr
        comp_tok, comp_val = self._get_dest(token, value)
        self._get_comp(comp_tok, comp_val)
        self._get_jump()

    def _get_dest(self, token, value):
        """
        Gets the 'dest' part of the instruction.
        """
        tok2, val2 = self.lexer.peek_token()
        if tok2 == Detector.operation and val2 == '=':
            self.lexer.next_token()
            self._dest = value
            comp_tok, comp_val = self.lexer.next_token()
        else:
            comp_tok, comp_val = token, value
        return comp_tok, comp_val

    def _get_comp(self, token, value):
        """
        Gets the 'comp' part of the instruction.
        """
        if token == Detector.operation and (value == '-' or value == '!'):
            tok2, val2 = self.lexer.next_token()
            self._comp = value + val2
        elif token == Detector.number or token == Detector.symbol:
            self._comp = value
            tok2, val2 = self.lexer.peek_token()
            if tok2 == Detector.operation and val2 != ';':
                self.lexer.next_token()
                tok3, val3 = self.lexer.next_token()
                self._comp += val2+val3

    def _get_jump(self):
        """
        Gets the 'jump' part of the instruction.
        """
        token, value = self.lexer.next_token()
        if token == Detector.operation and value == ';':
            jump_tok, jump_val = self.lexer.next_token()
            self._jmp = jump_val

    @property
    def instruction_type(self):
        """
        The extracted instruction type.
        """
        return self._instruction_type

    @property
    def symbol(self):
        """
        The extracted Symbol from instruction.
        """
        return self._symbol

    @property
    def dest(self):
        """
        The extracted 'dest' part of instruction.
        """
        return self._dest

    @property
    def comp(self):
        """
        The extracted 'comp' part of instruction.
        """
        return self._comp

    @property
    def jmp(self):
        """
        The extracted 'jmp' part of instruction.
        """
        return self._jmp

    def has_more_instructions(self):
        return self.lexer.has_more_instructions()

    def advance(self):
        """
        Gets the next instruction. Each instruction reside on a physical line.
        """
        self._init_instruction_info()

        self.lexer.next_instruction()
        token, val = self.lexer.curr_token

        if token == Detector.operation and val == '@':
            self._a_instruction()
        elif token == Detector.operation and val == '(':
            self._l_instruction()
        else:
            self._c_instruction(token, val)