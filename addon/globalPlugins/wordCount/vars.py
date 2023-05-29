# -*- coding: UTF-8 -*-
# WordCount add-on: Module for variables
# written by Rui Fontes <rui.fontes@tiflotecnia.com> Ângelo Abrantes <ampa4374@gmail.com> and Abel Passos do Nascimento Jr. <abel.passos@gmail.com>
# Copyright (C) 2022-2023 Rui Fontes <rui.fontes@tiflotecnia.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# import the necessary modules.
from .configPanel import *
import api
import ui
import textInfos
import collections
import string

# To start the translation process
addonHandler.initTranslation()

obj = None
text1 = ""
ourWord = ""
optionsList = [_("Alphabetically"), _("By number of occurences")]

def createInfo(pos):
	global obj
	obj = api.getFocusObject()
	treeInterceptor = obj.treeInterceptor
	if hasattr (treeInterceptor, 'TextInfo') and not treeInterceptor.passThrough:
		obj = treeInterceptor
	try:
		if pos == "sel":
			info = obj.makeTextInfo (textInfos.POSITION_SELECTION)
		else:
			info = obj.makeTextInfo (textInfos.POSITION_ALL)
	except (RuntimeError, NotImplementedError):
		info = None
	if not info or info.isCollapsed:
		# Translators: Message to announce when no text is selected
		ui.message(_("select some text first."))
		info = None
	return info

def createInfo1():
	info = obj.makeTextInfo(textInfos.POSITION_ALL)
	return info

	# Replace symbols and punctuation by a space to allow a better spliting of words...
def cleanPunctuation(text2):
	toRemove = string.punctuation.replace("\'", "").replace("-", "").replace("@", "").replace(" ", "")+"“"+"”"+"—"+"…"
	for z in range(len(toRemove)):
		X = toRemove[z]
		text2 = text2.translate(str.maketrans(X, " "))
	return text2

def countWords():
	info = createInfo("sel")
	# Prepare to count words
	text1 = info.text
	text2 = str(text1).lower()
	text2 = cleanPunctuation(text2)
	print(text2)
	return info, text2

def ListOfWords():
	info = createInfo("all")
	global text1
	text1 = info.text
	text2 = str(text1).lower()
	text2 = cleanPunctuation(text2)
	words = text2.split()
	words = sorted(words)
	wordList = collections.Counter([word for word in words if word not in ("-", "\'")]).most_common()
	return wordList, text1

def loadWords(wordList):
	# Load the word list.
	global wdsList, wdsSortedList
	wdsSortedList = []
	for word, count in wordList:
		if word[0].isalpha():
			wdsSortedList.append('{word}, {count}'.format(word=word, count=count))
		else:
			pass
	wdsList = sorted(wdsSortedList)
	if len(wordList) is 0:
		wdsList.append(_("There are no words"))
		wdsSortedList.append(_("There are no words"))
	return wdsList, wdsSortedList

def loadLines(ourWord):
	# Load the lines with our word.
	lns = text1.splitlines()
	lns1 = []
	lns2 = []
	for line in lns:
		if ourWord in line.lower():
			# Get all lines containing our word
			lns2.append((line, lns.index(line)))
	for line in lns2:
		# Divide line in 3 parts: 0=before ourWord, 1=ourWord and 2=after ourWord
		wordCheck = line[0].lower().partition(ourWord)
		if " "+ourWord +" " in line[0].lower():
			lns1.append((line[0], line[1]))
		# Check if the line starts with ourWord
		elif line[0].lower().startswith(ourWord) is True:
			# Check if 2 starts with a letter. If so, the line contains ourWord, but making part of other and not as a sepparate word... So we want it if not.
			if wordCheck[2][0].isalpha() is False:
				lns1.append((line[0], line[1]))
		# Check if line ends with ourWord
		elif line[0].lower().endswith(ourWord) is True:
			# Check if last character of 0 is a letter. If so, ourWord is not present as a word... So, we want it if not.
			if wordCheck[0][-1].isalpha() is False:
				lns1.append((line[0], line[1]))
		# OurWord is in the middle of the line, so check is it is a word or part of a word...
		else:
			if wordCheck[0][-1].isalpha() is True:
				pass
			elif wordCheck[2][0].isalpha() is True:
				pass
			else:
				lns1.append((line[0], line[1]))
	return lns1
