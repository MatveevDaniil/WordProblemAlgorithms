# WordProblemAlgorithms

This project will help you learn a lot about the foundations of the theory of algorithms on the problem of word equality in groups. In the study, we will tell you brick by brick what an algorithm is from a mathematical point of view, their capabilities and limitations, and how the most fundamental problem of group theory is related to the heart of the concept of an algorithm.
To better understand the rigorous mathematical definitions and theorems proven in our article, we have developed visualization software published in this repository. In addition to visualization, you can use this project to directly check the equality of group elements.


## Introduction to the paper

A common question explored by mathematicians has surrounded the idea of normal forms, or the irreducible forms of mathematical objects. Since the same structure may appear in different ways, it is helpful to know when two objects are in some sense equivalent. 
This question can appear in the form of determining if some function can be expressed as a polynomial equation (regular function). 
It also appears in an exciting example in Galois theory about the constructibility of the 17-gon: 

$$ 16\cos\left(\frac{2\pi}{17}\right) = -1 + \sqrt{17} + \sqrt{34-2\sqrt{17}} + 2\sqrt{17 + 3\sqrt{17}-\sqrt{34-2\sqrt{17})}-2\sqrt{34+2\sqrt{17}}}.$$

In group theory, this decision problem is frequently present when determining if two group elements given by words formed from a finite list of generators are the same. This is commonly referred to as "the word problem", and has been studied by algebraists from the 20th century on. In general, this is an example of an undecidable problem. However, extensive work has been done to uncover the structures necessary to allow us to answer this question. 

To establish the algorithmic undecidability of a problem, a formal definition of an algorithm is crucial.  Section 2 introduces Turing machines, a cornerstone of computational models, to unveil the fundamental limitations of algorithms. Leveraging this theory, Section 3 demonstrates the undecidability of the word problem for semigroups in general. Section 4 replicates this result for groups, while introducing free groups as the first non-trivial example of a structure with a solvable word problem.
We will then explore Coxeter groups, a particular group for which this question becomes decideable, before moving to a linear-time algorithm for a particular type of Coxeter group.



## Turing Machines Animations

This project simulates a Turing machine, a theoretical device that manipulates symbols on a strip of tape according to a table of rules.


### Installation

To run the project, you need Python 3 and the following libraries: `imageio` and `matplotlib`. You can install these libraries using pip:

```bash
pip3 install imageio matplotlib
```

### Run Example

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

## Data Format

The Turing machine program and initial tape state are defined in two separate files: a .csv file for the program and a .json file for the initial tape state.


### Initial Tape State File

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

### Program-Table File

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


## Right Angle Groups

This project contains Python scripts for working with right angle Coxeter and Artin groups.

## Word class

- `word.py`: This script contains the `Word` class and functions for parsing and preparing expressions. The `Word` class represents a word over some alphabet. It parses the expression of the word, stores the variables and their powers, and can format the word for output.

To use the `Word` class, import it from `word.py` and create an instance with the expression of the word as a string. For example:

Some examples
```python
from word import Word

word1 = Word('a^2b^3c^4')
word2 = Word('x_1^2*x_2x_3^4')
word3 = Word('x_{12}^2 (x_2x^{4})')
word4 = Word('yz x_{1}^2*x_{10}')
```

## Right Angle Group Class

- `right_angled_group.py`: This is the script of the class RAGroup. This class takes takes a list of generators, a list of commutations, and a group type as input. The group type can be either 'artin' or 'coxeter'. The class stores the generators and commutations, and checks that the group type and generators are valid. The class contain methods for checking the equality of two words in a group and visualization of this algorithm.

### Code Example

Here is an example of how to use the `RAGroup` class:

```python
# Define the generators for the group
generators = [f's_{i}' for i in range(1, 7)]
# Define the commutations for the group
commutations = [
    ('s_1', 's_4'),
    ('s_1', 's_5'),
    ('s_2', 's_5'),
    ('s_2', 's_6'),
    ('s_3', 's_6'),
    ('s_3', 's_4'),
    ('s_4', 's_1'),
    ('s_4', 's_3'),
    ('s_5', 's_1'),
    ('s_5', 's_2'),
    ('s_6', 's_2'),
    ('s_6', 's_3')
]
# Create instances of the RAGroup class for a Coxeter group and an Artin group
coxeter_group = RAGroup(generators, commutations, 'coxeter')
artin_group = RAGroup(generators, commutations, 'coxeter')
# Define a word in the Coxeter group
cox_identity = 's_4^{-1}s_1s_4^2s_1^{-1}s_2^{-1}s_2s_3 s_1^4 s_4^{-1}s_6^{-1}s_3s_6^2s_3^{-1}s_4s_3^{-1} s_3^2 s_4^{-1}s_2s_6^{-1}s_5s_2^{-1}s_5^{-1}'
# Define directories for storing the animations of the piling process
cox_animation_dir = './right_angle_groups/img/cox_animation'
art_animation_dir = './right_angle_groups/img/artin_animation'
# Create the directories if they do not exist
os.makedirs(cox_animation_dir, exist_ok=True)
os.makedirs(art_animation_dir, exist_ok=True)
# Create animations of the piling process for the Coxeter and Artin groups
coxeter_group.animate_piling(cox_identity, cox_animation_dir, show_ani=True, animation_speed=0.5)
artin_group.animate_piling(cox_identity, art_animation_dir, show_ani=True, animation_speed=0.5)
```

### Requirements

This project requires Python 3 and the following libraries: imageio, networkx, matplotlib.
You can install them using:

```bash
pip3 install imageio networkx matplotlib
```
