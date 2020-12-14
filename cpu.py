"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

#sprint material
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8
        self.registers[7] = 0xF4
        self.pc = 0 
        self.ram = [0] * 256
        self.halted = False
        self.fl = 0b00000000

    def load(self, filename):
        """Load a program into memory."""

        address = 0
       # open the file
        with open(filename) as my_file:
           for line in my_file:
                comment_split = line.split("#")
                maybe_binary_number = comment_split[0]
                try:
                    x = int(maybe_binary_number, 2)
                    self.ram_write(x, address)
                    address += 1
                except:
                    continue 

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == MUL:
            self.registers[reg_a] *= self.registers[reg_b]
            self.pc += 3
        elif op == CMP:
            if self.registers[reg_a] > self.registers[reg_b]:
                self.fl = 0b00000010
            elif self.registers[reg_a] < self.registers[reg_b]:
                self.fl = 0b00000100
            else: 
                self.fl = 0b00000001
            self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")

        """
        store value in memory
        """

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        """
        read from memory
        """
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value


    def run(self):
        """Run the CPU."""
        while not self.halted:
            instruction_to_execute = self.ram_read(self.pc)
            opperand_a = self.ram_read(self.pc + 1)
            opperand_b = self.ram_read(self.pc + 2)
            self.execute_intstruction(instruction_to_execute, opperand_a, opperand_b)

    def execute_intstruction(self, instruction, opperand_a, opperand_b):
        if instruction == HLT:
            self.halted = True
            self.pc += 1
        elif instruction == PRN:
            print(self.registers[opperand_a])
            self.pc += 2
        elif instruction == LDI:
            self.registers[opperand_a] = opperand_b
            self.pc += 3
        elif instruction == MUL:
            self.alu(instruction, opperand_a, opperand_b)
        elif instruction == CMP:
            self.alu(instruction, opperand_a, opperand_b)
        elif instruction == JMP:
            address = self.registers[opperand_a]
            pc = address
        elif instruction == JEQ:
            if self.fl == 0b00000001:
                address = self.registers[opperand_a]
            pc = address 
        elif instruction == JNE:
            if self.fl == 0b00000000:
                address = self.registers[opperand_a]
            pc = address 
        else:
            print('I dont know what to do.')