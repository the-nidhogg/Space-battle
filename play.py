#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from pygame import *
from pygame.font import *
from pygame.locals import *
from os import listdir,getcwd,system
from time import time,sleep
from math import fabs,atan,degrees
from random import randrange,choice 

#system("xrandr  | grep \* | cut -d' ' -f4>resolution.txt")
RESOLUTION=tuple([int(x)for x in(open("resolution.txt","r").read()[:-1].split("x"))])
RESOLUTION=(RESOLUTION[0],RESOLUTION[1])#[0]-100
init()
display.init()

class Fenetre(object):

	def __init__(self,x,y,number,full=FULLSCREEN):
		self.fenetre=display.set_mode((x,y),full) # FULLSCREEN=-2147483648
		mouse.set_visible(1)
		self.x,self.y=x,y
		self.number=number
		self.full=1
		self.select=""
		self.levelCampaign=1
		self.structure=[]
		self.mouseover=0
		self.new=None

	def etape(self,number):
		if number==1:				# ecran titre
			degres=90
			pos=(168,310)
			number=randrange(21)
			ennemi=[[216,randrange(21),[600,380]],
					[288,randrange(21),[550,405]],
					[360,randrange(21),[650,405]],
					[72,randrange(21),[566,430]],
					[144,randrange(21),[633,430]]]
			ball=[]
			explo=[]
			# degres; no; pos

			def aff(ball,explo):				#1152/665
				ecranTitre=[[decors["ecranTitre"],(RESOLUTION[0]/2-300,RESOLUTION[1]/20)]]+\
				[[font.Font(None,36).render(X,1,(255,255,255)),(RESOLUTION[0]/2+100,RESOLUTION[1]*(0.5+0.1425*(Y))-20)]for X,Y in [["PLAY",0],["NEW CAMPAIGN",1],["LOAD",2],["EXIT",3]]]
				self.fenetre.fill(0)
				self.fenetre.blit(decors["map4"],(0,0))
				self.fenetre.blit(sprites["vaisseau%i"%(number)],(RESOLUTION[0]/2+30,RESOLUTION[1]*(0.5+0.1425*(self.select-2))-20))
				if ball:
					destruct=[]
					for i in ball:
						try:self.fenetre.blit(ballPerso[i[1]][i[2]],tuple(i[0]))
						except:pass
						i[0]=(i[0][0]+5*i[3][0],i[0][1]+5*i[3][1])
						if i[0][0]>RESOLUTION[0] or i[0][0]<0 or i[0][1]>RESOLUTION[1] or i[0][1]<0:
							destruct.append(i)
						if collision(i[0],(RESOLUTION[0]/2+30,RESOLUTION[0]/2+30+34),(RESOLUTION[1]*(0.5+0.1425*(self.select-2))-20,RESOLUTION[1]*(0.5+0.1425*(self.select-2))-20+49)):
							destruct.append(i)
							explo=[0,i[0]]
					for i in destruct:ball.remove(i)
				if explo:
					if explo[0]>=10:self.fenetre.blit(sprites["expl%i"%(explo[0])],tuple(explo[1]))
					else:self.fenetre.blit(sprites["expl0%i"%(explo[0])],tuple(explo[1]))
					explo[0]+=1
					if explo[0]==11:explo=[]
				[self.fenetre.blit(x[0],x[1])for x in ecranTitre]
				return ball,explo

			def moteur(degres,pos,ball):
				degres+=0.5
				if degres>=360:degres-=360
				angle=convertAngle(degres)
				pos=(pos[0]+2*angle[0],pos[1]+2*angle[1])
				if not bool(randrange(100)) and not len(ball)>2:
					angle=int(fabs(degrees(atan((RESOLUTION[1]*(0.5+0.1425*(self.select-2))-20+32-pos[1])/(pos[0]-(RESOLUTION[0]/2+30+16)*1.0)))))
					if pos[0]>RESOLUTION[0]/2+30:angle=modifAngle(angle,270)
					if pos[1]<RESOLUTION[1]*(0.5+0.1425*(self.select-2))-20:angle=modifAngle(angle,180)
					angle2=angle-90
					if angle2<0:angle+=360
					converti=convertAngle(angle)
					ball.append([pos,choice([x+str(y)for x in ["five shot class ","shotGun class "]for y in [1,2,3]]),angle2,converti])
				return degres,pos,ball

			def affMoteur(vaisseau):
				angle=int(fabs(degrees(atan((RESOLUTION[1]*(0.5+0.1425*(self.select-2))-20+32-vaisseau[2][1])/(vaisseau[2][0]-(RESOLUTION[0]/2+30+16)*1.0)))))
				if vaisseau[2][0]>RESOLUTION[0]/2+30:angle=modifAngle(angle,270)
				if vaisseau[2][1]<RESOLUTION[1]*(0.5+0.1425*(self.select-2))-20:angle=modifAngle(angle,180)
				angle-=90
				if angle<0:angle+=360
				self.fenetre.blit(vaisseaux[vaisseau[1]][angle],tuple(vaisseau[2]))

			self.fenetre.fill(1)
			self.select=2		#selectable=["play","newCampaign","load","quit"]
			while 1:
				sleep(0.006125)
				ball,explo=aff(ball,explo)
				for i in ennemi:
					i[0],i[2],ball=moteur(i[0],i[2],ball)
					affMoteur(i)
				display.flip()
				for i in event.get():
					if i.type==QUIT:
						quit()
						exit()
						return
					elif i.type==MOUSEBUTTONDOWN:
						if collision(i.pos,(0,RESOLUTION[0]),(RESOLUTION[1]*(0.5+0.1425*-0.5),RESOLUTION[1]*(0.5+0.1425*0.5))):self.number=2;return
						elif collision(i.pos,(0,RESOLUTION[0]),(RESOLUTION[1]*(0.5+0.1425*0.5),RESOLUTION[1]*(0.5+0.1425*1.5))):
							self.number=3
							self.newCampaign()
							return
						elif collision(i.pos,(0,RESOLUTION[0]),(RESOLUTION[1]*(0.5+0.1425*1.5),RESOLUTION[1]*(0.5+0.1425*2.5))):self.number=4;return
						elif collision(i.pos,(0,RESOLUTION[0]),(RESOLUTION[1]*(0.5+0.1425*2.5),RESOLUTION[1]*(0.5+0.1425*3.5))):self.number=5;return
					elif i.type==KEYDOWN:
						if i.key==K_UP:	#kup
							if self.select>2:self.select-=1
						elif i.key==K_DOWN:	# kdown
							if self.select<5:self.select+=1
						elif i.key==K_RETURN:
							self.number,self.select=self.select,0
							if self.number==3:
								self.newCampaign()
							return
						elif i.key==K_ESCAPE:
							if self.full:
								self.full=0
								globals()["RESOLUTION"]=(RESOLUTION[0]-100,RESOLUTION[1]-100)
								self.fenetre=display.set_mode((RESOLUTION[0],RESOLUTION[1]))
							else:
								self.full=1
								globals()["RESOLUTION"]=(RESOLUTION[0]+100,RESOLUTION[1]+100)
								self.fenetre=display.set_mode((RESOLUTION[0],RESOLUTION[1]),FULLSCREEN)

		elif number==2:				# play
			if "vaisseau" not in globals():
				self.popUp("Chargez un fichier","ok")
				self.number=1
				return
			else:
				self.number=3
				return
				#self.demo()

		elif number==3:				#campaign
			self.levelCampaign=vaisseau.stade
			listPos=[[(65,290),(240,385)],[(260,465),(350,545)],[(450,430),(575,575)],[(564,225),(720,365)],[(770,370),(830,430)],[(945,415),(1070,600)],[(1085,160),(1295,366)]]
			degres=90
			pos=(168,310)#mil[0]+milvaisseau[0]...[1].+.[1]
			self.fenetre.fill(0)
			self.fenetre.blit(decors["map4"],(0,0))
			self.fenetre.blit(decors["map2"],(0,0))
			display.flip()
			def affich(self,degres,pos):
				self.fenetre.fill(0)
				self.fenetre.blit(decors["map4"],(0,0))
				self.fenetre.blit(decors["map2"],(0,0))
				for i in range(7):
					if self.levelCampaign<i+1:
						self.fenetre.blit(decors["lock"],((listPos[i][0][0]+listPos[i][1][0])/2.0-150,(listPos[i][0][1]+listPos[i][1][1])/2.0-150))
				center=vaisseaux[0][90].get_rect().move(pos[0],pos[1]).center
				degres-=90
				if degres<0:degres+=360
				self.fenetre.blit(vaisseaux[vaisseau.noShip][degres],vaisseaux[vaisseau.noShip][degres].get_rect(center=vaisseaux[vaisseau.noShip][90].get_rect().move(pos[0],pos[1]).center))
				degres+=90
				if self.mouseover:
					pos=listPos[self.select-1][0]
					#self.fenetre.subsurface(pos[0]-50,pos[1]-50,200,200).fill((0,0,0,50),special_flags=BLEND_RGBA_MULT)#BLEND_RGBA_ADD)
					self.fenetre.blit(font.Font(None,36).render("play",1,(255,255,255)),(pos[0]+10,pos[1]+10))
					self.fenetre.blit(font.Font(None,36).render("save",1,(255,255,255)),(pos[0]+10,pos[1]+42))
					self.fenetre.blit(font.Font(None,36).render("shop",1,(255,255,255)),(pos[0]+156,pos[1]+10))
					self.fenetre.blit(font.Font(None,36).render("equip.",1,(255,255,255)),(pos[0]+156,pos[1]+42))
					self.fenetre.blit(font.Font(None,36).render("caract.",1,(255,255,255)),(pos[0]+10,pos[1]+74))
					self.fenetre.blit(font.Font(None,36).render("ch. ship",1,(255,255,255)),(pos[0]+156,pos[1]+74))
				display.flip()#update((pos[0]-32,pos[0]+32,pos[1]-32,pos[1]+32))
			self.select=1			#selectable=number of galaxy
			while 1:
				sleep(0.0625)
				degres+=2
				if degres>=360:degres-=360
				angle=convertAngle(degres)
				pos=(pos[0]+2*angle[0],pos[1]+2*angle[1])
				affich(self,degres,pos)
				for i in event.get():
					if i.type==QUIT:exit()
					elif i.type==MOUSEBUTTONDOWN:
						for j,k in enumerate(listPos):
							if collision(i.pos,(k[0][0],k[1][0]),(k[0][1],k[1][1])):
								if self.levelCampaign>=j+1:
									self.select=j+1
									a=listPos[self.select-1]
									pos=((a[0][0]+a[1][0]+16)/2.0,(a[0][1]+a[1][1]-16)/2.0)
									degres=90
								break
						if self.mouseover:
							posx=listPos[self.select-1][0]
							if collision(i.pos,(posx[0]+10,posx[0]+96),(posx[1]+10,posx[1]+40)):
								if self.campagne(self.select) and self.select==self.levelCampaign:
									vaisseau.stade+=1		# renvoyer 1 pour avancer, 0 pour perdu
								self.levelCampaign=vaisseau.stade
							elif collision(i.pos,(posx[0]+10,posx[0]+96),(posx[1]+40,posx[1]+70)):

								if vaisseau.save()==1:#texte,filename(chemin),no
									self.fenetre.blit(font.Font(None,72).render("GAME SAVED",1,(255,255,255)),((RESOLUTION[0]-350)/2,(RESOLUTION[1]-32)/2))
									display.flip()
									sleep(3)
								else:
									self.fenetre.blit(font.Font(None,72).render("FAILED TO SAVE",1,(255,255,255)),((RESOLUTION[0]-350)/2,(RESOLUTION[1]-32)/2))
									display.flip()
									sleep(3)
								a=listPos[self.select-1]
								pos=((a[0][0]+a[1][0]+16)/2.0,(a[0][1]+a[1][1]-16)/2.0)
								degres=90
							elif collision(i.pos,(posx[0]+106,posx[0]+252),(posx[1]+10,posx[1]+40)):
								self.shop(self.select-1)
							elif collision(i.pos,(posx[0]+106,posx[0]+252),(posx[1]+40,posx[1]+70)):
								self.equiper()
							elif collision(i.pos,(posx[0]+10,posx[0]+96),(posx[1]+74,posx[1]+106)):
								self.caracteristique()
							elif collision(i.pos,(posx[0]+106,posx[0]+252),(posx[1]+74,posx[1]+106)):
								self.chShip()

					elif i.type==KEYDOWN:
						if i.key==K_UP:
							if self.select>1:
								self.select-=1
								a=listPos[self.select-1]
								pos=((a[0][0]+a[1][0]+16)/2.0,(a[0][1]+a[1][1]-16)/2.0)
								degres=90
						elif i.key==K_DOWN:
							if self.select<self.levelCampaign:
								self.select+=1
								a=listPos[self.select-1]
								pos=((a[0][0]+a[1][0]+16)/2.0,(a[0][1]+a[1][1]-16)/2.0)
								degres=90
						elif i.key==K_RETURN:
							if self.campagne(self.select) and self.select==self.levelCampaign:vaisseau.stade+=1		# renvoyer 1 pour avancer, 0 pour perdu
							self.levelCampaign=vaisseau.stade
						elif i.key==K_ESCAPE:
							self.number=1
							return
					elif i.type==MOUSEMOTION:
						self.mouseover=0
						for j,k in enumerate(listPos):
							if collision(i.pos,(k[0][0]-50,k[1][0]+150),(k[0][1]-50,k[1][1]+50)):
								if j+1==self.select:
									self.mouseover=1

		elif number==4:		# load
			self.number,nom=3,""
			listeNoms=listdir(getcwd()+"/save")
			listePos=[]
			def aff():
				self.fenetre.fill(0)
				self.fenetre.blit(decors["map4"],(0,0))
				if listeNoms==[]:
					self.fenetre.blit(font.Font(None,36).render("Veuillez cliquer sur 'NEW CAMPAIGN'",1,(255,255,255)),(RESOLUTION[0]/2-230,RESOLUTION[1]/2))
					self.fenetre.blit(font.Font(None,36).render("a l'ecran titre",1,(255,255,255)),(RESOLUTION[0]/2-130,RESOLUTION[1]/2+50))
					self.fenetre.blit(font.Font(None,36).render("retour = echap",1,(255,255,255)),(RESOLUTION[0]/2-130,RESOLUTION[1]/2+100))
				else:
					self.fenetre.blit(font.Font(None,36).render("Cliquez sur le fichier a charger",1,(255,255,255)),(RESOLUTION[0]/2-430,RESOLUTION[1]/2))
					self.fenetre.blit(font.Font(None,36).render("retour = echap",1,(255,255,255)),(RESOLUTION[0]/2-330,RESOLUTION[1]/2+100))
					a,b=0,0
					for i in listeNoms:
						self.fenetre.blit(font.Font(None,36).render(i[:10].replace(".save",""),1,(255,255,255)),(RESOLUTION[0]/2+b,RESOLUTION[1]/2+32*a))
						listePos.append([i,(RESOLUTION[0]/2+b,RESOLUTION[1]/2+32*a),(RESOLUTION[0]/2+b+140,RESOLUTION[1]/2+32*a+32)])
						a+=1
						if RESOLUTION[1]/2+32*a>=RESOLUTION[1]-100:
							a=0
							b+=140

					if nom!="":
						self.fenetre.blit(font.Font(None,36).render("charger "+nom.replace(".save",""),1,(255,255,255)),(RESOLUTION[0]/2-330,RESOLUTION[1]/2+300))
				display.flip()
			nameLoad=0
			aff()
			while not nameLoad:
				sleep(0.125)
				for i in event.get():
					if i.type==QUIT:quit();exit()
					elif i.type==MOUSEBUTTONDOWN:
						if collision(i.pos,(RESOLUTION[0]/2-330,RESOLUTION[1]/2+300),(RESOLUTION[0]/2-180,RESOLUTION[1]/2+332))and nom!="":
							nameLoad=1
							break
						for j in listePos:
							if collision(i.pos,[j[1][0],j[2][0]],[j[1][1],j[2][1]]):
								nom=j[0]
								aff()
								break
					elif i.type==KEYDOWN:
						if i.key==K_ESCAPE:
							self.number=1
							return
						elif i.key==K_RETURN and nom!="":
							nameLoad=1
							break
			globals()["vaisseau"]=Vaisseau("nonCharge","nonCharge","0",[1,nom])
			self.new=0
			return

		elif number==5:exit()# exit

	def newCampaign(self):
		self.number=3
		tiret,self.select,noShip,errors=[time(),0],"nom",0,[]
		nom,shipname="",""
		def affich(noShip,select,tiret,nom,shipname,errors=[]):
			self.fenetre.fill(0)
			self.fenetre.blit(decors["map4"],(0,0))
			self.fenetre.blit(decors["map2"],(0,0))
			if self.select=="nom":var=0
			elif self.select=="shipname":var=1
			elif self.select=="noShip":var=2
			else:var=3
			self.fenetre.blit(font.Font(None,36).render(nom+"".join(["_"for i in "0" if tiret and not var]),1,(255,255,255)),(RESOLUTION[0]/2,RESOLUTION[1]*(0.5)))
			self.fenetre.blit(font.Font(None,36).render(shipname+"".join(["_"for i in "0" if tiret and var==1]),1,(255,255,255)),(RESOLUTION[0]/2+196,RESOLUTION[1]*(0.5+0.1425)))
			newCampaign=[[font.Font(None,36).render(X,1,(255,255,255)),(RESOLUTION[0]/2-64,RESOLUTION[1]*(0.5+0.1425*Y))]for X,Y in [["NOM: ",0],["NOM DU VAISSEAU: ",1],["CHOIX DU VAISSEAU:",2],["VALIDER",3]]]
			[self.fenetre.blit(x[0],x[1])for x in newCampaign]
			self.fenetre.blit(sprites["vaisseau"+str(noShip)],(RESOLUTION[0]/2-98,RESOLUTION[1]*(0.5+0.1425*var)-16))
			display.flip()
		while 1:
			sleep(0.125)
			affich(noShip,self.select,tiret[1],nom,shipname,errors)
			if time()-tiret[0]>=0.5:tiret=[time(),not bool(tiret[1])]
			for i in event.get():
				if i.type==QUIT:
					self.number=1
					return 1
				elif i.type==MOUSEBUTTONDOWN:
					if collision(i.pos,(0,RESOLUTION[0]),(RESOLUTION[1]*(0.5+0.1425*0),RESOLUTION[1]*(0.5+0.1425))):self.select="nom"
					elif collision(i.pos,(0,RESOLUTION[0]),(RESOLUTION[1]*(0.5+0.1425*1),RESOLUTION[1]*(0.5+0.1425*2))):self.select="shipname"
					elif collision(i.pos,(0,RESOLUTION[0]),(RESOLUTION[1]*(0.5+0.1425*2),RESOLUTION[1]*(0.5+0.1425*3))):self.select="noShip"
					elif collision(i.pos,(0,RESOLUTION[0]),(RESOLUTION[1]*(0.5+0.1425*3),RESOLUTION[1]*(0.5+0.1425*4))):
						var=self.createNewProfile(nom,shipname,noShip)
						if var[0]:
							self.new=1
							return 0
				elif i.type==KEYDOWN:
					if i.key in range(48,58)+range(65,91)+range(97,123):
						if self.select=="nom":nom+=chr(i.key)
						elif self.select=="shipname":shipname+=chr(i.key)
					elif i.key==K_BACKSPACE:
						if self.select=="nom":nom=nom[:-1]
						elif self.select=="shipname":shipname=shipname[:-1]
					elif i.key==K_ESCAPE:
						self.number=1
						return 1
					elif i.key==K_TAB:
						self.select=['nom', 'shipname', 'noShip', 'valid'][{"nom":1,"shipname":2,"noShip":3,"valid":0}[self.select]]
					elif i.key==K_LEFT or i.key==K_RIGHT and self.select=="noShip":
						noShip+=1
						if noShip>=3:noShip=0
					elif i.key==K_RETURN and self.select=="valid" and nom!="" and shipname!="":
						var=self.createNewProfile(nom,shipname,noShip)
						if var[0]:
							self.new=1
							return 0
		return 0

	def createNewProfile(self,nom,nom2,no):
		"""renvoie une liste:
			[0] bon/pas bon
			[1] type d'erreur"""
		if nom+".save"in listdir(getcwd()+"/save"):return [0,0]
		globals()["vaisseau"]=Vaisseau(nom,nom2,no,[0,nom+".save"])
		self.levelCampaign=1
		return [1]

	def campagne(self,number):
		# renvoyer 1 pour avancer, 0 pour perdu
		globals()["campaign"]=Campaign(number,self.fenetre,self.new)
		return campaign.play()

	def shop(self,level):
		listeElements=[{3000:["arme",["shotGun class 1",3,0.333,8,0,[1.1,1.1,-3,0,0],0,0]],
						5500:["arme",["five shot class 1",2,0.5,8,0,[1.1,1,0,0.5,0],0,1]],
						5000:["amelioration","temps bouclier +3 secondes",[0,3],0],
						7500:["amelioration","intervale bouclier -5 secondes",[3,5],0],
						12500:["amelioration","furtivite +5 sencondes",[1,5],0],
						15000:["amelioration","blindage +0.5 points",[2,0.5],0]
						},
						{7000:["arme",["shotGun class 2",5,0.333,8,0,[1.1,1.1,-3,0,0],1,0]],
						15500:["arme",["five shot class 2",3,0.5,8,0,[1.1,1,0,1,0],1,1]],
						15000:["amelioration","temps bouclier +3 secondes",[0,3],1],
						17500:["amelioration","intervale bouclier -5 secondes",[3,5],1],
						25000:["amelioration","furtivite +5 sencondes",[1,5],1],
						30000:["amelioration","blindage +0.5 points",[2,0.5],1]
						},
						{15000:["arme",["shotGun class 3",7,0.333,8,0,[1.1,1.1,-3,0,0],2,0]],
						25500:["arme",["five shot class 3",5,0.5,8,0,[1.1,1,0,1.5,0],2,1]],
						20000:["amelioration","temps bouclier +3 secondes",[0,3],2],
						25000:["amelioration","intervale bouclier -4 secondes",[3,4],2],
						35000:["amelioration","furtivite +4 sencondes",[1,4],2],
						50000:["amelioration","blindage +0.25 points",[2,0.25],2]
						},
						
						{15000:["arme",["shotGun class 4",9,0.333,8,0,[1.1,1.1,-4,0,0],3,0]],
						25500:["arme",["five shot class 4",7,0.5,8,0,[1.1,1,0,2,0],3,1]],
						26500:["arme",["three shot 1",7,0.5,8,0,[1.1,1,0,2,0],3,1]],
						20000:["amelioration","temps bouclier +2 secondes",[0,2],3],
						25000:["amelioration","intervale bouclier -2 secondes",[3,2],3],
						35000:["amelioration","furtivite +3 sencondes",[1,3],3],
						50000:["amelioration","blindage +0.25 points",[2,0.25],3]
						},
						{15000:["arme",["shotGun class 5",11,0.333,8,0,[1.1,1.1,-4,0,0],4,0]],
						25500:["arme",["five shot class 5",9,0.5,8,0,[1.1,1,0,2,0],4,1]],
						20000:["amelioration","temps bouclier +2 secondes",[0,2],4],
						25000:["amelioration","intervale bouclier -2 secondes",[3,2],4],
						35000:["amelioration","furtivite +3 sencondes",[1,3],4],
						50000:["amelioration","blindage +0.25 points",[2,0.25],4]
						},
						{15000:["arme",["shotGun class 3",7,0.333,8,0,[1.1,1.1,-3,0,0],2,0]],
						25500:["arme",["five shot class 3",5,0.5,8,0,[1.1,1,0,1.5,0],0,1]],
						20000:["amelioration","temps bouclier +3 secondes",[0,3],2],
						25000:["amelioration","intervale bouclier -5 secondes",[3,5],2],
						35000:["amelioration","furtivite +5 sencondes",[1,5],2],
						50000:["amelioration","blindage +0.5 points",[2,0.5],2]
						}]
		achatPotentiel={i:listeElements[level][i]for i in listeElements[level]if listeElements[level][i]not in vaisseau.achats}
		choix="arme"
		select=""
		achat=1
		vente=0
		#~ self.gun	= [0]=nom; [1]=degats; [2]=cadence; [3]=vitesse; [4]=lastTir;[5]=liste;[6]=number galaxy; [7]=shot style
		#~  gun=[["primair",1,0.25,5,time(),[None],0],["secondair",2,1,7,time(),[None],0]]
		#~ self.coefVitesse=self.gun[self.activate][5][0]	*coef
		#~ self.coefEnergie=self.gun[self.activate][5][1]	*coef
		#~ self.coefTempsBouclier=self.gun[self.activate][5][2]	+temps en sec
		#~ self.coefDefense=self.gun[self.activate][5][3]	-degats
		#~ self.coefFurtivite=self.gun[self.activate][5][4]	+temps en sec
		def afficher():
			selectable=[]
			self.fenetre.fill(0)
			self.fenetre.blit(decors["map4"],(0,0))
			self.fenetre.blit(decors["map2"],(0,0))
			for i in range(0,RESOLUTION[0]/500+1):
				for j in range(0,RESOLUTION[1]/500+1):
					self.fenetre.blit(decors["filtreNoir"],(i*500,j*500))
			try:
				self.fenetre.subsurface(100,100,RESOLUTION[0]-200,5).fill((255,255,255))
				self.fenetre.subsurface(100,100,5,RESOLUTION[1]-200).fill((255,255,255))
				self.fenetre.subsurface(100,RESOLUTION[1]-100,RESOLUTION[0]-200,5).fill((255,255,255))
				self.fenetre.subsurface(RESOLUTION[0]-100,100,5,RESOLUTION[1]-195).fill((255,255,255))
				self.fenetre.subsurface(350,100,5,RESOLUTION[1]-200).fill((255,255,255))
			except:pass
			if choix=="amelioration":
				try:
					self.fenetre.subsurface(550,120,200,5).fill((255,255,255))
					self.fenetre.subsurface(550,120,5,50).fill((255,255,255))
					self.fenetre.subsurface(550,170,200,5).fill((255,255,255))
					self.fenetre.subsurface(750,120,5,55).fill((255,255,255))
				except:pass
			if choix=="arme":
				try:
					self.fenetre.subsurface(775,120,200,5).fill((255,255,255))
					self.fenetre.subsurface(775,120,5,50).fill((255,255,255))
					self.fenetre.subsurface(775,170,200,5).fill((255,255,255))
					self.fenetre.subsurface(975,120,5,55).fill((255,255,255))
				except:pass
			self.fenetre.blit(font.Font(None,36).render("Bienvenue Au Magasin Intergalactique!",1,(255,255,255)),((RESOLUTION[0]-500)/2.0,33))
			self.fenetre.blit(font.Font(None,36).render("Welcome To the Intergalactic Shop!",1,(255,255,255)),((RESOLUTION[0]-500)/2.0,66))
			self.fenetre.blit(font.Font(None,36).render("Echangez-nous de l'energie contre des objets!",1,(255,255,255)),(100,RESOLUTION[1]-66))
			self.fenetre.blit(font.Font(None,36).render("Vous possedez {} MegaWatt".format(vaisseau.money),1,(255,255,255)),(900,RESOLUTION[1]-66))
			self.fenetre.blit(font.Font(None,36).render("Acheter/Buy",1,(255,255,255)),(150,200))
			self.fenetre.blit(font.Font(None,36).render("Vendre/Sell",1,(255,255,255)),(150,250))
			self.fenetre.blit(font.Font(None,36).render("Quitter/Exit",1,(255,255,255)),(150,RESOLUTION[1]-200))
			self.fenetre.blit(font.Font(None,36).render("Ameliorations",1,(255,255,255)),(575,133))
			self.fenetre.blit(font.Font(None,36).render("Armes",1,(255,255,255)),(850,133))
			a=0
			if achat:
				for i in achatPotentiel:
					if achatPotentiel[i][0]==choix and choix=="amelioration":
						selectable.append([[400,1000],[200+a,200+a+24],i])
						self.fenetre.blit(font.Font(None,36).render(achatPotentiel[i][1],1,(255,255,255)),(400,200+a))
						self.fenetre.blit(font.Font(None,36).render(str(i)+" MW",1,(255,255,255)),(950,200+a))
						a+=24

					elif achatPotentiel[i][0]==choix and choix=="arme":
						selectable.append([[400,1000],[200+a,200+a+24],i])
						self.fenetre.blit(font.Font(None,36).render(achatPotentiel[i][1][0],1,(255,255,255)),(400,200+a))
						self.fenetre.blit(font.Font(None,36).render(str(i)+" MW",1,(255,255,255)),(950,200+a))
						self.fenetre.blit(font.Font(None,36).render("degats:{}   cadence:{}   vitesse:{}".format(achatPotentiel[i][1][1],achatPotentiel[i][1][2],achatPotentiel[i][1][3]),1,(255,255,255)),(450,200+a+24))
						self.fenetre.blit(font.Font(None,36).render("Vitesse:+{}%    Energie +{}%    temps Bouclier:{}s".format(
						(achatPotentiel[i][1][5][0]-1)*100,(achatPotentiel[i][1][5][1]-1)*100,achatPotentiel[i][1][5][2]),1,(255,255,255)),(450,200+a+48))
						self.fenetre.blit(font.Font(None,36).render("defense:+{} points   furtivite: +{} s".format(achatPotentiel[i][1][5][3],achatPotentiel[i][1][5][4]),1,(255,255,255)),(450,200+a+72))
						a+=96

			if select!="":
				self.fenetre.blit(decors["filtreRouge"],(selectable[select[0]][0][0],selectable[select[0]][1][0]))
				self.fenetre.blit(font.Font(None,36).render("Acheter",1,(255,255,255)),(950,600))
			display.flip()
			return selectable
		selectable=afficher()
		while 1:
			sleep(0.125)
			for i in event.get():
				if i.type==KEYDOWN:
					if i.key==K_ESCAPE:
						return
					elif i.key==K_RETURN and select!="":
						if choix=="arme":
							texte=objet[1][0]
						else:
							texte=objet[1]
						if self.popUp("Voulez-vous acheter\n{}\npour {}kW?".format(texte,select[1]),"oui","non"):
							if vaisseau.money>=select[1]:
								vaisseau.money-=select[1]
								vaisseau.achat(achatPotentiel[select[1]])
								del achatPotentiel[select[1]]
							else:
								self.popUp("Vous n'avez pas assez d'argent\nil vous manque %i kW"%(select[1]-vaisseau.money),"ok","")
								selectable=afficher()
							select=""
						selectable=afficher()
				elif i.type==MOUSEBUTTONDOWN:
					if collision(i.pos,(550,750),(120,170)):
						choix="amelioration"
						select=""
						selectable=afficher()
					elif collision(i.pos,(775,975),(120,170)):
						choix="arme"
						select=""
						selectable=afficher()
					elif collision(i.pos,(150,150+12*16),(RESOLUTION[1]-200,RESOLUTION[1]-150)):
						return
					elif collision(i.pos,(950,1000),(600,624))and select!="":
						if choix=="arme":
							texte=objet[1][0]
						else:
							texte=objet[1]
						if self.popUp("Voulez-vous acheter\n{}\npour {}kW?".format(texte,select[1]),"oui","non"):
							if vaisseau.money>=select[1]:
								vaisseau.money-=select[1]
								vaisseau.achat(achatPotentiel[select[1]])
								del achatPotentiel[select[1]]
							else:
								self.popUp("Vous n'avez pas assez d'argent\nil vous manque %i kW"%(select[1]-vaisseau.money),"ok","")
								selectable=afficher()
							select=""
						selectable=afficher()
					else:
						for k,j in enumerate(selectable):
							if collision(i.pos,j[0],j[1]):
								select=[k,j[2]]
								selectable=afficher()
								objet=achatPotentiel[select[1]]
								break

	def caracteristique(self):
		self.fenetre.blit(decors["map4"],(0,0,))
		cadre(self.fenetre,0,(100,100),(RESOLUTION[0]-100,RESOLUTION[1]-100))
		a,b,c=0,0,0
		for i in vaisseau.__dict__:
			if i in["balls","explo0","explo1","ballsSpe","achats","gun","equipes","shottedShip"]:continue
			chaine=str(i)+" = "+str(vaisseau.__dict__[i])
			if len(chaine)>=60:
				self.fenetre.blit(font.Font(None,24).render(chaine[:60],1,(255,255,255)),(110+b,110+a))
				a+=36
				self.fenetre.blit(font.Font(None,24).render(" "*5+chaine[60:],1,(255,255,255)),(110+b,110+a))
				if len(chaine[60:])>c:
					c=len(chaine[60:])
				if len(chaine[:60])>c:
					c=len(chaine[:60])
			else:
				self.fenetre.blit(font.Font(None,24).render(chaine,1,(255,255,255)),(110+b,110+a))
				if len(chaine)>c:
					c=len(chaine)
			a+=36
			if a>=RESOLUTION[1]-250:
				a=0
				b+=c*8
				c=0

		self.fenetre.blit(font.Font(None,36).render("ok",1,(255,255,255)),((RESOLUTION[0]-64)/2.0,(RESOLUTION[1]-100)))
		display.flip()
		while 1:
			sleep(0.125)
			for i in event.get():
				if i.type==KEYDOWN:
					if i.key==K_ESCAPE:
						return
				elif i.type==MOUSEBUTTONDOWN:
					if collision(i.pos,((RESOLUTION[0]-64)/2.0,(RESOLUTION[0]-64)/2.0+100),(RESOLUTION[1]-125,RESOLUTION[1]-25)):
						return

	def chShip(self):
		#cadre(fenetre,transparence,haut,bas,largeur=5,couleur=(255,255,255),bg=(0,0,0)):
		mouseOver=0
		selected=vaisseau.noShip
		from ressources.vaisseaux.caraVaisseaux import cara
		aviable=[]
		a=100
		b=0
		for i in cara:
			if vaisseau.shottedShip["vaisseau"+str(i)]>=cara[i][4]:
				aviable.append([((RESOLUTION[0]/3.0)*2-250+b,200+a),cara[i]])
				a+=48
				if a+200>=RESOLUTION[1]-148:
					b+=225
					a=100
		def afficher():
			self.fenetre.blit(decors["map4"],(0,0))
			cadre(self.fenetre,1,(100,100),(RESOLUTION[0]-100,RESOLUTION[1]-100))
			cadre(self.fenetre,1,(RESOLUTION[0]/3-100,150),(RESOLUTION[0]/3+100,200))
			cadre(self.fenetre,1,((RESOLUTION[0]/3.0)*2-100,150),((RESOLUTION[0]/3.0)*2+100,200))
			self.fenetre.blit(font.Font(None,32).render("equipe",1,(255,255,255)),(RESOLUTION[0]/3.0-50,165))
			self.fenetre.blit(font.Font(None,32).render("reserve",1,(255,255,255)),((RESOLUTION[0]/3.0)*2-50,165))
			overed=0
			a=100
			b=0
			for i in aviable:
				if mouseOver==i[1][5]:
					overed=1
					self.fenetre.blit(sprites["vaisseau"+str(i[1][5])],((RESOLUTION[0]/3.0)*2-150+b,175+a))
					self.fenetre.blit(font.Font(None,32).render("number {} ".format(i[1][5]),1,(255,0,0)),((RESOLUTION[0]/3.0)*2-250+b,200+a))
					self.fenetre.blit(font.Font(None,32).render("vie: {} ;vitesse: {} ".format(cara[mouseOver][0],
					cara[mouseOver][1]),1,(255,0,0)),((RESOLUTION[0]/3.0)*2-250+b,248+a))
					self.fenetre.blit(font.Font(None,32).render("blindage: {} ;shield: {}".format(cara[mouseOver][2],
					cara[mouseOver][3]),1,(255,0,0)),((RESOLUTION[0]/3.0)*2-250+b,296+a))
					a+=144
				else:
					self.fenetre.blit(sprites["vaisseau"+str(i[1][5])],((RESOLUTION[0]/3.0)*2-150+b,175+a))
					self.fenetre.blit(font.Font(None,32).render("number {} ".format(i[1][5]),1,(255,255,255)),((RESOLUTION[0]/3.0)*2-250+b,200+a))
					a+=48

				if a+200>=RESOLUTION[1]-148:
					b+=225
					a=100

			self.fenetre.blit(font.Font(None,32).render("number {} ".format(selected),1,(0,255,0)),(400,300))
			self.fenetre.blit(font.Font(None,32).render("vie {} ".format(cara[selected][0]),1,(0,255,0)),(400,348))
			self.fenetre.blit(font.Font(None,32).render("vitesse {} ".format(cara[selected][1]),1,(0,255,0)),(400,396))
			self.fenetre.blit(font.Font(None,32).render("blindage {} ".format(cara[selected][2]),1,(0,255,0)),(400,444))
			self.fenetre.blit(font.Font(None,32).render("temp shield {} ".format(cara[selected][3]),1,(0,255,0)),(400,486))
			self.fenetre.blit(font.Font(None,32).render("OK".format(cara[selected][3]),1,(255,255,255)),(RESOLUTION[0]/2.0-24,RESOLUTION[1]-100))
			display.flip()
		while 1:
			sleep(0.125)
			afficher()
			for i in event.get():
				if i.type==KEYDOWN:
					if i.key==K_ESCAPE:return
				elif i.type==MOUSEMOTION:
					mouseOver=-1
					for k,j in enumerate(aviable):
						if collision(i.pos,(j[0][0],j[0][0]+200),(j[0][1]-12,j[0][1]+50)):
							mouseOver=j[1][5]

				elif i.type==MOUSEBUTTONDOWN:
					if collision(i.pos,(RESOLUTION[0]/2.0-48,RESOLUTION[0]/2.0-24+96),(RESOLUTION[1]-100,RESOLUTION[1])):
						return
					for k,j in enumerate(aviable):
						if collision(i.pos,(j[0][0],j[0][0]+200),(j[0][1]-12,j[0][1]+36)):
							selected=j[1][5]
							vaisseau.chShip([["vitesseVaisseau",cara[selected][1]],["vieVaisseau",cara[selected][0]],
								["blindageVaisseau",cara[selected][2]],["shieldVaisseau",cara[selected][3]],
								["noShip",cara[selected][5]]])

	def equiper(self):
		mouseover=0
		def afficher():
			self.fenetre.fill(0)
			self.fenetre.blit(decors["map4"],(0,0))
			self.fenetre.blit(decors["map2"],(0,0))
			for i in range(0,RESOLUTION[0]/500+1):
				for j in range(0,RESOLUTION[1]/500+1):
					self.fenetre.blit(decors["filtreNoir"],(i*500,j*500))
			cadre(self.fenetre,1,(100,100),(RESOLUTION[0]-100,RESOLUTION[1]-100))
			cadre(self.fenetre,0,((RESOLUTION[0]-800)/2.0,110),((RESOLUTION[0]-400)/2.0,156))
			cadre(self.fenetre,0,((RESOLUTION[0]+200)/2.0,110),((RESOLUTION[0]+600)/2.0,156))
			self.fenetre.blit(font.Font(None,36).render("equipees",1,(255,255,255)),((RESOLUTION[0]-750)/2.0,120))
			self.fenetre.blit(font.Font(None,36).render("equipable",1,(255,255,255)),((RESOLUTION[0]+250)/2.0,120))
			overed=0
			coefVitesse=1
			coefEnergie=1
			coefBouclier=0.0
			coefDefense=0.0
			coefFurtivite=0.0
			for j,i in enumerate(vaisseau.equipes):
				self.fenetre.blit(font.Font(None,36).render(i[0],1,(0,0,255)),(150,225+j*50))
				if i[5][0] is not None:
					coefVitesse+=1-i[5][0]
					coefEnergie+=1-i[5][1]
					coefBouclier+=i[5][2]
					coefDefense+=i[5][3]
					coefFurtivite+=i[5][4]
			self.fenetre.blit(font.Font(None,36).render("vitesse: +%i "%((1-coefVitesse)*100)+"%",1,(0,255,0)),(150,350))
			self.fenetre.blit(font.Font(None,36).render("energie: +%i "%((1-coefEnergie)*100)+"%",1,(0,255,0)),(150,400))
			if coefBouclier>=0:self.fenetre.blit(font.Font(None,36).render("bouclie: +%i s"%(coefBouclier),1,(0,255,0)),(150,450))
			else:self.fenetre.blit(font.Font(None,36).render("bouclie: %i s"%(coefBouclier),1,(0,255,0)),(150,450))
			self.fenetre.blit(font.Font(None,36).render("Defense: +%i "%(coefDefense),1,(0,255,0)),(150,500))
			self.fenetre.blit(font.Font(None,36).render("Furtivite: +%i s"%(coefFurtivite),1,(0,255,0)),(150,550))
			for i,j in enumerate(vaisseau.gun):
				if overed:i+=3
				if mouseover-1==i:
					self.fenetre.blit(font.Font(None,36).render(j[0],1,(255,0,0)),(RESOLUTION[0]/2.0-100,(200+i*24)))
					overed=1
					self.fenetre.blit(font.Font(None,36).render("degats:{}   cadence:{}   vitesse:{}".format(j[1],j[2],j[3]),1,(255,0,0)),(RESOLUTION[0]/2.0-100,(200+i*24+24)))
					if j[5][0] is not None:
						self.fenetre.blit(font.Font(None,36).render("Vitesse:+{}%    Energie +{}%    temps Bouclier:{}s".format((j[5][0]-1)*100,(j[5][1]-1)*100,j[5][2]),1,(255,0,0)),(RESOLUTION[0]/2.0-100,(200+i*24+48)))
						self.fenetre.blit(font.Font(None,36).render("defense:+{} points   furtivite: +{} s".format(j[5][3],j[5][4]),1,(255,0,0)),(RESOLUTION[0]/2.0-100,(200+i*24+72)))
				else:self.fenetre.blit(font.Font(None,36).render(j[0],1,(255,255,255)),(RESOLUTION[0]/2.0-100,(200+i*24)))
			display.flip()
		while 1:
			sleep(0.125)
			afficher()
			for i in event.get():
				if i.type==KEYDOWN:
					if i.key==K_ESCAPE:
						return
				elif i.type==MOUSEBUTTONDOWN:
					for j in range(len(vaisseau.gun)):
						if collision(i.pos,(RESOLUTION[0]/2.0-100,RESOLUTION[0]/2.0+300),((200+j*24),200+j*24+24)):
							vaisseau.equipes=[vaisseau.gun[j],vaisseau.equipes[0]]
							vaisseau.equiper()
							break

				elif i.type==MOUSEMOTION:
					mouseover=0
					for j in range(len(vaisseau.gun)):
						if collision(i.pos,(RESOLUTION[0]/2.0-100,RESOLUTION[0]/2.0+300),((200+j*24),200+j*24+24)):
							mouseover=j+1
							break
		return

	def popUp(self,texte,proposition1,proposition2="",numberProppositions=2):
		texte=texte.split("\n")
		largeurPopUp=max([len(x)for x in texte])*16
		self.fenetre.subsurface((RESOLUTION[0]-largeurPopUp)/2.0,(RESOLUTION[1]-48)/2.0,largeurPopUp,96+20).fill((255,255,255))
		self.fenetre.subsurface((RESOLUTION[0]-largeurPopUp+5)/2.0,(RESOLUTION[1]-48+5)/2.0,largeurPopUp-5.0,96+15).fill(0)
		for j,i in enumerate(texte):
			self.fenetre.blit(font.Font(None,36).render(i,1,(255,255,255)),((RESOLUTION[0]-largeurPopUp+10)/2.0,(RESOLUTION[1]-48+j*48+10)/2.0))
		if numberProppositions==2:
			self.fenetre.blit(font.Font(None,36).render(proposition1,1,(255,255,255)),((RESOLUTION[0]-largeurPopUp+10)/2.0,(RESOLUTION[1]+96+10)/2.0))
			self.fenetre.blit(font.Font(None,36).render(proposition2,1,(255,255,255)),((RESOLUTION[0]-largeurPopUp+10)/2.0+16*len(proposition2),(RESOLUTION[1]+96+10)/2.0))
		elif numberProppositions==1:
			self.fenetre.blit(font.Font(None,36).render(proposition1,1,(255,255,255)),((RESOLUTION[0]-largeurPopUp+10)/2.0,(RESOLUTION[1]+96+10)/2.0))

		display.flip()
		while 1:
			sleep(0.125)
			for i in event.get():
				if i.type==KEYDOWN:
					if i.key in[K_RETURN,K_o,K_y] :return 1
					elif i.key in[K_ESCAPE,K_n]:return 0
				elif i.type==MOUSEBUTTONDOWN:
					if numberProppositions==2:
						if collision(i.pos,((RESOLUTION[0]-largeurPopUp+10)/2.0,(RESOLUTION[0]-largeurPopUp+10)/2.0+16*(len(proposition1)-1)),((RESOLUTION[1]+96+10)/2.0,(RESOLUTION[1]+96/2.0+48))):
							return 1
						elif collision(i.pos,((RESOLUTION[0]-largeurPopUp+10)/2.0+16*len(proposition1),(RESOLUTION[0]-largeurPopUp+10)/2.0+16*(len(proposition2)+len(proposition1))),((RESOLUTION[1]+96+10)/2.0,(RESOLUTION[1]+96+48)/2.0)):
							return 0
					elif numberProppositions==1:
						if collision(i.pos,((RESOLUTION[0]-largeurPopUp+10)/2.0,(RESOLUTION[0]-largeurPopUp+10)/2.0+16*(len(proposition1)-1)),((RESOLUTION[1]+96+10)/2.0,(RESOLUTION[1]+96+10)/2.0+48)):
							return


