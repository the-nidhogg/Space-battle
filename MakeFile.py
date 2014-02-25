#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import system,getcwd,chdir
while 1:
	nom=raw_input("chemin du programme compiler (sans l'extension): ")
	if nom[:2]=="cd":
		chdir(getcwd()+"/"+nom[3:])
		continue
	system("cython --embed {}.py -o {}.c".format(nom,nom))
	system("gcc {}.c -o {} $(pkg-config python --cflags) -lpython2.7".format(nom,nom))
