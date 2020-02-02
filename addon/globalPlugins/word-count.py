#-*- coding:utf-8 -*-
# Copyright (C) 2019 Rui Fontes <rui.fontes@tiflotecnia.com> based on a work of Oriol Gómez <ogomez.s92@gmail.com>
# This file is covered by the GNU General Public License.

import globalPluginHandler
import scriptHandler
import textInfos
from ui import message
import api
from globalCommands import SCRCAT_CONFIG
import appModuleHandler
import addonHandler
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def script_wordCount(self,gesture):
		obj = api.getFocusObject()
		treeInterceptor = obj.treeInterceptor
		if hasattr(treeInterceptor,'TextInfo') and not treeInterceptor.passThrough:
			obj = treeInterceptor
		try:
			info = obj.makeTextInfo(textInfos.POSITION_SELECTION)
			info1 = 	obj.makeTextInfo("selection")
		except (RuntimeError, NotImplementedError):
			info = None
		if not info or info.isCollapsed:

			# For translators: Message to announce when no text is selected
			message(_("select some text first."))
		else:

			# List of non supported apps. In some apps the count of paragraps and lines is too slow and may cause hangs in NVDA... 
			ans = ["winword", "wordpad", "dspeech"]
			if api.getFocusObject().appModule.appName in ans:
				# For translators: Message to announce the number of words and characters
				message(_("{arg0} words and {arg1} characters").format(
				arg0 = len(info.text.split()),
				arg1 = len(info.text)))
			else:
				# For translators: Message to announce the number of words, characters, paragraphs and lines
				message(_("{arg0} words and {arg1} characters in {arg2} paragraphs and {arg3} lines").format(
				arg0 = len(info1.text.split()),
				arg1 = len(info.text),
				arg2 = sum(1 for t in info1.getTextInChunks("paragraph")),
				arg3 = sum(1 for t in info1.getTextInChunks("line"))))

	# For translators: Message to be announced during Keyboard Help
	script_wordCount.__doc__ = _("Announces the number of elements in the selected text.")
	# For translators: Name of the section in "Input gestures" dialog.
	script_wordCount.category = _("Text editing")

	__gestures = {
		"kb:control+shift+f12": "wordCount",
	}