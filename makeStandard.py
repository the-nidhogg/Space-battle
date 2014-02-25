#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import system,getcwd,chdir
lettres="".join([chr(x)for x in range(65,91)+range(97,123)])
def stdard(nom):
	with open(nom,"r")as f:f=f.read()
	count=0
	comment=0
	txt=""
	for i in range(len(f)):
		if i+1==len(f):
			txt+=f[i]
			break
		if "#" in f[i] and not count%2:comment=1
		if comment and f[i]=="\n":comment=0
		if f[i]=="\"" and (f[i-1]!="\\" or (f[i-1]=="\\" and f[i-2]=="\\")) and not comment:count+=1
		if count%2 or comment:
			txt+=f[i]
			continue
		if f[i+1]in"+-*><!=/%"and f[i]not in" +-*/%!=><":
			txt+=f[i]+" "
			continue
		if f[i-1]in"+-*><!="and f[i]not in" =\"'":txt+=" "
		if f[i-1]in","and f[i]not in " \n\"'":txt+=" "
		if f[i-1]in")"and f[i]in lettres:txt+=" "
		if f[i-3:i]in[" in"]and f[i]in"(":txt+=" "
		if f[i-3:i]in[" in"]and f[i]in"(":txt+=" "
		if f[i]==":" and f[i+1]not in"\n":
			fini=0
			var=1
			cnt=[1,0,0]
			cntlettres=""
			while not fini:
				cntlettres+=f[i-var]
				if f[i-var]=="[":cnt[1]+=1
				if f[i-var]=="{":cnt[2]+=1
				if f[i-var]=="]":cnt[1]-=1
				if f[i-var]=="}":cnt[2]-=1
				if f[i-var]=="\t":cnt[0]+=1
				if f[i-var]=="\n":
					if not cnt[1]+cnt[2] and "adbmal"not in cntlettres:txt+=":\n"+"\t"*cnt[0]
					else:txt+=":"
					fini=1
				var+=1
			continue
		if f[i]==";":
			a=1
			var=1
			while f[i-var]!="\n":
				if f[i-var]=="\t":a+=1
				var+=1
			txt+="\n"+"\t"*a
			continue
		if f[i]=="\"" and f[i-1]=="=":txt+=" "
		txt+=f[i]
	with open("out","w")as g:g.write(txt)
while 1:
	nom=raw_input("chemin du programme a metttre dans les standards: ")
	if nom[:2]=="cd":
		chdir(getcwd()+"/"+nom[3:])
		continue
	stdard(nom)