class Campaign(object):

	def __init__(self,number,fenetre,new=0):
		self.fenetre=fenetre
		if new:
			self.number=""
			self.cinematique("intro")
		self.number=number
		self.gagne=1
		self.ennemi=[]
		self.score=0
		self.destructEnnemi=[]
		self.destructBallEnnemi=[]
		self.destructBallPerso=[]
		self.destructBallPersoSpe=[]
		self.key={K_UP:0,K_DOWN:0,K_LEFT:0,K_RIGHT:0,K_KP0:0,K_RCTRL:0,K_RSHIFT:0,K_KP1:0}
		self.loadCampaign()
		self.ennemiTues,self.ennemiRestant=0,sum([i["nombre"]for i in self.structure if "nombre"in i])
		self.ennemiTotal=self.ennemiRestant
		self.mute=0
		self.dead=[]
		self.bonus=[]
		self.followersPerso=[]
		self.followersEnnemi=[]
		self.listeCode={"term":"terminal"}

	def play(self):
		return self.boss()
		self.cinematique("level")
		vaisseau.initialize()
		mouse.set_visible(0)
		mixer.music.load(getcwd()+"/ressources/songs/tst2.mp3")
		self.tempsDebut=time()
		tempsActu=time()
		self.var=200
		while 1:
			pygame.time.Clock().tick(self.var)
			for i in event.get():
				if i.type==QUIT:
					Ennemi.ballNormal=[]
					vaisseau.balls=[]
					mixer.music.stop()
					self.quitter()
					mouse.set_visible(1)
					return 0
				elif i.type==KEYDOWN:

					if i.key in self.key:
						if i.key==K_KP0 and self.key[K_KP0]:
							self.key[K_KP0]=0
							continue
						self.key[i.key]=1
						if i.key==K_UP and self.key[K_DOWN]:self.key[i.key]=2
						elif i.key==K_RIGHT and self.key[K_LEFT]:self.key[i.key]=2
						elif i.key==K_DOWN and self.key[K_UP]:self.key[i.key]=2
						elif i.key==K_LEFT and self.key[K_RIGHT]:self.key[i.key]=2
						elif i.key==K_BACKSPACE:self.key[i.key]=1

					elif i.key==K_s:vaisseau.chGun()

					elif i.key==K_ESCAPE:
						if fenetre.full:
							fenetre.full=0
							globals()["RESOLUTION"]=(RESOLUTION[0]-100,RESOLUTION[1]-100)
							if vaisseau.pos[0]>=RESOLUTION[0]:vaisseau.pos[0]=RESOLUTION[0]-32
							if vaisseau.pos[1]>=RESOLUTION[1]:vaisseau.pos[1]=RESOLUTION[1]-64
							self.fenetre=display.set_mode((RESOLUTION[0],RESOLUTION[1]))
						else:
							fenetre.full=1
							globals()["RESOLUTION"]=(RESOLUTION[0]+100,RESOLUTION[1]+100)
							self.fenetre=display.set_mode((RESOLUTION[0],RESOLUTION[1]),FULLSCREEN)

					elif i.key==K_SPACE:
						action=self.pause()

						if action=="redo":
							self.__init__(self.number,self.fenetre)
							vaisseau.initialize()
							Ennemi.ballNormal=[]
							vaisseau.balls=[]
							mixer.music.stop()
							return self.play()

						elif action=="return":
							vaisseau.initialize()
							Ennemi.ballNormal=[]
							vaisseau.balls=[]
							mixer.music.stop()
							return 0

					elif i.key==K_m:
						if self.mute==0:
							mixer.music.stop()
							self.mute=1
						else:
							mixer.music.play(-1,0.0)
							self.mute=0

					elif i.key==K_KP2 and vaisseau.bonus["followers"]:
						if len(self.ennemi):
							self.followersPerso.append(Follower(choice(self.ennemi),vaisseau.pos))
							vaisseau.bonus["followers"]-=1

				elif i.type==KEYUP:
					if i.key in self.key and i.key!=K_KP0:
						self.key[i.key]=0
						if i.key==K_UP and self.key[K_DOWN]==2:self.key[K_DOWN]=1
						elif i.key==K_RIGHT and self.key[K_LEFT]==2:self.key[K_LEFT]=1
						elif i.key==K_DOWN and self.key[K_UP]==2:self.key[K_UP]=1
						elif i.key==K_LEFT and self.key[K_RIGHT]==2:self.key[K_RIGHT]=1
						elif i.key==K_RSHIFT:
							self.key[i.key]=0

			if time()-tempsActu>=2:
				tempsActu=time()
				for i in self.structure:
					if i["activate"]==1:
						if "executable" in i:
							if i["executable"][0]:
								execute=i["executable"][1]()
								if execute!=0:exec(execute)
								i["executable"][0]=0

						if i["fin"]==1:
							if not len(self.ennemi) or not [j for j in self.ennemi if collision(j.pos,(0,RESOLUTION[0]),(0,RESOLUTION[1]))]:
								Ennemi.ballNormal=[]
								vaisseau.balls=[]
								mixer.music.stop()
								mouse.set_visible(1)
								vaisseau.initialize()
								self.key={K_UP:0,K_DOWN:0,K_LEFT:0,K_RIGHT:0,K_KP0:0,K_RCTRL:0,K_RSHIFT:0,K_KP1:0}
								return self.finNiveau()

						elif i["totalcall"]<=i["nombre"]/i["groupe"] and time()-i["lastCall"]>=i["interval"]:
							i["totalcall"]+=1
							if i["totalcall"]>=i["nombre"]/i["groupe"]:
								i["activate"]=2
							if i["groupe"] in Ennemi.escadron:Ennemi.escadron[i["groupe"]]+=1
							else:Ennemi.escadron[i["groupe"]]=1
							for j in range(i["groupe"]):
								self.ennemi.append(Ennemi(i["forme"],i["pdv"],i["points"],i["pos"],j,i["armement"],i["ia"],i["angle"],i["groupe"],i["vaisseau"],i["chance"],i["cadence"],i["vitesse"],i["degat"],i["vitesseBall"],i["formeShot"]))
							i["lastCall"]=time()
					elif i["debut"]<=time()-self.tempsDebut and i["activate"]!=2:
						i["activate"]=1
						i["lastCall"]=time()

			#	affichage et actions
			self.fenetre.blit(decors["map4"],(0,0))

			self.destructBallPerso=[]
			self.destructEnnemi=[]
			self.destructBallEnnemi=[]
			self.destructBallPersoSpe=[]
			self.destructDead=[]
			destructBonus=[]
			destructFollowersPerso=[]

			for i in self.followersPerso:
				i.avancer()
				for j in self.ennemi:
					angle=int(fabs(degrees(atan((vaisseau.pos[1]+32-j.pos[1])/(j.pos[0]-(vaisseau.pos[0]+16)*1.0)))))-90
					if angle<0:angle+=360
					angle2=i.angle-90
					if angle2<0:angle2+=360
					if vaisseaux[0][angle].get_rect().move(j.pos[0],j.pos[1]).colliderect(spriteRotate["follower"][angle].get_rect().move(i.pos[0],i.pos[1])):
						if j.perdVie(vaisseau.degat_followers):
							vaisseau.shottedShip["vaisseau"+str(j.imgVaisseau)]+=1
							self.score+=j.point
							vaisseau.money+=j.vie[0]
							if j not in self.destructEnnemi:self.destructEnnemi.append(j)
							self.dead.append([1,[i.pos[0]+Follower.vitesse,i.pos[1]+Follower.vitesse],0])
						destructFollowersPerso.append(i)
						break
				angle=i.angle-90
				if angle<0:angle+=360
				self.fenetre.blit(ballPerso["follower"][angle],(i.pos[0],i.pos[1]))

			for i in destructFollowersPerso:self.followersPerso.remove(i)

			for i in self.bonus:
				if vaisseaux[0][angle].get_rect().move(vaisseau.pos[0],vaisseau.pos[1]).colliderect((i.pos[0],i.pos[1],i.pos[0]+32,i.pos[1]+32)):
					vaisseau.getBonus(i.objet)
					destructBonus.append(i)
					break
				i.afficher(self.fenetre)

			for i in destructBonus:self.bonus.remove(i)

			for i in self.dead:
				try:self.fenetre.blit(sprites["expl0%i"%(i[0])],(i[1][0],i[1][1]-20))
				except:self.fenetre.blit(sprites["expl10"],(i[1][0],i[1][1]-20))
				i[2]+=1
				if i[2]==5:
					i[0]+=1
					i[2]=0
				if i[0]==11:
					i[0]=0
					self.destructDead.append(i)

			for i in self.destructDead:self.dead.remove(i)

			for i in vaisseau.balls:
				i[0][0]+=i[2]*i[5][0]
				i[0][1]+=i[2]*i[5][1]
				if i[0][1]>RESOLUTION[1]+10 or i[0][1]<-10 or i[0][0]>RESOLUTION[0]+10 or i[0][0]<-10:
					self.destructBallPerso.append(i)
					continue
				for j in self.ennemi:
					angle=int(fabs(degrees(atan((vaisseau.pos[1]+32-j.pos[1])/(j.pos[0]-(vaisseau.pos[0]+16)*1.0)))))-90
					if angle<0:angle+=360
					angle2=i[1]-90
					if angle2<0:angle2+=360
					if vaisseaux[0][angle].get_rect().move(j.pos[0],j.pos[1]).colliderect(ballPerso[i[4]][angle].get_rect().move(i[0][0],i[0][1])):
						if j.perdVie(i[3]):
							vaisseau.shottedShip["vaisseau"+str(j.imgVaisseau)]+=1
							self.score+=j.point
							vaisseau.money+=j.vie[0]
							if j not in self.destructEnnemi:self.destructEnnemi.append(j)
							self.dead.append([1,[i[0][0]+i[3]*i[5][0]*2,i[0][1]+i[3]*i[5][1]*2],0])
						self.destructBallPerso.append(i)
						if not randrange(self.donnees["chances_bonus"]):self.bonus.append(Bonus(j.pos,choice(self.donnees["bonus"])))
						break
				angle=i[1]
				angle-=90
				if angle<0:angle+=360
				self.fenetre.blit(ballPerso[i[4]][angle],(i[0][0],i[0][1]))

			for i in self.destructBallPersoSpe:vaisseau.ballsSpe.remove(i)

			for i in self.ennemi:
				if i.kamikaze[0]=="o":
					if time()-i.kamikaze[1]>=i.tempskami:
						if i not in self.destructEnnemi:
							self.destructEnnemi.append(i)
							self.dead.append([1,[i.pos[0],i.pos[1]],0])
						continue
				if i.act(vaisseau)and i not in self.destructEnnemi:
					self.destructEnnemi.append(i)
					continue
				angle=int(fabs(degrees(atan((vaisseau.pos[1]+32-i.pos[1])/(i.pos[0]-(vaisseau.pos[0]+16)*1.0)))))
				if i.pos[0]>vaisseau.pos[0]:angle=modifAngle(angle,270)
				if i.pos[1]<vaisseau.pos[1]:angle=modifAngle(angle,180)
				angle-=90
				if angle<0:angle+=360
				self.fenetre.blit(vaisseaux[i.imgVaisseau][angle],tuple(i.pos))
				total=i.vie[0]+i.vie[1]
				try:
					self.fenetre.subsurface(i.pos[0]-1.5*(total),i.pos[1]-10,total*3,5).fill((128,128,128))
					self.fenetre.subsurface(i.pos[0]+1.5*total-i.vie[1]*3,i.pos[1]-9,i.vie[1]*3,3).fill((0,255,0))
				except:pass

			vaisseau.act(self.key)

			for i in Ennemi.ballesNormal:
				i[0][0]+=i[3]*i[4][0]
				i[0][1]+=i[3]*i[4][1]
				if i[0][1]>=RESOLUTION[1] or i[0][1]<=0 or i[0][0]>RESOLUTION[0] or i[0][0]<=0:
					self.destructBallEnnemi.append(i)
					continue
				angle=int(modulo(vaisseau.angle-90,360)[0])
				try:
					if ballPerso[i[5]][i[1]].get_rect().move(i[0][0],i[0][1]).colliderect(vaisseaux[vaisseau.noShip][angle].get_rect().move(vaisseau.pos[0],vaisseau.pos[1])):
						self.destructBallEnnemi.append(i)
						if not vaisseau.activateShield:
							vaisseau.perdVie(i[2])
							vaisseau.explo0=[1,[i[0][0]+i[3]*i[4][0]*2-vaisseau.pos[0],i[0][1]+i[3]*i[4][1]*2-vaisseau.pos[1]],0]
						else:vaisseau.explo1=[1,[i[0][0]+i[3]*i[4][0]*2-vaisseau.pos[0],i[0][1]+i[3]*i[4][1]*2-vaisseau.pos[1]],[0,0]]
						continue
				except:pass

				angle=i[1]
				angle-=90
				if angle<0:angle+=360
				self.fenetre.blit(ballPerso[i[5]][angle],(i[0][0],i[0][1]))

			pos=[]+vaisseau.pos
			center=vaisseaux[0][90].get_rect().move(pos[0],pos[1]).center
			degres=int(vaisseau.angle-90)
			if degres<0:degres+=360
			self.fenetre.blit(vaisseaux[vaisseau.noShip][degres],vaisseaux[vaisseau.noShip][degres].get_rect(center=vaisseaux[vaisseau.noShip][90].get_rect().move(pos[0],pos[1]).center))

			total=vaisseau.pdv[0]+vaisseau.pdv[1]
			try:
				self.fenetre.subsurface(vaisseau.pos[0]-1.5*(total),vaisseau.pos[1]-10,total*3,5).fill((128,128,128))
				self.fenetre.subsurface(vaisseau.pos[0]+1.5*total-vaisseau.pdv[1]*3,vaisseau.pos[1]-9,vaisseau.pdv[1]*3,3).fill((0,255,0))
			except:pass

			if vaisseau.activateShield:
				self.fenetre.blit(sprites["bouclier"],(center[0]-36,center[1]-30))
				if vaisseau.explo1[0]:
					self.fenetre.blit(sprites["expl20%i"%(vaisseau.explo1[0]-1)],(vaisseau.pos[0]+vaisseau.explo1[1][0],vaisseau.pos[1]+vaisseau.explo1[1][1]-20))
					vaisseau.explo1[2][0]+=1
					if vaisseau.explo1[2][0]==5:
						vaisseau.explo1[2][0]=0
						vaisseau.explo1[0]+=1
					if vaisseau.explo1[0]==5:
						vaisseau.explo1[0]=0
						vaisseau.explo1[2][1]+=1
					if vaisseau.explo1[2][1]==2:
						vaisseau.explo1[0]=0

			if vaisseau.explo0[0]:
				self.fenetre.blit(sprites["expl0%i"%(vaisseau.explo0[0]-1)],(vaisseau.pos[0]+vaisseau.explo0[1][0],vaisseau.pos[1]+vaisseau.explo0[1][1]-20))
				vaisseau.explo0[2]+=1
				if vaisseau.explo0[2]==5:
					vaisseau.explo0[0]+=1
					vaisseau.explo0[2]=0
				if vaisseau.explo0[0]==11:vaisseau.explo0[0]=0

			display.flip()
			for i in self.destructBallEnnemi:Ennemi.ballesNormal.remove(i)
			for i in self.destructBallPerso:vaisseau.balls.remove(i)

			for i in self.destructEnnemi:
				self.ennemiTues+=1
				self.ennemiRestant-=1
				self.ennemi.remove(i)

			if vaisseau.pdv[1]<=0:
				mixer.music.stop()
				vaisseau.ballsSpe=[]
				vaisseau.balls=[]
				Ennemi.ballsNormal=[]
				self.ecranPerdu()
				mouse.set_visible(1)
				vaisseau.initialize()
				return 0

	def pause(self):
		code=""
		mouse.set_visible(1)
		debutPause=time()
		def afficher():
			for i in range(RESOLUTION[0]/500+1):
				for j in range(RESOLUTION[1]/500+1):
					self.fenetre.blit(decors["filtreNoir"],(500*i,500*j))
			tempsRestant=int(int([x["debut"]for x in self.structure if x["fin"]==1][0])-(time()-self.tempsDebut))
			tempsRestant=[int(tempsRestant/60.0),(tempsRestant/60.0-int(tempsRestant/60.0))*0.6]
			self.fenetre.blit(font.Font(None,36).render("PRESS 'ENTER' KEY TO CONTINUE",1,(255,255,255)),(RESOLUTION[0]/2-150,RESOLUTION[1]/2-20))
			self.fenetre.blit(font.Font(None,18).render("LEVEL: {}".format(self.number),1,(255,255,255)),(0,RESOLUTION[1]/10))
			self.fenetre.blit(font.Font(None,18).render("SCORE: {}".format(self.score),1,(255,255,255)),(0,RESOLUTION[1]/10+50))
			self.fenetre.blit(font.Font(None,18).render("REMAINING NUMBER OF ENEMY: {}".format(self.ennemiRestant),1,(255,255,255)),(0,RESOLUTION[1]/10+100))
			self.fenetre.blit(font.Font(None,18).render("NUMBER OF DEAD ENEMY: {}".format(self.ennemiTues),1,(255,255,255)),(0,RESOLUTION[1]/10+150))
			self.fenetre.blit(font.Font(None,18).render("TOTAL NUMBER OF ENEMY: {}".format(self.ennemiTotal),1,(255,255,255)),(0,RESOLUTION[1]/10+200))
			self.fenetre.blit(font.Font(None,18).render("MONNEY: {}".format(vaisseau.money),1,(255,255,255)),(RESOLUTION[0]-300,RESOLUTION[1]/10))
			self.fenetre.blit(font.Font(None,18).render("TIME OF USE OF THE SHIELD: {}".format(vaisseau.shield-vaisseau.coefTempsBouclier),1,(255,255,255)),(RESOLUTION[0]-300,RESOLUTION[1]/10+50))
			self.fenetre.blit(font.Font(None,18).render("SELECTED WEAPON: {}".format(vaisseau.equipes[vaisseau.activate][0]),1,(255,255,255)),(RESOLUTION[0]-300,RESOLUTION[1]/10+100))
			self.fenetre.blit(font.Font(None,18).render("ARM AVAILABLE: {}".format("; ".join([x[0]for x in vaisseau.equipes])),1,(255,255,255)),(RESOLUTION[0]-300,RESOLUTION[1]/10+150))
			self.fenetre.blit(font.Font(None,18).render("TIME BOFERE USING SHIELD: {} second".format(str(vaisseau.cadenceShield-(time()-vaisseau.lastUsedShield))[:4]),1,(255,255,255)),(RESOLUTION[0]-300,RESOLUTION[1]/10+200))
			self.fenetre.blit(font.Font(None,18).render("TIME BEFORE THE END: {} minute(s)".format(sum(tempsRestant)),1,(255,255,255)),(RESOLUTION[0]-300,RESOLUTION[1]/10+250))
			#self.fenetre.blit(font.Font(None,18).render("CONTROLS",1,(255,255,255)),(RESOLUTION[0]/2-150,RESOLUTION[1]/2+30))
			self.fenetre.blit(font.Font(None,18).render("REDO",1,(255,255,255)),(RESOLUTION[0]/2-150,RESOLUTION[1]/2+80))
			self.fenetre.blit(font.Font(None,18).render("RETURN TO THE SCREEN OF THE SELECTION",1,(255,255,255)),(RESOLUTION[0]/2-150,RESOLUTION[1]/2+130))
			display.flip()
		afficher()
		while 1:
			sleep(0.25)
			for i in event.get():
				if i.type==KEYDOWN:
					if i.key==K_RETURN:
						if not self.code(code):
							self.tempsDebut+=time()-debutPause
							vaisseau.update(time()-debutPause)
							for i in self.structure:
								if i["activate"]==1:i["lastCall"]=time()
							mouse.set_visible(0)
							return
						else:
							code=""
							afficher()
					elif i.key==K_ESCAPE:code=""
					else:code+=str(i.unicode)

				if i.type==MOUSEBUTTONDOWN:
					if collision(i.pos,[RESOLUTION[0]/2-150,RESOLUTION[0]/2-100],[RESOLUTION[1]/2+80,RESOLUTION[1]/2+130]):
						return "redo"
					elif collision(i.pos,(RESOLUTION[0]/2-150,RESOLUTION[0]/2+300),(RESOLUTION[1]/2+130,RESOLUTION[1]/2+180)):
						return "return"

	def code(self,texte):
		if texte in self.listeCode:
			if self.listeCode[texte]=="terminal":
				self.terminal()
			return 1
		else:return 0

	def terminal(self):
		a=0
		self.fenetre.fill(0)
		display.flip()
		def afficherCommande():
			self.fenetre.subsurface(200,100+a,RESOLUTION[0]-201,36).fill(0)
			self.fenetre.blit(font.Font(None,36).render(">>>"+commande,1,(255,255,255)),(200,100+a))
			display.flip()

		def afficherResultat():
			self.fenetre.subsurface(200,100+a,RESOLUTION[0]-201,36).fill(0)
			self.fenetre.blit(font.Font(None,36).render(">>> "+result+": ' "+commande+" '",1,(255,255,255)),(200,100+a))
			if retour:self.fenetre.blit(font.Font(None,36).render(retour,1,(255,255,255)),(200,100+a+32))
			display.flip()

		commande=""
		afficherCommande()
		while 1:
			sleep(0.06125)
			for i in event.get():
				if i.type==KEYDOWN:
					if i.key==K_ESCAPE:return
					elif i.key==K_RETURN:
						a+=36
						result=""
						retour=""
						try:retour=str(eval(commande))
						except:
							try:exec(commande)in locals(),globals()
							except:result="echec de "
							else:result="reussi"
						else:result="reussi"
						afficherResultat()
						if retour:a+=36
						a+=36
						commande=""
					elif i.key==K_BACKSPACE:
						commande=commande[:-1]
						afficherCommande()
					else:
						try:commande+=str(i.unicode)
						except:pass
						afficherCommande()

	def quitter(self):
		return

	def ecranPerdu(self):
		for i in range(RESOLUTION[0]/500+1):
			for j in range(RESOLUTION[1]/500+1):
				self.fenetre.blit(decors["filtreNoir"],(500*i,500*j))
		self.fenetre.blit(font.Font(None,36).render("You died!",1,(255,255,255)),(RESOLUTION[0]/2-105,RESOLUTION[1]/2))
		self.fenetre.blit(font.Font(None,36).render("score:{}".format(self.score),1,(255,255,255)),(RESOLUTION[0]/2-95,RESOLUTION[1]/2+100))
		self.fenetre.blit(font.Font(None,36).render("press enter to continu",1,(255,255,255)),(RESOLUTION[0]/2-160,RESOLUTION[1]/2+200))
		display.flip()
		while 1:
			sleep(0.125)
			for i in event.get():
				if i.type==KEYDOWN:
					if i.key==K_RETURN:return 1
				elif i.type==MOUSEBUTTONDOWN:return 1

	def finNiveau(self):
		for i in range(RESOLUTION[0]/500+1):
			for j in range(RESOLUTION[1]/500+1):
				self.fenetre.blit(decors["filtreNoir"],(500*i,500*j))
		self.fenetre.blit(font.Font(None,36).render("You survived!",1,(255,255,255)),(RESOLUTION[0]/2-105,RESOLUTION[1]/2))
		self.fenetre.blit(font.Font(None,36).render("score:{}".format(self.score),1,(255,255,255)),(RESOLUTION[0]/2-95,RESOLUTION[1]/2+100))
		self.fenetre.blit(font.Font(None,36).render("press enter to continu",1,(255,255,255)),(RESOLUTION[0]/2-160,RESOLUTION[1]/2+200))
		display.flip()
		while 1:
			sleep(0.125)
			for i in event.get():
				if i.type==KEYDOWN:
					if i.key==K_RETURN:
						return self.boss()
				elif i.type==MOUSEBUTTONDOWN:
					return self.boss()

	def boss(self):
		if vaisseau.boss[self.number-1]:
			self.fenetre.fill(0)
			self.fenetre.blit(font.Font(None,36).render("Voulez-vous affronter le boss?",1,(255,255,255)),((RESOLUTION[0]-464)/2.0,(RESOLUTION[1]-32)/2.))
			self.fenetre.blit(font.Font(None,36).render("O/N ; Y/N",1,(255,255,255)),((RESOLUTION[0]-144)/2.0,(RESOLUTION[1]+32)/2.))
			display.flip()
			fini=0
			while not fini:
				sleep(0.125)
				for i in event.get():
					if i.type==KEYDOWN:
						if i.key in [K_o,K_y]:
							fini=1
							break
						elif i.key==K_n:return 1
		return self.playBoss()

	def playBoss(self):
		self.cinematique("boss")
		globals()["boss"]=Boss(self.number-1)
		self.tempsDebut=time()
		while 1:
			pygame.time.Clock().tick(200)
			for i in event.get():
				if i.type==KEYDOWN:
					if i.key in self.key:
						if i.key==K_KP0 and self.key[K_KP0]:
							self.key[K_KP0]=0
							continue
						self.key[i.key]=1
						if i.key==K_UP and self.key[K_DOWN]:self.key[i.key]=2
						elif i.key==K_RIGHT and self.key[K_LEFT]:self.key[i.key]=2
						elif i.key==K_DOWN and self.key[K_UP]:self.key[i.key]=2
						elif i.key==K_LEFT and self.key[K_RIGHT]:self.key[i.key]=2
						elif i.key==K_RSHIFT:
							self.key[i.key]=1
					elif i.key==K_s:vaisseau.chGun()
					elif i.key==K_ESCAPE:
						if fenetre.full:
							fenetre.full=0
							globals()["RESOLUTION"]=(RESOLUTION[0]-100,RESOLUTION[1]-100)
							if vaisseau.pos[0]>=RESOLUTION[0]:vaisseau.pos[0]=RESOLUTION[0]-32
							if vaisseau.pos[1]>=RESOLUTION[1]:vaisseau.pos[1]=RESOLUTION[1]-64
							self.fenetre=display.set_mode((RESOLUTION[0],RESOLUTION[1]))
							boss.posTourelles=[[(RESOLUTION[0]-445)/2.0,102],[(RESOLUTION[0]-45)/2.0,102],[(RESOLUTION[0]+355)/2.0,102]]
							boss.posPanneaux=[[(RESOLUTION[0]-534)/2.0,72],[(RESOLUTION[0]+534)/2.0,72]]
						else:
							fenetre.full=1
							globals()["RESOLUTION"]=(RESOLUTION[0]+100,RESOLUTION[1]+100)
							self.fenetre=display.set_mode((RESOLUTION[0],RESOLUTION[1]),FULLSCREEN)
					elif i.key==K_SPACE:
						action=self.pause()

						if action=="redo":
							self.__init__(self.number,self.fenetre)
							vaisseau.initialize()
							mixer.music.stop()
							boss.balls=[]
							return self.boss()

						elif action=="return":
							vaisseau.initialize()
							mixer.music.stop()
							boss.balls=[]
							return 0

					elif i.key==K_m:
						if self.mute==0:
							mixer.music.stop()
							self.mute=1
						else:
							mixer.music.play(-1,0.0)
							self.mute=0

				elif i.type==KEYUP:
					if i.key in self.key and i.key!=K_KP0:
						self.key[i.key]=0
						if i.key==K_UP and self.key[K_DOWN]==2:self.key[K_DOWN]=1
						elif i.key==K_RIGHT and self.key[K_LEFT]==2:self.key[K_LEFT]=1
						elif i.key==K_DOWN and self.key[K_UP]==2:self.key[K_UP]=1
						elif i.key==K_LEFT and self.key[K_RIGHT]==2:self.key[K_RIGHT]=1
						elif i.key==K_RSHIFT:
							self.key[i.key]=0

			boss.act()
			self.fenetre.blit(decors["map4"],(0,0))
			boss.act(self.fenetre)
			self.destructBallPersoSpe=[]
			self.destructBallPerso=[]
			self.destructBallEnnemi=[]

			for i in vaisseau.balls:
				i[0][0]+=i[2]*i[5][0]
				i[0][1]+=i[2]*i[5][1]
				collid=boss.collisions(i)
				if i[0][1]>RESOLUTION[1]+10 or i[0][1]<-10 or i[0][0]>RESOLUTION[0]+10 or i[0][0]<-10 or collid:
					self.destructBallPerso.append(i)
					if collid==2:
						vaisseau.money+=boss.money
						vaisseau.boss[self.number-1]=1
						sleep(2) 
						self.cinematique("boss fin",0)
						mouse.set_visible(1)
						return 1
					continue
				angle=i[1]-90
				if angle<0:angle+=360
				self.fenetre.blit(ballPerso[i[4]][angle],(i[0][0],i[0][1]))

			for i in self.destructBallPerso:
				vaisseau.balls.remove(i)

			angle=int(vaisseau.angle-90)
			if angle<0:angle+=360
			rect_vaisseau=vaisseaux[vaisseau.noShip][angle].get_rect().move(vaisseau.pos[0],vaisseau.pos[1])
			for i in boss.balls:
				#[0]=pos; [1]=angle; [2]=vitesse; [3]=degats; [4]= % x et y
				i[0][0]+=i[2]*i[4][0]
				i[0][1]+=i[2]*i[4][1]
				if 0>i[0][0] or i[0][0]>RESOLUTION[0]+10 or i[0][1]<0 or i[0][1]>RESOLUTION[1]+10:
					self.destructBallEnnemi.append(i)
					continue
				if ballPerso[i[5]][i[1]].get_rect().move(i[0][0],i[0][1]).colliderect(rect_vaisseau):
					self.destructBallEnnemi.append(i)
					if not vaisseau.activateShield:
						vaisseau.perdVie(i[3])
						vaisseau.explo0=[1,[i[0][0]+i[3]*i[4][0]*2-vaisseau.pos[0],i[0][1]+i[3]*i[4][1]*2-vaisseau.pos[1]],0]
					else:
						vaisseau.explo1=[1,[i[0][0]+i[3]*i[4][0]*2-vaisseau.pos[0],i[0][1]+i[3]*i[4][1]*2-vaisseau.pos[1]],[0,0]]
					continue
				angle=i[1]
				angle-=90
				if angle<0:angle+=360
				self.fenetre.blit(ballPerso[i[5]][angle],(i[0][0],i[0][1]))

			for i in self.destructBallEnnemi:boss.balls.remove(i)

			if self.number-1==0:vaisseau.act(self.key,[[0,RESOLUTION[0]-52],[150,RESOLUTION[1]-52]])
			else:vaisseau.act(self.key)

			pos=[]+vaisseau.pos
			center=vaisseaux[0][90].get_rect().move(pos[0],pos[1]).center
			degres=int(vaisseau.angle-90)
			if degres<0:degres+=360
			self.fenetre.blit(vaisseaux[vaisseau.noShip][degres],vaisseaux[vaisseau.noShip][degres].get_rect(center=vaisseaux[vaisseau.noShip][90].get_rect().move(pos[0],pos[1]).center))

			total=vaisseau.pdv[0]+vaisseau.pdv[1]
			try:
				self.fenetre.subsurface(vaisseau.pos[0]-1.5*(total),vaisseau.pos[1]-10,total*3,5).fill((128,128,128))
				self.fenetre.subsurface(vaisseau.pos[0]+1.5*total-vaisseau.pdv[1]*3,vaisseau.pos[1]-9,vaisseau.pdv[1]*3,3).fill((0,255,0))
			except:pass

			if vaisseau.activateShield:
				self.fenetre.blit(sprites["bouclier"],(center[0]-36,center[1]-30))
				if vaisseau.explo1[0]:
					self.fenetre.blit(sprites["expl20%i"%(vaisseau.explo1[0]-1)],(vaisseau.pos[0]+vaisseau.explo1[1][0],vaisseau.pos[1]+vaisseau.explo1[1][1]-20))
					vaisseau.explo1[2][0]+=1
					if vaisseau.explo1[2][0]==5:
						vaisseau.explo1[2][0]=0
						vaisseau.explo1[0]+=1
					if vaisseau.explo1[0]==5:
						vaisseau.explo1[0]=0
						vaisseau.explo1[2][1]+=1
					if vaisseau.explo1[2][1]==2:
						vaisseau.explo1[0]=0

			if vaisseau.explo0[0]:
				self.fenetre.blit(sprites["expl0%i"%(vaisseau.explo0[0]-1)],(vaisseau.pos[0]+vaisseau.explo0[1][0],vaisseau.pos[1]+vaisseau.explo0[1][1]-20))
				vaisseau.explo0[2]+=1
				if vaisseau.explo0[2]==5:
					vaisseau.explo0[0]+=1
					vaisseau.explo0[2]=0
				if vaisseau.explo0[0]==11:vaisseau.explo0[0]=0
			display.flip()
			if vaisseau.pdv[1]<=0:
				self.key={K_UP:0,K_DOWN:0,K_LEFT:0,K_RIGHT:0,K_KP0:0,K_RCTRL:0,K_RSHIFT:0,K_KP1:0}
				vaisseau.initialize()
				if self.continuer():
					return self.playBoss()
				else:
					return 0
		vaisseau.boss[self.number]=1
		return 1

	def continuer(self):
		vaisseau.initialize()
		self.fenetre.blit(decors["map4"],(0,0))
		self.fenetre.blit(font.Font(None,36).render("Vous avez perdu.",1,(255,255,255)),((RESOLUTION[0]-275)/2.0,(RESOLUTION[1])/2.0-36))
		self.fenetre.blit(font.Font(None,36).render("Voullez-vous essayer a nouveau?",1,(255,255,255)),((RESOLUTION[0]-400)/2.0,(RESOLUTION[1])/2.0))
		self.fenetre.blit(font.Font(None,36).render("O/N ; Y/N",1,(255,255,255)),((RESOLUTION[0]-200)/2.0,(RESOLUTION[1])/2.0+36))
		display.flip()
		while 1:
			sleep(0.125)
			for i in event.get():
				if i.key in [K_o,K_y]:return 1
				elif i.key==K_n:
					mouse.set_visible(1)
					return 0

	def cinematique(self,passage,chFond=1):
		with open("levels/textes/"+passage+str(self.number)+".cin","r")as f:f=f.read().replace("\n","")
		textes=eval(f)
		if not textes:
			return
		for i in textes:
			if chFond:
				self.fenetre.fill(0)
			else:
				self.fenetre.subsurface(0,RESOLUTION[1]-50-len(i)*36,RESOLUTION[0]-5,len(i)*36).fill(0)
			for k,j in enumerate(i):
				if type(j)==str:self.fenetre.blit(font.Font(None,36).render(j.decode('utf-8'),1,(255,255,255)),((RESOLUTION[0]-len(j)*12)/2.0,RESOLUTION[1]-50-(len(i)-k)*36))
				else:self.fenetre.blit(font.Font(None,36).render(j[0].decode('utf-8'),1,j[1]),((RESOLUTION[0]-len(j[0])*12)/2.0,RESOLUTION[1]-50-(len(i)-k)*36))
			display.flip()
			fini=0
			while not fini:
				sleep(0.125)
				for l in event.get():
					if l.type==KEYDOWN:
						if l.key!=K_ESCAPE:fini=1
						else:return
			if not chFond:self.fenetre.subsurface(0,RESOLUTION[1]-50-len(i)*36,RESOLUTION[0]-5,len(i)*36+36).fill(0)

	def loadCampaign(self):
		with open("levels/donnees1","r")as f:self.donnees=eval(f.read().replace("\n",""))
		self.structure=[]
		with open("levels/level{}".format(self.number),"r")as f:f=f.read().split("\n")
		for i in range(len(f)):
			if len(f[i])>=2:
				eval("self.structure.append({"+str(f[i])+"})")


