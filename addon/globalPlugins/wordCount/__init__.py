# -*- coding:utf-8 -*-
# WordCount: Add-on to count words and list them
# written by Rui Fontes <rui.fontes@tiflotecnia.com> Ângelo Abrantes <ampa4374@gmail.com> and Abel Passos do Nascimento Jr. <abel.passos@gmail.com>
# Based on a work of Oriol Gomez <ogomez.s92@gmail.com>
# Copyright (C) 2019 - 2023 Rui Fontes <rui.fontes@tiflotecnia.com>, Ângelo Abrantes <ampa4374@gmail.com> and Abel Passos Jr. <abel.passos@gmail.com>"
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Import the necessary modules
import globalPluginHandler
import globalVars
from .dialogs import *
from .vars import *
from scriptHandler import script

# To start the translation process
addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Creating the constructor of the newly created GlobalPlugin class.
	def __init__(self):
		# Call of the constructor of the parent class.
		super(globalPluginHandler.GlobalPlugin, self).__init__()

		# Adding a NVDA configurations section
		gui.NVDASettingsDialog.categoryClasses.append(wordCountSettingsPanel)

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(wordCountSettingsPanel)

	@script( 
		# Translators: Message to be announced during Keyboard Help 
		description=_("Announces the number of elements in the selected text."), 
		# Translators: Name of the section in "Input gestures" dialog. 
		category=_("Text editing"), 
		gesture="kb:control+shift+f12")
	def script_wordCount(self,gesture):
		info, text2 = countWords()
		if info == None:
			return
		else:
			# List of apps that needs \r as end of paragrap.
			apps = ["winword", "wordpad", "notepad", "wordim", "soffice", "dspeech", "outlook"]
			end_of_paragraph = "\r" if api.getFocusObject().appModule.appName in apps else "\n"
			# Counting paragraphs.
			paragraphcount = info.text.count(end_of_paragraph)
			# Translators: Message to announce the number of words and characters
			ui.message(_("{words} words and {characters} characters in {paragraphs} paragraphs").format(
				words = len(text2.split()),
				characters = len(info.text),
				paragraphs = paragraphcount)
			)

	@script( 
		# Translators: Message to be announced during Keyboard Help 
		description=_("Opens a dialog with the list of words found in the document."),
		# Translators: Name of the section in "Input gestures" dialog. 
		category=_("Text editing"), 
		gesture="kb:control+shift+f11")
	def script_Listing(self, gesture):
		# Translators: Message to announce it is working...
		ui.message(_("Wait please..."))
		gui.mainFrame._popupSettingsDialog(WordListDialog)


# Avoid use on secure screens
if globalVars.appArgs.secure:
	# Override the global plugin to disable it.
	GlobalPlugin = globalPluginHandler.GlobalPlugin
