import os
import json
import shutil
from typing import Optional
from collections import deque
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arrow


"""
Turing Machine Head Movement Variable
"""
class Move:
    left = 'L'
    right = 'R'
    neutral = 'N'
    L, R, N = left, right, neutral
    
    def __init__(self, move_str: str):
        if move_str.lower() in ('l', 'left'):
            self.move = Move.L
        elif move_str.lower() in ('r', 'right'):
            self.move = Move.R
        elif move_str.lower() in ('n', 'neutral'):
            self.move = Move.N
        else:
            raise ValueError(f'movement string should be from: ({Move.L, Move.R, Move.N}), you passed: {move_str}')
        
    def is_R(self) -> bool:
        return self.move == Move.R
    
    def is_L(self) -> bool:
        return self.move == Move.L
    
    def is_N(self) -> bool:
        return self.move == Move.N
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Move):
            return False
        return self.move == other.move
    
    def __hash__(self) -> int:
        return hash(self.move)
    
    def __str__(self) -> str:
        return self.move
    
    def __int__(self) -> int:
        if self.is_L():
            return -1
        elif self.is_R():
            return 1
        else:
            return 0
        
"""
Turing Machine Head State
"""
class State:
    initial = '0'
    final = '□' 
    
    def __init__(self, state_str: Optional[str] = '0'):
        self.state = state_str
        
    def is_final(self) -> bool:
        return self.state == State.final
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, State):
            return False
        return self.state == other.state
    
    def __hash__(self) -> int:
        return hash(self.state)
    
    def __str__(self) -> str:
        return self.state
    
"""
Turing Machine Tape cell letter
"""
class TapeLetter:
    empty = '∅'
    
    def __init__(self, letter_str: Optional[str] = '∅'):
        self.letter = letter_str
    
    def is_empty(self) -> bool:
        return self.letter == TapeLetter.empty
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, TapeLetter):
            return False
        return self.letter == other.letter
    
    def __hash__(self) -> int:
        return hash(self.letter)
    
    def __str__(self) -> str:
        return self.letter
    
"""
Turing Machine Program
"""
class TMProgram:
    def __init__(
            self,    
            command_list: list[tuple[tuple[State, TapeLetter], tuple[State, TapeLetter, Move]]] = []
    ):
        self.program = {}
        for idx, command in enumerate(command_list):
            inp = command[0]
            out = command[1]
            self.program[inp] = out
            
    def __getitem__(self, state_and_letter: tuple[State, TapeLetter]):
        return self.program[state_and_letter]
    
    def __eq__(self, other):
        if not isinstance(other, TMProgram):
            return False
        return self.program == other.program
    
    def json_dumps(self, indent: int = 2) -> str:
        command_list = []
        for (inp, out) in self.program.items():
            command_list.append([str(item) for item in inp + out])
        return json.dumps(command_list, indent=indent)
    
    def json_dump(self, file_name: str):
        with open(file_name, 'w') as file:
            file.write(self.json_dumps())
    
    def json_loads(self, input_str: str):
        self.program = {}
        command_list = json.loads(input_str)
        for command in command_list:
            cur_state = State(command[0])
            cur_tape_letter = TapeLetter(command[1])
            new_state = State(command[2])
            new_tape_letter = TapeLetter(command[3])
            move = Move(command[4])
            self.program[(cur_state, cur_tape_letter)] = (new_state, new_tape_letter, move)
    
    def json_load(self, file_name: str):
        with open(file_name, 'r') as f:
            self.json_loads(f.read())
            
    def csv_dumps(self) -> str:
        out_list = []
        for (inp, out) in self.program.items():
            out_list.append(','.join([str(el) for el in inp + out]))
        return '\n'.join(out_list)
    
    def csv_dump(self, file_name: str):
        with open(file_name, 'w') as file:
            file.write(self.csv_dumps())
    
    def csv_loads(self, inp_str: str):
        lines = inp_str.split('\n')
        for line in lines:
            entries = line.split(',')
            cur_state = State(entries[0])
            cur_tape_letter = TapeLetter(entries[1])
            new_state = State(entries[2])
            new_tape_letter = TapeLetter(entries[3])
            move = Move(entries[4])
            self.program[(cur_state, cur_tape_letter)] = (new_state, new_tape_letter, move)
    
    def csv_load(self, file_name: str):
        with open(file_name) as file:
            self.csv_loads(file.read())

