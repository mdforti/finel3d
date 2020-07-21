##############################################################################
# Selecciona las condiciones de contorno sin necesidad de correr un ejecutable.
# Corresponde a la version 1.0 del protocolo $BoundariesFormat 
# compatible con el BST usado anteriormente
#
# Codigos de nodos que interpreta la libreria boundaries handler
#
# Restricciones
#  2: Vinculo de 3ra especie
# 11: Restriccion en X
# 12: Restriccion en Y
#
# Fuerzas
# 3: Fuerza en X positiva
# 4: Fuerza en X negativa
#
###############################################################################
import numpy as np
import gmesh_handler as gmesh
import os
import platform
import pdb

def BST(file_name, num_of_nodes, elem_type):
    nodos = np.zeros(num_of_nodes, dtype=int)
    restricted = 0
    x_restricted = 0
    y_restricted = 0
    x_force_pos = 0
    neg_x_force_pos = 0

    if 'Linux' in platform.system():
        os.system('clear')
    elif 'Darwin' in platform.system():
        os.system('clear')
    else:
        os.system('cls')
    print('                                     pyBST')
    print()
    print('q: quit  c: continue')
    print('r: restrict 3 DOF')
    print('x: Positive force in x-axis   x-: Negative force in x-axis')
    print('rx: x restricted group   ry: y-restricted group')
    print('Code - Physical Group')

    while True:
        usr_input = input('> ')
        if len(usr_input) > 1:
            if usr_input[0] == 'r' and usr_input[1]==' ':
                print('Physical Group {}, fully restricted!'.format(usr_input[-1]))
                restricted = int(usr_input[-1])
            elif usr_input[0] == 'x' and usr_input[1]==' ':
                print('x force in Physical Group {}'.format(usr_input[-1]))
                x_force_pos = int(usr_input[-1])
            elif usr_input[0] == 'x' and usr_input[1]=='-':
                print('Negative x force in Physical Group {}'.format(usr_input[-1]))
                neg_x_force_pos = int(usr_input[-1])
            elif usr_input[0] == 'r' and usr_input[1]=='x':
                print('X restriction for Physical Group {}'.format(usr_input[-1]))
                x_restricted = int(usr_input[-1])
            elif usr_input[0] == 'r' and usr_input[1]=='y':
                print('Y restriction for Physical Group {}'.format(usr_input[-1]))
                y_restricted = int(usr_input[-1])
        else:
            if usr_input == 'q':
                exit()
            elif usr_input == 'c':
                break
            else:
                print('Incorrect format!')



    file = gmesh.read(file_name)
    physical_lines = file.find_physical_elements(ElementType=elem_type)

    if elem_type == 1:
        for i in physical_lines:
            if i[0] == restricted:
                nodos[i[2]-1], nodos[i[3]-1] = 2, 2
            elif i[0] == x_force_pos:
                nodos[i[2]-1], nodos[i[3]-1] = 3, 3
            elif i[0] == neg_x_force_pos:
                nodos[i[2]-1], nodos[i[3]-1] = 4, 4
            elif i[0] == x_restricted:
                nodos[i[2]-1], nodos[i[3]-1] = 11, 11
            elif i[0] == y_restricted:
                nodos[i[2]-1], nodos[i[3]-1] = 12, 12

    elif elem_type == 2:
        for i in physical_lines:
            if i[0] == restricted:
                nodos[i[2]-1], nodos[i[3]-1], nodos[i[4]-1] = 2, 2, 2
            elif i[0] == x_force_pos:
                nodos[i[2]-1], nodos[i[3]-1], nodos[i[4]-1] = 3, 3, 3
            elif i[0] == neg_x_force_pos:
                nodos[i[2]-1], nodos[i[3]-1], nodos[i[4]-1] = 4, 4, 4
            elif i[0] == x_restricted:
                nodos[i[2]-1], nodos[i[3]-1], nodos[i[4]-1] = 11, 11, 11
            elif i[0] == y_restricted:
                nodos[i[2]-1], nodos[i[3]-1], nodos[i[4]-1] = 12, 12, 12
        
            
    if os.path.exists('nodes_selection_file.dat'):
        os.remove('nodes_selection_file.dat')

    with open('nodes_selection_file.dat', 'a') as file:
        file.write('$BoundariesFormat\n')
        file.write('v1.0\n')
        file.write('$Nodes\n')
        file.write(str(num_of_nodes) + '\n')
        for node in nodos:
            file.write(str(node) + '\n')
        file.write('$end\n')

if __name__ == '__main__':
    BST(file_name = 'simple_cube1.msh', num_of_nodes = 14, elem_type=2)
