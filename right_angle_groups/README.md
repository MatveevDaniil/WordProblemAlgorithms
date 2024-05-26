# Right Angle Groups

This project contains Python scripts for working with right angle Coxeter and Artin groups.

# Word class

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

# Right Angle Group Class

- `right_angled_group.py`: This is the script of the class RAGroup. This class takes takes a list of generators, a list of commutations, and a group type as input. The group type can be either 'artin' or 'coxeter'. The class stores the generators and commutations, and checks that the group type and generators are valid. The class contain methods for checking the equality of two words in a group and visualization of this algorithm.

## Code Example

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

## Requirements

This project requires Python 3 and the following libraries: imageio, networkx, matplotlib.
You can install them using:

```bash
pip3 install imageio networkx matplotlib
```