class Ennemi(object):
	ballesNormal=[]
	tues=0
	escadron={}
	lastTir=time()
	calcCenter=image.load("ressources/sprites/vaisseau0.png").get_rect()

	def __init__(self,forme,pdv,points,structure,numero,armement,ia,angle,groupe,vaisseau,chance,cadence,vitesse,degats,vitesseBall,formeShot):
		self.identifiant=numero*Ennemi.escadron[groupe]
		self.forme=forme
		self.vie=[0,pdv]
		self.point=points
		self.structure=structure
		self.number=numero
		self.armement=armement
		self.groupe=groupe
		self.imgVaisseau=vaisseau
		if type(self.imgVaisseau)==list:self.imgVaisseau=choice(self.imgVaisseau)
		self.cadence,self.vitesse=cadence,vitesse
		self.chance=chance
		self.kamikaze=[0,0]
		self.tempskami=15
		self.angle=angle
		if type(self.angle)==list:self.angle=choice(self.angle)
		if Ennemi.escadron[groupe]%2 and not type(self.forme)==list:
			self.angle=modifAngle(self.angle,270)
		self.ia=ia
		self.pos=self.apparition()
		self.dead=[]
		self.count=0
		self.pdvKami=int(self.vie[1]*10/100.0)
		if not self.pdvKami:self.pdvKami=1
		self.degats=degats
		self.vitesseBall=vitesseBall
		self.formeShot=formeShot

	def apparition(self):
		if self.forme=="penta":
			if self.ia in [0,1]:
				if self.number==0:
					return [40+(-101+RESOLUTION[0])*(Ennemi.escadron[self.groupe]%2),-100]
				elif self.number==1:
					return [0+(-32+RESOLUTION[0])*(Ennemi.escadron[self.groupe]%2),-60]
				elif self.number==2:
					return [80+(-191+RESOLUTION[0])*(Ennemi.escadron[self.groupe]%2),-60]
				elif self.number==3:
					return [15+(-62+RESOLUTION[0])*(Ennemi.escadron[self.groupe]%2),0]
				elif self.number==4:
					return [55+(-142+RESOLUTION[0])*(Ennemi.escadron[self.groupe]%2),0]
			elif self.ia==2:
				if self.number==0:
					return [0+RESOLUTION[0]/2.0,-100]
				elif self.number==1:
					return [-40+RESOLUTION[0]/2.0,-100]
				elif self.number==2:
					return [40+RESOLUTION[0]/2.0,-100]
				elif self.number==3:
					return [-35+RESOLUTION[0]/2.0,-100]
				elif self.number==4:
					return [35+RESOLUTION[0]/2.0,-100]
		elif self.forme=="losange":
			if self.number==0:
				return [0+(-32+RESOLUTION[0])*(Ennemi.escadron[self.groupe]%2),-59]
			elif self.number==1:
				return [100+(-232+RESOLUTION[0])*(Ennemi.escadron[self.groupe]%2),-59]
			elif self.number==2:
				return [150+(-332+RESOLUTION[0])*(Ennemi.escadron[self.groupe]%2),0]
			elif self.number==3:
				return [50+(-132+RESOLUTION[0])*(Ennemi.escadron[self.groupe]%2),0]
		elif type(self.forme)==list:
			return self.forme

	def act(self,user):

		self.kami()
		self.tirer(user.pos)
		return self.deplacement(user.pos)

	def kami(self):
		if self.vie[1]<=self.pdvKami:
			if not bool(randrange(3)):
				self.kamikaze=["o",time()]
			else:self.kamikaze[0]=1

	def deplacement(self,pos):
		if self.kamikaze[0]=="o":
			if self.pos[0]>=pos[0] and self.pos[1]>=pos[1]:angle=[90,180]
			elif self.pos[0]>=pos[0] and self.pos[1]<=pos[1]:angle=[180,270]
			elif self.pos[0]<=pos[0] and self.pos[1]>=pos[1]:angle=[0,90]
			elif self.pos[0]<=pos[0] and self.pos[1]<=pos[1]:angle=[270,360]
			self.angle=randrange(int(angle[0]),int(angle[1]))
			angle=convertAngle(self.angle)
			self.pos=[self.pos[0]+self.vitesse*angle[0],self.pos[1]+self.vitesse*angle[1]]
			return

		if self.ia==0:		# rebondi sur les bords 
			if self.pos[0]>=RESOLUTION[0]-31 or self.pos[0]<0:
				self.angle=modifAngle(self.angle,270)
			if self.pos[1]>=RESOLUTION[1]+70 or self.pos[1]<-150:etat=1
			else:etat=0

		elif self.ia==1:	# tout droit et sort
			if self.pos[0]<=-32 or self.pos[0]>=RESOLUTION[0] or self.pos[1]<-150 or self.pos[1]>=RESOLUTION[1]+70:etat=1
			else:etat=0 
			
		elif self.ia==2:	#tourne aleatoirement (de haut en bas)
			self.count+=1
			if self.count==100:
				self.angle=choice(range(180,360))
				self.count=0
			if self.pos[0]>=RESOLUTION[0]-32 or self.pos[0]<=0:self.angle=modifAngle(self.angle,270)
			if self.pos[1]>=RESOLUTION[1]+70 or self.pos[1]<-150:etat=1
			else:etat=0

		elif self.ia==3:	#zigzag horizontal
			if self.count>=0:self.count+=1
			else:self.count-=1
			if self.count==100:
				self.angle=modifAngle(self.angle,180)
				self.count=-1
			elif self.count==-100:
				self.angle=modifAngle(self.angle,180)
				self.count=1
			if self.pos[0]<=-32 or self.pos[0]>=RESOLUTION[0]:etat=1
			else:etat=0 

		elif self.ia==4:	#zigzag vertical
			if self.count>=0:self.count+=1
			else:self.count-=1
			if self.count==100:
				self.angle=modifAngle(self.angle,90)
				self.count=-1
			elif self.count==-100:
				self.angle=modifAngle(self.angle,90)
				self.count=1
			if self.pos[1]>=RESOLUTION[1]+70 or self.pos[1]<-150:etat=1
			else:etat=0
		self.angle=modulo(self.angle,360)[0]
		angle=convertAngle(self.angle)
		self.pos=[self.pos[0]+self.vitesse*angle[0],self.pos[1]+self.vitesse*angle[1]]
		return etat

	def tirer(self,pos):
		if type(self.armement)==list:
			number=randrange(len(self.armement))
			armmt,self.armement=[]+self.armement,self.armement[number]
			if type(self.formeShot)==list:
				shot=1
				formeShot,self.formeShot=[]+self.formeShot,self.formeShot[number]
			else:shot=0
		else:armmt=0
		if time()-Ennemi.lastTir>=self.cadence and not randrange(self.chance):
			Ennemi.lastTir=time()
			angle=fabs(degrees(atan((pos[1]+32-self.pos[1])/(self.pos[0]-(pos[0]+16)*1.0))))
			if self.pos[0]>pos[0]:angle=modifAngle(angle,270)
			if self.pos[1]<pos[1]:angle=modifAngle(angle,180)
			angle2=convertAngle(modulo(angle-90,360)[0])
			angle1=convertAngle(angle)
			if self.armement==0:	# 1 shot
				Ennemi.ballesNormal.append([[self.pos[0]+16,self.pos[1]],int(angle),self.degats,self.vitesseBall,angle1,self.formeShot])
				#[0]=pos; [1]=angle; [2]=pdv; [3]=vitesse; [4]=%x,y; [5]=forme ball; 
			elif self.armement==1:# tire normal
				Ennemi.ballesNormal.append([[self.pos[0]+16,self.pos[1]],int(angle),self.degats,self.vitesseBall,angle1,self.formeShot])
			elif self.armement==2:# double
				centre=Ennemi.calcCenter.move(self.pos[0],self.pos[1]).center
				Ennemi.ballesNormal.append([[centre[0]-16*angle2[0],centre[1]-16*angle2[1]],int(angle),self.degats,self.vitesseBall,angle1,self.formeShot])
				Ennemi.ballesNormal.append([[centre[0]+16*angle2[0],centre[1]+16*angle2[1]],int(angle),self.degats,self.vitesseBall,angle1,self.formeShot])
			elif self.armement==3:# x5
				centre=Ennemi.calcCenter.move(self.pos[0],self.pos[1]).center
				Ennemi.ballesNormal.append([[centre[0]-16*angle2[0],centre[1]-16*angle2[1]],int(angle-20),self.degats,self.vitesseBall,convertAngle(angle-20),self.formeShot])
				Ennemi.ballesNormal.append([[centre[0]+16*angle2[0],centre[1]+16*angle2[1]],int(angle-10),self.degats,self.vitesseBall,convertAngle(angle-10),self.formeShot])
				Ennemi.ballesNormal.append([[centre[0]-16*angle2[0],centre[1]-16*angle2[1]],int(angle),self.degats,self.vitesseBall,angle1,self.formeShot])
				Ennemi.ballesNormal.append([[centre[0]+16*angle2[0],centre[1]+16*angle2[1]],int(angle+10),self.degats,self.vitesseBall,convertAngle(angle+10),self.formeShot])
				Ennemi.ballesNormal.append([[centre[0]-16*angle2[0],centre[1]-16*angle2[1]],int(angle+20),self.degats,self.vitesseBall,convertAngle(angle+20),self.formeShot])
		if armmt:
			self.armement=[]+armmt
			if shot:self.formeShot=[]+formeShot

	def perdVie(self,cbn):
		self.vie[1]-=cbn
		self.vie[0]+=cbn
		if self.vie[1]<=0:return 1
		return 0


