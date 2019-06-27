#!/usr/bin/python3

import csv
import sys
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup as Soup
from bs4 import BeautifulSoup

import re

from pathlib2 import Path
import pandas as pd

csv.field_size_limit(sys.maxsize)

current_motifs = []

def CSV_to_trainingSet(path: str):
	_macro_preced = None
	current_doc = []
	nb_files = []
	index = 0
	print(path)
	pattern = r"|=|\+|\*|`|ù|%|«|»|\^|¨|/|&|@|#|§|°|\$|£|~|=|<|>|\t"

	with open(path, newline='') as csvfile:
		for _,_,_,_,_,_,_,_,_,_,_, _macro_current, _,_,_,_,_,_motifs_, _text_ in  csv.reader(csvfile, delimiter=';'):
			if _text_ != "text":
				if _macro_current != _macro_preced:
					_macro_preced = _macro_current
					if _macro_current == 'Entete':
						current_doc.append(_macro_current + '\n')
					current_doc.append('==========\n')

				current_doc.append(re.sub(pattern, '', _text_) + '\n')

				if _motifs_ == "motifs":
					if not _text_ in current_motifs:
						current_motifs.append(re.sub(pattern, '', _text_) + '\n')


		for line in current_doc:
			title_file = "Train" + str(index) + ".ref"
			file = open("data-n-micros/" + title_file, "a")

			if line in current_motifs:
				file.write('==========\n')

			if line != 'Entete\n':
				file.write(line)
			else:
				file.write('==========\n')
				file.close()
				index += 1

	print(len(current_motifs), len(nb_files))


def CSV_Clean01_to_trainingSet(path: str):
	_macro_preced = None
	current_doc = []
	index = 0
	print(path)
	pattern = r"|=|\+|\*|`|ù|%|«|»|\^|¨|/|&|@|#|§|°|\$|£|~|=|<|>|\t"
	with open(path, newline='') as csvfile:
		for _,_,_macro_current,_,_text_,_,_ in  csv.reader(csvfile, delimiter=','):
			if _text_ != "text":
				if _macro_current != _macro_preced:
					_macro_preced = _macro_current
					if _macro_current == 'Entete':
						current_doc.append(_macro_current + '\n')
					current_doc.append('==========\n')

				current_doc.append(re.sub(pattern, '', _text_) + '\n')

		for line in current_doc:
			title_file = "Train-newZ" + str(index) + ".ref"
			file = open("data-new-n-micros/" + title_file, "a")

			if line in current_motifs:
				file.write('==========\n')

			if line != 'Entete\n':
				file.write(line)
			else:
				file.write('==========\n')
				file.close()
				index += 1

def CSV_Clean02_tsv_to_trainingSet(path: str):
	_macro_preced = None
	current_doc = []
	index = 0
	print(path)
	pattern = r"|=|\+|\*|`|ù|%|«|»|\^|¨|/|&|@|#|§|°|\$|£|~|=|<|>|\t"
	pattern_sur = r"Sur (l'|le|la|les)"
	with open(path, newline='') as csvfile:
		for _,_text_,_macro_current,_,_,_,_ in  csv.reader(csvfile, delimiter='\t'):
			if _text_ != "text":
				if _macro_current != _macro_preced:
					_macro_preced = _macro_current
					if _macro_current == 'Ent':
						current_doc.append(_macro_current + '\n')
					current_doc.append('==========\n')
				current_doc.append(re.sub(pattern, '', _text_) + '\n')

		for line in current_doc:
			title_file = "Train-newZ" + str(index) + ".ref"
			file = open("data-2new-n-micros/" + title_file, "a")

			if re.search(pattern_sur, line):
				# print(line)
				file.write('==========\n')
			if line != 'Ent\n':
				file.write(line)
			else:
				file.write('==========\n')
				file.close()
				index += 1

def is_excluded_title(text_normalized):
	return re.search(r'\\bmoyen(s)?\\b|\\bcour\\b|\\barr(ê|e)t(s?)\\b|\\bbranche(s)?\\b|\\bpourvoi(s)?\\b|appréciation souveraine', text_normalized)

def get_xml_files(path : str):
    all_objects = Path(path).glob('**/*.xml')
    files = [str(p) for p in all_objects if p.is_file()]
    return files

pattern_contains = re.compile(r'^.{0,6}\bsur\b')
pattern_contains_sreach = re.compile(r'^.{0,6}(sur ce|sur ce la cour|sur quoi|sur quoi la cour|sur (l )?appel (?!en).*|sur requ.te.*|sur renvoi.*)')

pattern_macros_4z = re.compile(r'^\bsur la procédure\b|motifs|\bfaits\b|par ces motifs|\bprocédure\b|expose du litige|motifs de la decision|sur ce|')

