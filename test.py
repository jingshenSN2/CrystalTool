import CrystalParser
import GraphConverter

cell = CrystalParser.parse_res('c21.res')
cell.calc_neighbors()
graph = GraphConverter.graph_converter(cell)

print(cell.atom_list)