class Vaisseau(object):
	calcCenter=image.load("ressources/sprites/vaisseau0.png").get_rect()

	def __init__(self,name,shipname,no=1,charger=[0,0]):
		self.name,self.shipname,self.noShip=name,shipname,no

		self.vitesseVaisseau=3
		self.vieVaisseau=50
		self.blindageVaisseau=0
		self.shieldVaisseau=3
		self.furtiviteVaisseau=0

		self.score=0
		self.level=[0,0]
		self.lives=self.vieVaisseau
		self.speed=0
		self.blindage=self.blindageVaisseau
		self.shield=3
		self.gun=[["primaire",1,0.25,5,time(),[None],0,0],["secondaire",2,0.5,7,time(),[None],0,0]]
		#["shotGun class 1",3,0.333,8,0,[1.1,1.1,-3,0,0],0,0]],
		self.money=0
		self.bonus={"followers":0}
		self.stade=1
		self.equipes=self.gun[:2]
		self.achats=[]
		self.furtivite=self.furtiviteVaisseau
		#noShip,score,level,lives,speed,blindage,shield,gun,money,bonus,gun[:2],furtivite
		self.shottedShip={"vaisseau"+str(x):0 for x in range(21)}
		self.balls=[]

		self.boss=[0,0,0,0,0]
		self.ballsSpe=[]
		self.missile=[]
		self.pos=[RESOLUTION[0]/2.0,RESOLUTION[1]-100]
		self.activate=0
		self.angle=90
		self.explo0=[0,0]
		self.explo1=[0,0]
		self.lastEnergieTire=time()
		self.cadenceEnergieTire=1
		self.cadenceShield=30
		self.lastUsedShield=time()-self.cadenceShield
		self.activateShield=0
		self.coefVitesse=1
		self.coefEnergie=1
		self.coefTempsBouclier=0
		self.coefDefense=0
		self.coefFurtivite=0
		self.degat_followers=10

		self.pdvBase=[0,(self.lives)]
		self.pdv=[]+self.pdvBase
		self.pdv[1]*=self.coefEnergie
		self.totalVie=self.pdvBase[1]*self.coefEnergie


		self.vitesseBase=(self.vitesseVaisseau+self.speed)
		self.vitesse=self.vitesseBase*self.coefEnergie
		self.equiper()

		if charger[0]:self.charger(charger[1])
		self.fichier=charger[1]

	def chShip(self,chara):
		for i in chara:
			self.__dict__[i[0]]=i[1]

	def initialize(self):
		self.pdv=[]+self.pdvBase
		self.pdv[1]*=self.coefEnergie
		self.totalVie=self.pdvBase[1]*self.coefEnergie
		self.pos=[RESOLUTION[0]/2.0,RESOLUTION[1]-100]
		self.angle=90
		for i in self.equipes:i[4]=0
		for i in self.gun:i[4]=0
		self.lastUsedShield=0
		self.lastEnergieTir=0
		self.balls=[]
		self.ballsSpe=[]
		self.missile=[]
		self.activate=0
		self.angle=90
		self.explo0=[0,0]
		self.explo1=[0,0]

	def charger(self,fichier):
		def decrypter(texte):
			clee=open(getcwd()+"/ressources/sprites/vaisseau0.png","r").read()
			texte_decry=""
			a,b=0,0
			while a<len(texte):
				nbr=ord(texte[a])-ord(clee[b])
				while nbr<=-1:
					nbr+=256
				texte_decry="".join(texte_decry+str(chr(nbr)))
				b+=1
				a+=1
				if b>=len(clee):b=0
			return texte_decry
		with open("save/"+fichier,"r") as f:
			self.__dict__=eval(decrypter(f.read()))

	def save(self):
		self.initialize()
		texte=str(self.__dict__)
		try:
			clee=open("ressources/sprites/vaisseau0.png","r").read()
			texte_cry,a,b="",0,0
			while a<len(texte):
				nbr=ord(texte[a])+ord(clee[b])
				while nbr>=256:
					nbr-=256
				texte_cry="".join(texte_cry+str(chr(nbr)))
				b+=1
				a+=1
				if b>=len(clee):b=0
			with open("save/"+self.fichier,"w")as f:
				f.write(texte_cry)
		except:return 0
		else:return 1

	def act(self,key,restriction=0):
		sens=0
		if key[K_UP]==1:sens=1
		if key[K_DOWN]==1:sens=-1
		if key[K_RIGHT]==1:
			self.angle-=0.5
			if sens==-1:self.angle-=0.5
			if sens==0:self.angle-=1.5
		if key[K_LEFT]==1:
			self.angle+=0.5
			if sens==-1:self.angle+=0.5
			if sens==0:self.angle+=1.5
		self.angle=modulo(self.angle,360)[0]
		if key[K_KP0] or key[K_KP1]:self.tirer()
		if key[K_RCTRL]:self.tirer(1)
		self.deplacement(sens,restriction)
		if key[K_RSHIFT]:self.activatingShield()
		if self.activateShield==1 and time()-self.lastUsedShield>=self.shield+self.coefTempsBouclier:self.activateShield=0

	def deplacement(self,sens,restriction=0):
		angle=convertAngle(self.angle)
		if not restriction:
			for i in [0,1]:
				if self.pos[i]+self.vitesse*self.coefVitesse*sens*angle[i]<=RESOLUTION[i]-34 and self.pos[i]+self.vitesse*self.coefVitesse*sens*angle[i]>=0:self.pos[i]+=self.vitesse*self.coefVitesse*sens*angle[i]
		else:
			for i in [0,1]:
				pos=self.pos[i]+self.vitesse*self.coefVitesse*sens*angle[i]
				if restriction[i][0]<=pos<=restriction[i][1]:self.pos[i]+=self.vitesse*self.coefVitesse*sens*angle[i]

	def chGun(self,number="x"):
		if number=="x":
			number=self.activate+1
		if number+1<=len(self.equipes):
			self.activate+=1
		else:
			self.activate=0

	def activatingShield(self):
		if time()-(self.lastUsedShield-self.coefTempsBouclier)>=self.cadenceShield:
			self.activateShield=1
			self.lastUsedShield=time()

	def tirer(self,energie=0):
		if energie:
			if time()-self.lastEnergieTire>=self.cadenceEnergieTire:
				self.lastEnergieTire=time()
				self.perdVie(1)
				centre=Vaisseau.calcCenter.move(self.pos[0],self.pos[1]).center
				angle=convertAngle(modulo(self.angle-90,360)[0])
				self.balls.append([[centre[0],centre[1]],int(self.angle),5,10,"ballEnergie",convertAngle(self.angle)])
		else:
			if time()-self.equipes[self.activate][4]>=self.equipes[self.activate][2]:
				centre=Vaisseau.calcCenter.move(self.pos[0],self.pos[1]).center
				angle=convertAngle(modulo(self.angle-90,360)[0])
				# self.balls 	[0]=pos; [1]=angle; [2]=vitesse; [3]=degats; [4]=nom
				# self.gun		[0]=nom; [1]=degats; [2]=cadence; [3]=vitesse; [4]=lastTir
				if self.equipes[self.activate][7]==0:
					self.balls.append([[centre[0]-14*angle[0],centre[1]-14*angle[1]],int(self.angle),self.equipes[self.activate][3],self.equipes[self.activate][1],self.equipes[self.activate][0],convertAngle(self.angle)])
					self.balls.append([[centre[0]+18*angle[0],centre[1]+18*angle[1]],int(self.angle),self.equipes[self.activate][3],self.equipes[self.activate][1],self.equipes[self.activate][0],convertAngle(self.angle)])
				elif self.equipes[self.activate][7]==1:
					self.balls.append([[centre[0],centre[1]],int(modulo(self.angle-20,360)[0]),self.equipes[self.activate][3],self.equipes[self.activate][1],self.equipes[self.activate][0],convertAngle(modulo(self.angle-20,360)[0])])
					self.balls.append([[centre[0],centre[1]],int(modulo(self.angle-10,360)[0]),self.equipes[self.activate][3],self.equipes[self.activate][1],self.equipes[self.activate][0],convertAngle(modulo(self.angle-10,360)[0])])
					self.balls.append([[centre[0],centre[1]],int(self.angle),self.equipes[self.activate][3],self.equipes[self.activate][1],self.equipes[self.activate][0],convertAngle(self.angle)])
					self.balls.append([[centre[0],centre[1]],int(modulo(self.angle+10,360)[0]),self.equipes[self.activate][3],self.equipes[self.activate][1],self.equipes[self.activate][0],convertAngle(modulo(self.angle+10,360)[0])])
					self.balls.append([[centre[0],centre[1]],int(modulo(self.angle+20,360)[0]),self.equipes[self.activate][3],self.equipes[self.activate][1],self.equipes[self.activate][0],convertAngle(modulo(self.angle+20,360)[0])])
				self.equipes[self.activate][4]=time()

	def perdVie(self,cbn):
		cbn-=self.coefDefense+self.blindage
		if cbn<0:return
		self.pdv[1]-=cbn
		self.pdv[0]+=cbn

	def update(self,temps):
		self.lastUsedShield+=temps
		self.lastEnergieTire+=temps
		for i in self.equipes:
			i[4]+=temps

	def equiper(self):
		self.coefVitesse,self.coefEnergie,self.coefTempsBouclier,self.coefDefense,self.coefFurtivite=1,1,0,0,0
		if self.equipes[0][5][0] is not None:
			self.coefVitesse=self.equipes[0][5][0]
			self.coefEnergie=self.equipes[0][5][1]
			self.coefTempsBouclier=self.equipes[0][5][2]
			self.coefDefense=self.equipes[0][5][3]
			self.coefFurtivite=self.equipes[0][5][4]
		if self.equipes[1][5][0] is not None:
			self.coefVitesse+=self.equipes[1][5][0]-1
			self.coefEnergie+=self.equipes[1][5][1]-1
			self.coefTempsBouclier+=self.equipes[1][5][2]
			self.coefDefense+=self.equipes[1][5][3]
			self.coefFurtivite+=self.equipes[1][5][4]
		self.pdv=[]+self.pdvBase
		self.pdv[1]*=self.coefEnergie
		self.totalVie=self.pdvBase[1]*self.coefEnergie
		self.vitesseBase=(self.vitesseVaisseau+self.speed)
		self.vitesse=self.vitesseBase*self.coefVitesse

	def achat(self,objet):
		#~ ["arme",["shotGun class 1",3,0.333,8,[1.1,1.1,-3,0,0]]],
	#~ 5000:["amelioration","temps bouclier +3 secondes",[0,3]],
	#~ 15000:["amelioration","furtivite +5 sencondes",[1,5]],
	#~ 12500:["amelioration","blindage +0.5 points",[2,0.5]]
		if len(objet)==2:
			self.gun.append(objet[1])
		else:
			if objet[2][0]==0:
				self.shield+=objet[2][1]
			elif objet[2][0]==1:
				self.furtivite+=objet[2][1]
			elif objet[2][0]==2:
				self.blindage+=objet[2][1]
			elif objet[2][0]==3:
				self.cadenceShield-=objet[2][1]
			elif objet[2][0]==4:
				self.shield+=objet[2][1]
		self.achats.append(objet)

	def getBonus(self,objet):
		if objet=="vie":
			self.pdv[0]-=10
			if self.pdv[0]<0:self.pdv[0]=0
			self.pdv[1]+=10
			if self.pdv[1]>self.pdvBase[1]:self.pdv[1]=self.pdvBase[1]
		elif objet=="followers":self.bonus["followers"]+=5


