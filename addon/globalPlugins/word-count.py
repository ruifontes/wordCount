# -*- coding:utf-8 -*-
# Copyright (C) 2022 Rui Fontes <rui.fontes@tiflotecnia.com> based on a work of Oriol Gomez <ogomez.s92@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import globalPluginHandler
import api
import textInfos
from textInfos import offsets
import collections
import string
import wx
import gui
from gui import guiHelper
from ui import message
from time import sleep
import globalVars
from keyboardHandler import KeyboardInputGesture
from globalCommands import SCRCAT_CONFIG
import addonHandler
addonHandler.initTranslation()

text = ""
text1 = ""
wordList = []
lns = []
lns1 = []
ourWord = ""

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def script_wordCount(self,gesture):
		obj = api.getFocusObject()
		treeInterceptor = obj.treeInterceptor
		if hasattr(treeInterceptor,'TextInfo') and not treeInterceptor.passThrough:
			obj = treeInterceptor
		try:
			info = obj.makeTextInfo(textInfos.POSITION_SELECTION)
		except (RuntimeError, NotImplementedError):
			info = None
		if not info or info.isCollapsed:

			# For translators: Message to announce when no text is selected
			message(_("select some text first."))
		else:

			#Prepare to count words
			global text1
			text1 = info.text
			text2 = str(text1).lower()

			toRemove = string.punctuation.replace("\'", "").replace("-", "").replace("@", "").replace(" ", "")+"“"+"”"+"—"+"…"
			for z in range(len(toRemove)):
				X = toRemove[z]
				text2 = text2.translate(str.maketrans(X, " "))

			# List of apps that needs \r as end of paragrap.
			apps = ["winword", "wordpad", "wordim", "soffice", "dspeech", "outlook"]
			if api.getFocusObject().appModule.appName in apps:

				# Counting paragraphs for apps that needs \r as end of paragrap.
				paragraphcount = 0
				for line in info.text:
					if "\r" in line:
						paragraphcount = paragraphcount + 1

				# For translators: Message to announce the number of words and characters
				message(_("{arg0} words and {arg1} characters in {arg2} paragraphs").format(
				arg0 = len(text2.split()),
				arg1 = len(info.text),
				arg2 = paragraphcount))

			else:

				# Counting paragraphs for apps that needs \n as end of paragrap.
				paragraphcount = 0
				for line in info.text:
					if "\n" in line:
						paragraphcount = paragraphcount + 1

				# For translators: Message to announce the number of words, characters, paragraphs and lines
				message(_("{arg0} words and {arg1} characters in {arg2} paragraphs and {arg3} lines").format(
				arg0 = len(text2.split()),
				arg1 = len(info.text),
				arg2 = paragraphcount,
				arg3 = len(info.text.splitlines())))

	def ListOfWords(self):
		obj = api.getFocusObject()
		treeInterceptor = obj.treeInterceptor
		if hasattr (treeInterceptor, 'TextInfo') and not treeInterceptor.passThrough:
			obj = treeInterceptor
		try:
			info = obj.makeTextInfo (textInfos.POSITION_ALL)
		except (RuntimeError, NotImplementedError):
			info = None
		if not info or info.isCollapsed:
			message (_("Error"))
		else:

			global text1
			text1 = info.text
			text2 = str(text1).lower()

			toRemove = string.punctuation.replace("\'", "").replace("-", "").replace("@", "").replace(" ", "")+"“"+"”"+"—"+"…"
			for z in range(len(toRemove)):
				X = toRemove[z]
				text2 = text2.translate(str.maketrans(X, " "))
			words = text2.split()
		global wordList
		wordList = collections.Counter([word for word in words if word not in ("-", "\'")]).most_common()
		return text1, wordList

	def ListOfLines(self):
		global lns
		lns = text1.splitlines()
		return lns

	def script_Listing(self, gesture):
		# For translators: Message to announce it is working...
		message(_("Wait please..."))
		sleep(.3)
		self.ListOfWords()
		self.ListOfLines()
		gui.mainFrame._popupSettingsDialog(WordListDialog)

	# For translators: Message to be announced during Keyboard Help
	script_wordCount.__doc__ = _("Announces the number of elements in the selected text.")
	# For translators: Name of the section in "Input gestures" dialog.
	script_wordCount.category = _("Text editing")

	# For translators: Message to be announced during Keyboard Help
	script_Listing.__doc__ = _("Opens a dialog with the list of words found in the document.")
	# For translators: Name of the section in "Input gestures" dialog.
	script_Listing.category = _("Text editing")

	__gestures={
		"kb:control+shift+f11": "Listing",
		"kb:control+shift+f12": "wordCount",
	}


# Avoid use on secure screens
if globalVars.appArgs.secure:
	# Override the global plugin to disable it.
	GlobalPlugin = globalPluginHandler.GlobalPlugin


