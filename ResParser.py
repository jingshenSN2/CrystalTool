def parse_res(filename):
    flag = False
    atomSet = set()
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            if line.startswith('CELL'):
                line = line.strip('CELL ')
                _, a, b, c, alpha, beta, gamma = map(float, line.split())
                print(a, b, c, alpha, beta, gamma)
            if line.startswith('MOLE'):
                flag = not flag
                continue
            if flag:
                tmp = line.split()
                elename = tmp[0]
                x, y, z = map(float, tmp[2:5])
                intensity = -1
                if len(tmp) == 8:
                    intensity = tmp[7]
                print(elename, x, y, z, intensity)


parse_res('c21.res')