pattern_normalize = re.compile(r'^(sur )?((le|l|les|la|une|un|ce|sa|ses|de|mon|son|des|à|leur|cette) )?')

def contains_title(text_normalized: str) -> bool:
	r1 = len(pattern_contains.findall(text_normalized)) > 0
	# r2 = len(text) <= 100
	r3 = not len(pattern_contains_sreach.findall(text_normalized))
	return r1 & r3


def normalize_title_text(texts: str) -> bool:
	return pattern_normalize.sub("", texts.lower())

# [(a,x) for a in range(1,2) for x in range(1,10)]


def macros_4z(text: str) -> bool:
	return pattern_macros_4z.findall(text)


pattern_br = re.compile(r"-|=|\*|`|%|\^|¨|§|/|&|@|#|=|°\$|£|<|>|Oo|oO|\t|")


def xml_to_Texte(path: str, data_file: str):

	infile = open(path, 'r')

	Text_CONTENU_Brut = []
	Text_CONTENU_Brut.append("==========\n")
	counte = 0
	contents = infile.read()
	soup = BeautifulSoup(contents,'xml')
	Text_CONTENU = []
	if soup.find(re.compile("CONTENU|NonStructure")) is not None: #CONTENU "\bCONTENU\b|\bNonStructure\b
		Text_CONTENU = soup.find(re.compile("CONTENU|NonStructure")).text
		Text_CONTENU = re.sub("<br/>", "\n", Text_CONTENU)
		Text_CONTENU = pattern_br.sub("", Text_CONTENU)
	else:
		print("Error in Path : ", path)

	if len(Text_CONTENU) > 0:
		for line in Text_CONTENU.split("\n"):
			line = line.strip()
			if line != '' :
				# print(line)
				title = macros_4z(line.lower())
				text_normalized = normalize_title_text(line)
				if contains_title(text_normalized):
					counte += 1
					Text_CONTENU_Brut.append("==========\n" + line+'\n')
				else:
					if title and len(line) <= 50:
						counte += 1
						Text_CONTENU_Brut.append("==========\n")

					Text_CONTENU_Brut.append(line + '\n')

		if counte >= 5:
			Text_CONTENU_Brut.append("==========")
			print(data_file, path)
			with open(data_file, 'w') as save_txt:
				save_txt.writelines(Text_CONTENU_Brut)

def loop():
	#print(len(get_xml_files("/Users/sabbar/Desktop/ELS/extr/data-brut-xml/juri/")))
	for i, file_xml in enumerate(get_xml_files("/home/ec2-user/ELS/py3/clean_/data/Mega-data/0/")):
		data_file = "1-Training/Train" + str(i) + ".ref"
		#print(i, data_file, file_xml)
		xml_to_Texte(file_xml, data_file)

#loop()

def get_ref_files(path : str):
    all_objects = Path(path).glob('**/*.ref')
    files = [str(p) for p in all_objects if p.is_file()]
    return files


def isole_title( path: str, data_file: str):
	file = open(path, "r")
	Text_CONTENU_sans_title = []
	tmp = 0
	for line in file:
		# print(line)
		if tmp != 0:
			tmp = 0
		else:
			Text_CONTENU_sans_title.append(line)
		if line == "==========\n":
			tmp = 1

	with open(data_file, 'w') as save_txt:
		for i, l in enumerate(Text_CONTENU_sans_title):
			if len(Text_CONTENU_sans_title) > i +1:
			 	if l != Text_CONTENU_sans_title[i+1:i+2][0]:
			 		save_txt.write(l)
		save_txt.write("==========")



def loop_isole_title():
	for i, file_ref in enumerate(get_ref_files("/home/ec2-user/ELS/Zoning-micro/data/0-5117-data/")):
		data_file = "without-Title/Train" + str(i) + ".ref"
		isole_title(file_ref, data_file)

loop_isole_title()
print("finish")

#print(len(get_xml_files("/home/ec2-user/ELS/py3/clean_/data/Mega-data/0/")))
# xml_to_Texte( "/Users/sabbar/Desktop/ELS/extr/data-brut-xml/juri/capp/global/JURI/TEXT/00/00/06/93/44/JURITEXT000006934496.xml", "file_xml.txt")
# CSV_to_trainingSet("/Users/sabbar/Desktop/ELS/extr/annatation-clean/V7_zonage-Tableau-micro.csv")
# CSV_Clean01_to_trainingSet("/Users/sabbar/Desktop/ELS/zoning_legal_cases-dev/data/data/annotations-clean.csv")
# CSV_Clean02_tsv_to_trainingSet("/Users/sabbar/Desktop/ELS/zoning_legal_cases-dev/data/data/annotations-jurica.tsv")









