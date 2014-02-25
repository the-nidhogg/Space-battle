

															+-------------------+
															|	space battle	|
															+-------------------+



Pour faire fonctionner spacebattle, vous avez besoin d'installer python 2.x ainsi que de pygame.
Sous linux, il pourait malgrè tout fonctionner seul, en lançant le fichier play, qui est au format elf.


installations de python et pygame:

	sous windows:
		python:
			http://python.org/download/
			prenez une version 2.x.x, mais pas 3.x.x

		pygame:
			http://pygame.org/download.shtml

			prenez par exemple:
				pygame-1.9.1.win32-py2.7.msi
				ou
				pygame-1.9.2a0.win32-py2.7.msi

			ne prenez pas:
				pygame-1.9.1.win32-py3.1.msi
				ou
				pygame-1.9.2a0.win32-py3.2.msi
				qui sont fait pour python 3.x

	sous linux en console:
		sudo apt-get install python
		sudo apt-get install python-pygame
		
	pour mac, voir sur les sites
			http://python.org/download/			pour python
			http://pygame.org/download.shtml	pour pygame


Si votre rélolution est supèrieur à celle indiquée dans le fichier 'resolution.txt', vous pouvez mettre la votre.
En cas de problème, remettre la résolution sur 1366x768
Attention à respecter le format d'écriture: LARGEURxHAUTEUR
Si la résolution de base est trop grande (plantage), vous pouvez mettre votre résolution la plus grande, mais si elle n'est pas
proche de celle de base, la qualité de jeu sera amoindrie...

controls:

	hors combat
		echap :		la plupart du temps, pour revenir en arrière, ou passer les dialogues
		entrée :	confirmer (oui, ou ok...)
		tabs :		changer de champ pour l'écriture des noms lors d'une nouvelle campaigne

	en combat
		espace:		pause
		touches directionnells:	avancer; tourner
		0:			tir automatique avec l'arme selectionnée
		1:			tir manuel
		2:			Missile tête chercheuse (si possédé)
		m:			mute = active/desactive la musique
		s:			change d'arme (entre les armes équipées)
		maj:		activer bouclier
		ctrl:		tir d'énergie

