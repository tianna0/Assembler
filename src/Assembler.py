import sys
import Generator
import Instruction
import SymbolMap


class Assembler:
    """
    Reads .asm file and creates a new .hack file which has the assembled machine code as a text file.
    """
    def __init__(self):
        self.symbol_address = 16
        self.symbols_map = SymbolMap.SymbolMap()

    @staticmethod
    def hack_file(asm_file):
        """
        Suggests a file name for the Hack Machine Code source file.
        """
        if asm_file.endswith('.asm'):
            return asm_file.replace('.asm', '.hack')
        else:
            return asm_file + '.hack'

    def look_up_address(self, symbol):
        """
        Look up the address of a symbol.
        """
        if symbol.isdigit():
            return symbol
        else:
            if not self.symbols_map.contains(symbol):
                self.symbols_map.add_entry(symbol, self.symbol_address)
                self.symbol_address += 1
            return self.symbols_map.get_address(symbol)

    def memory_location(self, file):
        """
        Determine memory locations of label definitions.
        """
        parser = Instruction.Instruction(file)
        curr_address = 0
        while parser.has_more_instructions():
            parser.advance()
            inst_type = parser.instruction_type
            if inst_type in [parser.a_instr, parser.c_instr]:
                curr_address += 1
            elif inst_type == parser.l_instr:
                self.symbols_map.add_entry(parser.symbol, curr_address)

    def output_file(self, asm_file, hack_file):
        """
        Generate hack machine code and write results to output file.
        """
        parser = Instruction.Instruction(asm_file)
        with open(hack_file, 'w', encoding='utf-8') as hack_file:
            code = Generator.Generator()
            while parser.has_more_instructions():
                parser.advance()
                inst_type = parser.instruction_type
                if inst_type == parser.a_instr:
                    hack_file.write(code.gen_a_instruction(self.look_up_address(parser.symbol)) + '\n')
                elif inst_type == parser.c_instr:
                    hack_file.write(code.gen_c_instruction(parser.dest, parser.comp, parser.jmp) + '\n')
                

    def assemble(self, file):
        self.memory_location(file)
        self.output_file(file, self.hack_file(file))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("proceesed")
    else:
        asm_file = sys.argv[1]

    hack_assembler = Assembler()
    hack_assembler.assemble(asm_file)