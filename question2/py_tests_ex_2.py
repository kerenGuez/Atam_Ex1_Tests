import os
import sys
from string import ascii_uppercase
from random import randint, sample

from generate_graphs import (generate_random_acyclic_graph,
                             generate_random_cyclic_graph,
                             generate_from_lists,
                             visualize_graph)

COLOR_END = "\033[0m"
COLOR_AQUA = "\033[96m"
COLOR_YELLOW = "\033[93m"
TMP_FILE_PATH = "tmp_file"
OUTPUT_DIR = "graphs"
MAX_NODES = 8


def generate_letters(num_nodes):
    return sample(ascii_uppercase, num_nodes)


def make_dict(letters, graph):
    nodes = list(graph.nodes)
    return {nodes[i]: letters[i] for i in range(len(letters))}


def convert_num_to_char(num, convert_dict):
    return convert_dict[num]


def generate_data_section(graph, convert_dict):
    start_section = ".section .data\n"
    mid_section = ""
    for node in graph.nodes():
        mid_section += (f"{convert_num_to_char(node, convert_dict)}: .quad "
                        f"{', '.join([convert_num_to_char(n[1], convert_dict) for n in graph.edges(node)] + ['0'])}\n")

    mid_section += (
                "\nvertices: .quad " + ', '.join([convert_num_to_char(n, convert_dict) for n in graph.nodes] + ["0"])
                + "\n")
    end_section = "circle: .byte 0\n"
    return start_section + mid_section + end_section, mid_section


def generate_sample_file(data_section, is_circle):
    sample_file = f""".global _start

.section .text

  movb circle, %al
  cmpb ${is_circle}, %al
  jne bad_exit

  movq $60, %rax
  movq $0, %rdi
  syscall

bad_exit:
  movq $60, %rax
  movq $1, %rdi
  syscall


{data_section}

"""

    return sample_file


def write(tmp_file_path, content):
    with open(tmp_file_path, 'w') as file:
        file.write(content)


def create_tmp_file(graph, is_circle):
    num_nodes = len(graph.nodes)
    letters = generate_letters(num_nodes)
    conversion_dict = make_dict(letters, graph)
    data_section, array_str = generate_data_section(graph, conversion_dict)
    sample_file = generate_sample_file(data_section, is_circle)
    write(TMP_FILE_PATH, sample_file)
    return array_str


def basic_cyclic_graphs():
    nodes1 = [0, 1]
    edges1 = [(0, 1), (1, 0)]
    graph1 = generate_from_lists(nodes1, edges1)

    nodes2 = [0]
    edges2 = [(0, 0)]
    graph2 = generate_from_lists(nodes2, edges2)

    nodes3 = [0, 1, 2]
    edges3 = [(0, 1), (1, 2), (2, 0)]
    graph3 = generate_from_lists(nodes3, edges3)

    return [graph1, graph2, graph3]


def basic_none_cyclic_graphs():
    nodes1 = [0, 1]
    edges1 = [(0, 1)]
    graph1 = generate_from_lists(nodes1, edges1)

    nodes2 = [0]
    edges2 = []
    graph2 = generate_from_lists(nodes2, edges2)

    nodes3 = [0, 1, 2]
    edges3 = [(0, 1), (1, 2), (0,2)]
    graph3 = generate_from_lists(nodes3, edges3)

    nodes4 = []
    edges = []
    graph4 = generate_from_lists(nodes4, edges)

    return [graph1, graph2, graph3, graph4]


def run_generic_test(asm_file, tests_file, graph, is_circle, file_path):
    array_str = create_tmp_file(graph=graph, is_circle=is_circle)
    visualize_graph(graph, file_path)
    print(f"{COLOR_YELLOW} Testing graph found on '{file_path}': with Num Nodes: {len(graph.nodes)}{COLOR_END}\n{array_str}")
    os.system(f'./{tests_file} {asm_file} {TMP_FILE_PATH}')
    os.system(f'rm -f {TMP_FILE_PATH}')
    print()


def run_generic_tests(asm_file, tests_file, test_name, is_circle, generate_func, basic_graphs, generate_num=10):
    print(f"{COLOR_AQUA} --- Running Basic {test_name} Tests --- {COLOR_END}")
    for i, graph in enumerate(basic_graphs):
        run_generic_test(asm_file=asm_file,
                         tests_file=tests_file,
                         graph=graph,
                         is_circle=is_circle,
                         file_path=f"{OUTPUT_DIR}/{test_name}_basic_{i}.png")

    print(f"{COLOR_AQUA} --- Running Randomized {test_name} Tests --- {COLOR_END}")
    for i in range(generate_num):
        num_nodes = randint(2, MAX_NODES)
        graph = generate_func(num_nodes)
        run_generic_test(asm_file=asm_file,
                         tests_file=tests_file,
                         graph=graph,
                         is_circle=is_circle,
                         file_path=f"{OUTPUT_DIR}/{test_name}_{i}.png")


def run_cyclic_tests(asm_file, tests_file, generate_num=10):
    basic_cyclic = basic_cyclic_graphs()
    run_generic_tests(asm_file=asm_file,
                      tests_file=tests_file,
                      test_name="Cyclic Graphs",
                      is_circle=1,
                      generate_func=generate_random_cyclic_graph,
                      basic_graphs=basic_cyclic,
                      generate_num=generate_num)


def run_none_cyclic_tests(asm_file, tests_file, generate_num=10):
    basic_none_cyclic = basic_none_cyclic_graphs()

    run_generic_tests(asm_file=asm_file,
                      tests_file=tests_file,
                      test_name="None Cyclic Graphs",
                      is_circle=-1,
                      generate_func=generate_random_acyclic_graph,
                      basic_graphs=basic_none_cyclic,
                      generate_num=generate_num)


def run_all(asm_file, tests_file, generate_num=10):
    run_cyclic_tests(asm_file=asm_file, tests_file=tests_file, generate_num=generate_num)
    run_none_cyclic_tests(asm_file=asm_file, tests_file=tests_file, generate_num=generate_num)


if __name__ == '__main__':
    arguments = sys.argv[1:]
    the_asm_file = arguments[0]
    the_tests_file = arguments[1]
    if len(arguments) < 2:
        print('Usage: python3 py_tests_ex_2.py <asm_file> <tests_file> (?generate_num)')
        sys.exit(1)

    if len(arguments) >= 3:
        the_generate_num = int(arguments[2])
    else:
        the_generate_num = 10

    os.system(f"[ -d '{OUTPUT_DIR}' ] && rm -rf '{OUTPUT_DIR}'; mkdir -p '{OUTPUT_DIR}'")
    run_all(asm_file=the_asm_file, tests_file=the_tests_file, generate_num=the_generate_num)
