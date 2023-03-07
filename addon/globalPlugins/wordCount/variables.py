# -*- coding: UTF-8 -*-
# Part of wordCount add-on
# Module for variables
# written by Rui Fontes <rui.fontes@tiflotecnia.com> Ângelo Abrantes <ampa4374@gmail.com> and Abel Passos do Nascimento Jr. <abel.passos@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# import the necessary modules.
from .update import *
import api
import textInfos
from textInfos import offsets
import collections
import string
# For translation process
addonHandler.initTranslation()

text = ""
text1 = ""
text2 = ""
wordList = []
wdsList = []
wdsList1 = []
lns1 = []
ourWord = ""
optionsList = [_("Alphabetically"), _("By number of occurences")]

def countWords():
	global mute
	mute = False
	obj = api.getFocusObject()
	treeInterceptor = obj.treeInterceptor
	if hasattr(treeInterceptor,'TextInfo') and not treeInterceptor.passThrough:
		obj = treeInterceptor
	try:
		global info
		info = obj.makeTextInfo(textInfos.POSITION_SELECTION)
	except (RuntimeError, NotImplementedError):
		info = None
	if not info or info.isCollapsed:
		mute = True
		# Translators: Message to announce when no text is selected
		ui.message(_("select some text first."))
	else:
		# Prepare to count words
		global text1, text2
		text1 = info.text
		text2 = str(text1).lower()
		# A dictionary to replace symbols and punctuation by a space to allow a better spliting of words...
		toRemove = string.punctuation.replace("\'", "").replace("-", "").replace("@", "").replace(" ", "")+"“"+"”"+"—"+"…"
		for z in range(len(toRemove)):
			X = toRemove[z]
			text2 = text2.translate(str.maketrans(X, " "))

def ListOfWords():
	obj = api.getFocusObject()
	treeInterceptor = obj.treeInterceptor
	if hasattr (treeInterceptor, 'TextInfo') and not treeInterceptor.passThrough:
		obj = treeInterceptor
	try:
		info = obj.makeTextInfo (textInfos.POSITION_ALL)
	except (RuntimeError, NotImplementedError):
		info = None
	if not info or info.isCollapsed:
		ui.message (_("Error"))
	else:
		global text1
		text1 = info.text
		text2 = str(text1).lower()
		# A dictionary to replace symbols and punctuation by a space to allow a better spliting of words...
		toRemove = {
			'!' : ' ',
			'"' : ' ',
			'#' : ' ',
			'$' : ' ',
			'%' : ' ',
			'(' : ' ',
			')' : ' ',
			'*' : ' ',
			'+' : ' ',
			',' : ' ',
			'.' : ' ',
			'/' : ' ',
			':' : ' ',
			';' : ' ',
			'<' : ' ',
			'=' : ' ',
			'>' : ' ',
			'?' : ' ',
			'[' : ' ',
			'\\' : ' ',
			']' : ' ',
			'^' : ' ',
			'_' : ' ',
			'`' : ' ',
			'{' : ' ',
			'|' : ' ',
			'}' : ' ',
			'~' : ' ',
			'“' : ' ',
			'”' : ' ',
			'—' : ' ',
			'…' : ' ',
		}
		text2 = text2.translate(str.maketrans(toRemove))
		words = text2.split()
		words = sorted(words)
	global wordList
	wordList = collections.Counter([word for word in words if word not in ("-", "\'")]).most_common()
	return text1, wordList

def loadWords():
	# Load the word list.
	global wdsList
	wdsList = []
	for word, count in wordList:
		if word[0].isalpha():
			wdsList.append('{word}, {count}'.format(word=word, count=count))
		else:
			pass
	if config.conf[ourAddon.name]["order"] == 0:
		wdsList = sorted(wdsList)
	else:
		pass
	if len(wordList) is 0:
		wdsList.append(_("There are no words"))
	return wdsList

def loadLines():
	# Load the lines with our word.
	global lns1
	from .dialogs import ourWord
	lns = text1.splitlines()
	lns1 = []
	lns2 = []
	ui.message(str(lns))
	for line in lns:
		if ourWord in line.lower():
			# Get all lines containing our word
			lns2.append(line)
	for line in lns2:
		## ui.message(line)
		# Divide line in 3 parts: 0=before ourWord, 1=ourWord and 2=after ourWord
		wordCheck = line.lower().partition(ourWord)
		## ui.message(str(wordCheck))
		if " "+ourWord +" " in line.lower():
			lns1.append(line)
			## ui.message("passou à zero" + line)
		# Check if the line starts with ourWord
		elif line.lower().startswith(ourWord) is True:
			# Check if 2 starts with a letter. If so, the line contains ourWord, but making part of other and not as a sepparate word...
			if wordCheck[2][0].isalpha() is True:
				pass
				## ui.message("Chumbou à primeira")
			else:
				lns1.append(line)
				## ui.message("passou à primeira" + line)
		# Check if line ends with ourWord
		elif line.lower().endswith(ourWord) is True:
			# Check if last character of 0 is a letter. If so, ourWord is not present as a word...
			if wordCheck[0][-1].isalpha() is True:
				pass
				## ui.message("Chumbou à segunda")
			else:
				lns1.append(line)
				## ui.message("passou à segunda" + line)
		# OurWord is in the middle of the line, so check is it is a word or part of a word...
		else:
			if wordCheck[0][-1].isalpha() is True:
				pass
				## ui.message("Chumbou à terceira")
			elif wordCheck[2][0].isalpha() is True:
				pass
				## ui.message("Chumbou à quarta")
			else:
				lns1.append(line)
	return lns1
