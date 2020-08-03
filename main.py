#!/usr/bin/env python

# Emulator
# Nathanael Key

import sys

class Emulator():
    def __init__(self):
        self.syntax = {
            "mov": self.mov,
            "push": self.push,
            "pop": self.pop
        }
        self.registers = {
            "ax": 0,
            "bx": 0,
            "cx": 0,
            "dx": 0
        }
        self.stack = []

    # read source code from file
    def read_src(self, src_file):
        with open(src_file, "r") as f:
            self.src = f.read()
    
    # lineify source code
    def line_src(self):
        self.src = self.src.strip("\n").split("\n")

    # tokenize source code
    def token_src(self):
        self.src = [line.split(" ") for line in self.src]

    # run/interpret source code
    def run_src(self):
        for line in self.src:
            self.syntax[line[0]](line[1:])

    # pop data from register
    def pop_reg(self, reg):
        if reg in self.registers:
            return int(self.registers[reg])

        else:
            raise SyntaxError("`{}` register not supported".format(reg))

    # push data to register
    def push_reg(self, data, reg):
        if reg in self.registers:
            self.registers[reg] = data

        else:
            raise SyntaxError("`{}` register not supported".format(reg))

    # check parameters
    def check_param(self, param, oper, leng):
        if len(param) != leng:
            raise SyntaxError("`{}` expects {} parameters".format(oper, leng))

    # convert data/reg to data
    def to_data(self, data):
        try:
            return int(data)

        except ValueError:
            return self.pop_reg(data)

    # mov [data/reg] [reg]
    def mov(self, param):
        self.check_param(param, "mov", 2)

        data = self.to_data(param[0])

        self.push_reg(data, param[1])

        return param

    # push [data/reg]
    def push(self, param):
        self.check_param(param, "push", 1)

        data = self.to_data(param[0])

        self.stack.append(data)

    # pop [reg]
    def pop(self, param):
        self.check_param(param, "pop", 1)

        self.push_reg(self.stack.pop(), param[0])

def main():
    emu = Emulator()
    emu.read_src("src")
    emu.line_src()
    emu.token_src()
    emu.run_src()

    print(emu.registers)
    print(emu.stack)

if __name__ == "__main__":
    main()

sys.exit()