class Boss(object):

	def __init__(self,number):
		with open("levels/caracteristique/boss%i.car"%number,"r")as f:f=f.read().replace("\n","")
		self.__dict__=eval(f)
		self.act=eval("self.act%i"%(number))
		self.collisions=eval("self.collisions%i"%(number))

	def act0(self,fenetre=0):
		if not fenetre:
			self.ia0()
			if self.pdvPanneaux[0][1] and time()-self.lastRecup>=self.tempsRecup:
				self.pdvPanneaux[0][1]-=1
				self.pdvPanneaux[0][2]+=1
				self.lastRecup=time()
			if self.pdvPanneaux[1][1] and time()-self.lastRecup>=self.tempsRecup:
				self.pdvPanneaux[1][1]-=1
				self.pdvPanneaux[1][2]+=1
				self.lastRecup=time()
			for i in [0,1,2]:
				if not self.etatTourelles[i]:
					self.deplacement0(i)
					self.tirer0(i)
		else:self.afficher0(fenetre)

	def collisions0(self,i):
		#return 1 si touche
		#return 2 si gagne
		#return 0 si rien
		for j in [0,1]:
			if collision(i[0],[self.posPanneaux[j][0],self.posPanneaux[j][0]+62],[self.posPanneaux[j][1],self.posPanneaux[j][1]+62]):
				if not self.bouclierGeneralise[0]:
					if self.pdvPanneaux[j][2]>0:
						self.pdvPanneaux[j][2]-=i[3]
						self.pdvPanneaux[j][1]+=i[3]/2
						self.pdvPanneaux[j][0]+=i[3]/2+i[3]%2
					else:
						self.etatPanneaux[j]=1
						self.exploPanneaux[j]=[[1,[self.posPanneaux[j][0]+choice(range(62)),self.posPanneaux[j][1]+choice(range(62))],0],
											  [5,[self.posPanneaux[j][0]+choice(range(62)),self.posPanneaux[j][1]+choice(range(62))],0]]
				else:
					self.impact.append([1,[i[0][0],i[0][1]],[0,0]])
				return 1
		for j in [0,1,2]:
			angle=int(self.angleTourelles[j]+90)
			if angle>360:angle-=360
			pos=spriteRotate["boss00"][angle].get_rect(center=spriteRotate["boss00"][0].get_rect().move(self.posTourelles[j]).center)
			if collision(i[0],[pos[0]+22,pos[0]+58],[pos[1]+23,pos[1]+59]):
				if not self.boucliers:
					if self.pdvTourelles[j][2]>0:
						self.pdvTourelles[j][2]-=i[3]
						self.pdvTourelles[j][0]+=i[3]
					else:
						self.etatTourelles[j]=1
						self.exploTourelles[j]=[[1,[self.posTourelles[j][0]+choice(range(32)),self.posTourelles[j][1]+choice(range(32))],0],
												[5,[self.posTourelles[j][0]+choice(range(32)),self.posTourelles[j][1]+choice(range(32))],0]]
						if self.etatTourelles[0]and self.etatTourelles[1]and self.etatTourelles[2]:return 2
				else:
					self.impact.append([1,[i[0][0],i[0][1]],[0,0]])
				return 1
		return 0

	def ia0(self):
		if self.etatPanneaux[0] and self.etatPanneaux[1]:
			self.boucliers=0
			return
		if self.reparation:
			if time()-self.reparation>=self.tempsRecup:
				self.reparation=time()
				if self.etatPanneaux[0]:
					self.pdvPanneaux[0][0]-=1
					self.pdvPanneaux[0][2]+=1
					if self.pdvPanneaux[0][0]==0:
						self.reparation=0
						self.bouclierGeneralise=[0,0]
						self.etatPanneaux[0]=0
				elif self.etatPanneaux[1]:
					self.pdvPanneaux[1][0]-=1
					self.pdvPanneaux[1][2]+=1
					if self.pdvPanneaux[1][0]==0:
						self.reparation=0
						self.bouclierGeneralise=[0,0]
						self.etatPanneaux[1]=0
			return
		if self.etatPanneaux[0] ^ self.etatPanneaux[1]:
			if self.timer:
				if time()-self.timer>=5:
					self.bouclierGeneralise=[1,time()]
					self.reparation=time()
					self.pdvPanneaux[0][0]+=self.pdvPanneaux[0][1]
					self.pdvPanneaux[0][1]=0
					self.pdvPanneaux[1][0]+=self.pdvPanneaux[1][1]
					self.pdvPanneaux[1][1]=0
					self.timer=0
			else:
				self.timer=time()

	def deplacement0(self,i):
		try:angle=fabs(degrees(atan((vaisseau.pos[1]+32-self.posTourelles[i][1])/(self.posTourelles[i][0]-(vaisseau.pos[0]+16)*1.0))))
		except:angle=fabs(degrees(atan((vaisseau.pos[1]+32-self.posTourelles[i][1])/(self.posTourelles[i][0]-(vaisseau.pos[0]+16)*1.0+0.0001))))
		if self.posTourelles[i][0]>vaisseau.pos[0]:angle=modifAngle(angle,270)
		if self.posTourelles[i][1]<vaisseau.pos[1]:angle=modifAngle(angle,180)
		self.angleTourelles[i]=angle

	def tirer0(self,i):
		if time()-self.lastRafale[i]>=self.cadenceRafale and not randrange(100):
			self.lastRafale[i]=time()
			self.rafale[i]+=1

		if 10>self.rafale[i]>0 and time()-self.lastTir[i]>=self.cadence:
			self.lastTir[i]=time()
			angle=convertAngle(self.angleTourelles[i])
			angle1=convertAngle(modulo(self.angleTourelles[i]-90,360)[0])
			angle2=self.angleTourelles[i]
			if angle2>360:
				angle2-=360
			self.balls.append([[self.posTourelles[i][0]+40-12*angle1[0],self.posTourelles[i][1]+40-12*angle1[1]],int(angle2),5,3,[angle[0],angle[1]],"shotGun class 1"])
			self.balls.append([[self.posTourelles[i][0]+40+16*angle1[0],self.posTourelles[i][1]+40+16*angle1[1]],int(angle2),5,3,[angle[0],angle[1]],"shotGun class 1"])
			#[0]=pos; [1]=angle; [2]=vitesse; [3]=degats; [4]= % x et y; [5]=nom
			self.rafale[i]+=1
			if self.rafale[i]==10:
				self.rafale[i]=0

	def afficher0(self,fenetre):
		for i in range(0,RESOLUTION[0],150):
			fenetre.blit(sprites["boss01"],(i,0))
		fenetre.blit(sprites["boss0"],((RESOLUTION[0]-800)/2.0,0))
		for i in[0,1,2]:
			angle=int(self.angleTourelles[i]+90)
			if angle>360:angle-=360
			pos=spriteRotate["boss00"][angle].get_rect(center=spriteRotate["boss00"][0].get_rect().move(self.posTourelles[i]).center)
			fenetre.blit(spriteRotate["boss00"][angle],pos)
			fenetre.subsurface(self.posTourelles[i][0]+14,self.posTourelles[i][1]+19,50,10).fill((118,118,118))

			a,b=0,(self.pdvTourelles[i][0]+self.pdvTourelles[i][1]+self.pdvTourelles[i][2]-1)/4.0
			c=0
			for j in range(self.pdvTourelles[i][0]):
				if a==0:fenetre.blit(sprites["barreg1"],(20+self.posTourelles[i][0]+a*3-b*1.5,self.posTourelles[i][1]-50+c*8))
				elif a==b:fenetre.blit(sprites["barreg3"],(20+self.posTourelles[i][0]+a*3-b*1.5,self.posTourelles[i][1]-50+c*8))
				else:fenetre.blit(sprites["barreg2"],(20+self.posTourelles[i][0]+a*3-b*1.5,self.posTourelles[i][1]-50+c*8))
				if a==50:
					c+=1
					a=0
					a+=1
			for j in range(self.pdvTourelles[i][1]):
				if a==0:fenetre.blit(sprites["barrer1"],(20+self.posTourelles[i][0]+a*3-b*1.5,self.posTourelles[i][1]-50+c*8))
				elif a==b:fenetre.blit(sprites["barrer3"],(20+self.posTourelles[i][0]+a*3-b*1.5,self.posTourelles[i][1]-50+c*8))
				else:fenetre.blit(sprites["barrer2"],(20+self.posTourelles[i][0]+a*3-b*1.5,self.posTourelles[i][1]-50+c*8))
				if a==50:
					c+=1
					a=0
				a+=1
			for j in range(self.pdvTourelles[i][2]):
				if a==0:fenetre.blit(sprites["barrev1"],(20+self.posTourelles[i][0]+a*3-b*1.5,self.posTourelles[i][1]-50+c*8))
				elif a==b:fenetre.blit(sprites["barrev3"],(20+self.posTourelles[i][0]+a*3-b*1.5,self.posTourelles[i][1]-50+c*8))
				else:fenetre.blit(sprites["barrev2"],(20+self.posTourelles[i][0]+a*3-b*1.5,self.posTourelles[i][1]-50+c*8))
				if a==50:
					c+=1
					a=0
				a+=1
			if self.etatTourelles[i]:
				for j in self.exploTourelles[i]:
					try:fenetre.blit(sprites["expl0%i"%(j[0]-1)],(j[1][0],j[1][1]))
					except:
						try:fenetre.blit(sprites["expl%i"%(j[0]-1)],(j[1][0],j[1][1]))
						except:pass
					j[2]+=1
					if j[2]>=5:
						j[0]+=1
						j[2]=0
					if j[0]>=11:
						j=[]+[1,[self.posTourelles[i][0]+choice(range(32)),self.posTourelles[i][1]+choice(range(32))],0]

		for i in [0,1]:
			a,b=0,(self.pdvPanneaux[i][0]+self.pdvPanneaux[i][1]+self.pdvPanneaux[i][2]-1)/4.0
			c=0
			for j in range(self.pdvPanneaux[i][0]):
				if a==0:fenetre.blit(sprites["barreg1"],(20+self.posPanneaux[i][0]+a*3-b*1.5,self.posPanneaux[i][1]-50+c*8))
				elif a==b:fenetre.blit(sprites["barreg3"],(20+self.posPanneaux[i][0]+a*3-b*1.5,self.posPanneaux[i][1]-50+c*8))
				else:fenetre.blit(sprites["barreg2"],(20+self.posPanneaux[i][0]+a*3-b*1.5,self.posPanneaux[i][1]-50+c*8))
				if a==50:
					c+=1
					a=0
				a+=1
			for j in range(self.pdvPanneaux[i][1]):
				if a==0:fenetre.blit(sprites["barrer1"],(20+self.posPanneaux[i][0]+a*3-b*1.5,self.posPanneaux[i][1]-50+c*8))
				elif a==b:fenetre.blit(sprites["barrer3"],(20+self.posPanneaux[i][0]+a*3-b*1.5,self.posPanneaux[i][1]-50+c*8))
				else:fenetre.blit(sprites["barrer2"],(20+self.posPanneaux[i][0]+a*3-b*1.5,self.posPanneaux[i][1]-50+c*8))
				if a==50:
					c+=1
					a=0
				a+=1
			for j in range(self.pdvPanneaux[i][2]):
				if a==0:fenetre.blit(sprites["barrev1"],(20+self.posPanneaux[i][0]+a*3-b*1.5,self.posPanneaux[i][1]-50+c*8))
				elif a==b:fenetre.blit(sprites["barrev3"],(20+self.posPanneaux[i][0]+a*3-b*1.5,self.posPanneaux[i][1]-50+c*8))
				else:fenetre.blit(sprites["barrev2"],(20+self.posPanneaux[i][0]+a*3-b*1.5,self.posPanneaux[i][1]-50+c*8))
				if a==50:
					c+=1
					a=0
				a+=1
			if self.etatPanneaux[i]:
				for j in self.exploPanneaux[i]:
					try:fenetre.blit(sprites["expl0%i"%(j[0]-1)],(j[1][0],j[1][1]))
					except:
						try:fenetre.blit(sprites["expl%i"%(j[0]-1)],(j[1][0],j[1][1]))
						except:pass
					j[2]+=1
					if j[2]>=5:
						j[0]+=1
						j[2]=0
					if j[0]>=11:
						j=[]+[1,[self.posPanneaux[i][0]+choice(range(62)),self.posPanneaux[i][1]+choice(range(62))],0]
		if self.boucliers:
			for i in [0,1,2]:
				fenetre.blit(sprites["bouclier"],(self.posTourelles[i][0]+7,self.posTourelles[i][1]+7))
		if self.bouclierGeneralise[0]:
			for i in [0,1]:
				fenetre.blit(sprites["bouclier"],(self.posPanneaux[i][0],self.posPanneaux[i][1]))
		delete=[]
		for i in self.impact:
			fenetre.blit(sprites["expl20%i"%(i[0]-1)],(i[1][0],i[1][1]))
			i[2][0]+=1
			if i[2][0]==5:
				i[2][0]=0
				i[0]+=a
			if i[0]==5:
				i[0]=1
				i[2][1]+=1
			if i[2][1]==2:
				delete.append(i)
		for i in delete:self.impact.remove(i)

	def act1(self,fenetre=0):
		if not fenetre:self.ia1()
		else:self.afficher1(fenetre)

	def ia1(self):

		try:self.target=fabs(degrees(atan((vaisseau.pos[1]+32-self.pos[1])/(self.pos[0]-(vaisseau.pos[0]+16)*1.0))))
		except:self.target=fabs(degrees(atan((vaisseau.pos[1]+32-self.pos[1])/(self.pos[0]-(vaisseau.pos[0]+16)*1.0+0.0001))))
		if self.pos[0]>vaisseau.pos[0]:self.target=modifAngle(self.target,270)
		if self.pos[1]<vaisseau.pos[1]:self.target=modifAngle(self.target,180)

		if time()-self.lastChDir>=10 or not randrange(5000):
			self.lastChDir=time()
			self.posTarget=[randrange(100,RESOLUTION[0]-100),randrange(50,RESOLUTION[1]-50)]
			if not self.pos[0]-(self.posTarget[0]):self.angleTarget=fabs(degrees(atan((self.posTarget[1]-self.pos[1])/(self.pos[0]-(self.posTarget[0])+0.1))))
			else:self.angleTarget=fabs(degrees(atan((self.posTarget[1]-self.pos[1])/(self.pos[0]-(self.posTarget[0])))))
			if self.pos[0]>self.posTarget[0]:self.angleTarget=modifAngle(self.angleTarget,270)
			if self.pos[1]<self.posTarget[1]:self.angleTarget=modifAngle(self.angleTarget,180)

		if not collision(self.pos,(self.posTarget[0]-50,self.posTarget[0]+50),(self.posTarget[1]-50,self.posTarget[1]+50)):
			angle=convertAngle(self.angleTarget)
			self.pos[0]+=self.vitesse*angle[0]
			self.pos[1]+=self.vitesse*angle[1]

		if not self.activateShield and time()-self.lastShield>=60 or not randrange(5000):
			self.activateShield=1
			self.lastShield=time()
		elif self.activateShield and time()-self.lastShield>=10:
			self.activateShield=0

		if time()-self.lastRafale>=60 or self.rafale[1]:
			self.lastRafale=time()
			self.rafale1()

		elif time()-self.lastTir>=1 and len(self.balls)<=9:
			self.tirer1()

	def rafale1(self):
		if time()-self.rafale[1]>=0.25:
			self.rafale[0]+=1
			self.rafale[1]=time()
			angle=convertAngle(self.target)
			self.balls.append([[self.pos[0],self.pos[1]],int(self.target),7,5,[]+angle,"five shot class 3"])
			self.balls.append([[self.pos[0],self.pos[1]],int(modulo(self.target+15,360)[0]),10,3,convertAngle(modulo(self.target+15,360)[0]),"five shot class 2"])
			self.balls.append([[self.pos[0],self.pos[1]],int(modulo(self.target-15,360)[0]),10,3,convertAngle(modulo(self.target-15,360)[0]),"five shot class 2"])
		if self.rafale[0]>=15:
			self.rafale=[0,0]

	def tirer1(self):
		self.lastTir=time()
		angle=convertAngle(self.target)
		angle2=convertAngle(modulo(self.target-90,360)[0])
		self.balls.append([[self.pos[0]+14*angle2[0],self.pos[1]+14*angle2[1]],int(self.target),7,5,[]+angle,"shotGun class 2"])
		self.balls.append([[self.pos[0]-18*angle2[0],self.pos[1]-18*angle2[1]],int(self.target),7,5,[]+angle,"shotGun class 2"])

	def collisions1(self,i):
		#return 1 si touche
		#return 2 si gagne
		#return 0 si rien
		# i= [0]=pos; [1]=angle; [2]=vitesse; [3]=degats; [4]=nom
		if vaisseaux[2][modulo(int(self.target)-90,360)[0]].get_rect().move(self.pos[0],self.pos[1]).colliderect(ballPerso[i[4]][i[1]].get_rect().move(i[0][0],i[0][1])):
			pdv=i[3]-1.5
			if pdv<0:pdv=0
			if not self.activateShield:
				if self.pdv[self.niveauPdv]-pdv<=0:
					if self.niveauPdv==2:return 2
					else:
						self.pdv[self.niveauPdv]=0
						self.pdv[self.niveauPdv]-=pdv-self.pdv[self.niveauPdv]
						self.niveauPdv-=1
						self.explo.append([0,0,i[0]])
						if self.niveauPdv==6:
							self.prim,self.sec=self.sec,(255,0,255)
						if self.niveauPdv==5:
							self.prim,self.sec=self.sec,(0,255,255)
						if self.niveauPdv==4:
							self.prim,self.sec=self.sec,(0,0,255)
						if self.niveauPdv==3:
							self.prim,self.sec=self.sec,(0,255,0)
						if self.niveauPdv==2:
							self.prim,self.sec=self.sec,(255,0,0)
						return 1
				else:
					self.pdv[self.niveauPdv]-=pdv
					self.explo.append([0,0,i[0]])
					return 1
			else:
				self.impact.append([0,0,0,[i[0][0],i[0][1]]])
				return 0
		else:
			return 0

	def afficher1(self,fenetre):
		fenetre.blit(vaisseaux[0][modulo(int(self.target)-90,360)[0]],(self.pos[0],self.pos[1]))
		destruct=[]
		for i in self.explo:
			try:fenetre.blit(sprites["expl0%i"%(i[1])],tuple(i[2]))
			except:fenetre.blit(sprites["expl%i"%(i[1])],tuple(i[2]))
			i[0]+=1
			if i[0]==10:
				i[0]=0
				i[1]+=1
			if i[1]==11:destruct.append(i)
		for i in destruct:self.explo.remove(i)
		destruct=[]
		for i in self.impact:
			fenetre.blit(sprites["expl20%i"%(i[2])],tuple(i[3]))
			i[0]+=1
			if i[0]==10:
				i[2]+=1
				i[0]=0
			if i[2]==5:
				i[2]=0
				i[1]+=1
			if i[1]==5:destruct.append(i)
		for i in destruct:self.impact.remove(i)
		if self.activateShield:
			fenetre.blit(sprites["bouclier"],(self.pos[0]-30,self.pos[1]-20))

		pos0=self.pos[0]
		pos1=self.pos[1]
		if pos0>RESOLUTION[0]-170:pos0=RESOLUTION[0]-170
		elif pos0<170:pos0=170
		if pos1<=0:pos0=1
		elif pos1>RESOLUTION[1]-7:pos1=RESOLUTION[1]-7
		try:
			fenetre.subsurface(pos0-144,pos1-16,304,5).fill((128,128,128))
			fenetre.subsurface(pos0-142,pos1-15,self.pdv[self.niveauPdv]*3,3).fill(self.prim)
			fenetre.subsurface(pos0-142+self.pdv[self.niveauPdv]*3,pos1-15,(100-self.pdv[self.niveauPdv])*3,3).fill(self.sec)
		except:pass








	def collisions2(self,i):
		pass



	def act2(self,fenetre=0):
		if not fenetre:self.ia2()
		else:self.afficher2(fenetre)



	def ia2(self):
		pass



	def afficher2(self):
		pass









	def act3(self,fenetre=0):
		self.act0(fenetre)
		
	def collisions3(self,i):
		return self.collisions0(i)
	
	def act4(self,fenetre=0):
		self.act0(fenetre)
		
	def collisions4(self,i):
		return self.collisions0(i)


