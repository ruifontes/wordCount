# -*- coding: UTF-8 -*-
# WordCount add-on: Module for dialogs
# written by Rui Fontes <rui.fontes@tiflotecnia.com>, Ângelo Abrantes <ampa4374@gmail.com> and Abel Passos do Nascimento Jr. <abel.passos@gmail.com>
# Copyright (C) 2022-2023 Rui Fontes <rui.fontes@tiflotecnia.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# import the necessary modules.
from .configPanel import *
from .vars import *
from keyboardHandler import KeyboardInputGesture
from time import sleep

# To start the translation process
addonHandler.initTranslation()


class WordListDialog(wx.Dialog):
	# A dialog  to insert words from a list.
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		# Translators: Title of the dialog showing the list of words
		self.SetTitle(_("Words and its occurrences"))
		wordList, text1= ListOfWords()
		global wdsList, wdsSortedList
		wdsList, wdsSortedList = loadWords(wordList)

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		# Translators: Ordering options
		self.radio_box_1 = wx.RadioBox(self, wx.ID_ANY, _("Order by:"), choices=[_("Alphabetically"), _("By number of occurences")], majorDimension=2) 
		self.radio_box_1.SetSelection(config.conf["wordCount"]["order"])
		sizer_1.Add(self.radio_box_1, 0, 0, 0)

		# Translators: Button to reorder the list
		self.button_0 = wx.Button(self, wx.ID_ANY, _("&Reorder"))
		sizer_1.Add(self.button_0, 0, 0, 0)
		self.button_0.Hide()

		if self.radio_box_1.GetSelection() == 0:
			self.list_box_1 = wx.ListBox(self, wx.ID_ANY, choices= wdsList, style=wx.LB_SINGLE)
		else:
			self.list_box_1 = wx.ListBox(self, wx.ID_ANY, choices= wdsSortedList, style=wx.LB_SINGLE)
		self.list_box_1.SetMinSize((800, 500))
		self.list_box_1.SetFocus()
		self.list_box_1.SetSelection(0)
		sizer_1.Add(self.list_box_1, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		# Translators: Name of button to show the list of lines containing the selected word
		self.button_1 = wx.Button(self, wx.ID_ANY, _("&Show occurrences"))
		self.button_1.SetDefault()
		sizer_2.Add(self.button_1, 0, 0, 0)

		self.button_CLOSE = wx.Button(self, wx.ID_CLOSE, "")
		sizer_2.AddButton(self.button_CLOSE)

		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetEscapeId(self.button_CLOSE.GetId())
		self.Bind(wx.EVT_RADIOBOX, self.reload, self.radio_box_1)
		self.Bind(wx.EVT_BUTTON, self.reload1, self.button_0)
		self.Bind(wx.EVT_BUTTON, self.onOkButton, self.button_1)

		self.Layout()
		self.CentreOnScreen()

	def reload(self, event):
		event.Skip()
		config.conf["wordCount"]["order"] = self.radio_box_1.GetSelection()
		self.button_0.Show()

	def reload1(self, event):
		self.Hide()
		if self.radio_box_1.GetSelection() == 0:
			self.list_box_1.Set(wdsList)
		else:
			self.list_box_1.Set(wdsSortedList)
		self.button_0.Hide()
		self.list_box_1.SetFocus()
		self.Show()

	def onOkButton(self, event):
		index = self.list_box_1.GetSelection()
		global ourWord
		if self.radio_box_1.GetSelection() == 0:
			ourWord = str(wdsList[index])
		else:
			ourWord = str(wdsSortedList[index])
		x = ourWord.index(",")
		ourWord = ourWord[:x]
		self.Destroy()
		gui.mainFrame._popupSettingsDialog(showOccursDialog)


class showOccursDialog(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		# Translators: Name of dialog showing the list of lines containing the selected word
		self.SetTitle(_("Lines containing our word"))
		lns1 = loadLines(ourWord)

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		self.wordsListBox = wx.ListBox(self, wx.ID_ANY, choices = [item[0] for item in lns1])
		sizer_1.Add(self.wordsListBox, 0, 0, 0)
		if self.wordsListBox.GetCount():
			self.wordsListBox.SetSelection(0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		# Translators: Name of button to show the list of lines containing the selected word
		self.button_1 = wx.Button(self, wx.ID_ANY, _("&Go to line"))
		self.button_1.SetDefault()
		sizer_2.Add(self.button_1, 0, 0, 0)

		self.button_CLOSE = wx.Button(self, wx.ID_CLOSE, "")
		sizer_2.AddButton(self.button_CLOSE)

		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.Bind(wx.EVT_BUTTON, self.goToText, self.button_1)
		self.SetEscapeId(self.button_CLOSE.GetId())

		self.Layout()
		self.CentreOnScreen()

	def goToText(self, evt):
		self.Destroy()
		# Place cursor at the begin
		KeyboardInputGesture.fromName("Control+home").send()
		# Object representing the text
		info = createInfo1()
		# Lets calculate where is the text where we want to place the cursor
		index = self.wordsListBox.GetSelection()
		ourLine = self.wordsListBox.GetString(index)
		# Initial value
		charsToMove = -1
		# Where to start searching the expression
		idx = 0
		if index > 0:
			# We have more than one line, so lets verify all since two or more can be equal...
			x = 0
			while x <= index:
				# We start searching at idx position, initially 0
				found = info.text[idx:].find(ourLine)
				foundIndex = found + idx
				if found < 0:
					break
				if foundIndex >= 0:
					charsToMove = foundIndex
				# Next search will begin here...
				idx = foundIndex+1
				x+= 1
		else:
			charsToMove = info.text.find(ourLine)
		print(str(charsToMove))
		info.move(textInfos.UNIT_CHARACTER, charsToMove)
		info.updateCaret()
