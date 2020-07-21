# Elementos Finitos

Este programa resuelve un mesh utilizando metodos de elementos finitos. La aplicacion es compatible con Linux y Windows. Necesita tener instalado Python 3.8.

## Instalación
Clonar el repositorio con el comando:
```
$ git clone https://github.com/rodrigolx31/finel3d.git
```
Es recomendable utilizar un entorno virtual de Python, que puede ser creado con:
```
python3 -m venv /path/to/new/virtual/environment
```
Y, posteriormente activado con:
```
source /path/to/new/virtual/environment/bin/activate
```
Instalar los requisitos:
```
$ pip install -r requirements.txt
```
Con esto deberia estar instalado y lilsto para usar.

## Utilización

* Se debe utilizar un mesheado en formato .msh (version 2 de Gmsh). Debe estar en: /mesh. 
* Con el parametro `-f` se resuelve el mallado.
* Con el parametro `-v` se visualiza.(actualmente no funciona)
* Con el parametro `-g` se abre el mesheado en Gmsh
* Con el parametro `-c` se limpia el archivo generado.

La herramienta para seleccionar las condiciones de contorno debe ser utilizada definiendo Physical Groups (PG) en Gmsh. (con numeros del 1 al 9).
Los comandos a ser utilizados deberian aparecer en pantalla. (Se debe escribir el comando + espacio + el PG a aplicar)
Ej:
```
r 2
```
Restringe todos los grados de libertad de PG que tenga el numero 2.
luego, continuar con c.

Comandos:
* x/y: Fuerzas positivas y negativas en los ejes X e Y respectivamente. (x- fuerza negativa).
* r: Empotramiento.
* e: vinculo en un solo eje (No implementado)
* v/b: combinacion de fuerzas y vinculos (No implementado)
* c: continuar
## Ejemplo
```
$ python finel.py -f mesh1.msh
```