class Follower(object):
	vitesse=5

	def __init__(self,cible,pos):
		self.pos=[]+pos
		self.cible=cible
		self.angle=0

	def avancer(self):
		for i in [0,1]:
			if self.pos[i]>self.cible.pos[i]:self.pos[i]+=-Follower.vitesse
			elif self.pos[i]<self.cible.pos[i]:self.pos[i]+=Follower.vitesse

		try:angle=fabs(degrees(atan((self.cible.pos[1]+16-self.pos[1])/(self.pos[0]-(self.cible.pos[0]+16)*1.0))))
		except:angle=fabs(degrees(atan((self.cible.pos[1]+16-self.pos[1])/(self.pos[0]-(self.cible.pos[0]+16)*1.0+0.0001))))
		if self.pos[0]>self.cible.pos[0]:angle=modifAngle(angle,270)
		if self.pos[1]<self.cible.pos[1]:angle=modifAngle(angle,180)
		self.angle=int(angle)


class Bonus(object):

	def __init__(self,pos,objet):
		self.pos=[]+pos
		self.objet=objet
		self.step=0
		self.degres=0
		self.timer=time()

	def afficher(self,fenetre):
		if self.objet=="vie":
			fenetre.blit(sprites[self.objet+str(self.step)],(self.pos[0],self.pos[1]))
			if time()-self.timer>=0.25:
				self.timer=time()
				self.step+=1
				if self.step==4:self.step=0
		elif self.objet=="followers":
			fenetre.blit(spriteRotate[self.objet][self.degres],(self.pos[0],self.pos[1]))
			if time()-self.timer>=0.125:
				self.timer=time()
				self.degres+=15
				if self.degres==360:self.degres=0


