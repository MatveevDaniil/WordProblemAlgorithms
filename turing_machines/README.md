# Turing Machines Animations

This project simulates a Turing machine, a theoretical device that manipulates symbols on a strip of tape according to a table of rules.


## Installation

To run the project, you need Python 3 and the following libraries: `imageio` and `matplotlib`. You can install these libraries using pip:

```bash
pip3 install imageio matplotlib
```

## Run Example

The main execution of the program is in `turing_machine.py`. Here's a brief explanation of the code:

```python
if __name__ == '__main__':
    # Initialize the Turing Machine
    tm = TM()  
    # Directory where the program files are stored
    programs_dir = './turing_machines/tm_programs'  
    # Directory where the output images will be stored
    img_dir = './turing_machines/img'  
    # Name of the program to be loaded
    program_name = 'unary_mult_tape_prog'  
    # Load the information about Turing Machine:
    # program, tape, head... 
    tm.load_program_tape(f'{programs_dir}/{program_name}.json')  
    # Define the output directory 
    # Vizualization of steps of a TM will be stored here
    output_dir = f'{img_dir}/{program_name}'  
    # Now we de
    tm.animated_run(output_dir, show_ani=True, animation_speed=2.0, verbose=False)  
```

Now you can run the script in terminal using:

```bash
python3 turing_machine.py
```

# Data Format

The Turing machine program and initial tape state are defined in two separate files: a .csv file for the program and a .json file for the initial tape state.


## Initial Tape State File

The initial tape state file is a .json file with the following keys:

- tape_string: The initial state of the tape.
- program_csv_path: The path to the .csv file containing the program.
- state: The initial state of the Turing machine.
- head: The initial position of the tape head.
- time: The initial time.

Example (unary_mult_tape_prog.json):
```json
{
    "tape_string": "b111b11b",
    "program_csv_path": "./turing_machines/tm_programs/unary_mult_program.csv",
    "state": "0",
    "head": 3,
    "time": 0
}
```

## Program-Table File

The program file is table file which represent program of a Turing Machine. It should be a .csv file with the following columns:

- state: The current state of the Turing machine.
- tape_letter: The letter currently under the tape head.
- new_state: The new state after the transition.
- new_letter: The new letter to be written on the tape.
- step: The direction in which the tape head should move (L for left, R for right, N for no move).
- '-': This sign means that the state/letter should not change.

Example (unary_mult_program.csv):
| state | tape_letter | new_state | new_letter | step |
|-------|-------------|-----------|------------|------|
| 0     | b           | 9         | -          | R    |
| 0     | 0           | -         | -          | L    |
| 0     | 1           | 1         | 0          | R    |
| 1     | b           | 2         | -          | R    |
| 1     | 0           | -         | -          | R    |
| 1     | 1           | -         | -          | N    |
| ...   | ...         | ...       | ...        | ...  |
...