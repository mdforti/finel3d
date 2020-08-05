import numpy as np
import sys
import os
import pdb

class read:
    def __init__(self, filepath):

        self.file_path = filepath
        if not os.path.isfile(self.file_path):
            print()
            print("can´t open boundary condition file!")
            print('The file {} does not exist!'.format(self.file_path))
            sys.exit()
        else:
            with open(self.file_path) as file:
                while True:
                    line = file.readline().rstrip()
                    if line =='$BoundariesFormat':
                        file_format = file.readline().rstrip()
                        if file_format == 'v1.0':
                            print('File found!')
                            print('Boundaries condition file format: '+file_format)
                        else:
                            print('Format not suported')
                            sys.exit()
                    if line == '$end':
                        break

    def get_boundaries(self):
        lines = []
        nodes = []
        with open(self.file_path) as file:
            while True:
                line = file.readline().rstrip()
                if line =='$Nodes':
                    self.nodes_size = np.fromstring(file.readline().rstrip(), sep=' ')
                    for i in range(int(self.nodes_size)):
                        data = int(file.readline().rstrip())
                        nodes.append(data)
                        self.nodes = nodes
                if line == '$end':
                    break
        return self.nodes
    
    def get_r_s(self, nodes, dof_per_node):
        s = []
        r = []
        if dof_per_node ==2:
            for i in range(len(nodes)):
        
                # NODOS CON VINCULO DE 3ra ESPECIE
                if nodes[i] == 2:
                    s.append(2*i)
                    s.append(2*i+1)
                # NODO CON VINCULO DE 2da ESPECIE en X
                elif nodes[i] == 11:
                    s.append(2*i)
                    r.append(2*i+1)
                # NODO CON VINCULO DE 2da ESPECIE EN Y
                elif nodes[i] == 12:
                    s.append(2*i+1)
                    r.append(2*i)
                # NODO CON FUERZAS EN X Y VINCULOS DE 2da ESPECIE (en Y)
                elif nodes[i]==13:
                    s.append(2*i+1)
                    r.append(2*i)
                elif nodes[i]==14:
                    s.append(2*i+1)
                    r.append(2*i)
                # NODO CON FUERZAS EN Y Y VINCULOS DE 2da ESPECIE (en X)
                elif nodes[i]==15:
                    r.append(2*i+1)
                    s.append(2*i)
                elif nodes[i]==16:
                    r.append(2*i+1)
                    s.append(2*i)
                # NODOS CON FUERZAS Y VINCULOS de 3ra ESPECIE
                elif nodes[i]==7:
                    s.append(2*i)
                    s.append(2*i+1)
                elif nodes[i]==8:
                    s.append(2*i)
                    s.append(2*i+1)
                elif nodes[i]==9:
                    s.append(2*i)
                    s.append(2*i+1)
                elif nodes[i]==10:
                    s.append(2*i)
                    s.append(2*i+1)
                else:
                    r.append(2*i)
                    r.append(2*i+1)

        elif dof_per_node == 3:

            for i in range(len(nodes)):
        
                # NODOS CON VINCULO DE 3ra ESPECIE
                if nodes[i] == 2:
                    s.append(3*i)
                    s.append(3*i+1)
                    s.append(3*i+2)
                # SOLAMENTE ESTA MODIFICADO EL CODIGO DE ARRIBA, SE DEBE MODIFICAR TAMBIEN LOS CODIGOS DE
                # ABAJO PARA RESOLVER UN MESHADO 3D
                # NODO CON VINCULO DE 2da ESPECIE en X
                elif nodes[i] == 11:
                    s.append(2*i)
                    r.append(2*i+1)
                # NODO CON VINCULO DE 2da ESPECIE EN Y
                elif nodes[i] == 12:
                    s.append(2*i+1)
                    r.append(2*i)
                # NODO CON FUERZAS EN X Y VINCULOS DE 2da ESPECIE (en Y)
                elif nodes[i]==13:
                    s.append(2*i+1)
                    r.append(2*i)
                elif nodes[i]==14:
                    s.append(2*i+1)
                    r.append(2*i)
                # NODO CON FUERZAS EN Y Y VINCULOS DE 2da ESPECIE (en X)
                elif nodes[i]==15:
                    r.append(2*i+1)
                    s.append(2*i)
                elif nodes[i]==16:
                    r.append(2*i+1)
                    s.append(2*i)
                # NODOS CON FUERZAS Y VINCULOS de 3ra ESPECIE
                elif nodes[i]==7:
                    s.append(2*i)
                    s.append(2*i+1)
                elif nodes[i]==8:
                    s.append(2*i)
                    s.append(2*i+1)
                elif nodes[i]==9:
                    s.append(2*i)
                    s.append(2*i+1)
                elif nodes[i]==10:
                    s.append(2*i)
                    s.append(2*i+1)
                else:
                    r.append(3*i)
                    r.append(3*i+1)
                    r.append(3*i+2)
                    
        elif dof_per_node == 1:
                for i in range(len(nodes)):

                    if nodes[i] == 2:
                        s.append(i)
                    else:
                        r.append(i)

        r = np.array(r)
        s = np.array(s)
        return r, s

    def get_forces(self, nodes, dof_per_node):
        if dof_per_node == 2:
            F = np.zeros(2*len(nodes)).reshape(-1,1)
            f1 = float(input('X Force: '))
            f2 = float(input('Y Force: '))       
            for i in range(len(nodes)):
                if nodes[i] == 3:
                    F[2*i] = f1
                elif nodes[i] == 4:
                    F[2*i]=-f1
                elif nodes[i] == 5:
                    F[2*i+1] =f2
                elif nodes[i] == 6:
                    F[2*i+1] =-f2
        else:
            print('Cant assembly Force Vector. Exiting')
            exit()

        return F
    
    def get_stress(self, nodes, lines, forces, nodetype, ElementType, dof_per_node):
        F = np.zeros(dof_per_node*len(nodes)).reshape(-1,1)

        if ElementType == 2:
            thickness = 1
            for i in range(len(lines)):
                # Fuerza aplicada en la linea 1 (la de arriba)
                nod1 = nodes[lines[i][2]-1]
                nod2 = nodes[lines[i][3]-1]
                longit = np.linalg.norm(nod1-nod2)

                # FUERZAS SOLAS
                # 3 - FUERZAS X POSITIVAS
                if nodetype[lines[i][2]-1] == 3:
                    F[2*(lines[i][2]-1)] += longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 3:
                    F[2*(lines[i][3]-1)] += longit*thickness*forces[lines[i][0]]/2
                # 4 - FUERZAS X NEGATIVAS
                if nodetype[lines[i][2]-1] == 4:
                    F[2*(lines[i][2]-1)] -= longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 4:
                    F[2*(lines[i][3]-1)] -= longit*thickness*forces[lines[i][0]]/2
                # 5 - FUERZAS Y POSITIVAS
                if nodetype[lines[i][2]-1] == 5:
                    F[(2*(lines[i][2]-1))+1] += longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 5:
                    F[(2*(lines[i][3]-1))+1] += longit*thickness*forces[lines[i][0]]/2
                # 6 - FUERZAS Y NEGATIVAS
                if nodetype[lines[i][2]-1] == 6:
                    F[(2*(lines[i][2]-1))+1] -= longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 6:
                    F[(2*(lines[i][3]-1))+1] -= longit*thickness*forces[lines[i][0]]/2

                # FUERZAS Y VINCULOS
                # 7 - FUERZAS X POSITIVAS + VINCULO 3ra especie
                if nodetype[lines[i][2]-1] == 7:
                    F[2*(lines[i][2]-1)] += longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 7:
                    F[2*(lines[i][3]-1)] += longit*thickness*forces[lines[i][0]]/2
                # 8 - FUERZAS X NEGATIVAS + VINCULO 3ra especie
                if nodetype[lines[i][2]-1] == 8:
                    F[2*(lines[i][2]-1)] -= longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 8:
                    F[2*(lines[i][3]-1)] -= longit*thickness*forces[lines[i][0]]/2
                # 9 - FUERZAS Y POSITIVAS + VINCULO 3ra especie
                if nodetype[lines[i][2]-1] == 9:
                    F[(2*(lines[i][2]-1))+1] += longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 9:
                    F[(2*(lines[i][3]-1))+1] += longit*thickness*forces[lines[i][0]]/2
                # 10 - FUERZAS Y NEGATIVAS + VINCULO 3ra especie
                if nodetype[lines[i][2]-1] == 10:
                    F[(2*(lines[i][2]-1))+1] -= longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 10:
                    F[(2*(lines[i][3]-1))+1] -= longit*thickness*forces[lines[i][0]]/2
                
                # FUERZAS Y RESTRICCIONES
                # 13 - FUERZA X POSITIVA + RESTRICCION Y
                if nodetype[lines[i][2]-1] == 13:
                    F[2*(lines[i][2]-1)] += longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 13:
                    F[2*(lines[i][3]-1)] += longit*thickness*forces[lines[i][0]]/2
                # 14 - FUERZA X NEGATIVA + RESTRICCION Y
                if nodetype[lines[i][2]-1] == 14:
                    F[2*(lines[i][2]-1)] -= longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 14:
                    F[2*(lines[i][3]-1)] -= longit*thickness*forces[lines[i][0]]/2
                # 9 - FUERZAS Y POSITIVAS + RESTRICCION X
                if nodetype[lines[i][2]-1] == 15:
                    F[(2*(lines[i][2]-1))+1] += longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 15:
                    F[(2*(lines[i][3]-1))+1] += longit*thickness*forces[lines[i][0]]/2
                # 10 - FUERZAS Y NEGATIVAS + RESTRICCION X
                if nodetype[lines[i][2]-1] == 16:
                    F[(2*(lines[i][2]-1))+1] -= longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 16:
                    F[(2*(lines[i][3]-1))+1] -= longit*thickness*forces[lines[i][0]]/2
        if ElementType == 4:

            for i in range(len(lines)):
                # Fuerza aplicada en la linea 1 (la de arriba)
                a = nodes[lines[i][2]-1]
                b = nodes[lines[i][3]-1]
                c = nodes[lines[i][4]-1]
                cross_prod = np.cross( b-a, c-a )
                area = 0.5 * np.linalg.norm(cross_prod)
                # FUERZAS SOLAS
                # 3 - FUERZAS X POSITIVAS
                if nodetype[lines[i][2]-1] == 3:
                    F[3*(lines[i][2]-1)] += area*forces[lines[i][0]]/3
                if nodetype[lines[i][3]-1] == 3:
                    F[3*(lines[i][3]-1)] += area*forces[lines[i][0]]/3
                if nodetype[lines[i][3]-1] == 3:
                    F[3*(lines[i][4]-1)] += area*forces[lines[i][0]]/3
                
                # 4 - FUERZAS X NEGATIVAS
                if nodetype[lines[i][2]-1] == 4:
                    F[3*(lines[i][2]-1)] -= area*forces[lines[i][0]]/3
                if nodetype[lines[i][3]-1] == 4:
                    F[3*(lines[i][3]-1)] -= area*forces[lines[i][0]]/3
                if nodetype[lines[i][3]-1] == 4:
                    F[3*(lines[i][4]-1)] -= area*forces[lines[i][0]]/3

                # 5 - FUERZAS Y POSITIVAS
                if nodetype[lines[i][2]-1] == 5:
                    F[(2*(lines[i][2]-1))+1] += longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 5:
                    F[(2*(lines[i][3]-1))+1] += longit*thickness*forces[lines[i][0]]/2
                # 6 - FUERZAS Y NEGATIVAS
                if nodetype[lines[i][2]-1] == 6:
                    F[(2*(lines[i][2]-1))+1] -= longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 6:
                    F[(2*(lines[i][3]-1))+1] -= longit*thickness*forces[lines[i][0]]/2

                # FUERZAS Y VINCULOS
                # 7 - FUERZAS X POSITIVAS + VINCULO 3ra especie
                if nodetype[lines[i][2]-1] == 7:
                    F[2*(lines[i][2]-1)] += longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 7:
                    F[2*(lines[i][3]-1)] += longit*thickness*forces[lines[i][0]]/2
                # 8 - FUERZAS X NEGATIVAS + VINCULO 3ra especie
                if nodetype[lines[i][2]-1] == 8:
                    F[2*(lines[i][2]-1)] -= longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 8:
                    F[2*(lines[i][3]-1)] -= longit*thickness*forces[lines[i][0]]/2
                # 9 - FUERZAS Y POSITIVAS + VINCULO 3ra especie
                if nodetype[lines[i][2]-1] == 9:
                    F[(2*(lines[i][2]-1))+1] += longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 9:
                    F[(2*(lines[i][3]-1))+1] += longit*thickness*forces[lines[i][0]]/2
                # 10 - FUERZAS Y NEGATIVAS + VINCULO 3ra especie
                if nodetype[lines[i][2]-1] == 10:
                    F[(2*(lines[i][2]-1))+1] -= longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 10:
                    F[(2*(lines[i][3]-1))+1] -= longit*thickness*forces[lines[i][0]]/2
                
                # FUERZAS Y RESTRICCIONES
                # 13 - FUERZA X POSITIVA + RESTRICCION Y
                if nodetype[lines[i][2]-1] == 13:
                    F[2*(lines[i][2]-1)] += longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 13:
                    F[2*(lines[i][3]-1)] += longit*thickness*forces[lines[i][0]]/2
                # 14 - FUERZA X NEGATIVA + RESTRICCION Y
                if nodetype[lines[i][2]-1] == 14:
                    F[2*(lines[i][2]-1)] -= longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 14:
                    F[2*(lines[i][3]-1)] -= longit*thickness*forces[lines[i][0]]/2
                # 9 - FUERZAS Y POSITIVAS + RESTRICCION X
                if nodetype[lines[i][2]-1] == 15:
                    F[(2*(lines[i][2]-1))+1] += longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 15:
                    F[(2*(lines[i][3]-1))+1] += longit*thickness*forces[lines[i][0]]/2
                # 10 - FUERZAS Y NEGATIVAS + RESTRICCION X
                if nodetype[lines[i][2]-1] == 16:
                    F[(2*(lines[i][2]-1))+1] -= longit*thickness*forces[lines[i][0]]/2
                if nodetype[lines[i][3]-1] == 16:
                    F[(2*(lines[i][3]-1))+1] -= longit*thickness*forces[lines[i][0]]/2

        if ElementType == 1:
            for i in range(len(lines)):
                # FUERZAS SOLAS
                # 3 - FUERZAS X POSITIVAS
                if nodetype[lines[i][2]-1] == 3:
                    F[2*(lines[i][2]-1)] += thickness*forces[lines[i][0]]
                if nodetype[lines[i][3]-1] == 3:
                    F[2*(lines[i][3]-1)] += thickness*forces[lines[i][0]]
                # 4 - FUERZAS X NEGATIVAS
                if nodetype[lines[i][2]-1] == 4:
                    F[2*(lines[i][2]-1)] -= thickness*forces[lines[i][0]]
                if nodetype[lines[i][3]-1] == 4:
                    F[2*(lines[i][3]-1)] -= thickness*forces[lines[i][0]]
                # 5 - FUERZAS Y POSITIVAS
                if nodetype[lines[i][2]-1] == 5:
                    F[(2*(lines[i][2]-1))+1] += thickness*forces[lines[i][0]]
                if nodetype[lines[i][3]-1] == 5:
                    F[(2*(lines[i][3]-1))+1] += thickness*forces[lines[i][0]]
                # 6 - FUERZAS Y NEGATIVAS
                if nodetype[lines[i][2]-1] == 6:
                    F[(2*(lines[i][2]-1))+1] -= thickness*forces[lines[i][0]]
                if nodetype[lines[i][3]-1] == 6:
                    F[(2*(lines[i][3]-1))+1] -= thickness*forces[lines[i][0]]

                # FUERZAS Y VINCULOS
                # 7 - FUERZAS X POSITIVAS + VINCULO 3ra especie
                if nodetype[lines[i][2]-1] == 7:
                    F[2*(lines[i][2]-1)] += thickness*forces[lines[i][0]]
                if nodetype[lines[i][3]-1] == 7:
                    F[2*(lines[i][3]-1)] += thickness*forces[lines[i][0]]
                # 8 - FUERZAS X NEGATIVAS + VINCULO 3ra especie
                if nodetype[lines[i][2]-1] == 8:
                    F[2*(lines[i][2]-1)] -= thickness*forces[lines[i][0]]
                if nodetype[lines[i][3]-1] == 8:
                    F[2*(lines[i][3]-1)] -= thickness*forces[lines[i][0]]
                # 9 - FUERZAS Y POSITIVAS + VINCULO 3ra especie
                if nodetype[lines[i][2]-1] == 9:
                    F[(2*(lines[i][2]-1))+1] += thickness*forces[lines[i][0]]
                if nodetype[lines[i][3]-1] == 9:
                    F[(2*(lines[i][3]-1))+1] += thickness*forces[lines[i][0]]
                # 10 - FUERZAS Y NEGATIVAS + VINCULO 3ra especie
                if nodetype[lines[i][2]-1] == 10:
                    F[(2*(lines[i][2]-1))+1] -= thickness*forces[lines[i][0]]
                if nodetype[lines[i][3]-1] == 10:
                    F[(2*(lines[i][3]-1))+1] -= thickness*forces[lines[i][0]]

                # FUERZAS Y RESTRICCIONES
                # 13 - FUERZA X POSITIVA + RESTRICCION Y
                if nodetype[lines[i][2]-1] == 13:
                    F[2*(lines[i][2]-1)] += thickness*forces[lines[i][0]]
                if nodetype[lines[i][3]-1] == 13:
                    F[2*(lines[i][3]-1)] += thickness*forces[lines[i][0]]
                # 14 - FUERZA X NEGATIVA + RESTRICCION Y
                if nodetype[lines[i][2]-1] == 14:
                    F[2*(lines[i][2]-1)] -= thickness*forces[lines[i][0]]
                if nodetype[lines[i][3]-1] == 14:
                    F[2*(lines[i][3]-1)] -= thickness*forces[lines[i][0]]
                # 9 - FUERZAS Y POSITIVAS + RESTRICCION X
                if nodetype[lines[i][2]-1] == 15:
                    F[(2*(lines[i][2]-1))+1] += longit*thickness*forces[lines[i][0]]
                if nodetype[lines[i][3]-1] == 15:
                    F[(2*(lines[i][3]-1))+1] += thickness*forces[lines[i][0]]
                # 10 - FUERZAS Y NEGATIVAS + RESTRICCION X
                if nodetype[lines[i][2]-1] == 16:
                    F[(2*(lines[i][2]-1))+1] -= thickness*forces[lines[i][0]]
                if nodetype[lines[i][3]-1] == 16:
                    F[(2*(lines[i][3]-1))+1] -= thickness*forces[lines[i][0]]

        if dof_per_node == 1:
            F = F[0::2]

        return F