mixer.init()
fenetre=Fenetre(RESOLUTION[0],RESOLUTION[1],1,FULLSCREEN)

sprites={x.replace(".png",""):image.load(getcwd()+"/ressources/sprites/"+x).convert_alpha()for x in listdir(getcwd()+"/ressources/sprites")}
spriteRotate={x.replace(".png",""):{y:transform.rotate(image.load(getcwd()+"/ressources/sprites/"+x+".png").convert_alpha(),y)for y in range(361)}for x in ["boss00","followers","follower"]}
decors={x.replace(".png",""):image.load(getcwd()+"/ressources/decors/"+x).convert_alpha()for x in listdir(getcwd()+"/ressources/decors")}
vaisseaux=[{i:transform.rotate(image.load("ressources/sprites/vaisseau"+str(j)+".png").convert_alpha(),i)for i in range(361)}for j in range(22)]
ballPerso={i:{j:transform.rotate(image.load("ressources/sprites/"+str(i)+".png").convert_alpha(),j)for j in range(361)} for i in ["primaire","secondaire","ballEnergie","shotGun class 1","shotGun class 2","shotGun class 3","five shot class 4","five shot class 5",'five shot class 1','five shot class 2','five shot class 3',"follower", "three shot 1", "three shot 2", "three shot 3"]}