class WordListDialog(wx.Dialog):
	# A dialog  to insert words from a list.
	_instance = None

	def __new__(cls, *args, **kwargs):
		if WordListDialog._instance is None:
			return wx.Dialog.__new__(cls)
		return WordListDialog._instance

	def __init__(self, parent):
		if WordListDialog._instance is not None:
			return
		WordListDialog._instance = self
		# Translators: Title of the dialog.
		title = _("Word list")
		super(WordListDialog, self).__init__(parent, wx.ID_ANY, title)
		self._loadWords()
		self.doGui()

	def _loadWords(self):
		# Load the word list.
		self.wdsList = []
		for word, count in wordList:
			self.wdsList.append('{word}, {count}'.format(word=word, count=count))
		if len(wordList)is 0:
			self.wdsList.append(_("There are no words"))

	def doGui(self):
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		# the list box
		# Translators: This is the label of the list  appearing on List of Words dialog.
		wordsListDialog = _("Words and its occurrences")
		self.wordsListBox = sHelper.addLabeledControl(wordsListDialog, wx.ListBox, id = wx.ID_ANY, choices=self.wdsList, style = wx.LB_SINGLE, size = (700,580))
		if self.wordsListBox.GetCount():
			self.wordsListBox.SetSelection(0)

		# Buttons
		if len(wordList)is not 0:
			bHelper= guiHelper.ButtonHelper(wx.HORIZONTAL)
			# Translators: This is a label of a button appearing on List of Words dialog.
			showButton =  bHelper.addButton(self, id = wx.ID_ANY, label=_("&Show occurrences"))
			showButton.SetDefault()
			sHelper.addItem(bHelper)
		bHelper = sHelper.addDialogDismissButtons(guiHelper.ButtonHelper(wx.HORIZONTAL))
		closeButton = bHelper.addButton(self, id = wx.ID_CLOSE, label = _("&Close"))
		if len(wordList)is 0:
			closeButton.SetDefault()
			mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
			mainSizer.Fit(self)
			self.SetSizer(mainSizer)
			# Events
			closeButton.Bind(wx.EVT_BUTTON, lambda evt: self.Destroy())
			self.SetEscapeId(wx.ID_CLOSE)
		else:
			mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
			mainSizer.Fit(self)
			self.SetSizer(mainSizer)
			# Events
			showButton.Bind(wx.EVT_BUTTON, self.onOkButton)
			closeButton.Bind(wx.EVT_BUTTON, lambda evt: self.Destroy())
			self.SetEscapeId(wx.ID_CLOSE)



	def onOkButton(self, evt):
		index = self.wordsListBox.GetSelection()
		global ourWord
		ourWord = str(wordList[index])
		x = ourWord.index(",")
		ourWord = ourWord[2:x-1]
		self.Close()
		gui.mainFrame._popupSettingsDialog(showOccursDialog)
		return ourWord

	def Destroy(self):
		WordListDialog._instance = None
		super(WordListDialog, self).Destroy()

	@classmethod
	def run(cls):
		if isOpened(cls):
			return
		mainFrame.prePopup()
		d = cls(mainFrame)
		d.CentreOnScreen()
		d.Show()
		mainFrame.postPopup()

class showOccursDialog(wx.Dialog):
	# A dialog  to insert the lines where our word appear.
	_instance = None

	def __new__(cls, *args, **kwargs):
		if showOccursDialog._instance is None:
			return wx.Dialog.__new__(cls)
		return showOccursDialog._instance

	def __init__(self, parent):
		if showOccursDialog._instance is not None:
			return
		showOccursDialog._instance = self
		# Translators: Title of the dialog.
		title = _("Lines containing our word")
		super(showOccursDialog, self).__init__(parent, wx.ID_ANY, title)
		self._loadLines()
		self.doGui()

	def _loadLines(self):
		# Load the lines with our word.
		global lns1
		lns1 = []
		lns2 = []
		for line in lns:
			if ourWord in line.lower():
				lns2.append(line)
		for line in lns2:
			wordCheck = line.lower().partition(ourWord)
			if line.lower().startswith(ourWord) is True:
				if wordCheck[2][0].isalpha() is True:
					pass
				else:
					lns1.append(line)
			elif line.lower().endswith(ourWord) is True:
				if wordCheck[0][-1].isalpha() is True:
					pass
				else:
					lns1.append(line)
			else:
				if wordCheck[0][-1].isalpha() or wordCheck[2][0].isalpha() is True:
					pass
				else:
					lns1.append(line)
		return lns1

	def doGui(self):
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		# the list box
		# Translators: This is the label of the list  appearing on List of Words dialog.
		showOccursDialog = _("Lines containing our word")
		self.windowsListBox =sHelper.addLabeledControl(showOccursDialog, wx.ListBox, id = wx.ID_ANY, choices = lns1, style = wx.LB_SINGLE, size = (700,580))
		if self.windowsListBox.GetCount():
			self.windowsListBox.SetSelection(0)
		# Buttons
		bHelper= guiHelper.ButtonHelper(wx.HORIZONTAL)
		# Translators: This is a label of a button appearing on List of Words dialog.
		okButton =  bHelper.addButton(self, id = wx.ID_ANY, label=_("&Ok"))
		okButton.SetDefault()
		sHelper.addItem(bHelper)
		bHelper = sHelper.addDialogDismissButtons(guiHelper.ButtonHelper(wx.HORIZONTAL))
		closeButton= bHelper.addButton(self, id = wx.ID_CLOSE, label = _("&Close"))
		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		# Events
		okButton.Bind(wx.EVT_BUTTON,self.onOkButton)
		closeButton.Bind(wx.EVT_BUTTON, lambda evt: self.Destroy())
		self.SetEscapeId(wx.ID_CLOSE)

	def onOkButton(self, evt):
		self.Close()

	def Destroy(self):
		showOccursDialog._instance = None
		super(showOccursDialog, self).Destroy()

	@classmethod
	def run(cls):
		if isOpened(cls):
			return
		mainFrame.prePopup()
		d = cls(mainFrame)
		d.CentreOnScreen()
		d.Show()
		mainFrame.postPopup()
