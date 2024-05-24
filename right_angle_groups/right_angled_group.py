import os
from typing import Tuple
from collections import defaultdict
from math import cos, sin, pi, sqrt

import imageio
import networkx as nx
from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.animation as animation

rc('text',usetex=True)
rc('text.latex', preamble=r'\usepackage{amsmath}')

from word import Word


"""
Right-angled group class
"""
class RAGroup:
    def __init__(
            self, 
            generators: list[str], 
            commutations: list[Tuple[str]],
            group_type: str
    ):
        self.group_type = group_type
        if group_type not in ('artin', 'coxeter'):
            raise ValueError(f"unknown group type {group_type}. I know only artin, coxeter.")
        self.generators = generators + ['1']
        self.generators_set = set(generators)
        self.commutations = defaultdict(set)
        self.commutations_diagram = set()
        for commut in commutations:
            if commut[0] not in self.generators_set or \
                    commut[0] not in self.generators_set:
                raise ValueError(f"unkown generator {commut}. I know only {self.generators}.")
            self.commutations_diagram.add(tuple(sorted(commut)))
            self.commutations[commut[0]].add(commut[1])
            self.commutations[commut[1]].add(commut[0])
        for generator in self.generators:
            self.commutations[generator].add(generator)
        self.uncommutations = {}
        for generator in self.generators:
            self.uncommutations[generator] = self.generators_set - self.commutations[generator]
                
    def unknown_generators(self, word):
        for variable in word.variables:
            if variable not in self.generators_set:
                raise ValueError(f"unkown generator {variable}. I know only {self.generators}.")
    
    @staticmethod
    def sign(number: int) -> int:
        if number == 0:
            return 0
        return 1 if number > 0 else -1
    
    def piling_pop_condition(self, piling, var, eps):
        if piling[var]:
            if self.group_type == 'artin' and piling[var][-1] == -eps:
                return True
            elif self.group_type == 'coxeter' and piling[var][-1] != 0:
                return True
        return False
                
    def generate_piling(
        self, 
        word: str, 
        animate: bool=False, 
        max_stack_len: int=None, 
        dir_path: str=None
    ) -> dict[str, list[str]]:
        word = Word(word, verbose=False)
        
        self.unknown_generators(word)
        if max_stack_len is None:
            max_stack_len = 0
        piling = {generator: [] for generator in self.generators if generator != '1'}
        frame = 0
        if animate:
            formatted_word = word.format_word(-1)
            self.plot_piling(piling, max_stack_len, formatted_word, '_', f'{dir_path}/{frame:0>6}')
            frame += 1
        for idx, (var, power) in enumerate(word.var_power):
            eps = self.sign(power)
            for _ in range(abs(power)):
                if self.piling_pop_condition(piling, var, eps):
                    if piling[var]:
                        piling[var].pop()
                    for var2 in self.uncommutations[var]:
                        if piling[var2]:
                            piling[var2].pop()
                else:
                    piling[var].append(eps)
                    max_stack_len = max(max_stack_len, len(piling[var]))
                    for var2 in self.uncommutations[var]:
                        piling[var2].append(0)
                        max_stack_len = max(max_stack_len, len(piling[var2]))
                if animate:
                    formatted_word = word.format_word(idx)
                    self.plot_piling(piling, max_stack_len, formatted_word, var, f'{dir_path}/{frame:0>6}')
                frame += 1

                        
        return piling, max_stack_len
    
    def plot_piling(
        self, 
        piling: dict[str, list[int]], 
        max_height: int, 
        formatted_word: str,
        cur_var: str,
        fname: str
    ):
        fig, (ax, ax_graph) = plt.subplots(
            1, 2, figsize=(10, 5),
        )
        
        
        # plot piling
        for stack_index, stack in enumerate(piling.values()):
            line = plt.Line2D(
                [stack_index, stack_index], 
                [-1, max_height - .2], 
                color='black', 
                zorder=0)
            ax.add_line(line)
            for level_index, value in enumerate(stack):
                x = stack_index
                y = max_height - level_index - 1
                circle = plt.Circle((x, y), 0.4, color='white', ec='black', zorder=1)
                ax.add_patch(circle)
                if value == 1:
                    ax.plot([x - 0.2, x + 0.2], [y, y], color='red', linewidth=2, zorder=2)
                    ax.plot([x, x], [y - 0.2, y + 0.2], color='red', linewidth=2, zorder=2)
                elif value == -1:
                    ax.plot([x - 0.2, x + 0.2], [y, y], color='red', linewidth=2, zorder=2)
        piling_keys = list(piling)
        for i in range(len(piling)):
            if piling_keys[i] != cur_var:
                ax.text(i, -1.5, f'${piling_keys[i]}$', ha='center', va='center', fontsize=14, zorder=3)
            else:
                stack_label = r'$\boldsymbol{' + piling_keys[i] + '}$'
                ax.text(i, -1.5, stack_label, ha='center', va='center', fontsize=14, zorder=3)
        horizontal_line = plt.Line2D(
            [-1, len(piling)], 
            [max_height - .2, max_height - .2], 
            linewidth=4, 
            color='black', 
            zorder=0)
        ax.add_line(horizontal_line)
        ax.set_xlim(-1, len(piling))
        ax.set_ylim(-1, max_height)
        ax.set_aspect('equal', 'box')
        ax.invert_yaxis() 
        ax.axis('off')
        
        # plot graph
        G = nx.Graph()
        num_nodes = len(piling)
        angle_step = 2 * pi / num_nodes
        node_positions = {}
        node_radius = 0.2
        # plot nodes
        for i, node_key in enumerate(piling.keys()):
            x = cos(i * angle_step)
            y = sin(i * angle_step)
            node_positions[node_key] = (x, y)
            if node_key != cur_var:
                G.add_node(node_key, pos=(x, y), label=f'${node_key}$')
            else:
                node_text = r'$\boldsymbol{' + node_key + '}$'
                G.add_node(node_key, pos=(x, y), label=node_text)
        G.add_edges_from(self.commutations_diagram)
        pos = nx.get_node_attributes(G, 'pos')
        labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_nodes(G, pos, ax=ax_graph, node_size=1000, node_color='skyblue', alpha=0.7)
        # plot commuting edges
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            vec_x, vec_y = x1 - x0, y1 - y0
            length = sqrt(vec_x**2 + vec_y**2)
            norm_x, norm_y = vec_x / length, vec_y / length
            start_x = x0 + norm_x * node_radius
            start_y = y0 + norm_y * node_radius
            end_x = x1 - norm_x * node_radius
            end_y = y1 - norm_y * node_radius
            ax_graph.plot([start_x, end_x], [start_y, end_y], color='black', zorder=0)
        nx.draw_networkx_labels(G, pos, labels, font_size=14, font_weight='bold', font_color='black')
        padding = 1.2 * node_radius
        ax_graph.set_xlim(-1 - padding, 1 + padding)
        ax_graph.set_ylim(-1 - padding, 1 + padding)
        ax_graph.set_aspect('equal', 'box')
        # plot noncommuting edges
        for var2 in self.uncommutations.get(cur_var, []):
            x0, y0 = pos[cur_var]
            x1, y1 = pos[var2]
            vec_x, vec_y = x1 - x0, y1 - y0
            length = sqrt(vec_x**2 + vec_y**2)
            norm_x, norm_y = vec_x / length, vec_y / length
            start_x = x0 + norm_x * node_radius
            start_y = y0 + norm_y * node_radius
            end_x = x1 - norm_x * node_radius
            end_y = y1 - norm_y * node_radius
            ax_graph.plot([start_x, end_x], [start_y, end_y], color='red', zorder=0, linewidth=2)
        
        ax_graph.set_ylim(-2, 1.24)
        ax_graph.axis('off')
        
        ax_graph.text(0, -1.3 - padding, formatted_word, ha='center', va='center', fontsize=14)

        plt.savefig(fname, bbox_inches='tight')
        plt.close()
        
    def animate_folder(self, folder_path: str, output_file: str, show_ani: bool=False, animation_speed: float=1.0):
        image_files = sorted([f for f in os.listdir(folder_path) if f.endswith(('png'))])
        images = [imageio.imread(os.path.join(folder_path, file)) for file in image_files]
        fig, ax = plt.subplots()
        ax.axis('off')
        img_display = ax.imshow(images[0])
        def update(frame):
            img_display.set_array(images[frame])
            return img_display,
        if animation_speed < 0.1 or animation_speed > 10:
            raise ValueError('animation speed should be in range (0.1, 10)')
        frame_interval = 1000. / animation_speed
        ani = animation.FuncAnimation(fig, update, frames=len(images), interval=frame_interval, blit=True)
        ani.save(output_file, writer='imagemagick', savefig_kwargs={'pad_inches': 0})

        if show_ani:
            plt.show()
            plt.close()
        else:
            plt.close()
    
    def animate_piling(self, word: str, dir_path: str, show_ani: bool=False, animation_speed: float=1.0):
        piling, max_stack_len = self.generate_piling(word)
        self.generate_piling(word, True, max_stack_len, dir_path)
        self.animate_folder(dir_path, f'{dir_path}/animation.gif', show_ani, animation_speed)
        

if __name__ == '__main__':
    generators = [f's_{i}' for i in range(1, 7)]
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

    coxeter_group = RAGroup(generators, commutations, 'coxeter')
    artin_group = RAGroup(generators, commutations, 'coxeter')

    cox_identity = 's_4^{-1}s_1s_4^2s_1^{-1}s_2^{-1}s_2s_3 s_1^4 s_4^{-1}s_6^{-1}s_3s_6^2s_3^{-1}s_4s_3^{-1} s_3^2 s_4^{-1}s_2s_6^{-1}s_5s_2^{-1}s_5^{-1}'

    cox_animation_dir = './right_angle_groups/img/cox_animation'
    art_animation_dir = './right_angle_groups/img/artin_animation'
    os.makedirs(cox_animation_dir, exist_ok=True)
    os.makedirs(art_animation_dir, exist_ok=True)

    coxeter_group.animate_piling(cox_identity, cox_animation_dir, show_ani=True, animation_speed=0.5)
    artin_group.animate_piling(cox_identity, art_animation_dir, show_ani=True, animation_speed=0.5)