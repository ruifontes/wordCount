# -*- coding:utf-8 -*-
# Copyright (C) 2019 - 2023 Rui Fontes <rui.fontes@tiflotecnia.com>, Ângelo Abrantes <ampa4374@gmail.com> and Abel Passos Jr. <abel.passos@gmail.com>"
# Based on a work of Oriol Gomez <ogomez.s92@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Import the necessary modules
import globalPluginHandler
from .update import *
from .dialogs import *
from .variables import *
from .configPanel import wordCountSettingsPanel
from scriptHandler import script
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Creating the constructor of the newly created GlobalPlugin class.
	def __init__(self):
		# Call of the constructor of the parent class.
		super(globalPluginHandler.GlobalPlugin, self).__init__()

		# Adding a NVDA configurations section
		gui.NVDASettingsDialog.categoryClasses.append(wordCountSettingsPanel)

		# To allow waiting end of network tasks
		core.postNvdaStartup.register(self.networkTasks)

	def networkTasks(self):
		# Calling the update process...
		_MainWindows = Initialize()
		_MainWindows.start()

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		core.postNvdaStartup.unregister(self.networkTasks)
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(wordCountSettingsPanel)

	@script( 
		# Translators: Message to be announced during Keyboard Help 
		description=_("Announces the number of elements in the selected text."), 
		# Translators: Name of the section in "Input gestures" dialog. 
		category=_("Text editing"), 
		gesture="kb:control+shift+f12")
	def script_wordCount(self,gesture):
		countWords()
		from .variables import info, text1, text2, mute
		if mute == True:
			return
		else:
			# List of apps that needs \r as end of paragrap.
			apps = ["winword", "wordpad", "notepad", "wordim", "soffice", "dspeech", "outlook"]
			if api.getFocusObject().appModule.appName in apps:
				# Counting paragraphs for apps that needs \r as end of paragrap.
				paragraphcount = 0
				for line in info.text:
					if "\r" in line:
						paragraphcount = paragraphcount + 1

				# Translators: Message to announce the number of words and characters
				ui.message(_("{arg0} words and {arg1} characters in {arg2} paragraphs").format(
				arg0 = len(text2.split()),
				arg1 = len(info.text),
				arg2 = paragraphcount))

			else:
				# Counting paragraphs for apps that needs \n as end of paragrap.
				paragraphcount = 0
				for line in info.text:
					if "\n" in line:
						paragraphcount = paragraphcount + 1

				# Translators: Message to announce the number of words, characters, paragraphs and lines
				ui.message(_("{arg0} words and {arg1} characters in {arg2} paragraphs and {arg3} lines").format(
				arg0 = len(text2.split()),
				arg1 = len(text1),
				arg2 = paragraphcount,
				arg3 = len(info.text.splitlines())))

	@script( 
		# Translators: Message to be announced during Keyboard Help 
		description=_("Opens a dialog with the list of words found in the document."),
		# Translators: Name of the section in "Input gestures" dialog. 
		category=_("Text editing"), 
		gesture="kb:control+shift+f11")
	def script_Listing(self, gesture):
		# Translators: Message to announce it is working...
		ui.message(_("Wait please..."))
		ListOfWords()
		gui.mainFrame._popupSettingsDialog(WordListDialog)


# Avoid use on secure screens
if globalVars.appArgs.secure:
	# Override the global plugin to disable it.
	GlobalPlugin = globalPluginHandler.GlobalPlugin