# non alpha
decors["map4"]=image.load(getcwd()+"/ressources/decors/map4.png").convert()
sprites["boss0"]=image.load(getcwd()+"/ressources/sprites/boss0.png").convert()
sprites["boss01"]=image.load(getcwd()+"/ressources/sprites/boss01.png").convert()


collision=lambda a,b,c:b[0]<a[0]<b[1] and c[0]<a[1]<c[1]

def cadre(fenetre,transparence,haut,bas,largeur=5,couleur=(255,255,255),bg=(0,0,0)):
	try:
		if not transparence:
			fenetre.subsurface(haut[0],haut[1],bas[0]-haut[0],bas[1]-haut[1]).fill(couleur)
			fenetre.subsurface(haut[0]+largeur,haut[1]+largeur,bas[0]-haut[0]-largeur*2,bas[1]-haut[1]-largeur*2).fill(bg)
		else:
			fenetre.subsurface(haut[0],haut[1],largeur,bas[1]-haut[1]).fill(couleur)
			fenetre.subsurface(haut[0],haut[1],bas[0]-haut[0],largeur).fill(couleur)
			fenetre.subsurface(haut[0],bas[1],bas[0]-haut[0],largeur).fill(couleur)
			fenetre.subsurface(bas[0],haut[1],largeur,bas[1]-haut[1]).fill(couleur)
			fenetre.subsurface(bas[0],bas[1],largeur,largeur).fill(couleur)
	except:pass

def convertAngle(angle):
	if angle>360:angle-=360
	elif angle<0:angle+=360
	if angle>90:angle90=fabs(90-(angle-90))
	else:angle90=angle
	if angle90>=90:angle90=fabs(angle90-180)
	y=1/90.0*angle90
	x=1-y
	if angle>90 and angle<270:x*=-1
	if angle>0 and angle<180:y*=-1
	return [x,y]

def modulo(nombre,modul):
	degres=0
	while nombre>=modul:
		nombre-=modul
		degres+=1
	while nombre<0:
		nombre+=modul
		degres+=1
	return nombre,degres

def modifAngle(angle,symetrie):
	if symetrie>360:symetrie-=360
	if angle>=symetrie:angle-=(angle-symetrie)*2
	else:angle+=(symetrie-angle)*2
	if angle<0:angle+=360
	elif angle>=360:angle-=360
	return angle


while 1:
	fenetre.etape(fenetre.number)
