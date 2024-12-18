import re
from pathlib import Path
from helpers import read_file
import time


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


COMBO_OPERAND = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: None,  # A
    5: None,  # B
    6: None,  # C
    # 7: None
}


class Register:
    def __init__(self, number):
        self.number = number


class Computer:
    def __init__(self, looking_for_a=False):
        registers, program = DATA.strip().split("\n\n")
        # a, b, c = registers.strip().split("\n")
        # a = int(a.strip().split(" ")[-1])
        # b = int(b.strip().split(" ")[-1])
        # c = int(c.strip().split(" ")[-1])

        # a, b, c = a, b, c
        a, b, c = list(map(int, re.findall("\d+", registers)))
        self.a = Register(a)
        self.b = Register(b)
        self.c = Register(c)

        # self.a = a
        # self.b = b
        # self.c = c

        COMBO_OPERAND[4] = self.a
        COMBO_OPERAND[5] = self.b
        COMBO_OPERAND[6] = self.c

        self.program = list(map(int, program.strip().split(" ")[-1].split(",")))

        self.i = 0

        self.log = []
        self.looking_for_a = looking_for_a

    def __str__(self):
        string = f"Register A: {self.a.number}\nRegister B: {self.b.number}\nRegister C: {self.c.number}\n\nLog: {self.log_string()}\n\n"
        return string

    def log_string(self):
        return ",".join(list(map(str, self.log)))

    def reset(self):
        self.__init__(self.looking_for_a)

    def get_combo_operand_number(self, operand):
        match operand:
            case 4:
                return self.a.number
            case 5:
                return self.b.number
            case 6:
                return self.c.number
            case _:
                return operand

    def set_a(self, num):
        self.a.number = num

    def set_b(self, num):
        self.b.number = num

    def set_c(self, num):
        self.c.number = num

    def adv(self, operand):
        denom = self.get_combo_operand_number(operand)

        new_a = int(self.a.number / (2**denom))
        self.set_a(new_a)

    def bxl(self, operand):
        self.set_b(self.b.number ^ operand)

    def bst(self, operand):
        combo_op = self.get_combo_operand_number(operand)
        self.set_b(combo_op % 8)

    def jnz(self, operand):
        if self.a.number == 0:
            return

        self.i = operand

    def bxc(self, operand):
        self.set_b(self.b.number ^ self.c.number)

        # read operand

    def out(self, operand):
        combo_op = self.get_combo_operand_number(operand)
        mod8 = combo_op % 8
        # print(mod8)
        self.log.append(mod8)

    def bdv(self, operand):
        denom = self.get_combo_operand_number(operand)

        self.set_b(int(self.a.number / (2**denom)))

    def cdv(self, operand):
        denom = self.get_combo_operand_number(operand)
        self.set_c(int(self.a.number / (2**denom)))

    def run_program(self):
        last_i = -1
        try:
            while self.i < len(self.program):
                if last_i == self.i:
                    break

                if self.looking_for_a:
                    for i in range(len(self.log)):
                        if self.log[i] != self.program[i]:
                            break

                last_i = self.i

                opcode = self.program[self.i]
                operand = self.program[self.i + 1]

                # print(opcode, operand, self.i)

                # print(self)

                self.run(opcode, operand)

            # if self.i == 4:
            #     break

        except:
            pass

        # print(self)

    def run(self, opcode, operand):
        match opcode:
            case 0:
                self.adv(operand)
            case 1:
                self.bxl(operand)
            case 2:
                self.bst(operand)
            case 3:
                return self.jnz(operand)
            case 4:
                self.bxc(operand)
            case 5:
                self.out(operand)
            case 6:
                self.bdv(operand)
            case 7:
                self.cdv(operand)
            case _:
                self.i = len(self.program) + 1
                return

        self.i += 2

    def test_run(self):

        i = 999999999
        i += 1
        while True:
            # computer = Computer(a, b, c, program, True)
            # for i in range(10000000, 999999999):
            self.set_a(i)

            self.run_program()
            if self.log == self.program:
                return i

            if i >= 10000000 and (i % 10000000) == 0:
                print("Checked up to", i)

            self.reset()
            i += 1


def part1():
    c = Computer()

    c.run_program()


def part2():
    # a, b, c, program = parse()
    # print(a, b, c, program)
    c = Computer(True)

    start = time.time()
    num = c.test_run()
    end = time.time()

    print(f"Completed Part 2 in {end - start} seconds")
    return num


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
