import re
from collections import defaultdict


class Proc(object):

    def __init__(self):
        self.r0 = 0
        self.r1 = 0
        self.r2 = 0
        self.r3 = 0
        self.fuzzed_dict = defaultdict(set)
        self.dict_by_sample = defaultdict(list)
        self.opcode_map = dict()

    def get_registers(self):
        return [self.r0, self.r1, self.r2, self.r3]

    def set_registers(self, vals):
        self.r0, self.r1, self.r2, self.r3 = vals

    def do_add_r(self, a, b, c):
        a = f"r{a}"
        b = f"r{b}"
        c = f"r{c}"
        setattr(self, c, getattr(self, a) + getattr(self, b))

    def do_add_i(self, a, b, c):
        a = f"r{a}"
        c = f"r{c}"
        setattr(self, c, getattr(self, a) + b)

    def do_mul_r(self, a, b, c):
        a = f"r{a}"
        b = f"r{b}"
        c = f"r{c}"
        setattr(self, c, getattr(self, a) * getattr(self, b))

    def do_mul_i(self, a, b, c):
        a = f"r{a}"
        c = f"r{c}"
        setattr(self, c, getattr(self, a) * b)

    def do_ban_r(self, a, b, c):
        a = f"r{a}"
        b = f"r{b}"
        c = f"r{c}"
        setattr(self, c, getattr(self, a) & getattr(self, b))

    def do_ban_i(self, a, b, c):
        a = f"r{a}"
        c = f"r{c}"
        setattr(self, c, getattr(self, a) & b)

    def do_bor_r(self, a, b, c):
        a = f"r{a}"
        b = f"r{b}"
        c = f"r{c}"
        setattr(self, c, getattr(self, a) | getattr(self, b))

    def do_bor_i(self, a, b, c):
        a = f"r{a}"
        c = f"r{c}"
        setattr(self, c, getattr(self, a) | b)

    def do_set_r(self, a, b, c):
        a = f"r{a}"
        c = f"r{c}"
        setattr(self, c, getattr(self, a))

    def do_set_i(self, a, b, c):
        c = f"r{c}"
        setattr(self, c, a)

    def do_gtir(self, a, b, c):
        b = f"r{b}"
        c = f"r{c}"
        setattr(self, c, 1) if a > getattr(self, b) else setattr(self, c, 0)

    def do_gtri(self, a, b, c):
        a = f"r{a}"
        c = f"r{c}"
        setattr(self, c, 1) if getattr(self, a) > b else setattr(self, c, 0)

    def do_gtrr(self, a, b, c):
        a = f"r{a}"
        b = f"r{b}"
        c = f"r{c}"
        setattr(self, c, 1) if getattr(self, a) > getattr(self, b) else setattr(self, c, 0)

    def do_eqir(self, a, b, c):
        b = f"r{b}"
        c = f"r{c}"
        setattr(self, c, 1) if a == getattr(self, b) else setattr(self, c, 0)

    def do_eqri(self, a, b, c):
        a = f"r{a}"
        c = f"r{c}"
        setattr(self, c, 1) if getattr(self, a) == b else setattr(self, c, 0)

    def do_eqrr(self, a, b, c):
        a = f"r{a}"
        b = f"r{b}"
        c = f"r{c}"
        setattr(self, c, 1) if getattr(self, a) == getattr(self, b) else setattr(self, c, 0)

    def fuzz(self, opcode, a, b, c, before, after):
        for func in [getattr(self, i) for i in dir(self) if re.search(f'^do_', i) is not None]:
            self.set_registers(before)
            func(a, b, c)
            if self.get_registers() == after:
                self.dict_by_sample[(a, b, c, tuple(before), tuple(after))].append(opcode)
                self.fuzzed_dict[opcode].add(func)

    def map_opcodes(self):
        fuzzed_dict_copy = self.fuzzed_dict.copy()
        modifed = True
        while modifed is True:
            modifed = False
            for opcode in fuzzed_dict_copy.keys():
                if len(fuzzed_dict_copy[opcode]) == 1:
                    self.opcode_map[opcode] = list(fuzzed_dict_copy[opcode])[0]
            for correct_opcode in self.opcode_map.keys():
                func = self.opcode_map[correct_opcode]
                for opcode in fuzzed_dict_copy.keys():
                    if func in fuzzed_dict_copy[opcode]:
                        fuzzed_dict_copy[opcode].remove(func)
                        modifed = True

    def __repr__(self):
        return f"{self.r0}, {self.r1}, {self.r2}, {self.r3}"


if __name__ == "__main__":
    with open("Day16In.txt", "r") as f:
        content = f.read().splitlines()

    last_index = [i for i, s in enumerate(content) if s.find("After:") != -1][-1]
    part1in = content[:last_index + 1]
    part2in = [i for i in content[last_index + 1:] if i != '']

    p = Proc()
    reg_state_rexp = re.compile(r'(\[[0-9, ]+\])')
    op_match_rexp = re.compile(r'(\d+) (\d+) (\d+) (\d+)')
    inputs = list()
    for i, s in enumerate(part1in):
        before_line = s.find("Before:")
        if before_line == -1:
            continue
        before_match = re.search(reg_state_rexp, s)
        before = eval(before_match.groups()[0])
        op_match = re.search(op_match_rexp, part1in[i + 1])
        opcode, a, b, c = [int(i) for i in op_match.groups()]
        after_match = re.search(reg_state_rexp, part1in[i + 2])
        after = eval(after_match.groups()[0])
        # parsing for part 1 done

        inputs.append((opcode, a, b, c, before, after))

    for i in inputs:
        p.fuzz(*i)

    gr_eq_3 = [k for k, v in p.dict_by_sample.items() if len(v) >= 3]
    print(f"Part 1: {len(gr_eq_3)}")

    p.map_opcodes()
    p.set_registers([0, 0, 0, 0])
    for line in part2in:
        op_match = re.search(op_match_rexp, line)
        opcode, a, b, c = [int(i) for i in op_match.groups()]
        p.opcode_map[opcode](a, b, c)

    print(f"Part 2: {p.r0}")
