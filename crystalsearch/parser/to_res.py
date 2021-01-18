def to_res(input_filename, output_filename, match_result):
    """储存Cell类到res文件, 测试版"""
    element_map = {}
    for atom1, atom2 in match_result.items():
        element_name = atom1.element + atom1.index
        element_map[element_name] = atom2.element
    with open(input_filename, 'r') as inp, open(output_filename, 'w+') as output:
        counter = 0
        index_map = {}
        for line in inp.readlines():
            if line.startswith('SFAC'):
                tmp = line.split()
                for i in range(1, len(tmp)):
                    index_map[tmp[i]] = i
            if line.startswith('MOLE'):
                counter = counter + 1
            elif counter == 1:
                tmp = line.split()
                element_name = tmp[0]
                if element_name in element_map:
                    tmp[0] = element_map[element_name]
                else:
                    tmp[0] = 'H'
                tmp[1] = str(index_map[tmp[0]])
                line = ' '.join(tmp) + '\n'
            output.write(line)
