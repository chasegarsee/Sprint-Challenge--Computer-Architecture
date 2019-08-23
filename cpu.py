import sys


# make a new CPU
class CPU:

    def __init__(self):
        self.registers = [0] * 8
        self.running = False
        self.ram[0] * 256
        self.PC = 0
        self.flag = 0b00000000

    def ram_read(self, MAR):
        try:
            return self.ram[MAR]
        except:
            print("Index out of Range")

    def ram_write(self, MAR, MDR):
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
                    number = comment_split[0].strip()  # trim whitespace
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
        # elif op == "SUB": etc
        elif op == "MUL":
            self.registers[register_a] = self.registers[register_a] * \
                self.registers[register_b]
        elif op == "CMP":
            if self.registers[register_a] == self.registers[register_b]:
                self.flag = 0b00000001
            elif self.registers[register_a] > self.registers[register_b]:
                self.flag = 0b00000010
            else:
                self.flag = 0b00000100
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