"""
Turing Machine Program
"""
class TM:
    def __init__(self, 
                 init_tape: list[TapeLetter] = [TapeLetter()], 
                 init_program: TMProgram = TMProgram(), 
                 init_state: State = State(),
                 init_head: int = 0,
                 init_time: int = 0):
        self.tape = deque(init_tape)
        self.program = init_program
        self.state = init_state
        self.head = init_head
        self.time = init_time
        
    def tape_str(self) -> list[str]:
        return [str(item) for item in self.tape]
    
    def time_pp(self, verbose: bool = True, plot_dir: str = ''):
        new_state, new_letter, move = self.program[(self.state, self.tape[self.head])]
        letter_changed = self.tape[self.head] != new_letter
        self.tape[self.head] = new_letter
        if move.is_R():
            if self.head == len(self.tape) - 1:
                self.tape.append(TapeLetter())
            self.head += 1
        elif move.is_L():
            if self.head == 0:
                self.tape.appendleft(TapeLetter())
                self.head += 1
            self.head -= 1
        state_changed = self.state != new_state
        self.state = new_state
        self.time += 1        
        if verbose:
            self.plot(letter_changed, state_changed, plot_dir, int(move))
            
    def plot(self, 
             letter_changed: bool = False, 
             state_changed: bool = False, 
             plot_dir: str = '', 
             move: int = 0
    ):
        tape_letters = [r"$\ldots$"] + self.tape_str() + [r"$\ldots$"]
        fig, ax = plt.subplots()
        
        x_pos = 0
        head_pos = self.head + 1
        prev_pos = head_pos - move
        for idx, letter in enumerate(tape_letters):
            tape_cell = matplotlib.patches.Rectangle(
                xy=(x_pos, 0), width=1, height=1, facecolor="white", edgecolor="black"
            )
            ax.add_patch(tape_cell)
            letter_color = 'black'
            if letter_changed and idx == prev_pos:
                letter_color = 'red'
            ax.text(x_pos + 0.5, 0.5, letter, color=letter_color, ha="center", va="center", fontsize=14)
            x_pos += 1
            
        head_cell = Rectangle(xy=(head_pos, -2), width=1, height=1, facecolor="white", edgecolor="black")
        ax.add_patch(head_cell)
        state_color = 'black'
        if state_changed:
            state_color = 'red'
        ax.text(head_pos + 0.5, -1.5, self.state, color=state_color, ha="center", va="center", fontsize=14)
        
        arrow = Arrow(x=head_pos + 0.5, y=-1, dx=0, dy=1, width=0.3, color='black', linewidth=0.05)
        ax.add_patch(arrow)
        
        h = 0.1
        ax.set_xlim(0+h, x_pos-h)
        ax.set_ylim(-2-h, 1+h)
        ax.axis("off")
        ax.set_aspect('equal')
        if plot_dir:
            zeros_tab = '0' * (4 - len(str(self.time)))
            plt.savefig(f"{plot_dir}/{zeros_tab}{self.time}", dpi=300)
        plt.plot()
        
    def run(self, verbose: bool = True, plot_dir : str = ''):
        if plot_dir:
            if os.path.exists(plot_dir):
                shutil.rmtree(plot_dir)
            if not os.path.exists(plot_dir):
                os.mkdir(plot_dir)
        if verbose:
            self.plot(plot_dir=plot_dir)
        while not self.state.is_final():
            self.time_pp(verbose, plot_dir)

    def json_loads(self, input_str: str):
        data = json.loads(input_str)
        self.tape = deque(TapeLetter(letter) for letter in data['tape_string'])
        self.program = TMProgram()
        self.program.csv_loads(data['program_csv'])
        self.state = State(data['state'])
        self.head = data['head']
        self.time = data['time']

    def json_load(self, file_name: str):
        with open(file_name, 'r') as f:
            self.json_loads(f.read())

    def json_dumps(self, indent: int = 2) -> str:
        data = {
            'tape_string': ''.join(self.tape_str()),
            'program_csv': self.program.csv_dumps(),
            'init_state': str(self.state),
            'head': self.head,
            'time': self.time
        }
        return json.dumps(data, indent=indent)
    
    def json_dump(self, file_name: str):
        with open(file_name, 'w') as file:
            file.write(self.json_dumps())
            
if __name__ == '__main__':
    tm = TM()
    tm.json_load('turing_machines/tm_unary_add.json')
    tm.run(True, 'turing_machines/tm_unary_add')