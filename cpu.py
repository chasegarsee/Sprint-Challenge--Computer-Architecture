import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
CMP = 0b10100111
MUL = 0b10100010
ADD = 0b10100000
JMP = 0b01010100
JEQ = 0b01010101
JNQ = 0b01010110
PUSH = 0b01000101
POP = 0b01000110
RET = 0b00010001


# make a new CPU
class CPU:

    def __init__(self):
        self.registers = [0] * 8
        self.running = False
        self.ram = [0] * 256
        self.PC = 0
        self.SP = 7
        self.flag = 0b00000000

    def ram_read(self, MAR):
        try:
            return self.ram[MAR]
        except:
            print("Index out of Range")

    def ram_write(self, MDR, MAR):
        try:
            self.ram[MAR] = MDR
        except:
            print("Index out of Range")

    def increment_PC(self, op_code):
        add = (op_code >> 6) + 1
        self.PC += add

    def load(self, file_name):
        address = 0

        try:
            with open(file_name) as f:
                for line in f:
                    comment_split = line.split('#')
                    number = comment_split[0].strip()
                    if number == "":
                        continue
                    val = int(number, 2)
                    self.ram_write(val, address)
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {file_name} not found")
            sys.exit(2)

    def alu(self, op, register_a, register_b):
        if op == "ADD":
            self.registers[register_a] += self.registers[register_b]
        elif op == "MUL":
            self.registers[register_a] = self.registers[register_a] * \
                self.registers[register_b]
        elif op == "CMP":
            if self.registers[register_a] == self.registers[register_b]:
                self.flag = HLT
            elif self.registers[register_a] > self.registers[register_b]:
                self.flag = 0b00000010
            else:
                self.flag = 0b00000100
        else:
            raise Exception("Invalid ALU operation")

    def trace(self):

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            # self.fl,
            # self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            op_code = self.ram_read(self.PC)

            if op_code == HLT:
                self.running = False
                sys.exit(1)
            elif op_code == LDI:
                address = self.ram_read(self.PC + 1)
                data = self.ram_read(self.PC + 2)
                self.registers[address] = data
                self.increment_PC(op_code)

            elif op_code == PRN:
                address_a = self.ram_read(self.PC + 1)
                print(self.registers[address_a])
                self.increment_PC(op_code)
                pass

            elif op_code == CMP:
                address_a = self.ram_read(self.PC + 1)
                address_b = self.ram_read(self.PC + 2)
                self.alu('CMP', address_a, address_b)
                self.increment_PC(op_code)

            elif op_code == ADD:
                address_a = self.ram_read(self.PC + 1)
                address_b = self.ram_read(self.PC + 2)
                self.alu('ADD', address_a, address_b)
                self.increment_PC(op_code)

            elif op_code == MUL:
                address_a = self.ram_read(self.PC + 1)
                address_b = self.ram_read(self.PC + 2)
                self.alu('MUL', address_a, address_b)
                self.increment_PC(op_code)

            elif op_code == JMP:
                register_address = self.ram_read(self.PC + 1)
                self.PC = self.registers[register_address]

            elif op_code == JEQ:
                register_address = self.ram_read(self.PC + 1)
                if self.flag == HLT:
                    self.PC = self.registers[register_address]
                else:
                    self.increment_PC(op_code)

            elif op_code == JNQ:
                register_address = self.ram_read(self.PC + 1)
                if self.flag != HLT:
                    self.PC = self.registers[register_address]
                else:
                    self.increment_PC(op_code)
            elif op_code == PUSH:
                register_address = self.ram_read(self.PC + 1)
                val = self.registers[register_address]
                self.registers[self.SP] -= 1
                self.ram[self.registers[self.SP]] = val
                self.increment_PC(op_code)
            elif op_code == POP:
                register_address = self.ram_read(self.PC + 1)
                val = self.ram[self.registers[self.SP]]
                self.registers[register_address] = val
                self.registers[self.SP] += 1
                self.increment_PC(op_code)
            elif op_code == 0b01010000:
                self.registers[self.SP] -= 1
                self.ram[self.registers[self.SP]] = self.PC + 2
                address_of_subroutine = self.ram[self.PC + 1]
                self.PC = self.registers[address_of_subroutine]
            # RET
            elif op_code == RET:
                self.PC = self.ram[self.registers[self.SP]]
                self.registers[self.SP] += 1
            else:
                print('here is the else')
