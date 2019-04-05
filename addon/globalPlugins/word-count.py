# coding=utf-8
# Copyright (C) 2019 Rui Fontes <rui.fontes@tiflotecnia.com> based on a work of Oriol Gómez <ogomez.s92@gmail.com>
# This file is covered by the GNU General Public License.

import globalPluginHandler
import scriptHandler
import textInfos
from ui import message
import api
from globalCommands import SCRCAT_CONFIG
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
		except (RuntimeError, NotImplementedError):
			info = None
		if not info or info.isCollapsed:
			# For translators: Message to announce when no text is selected
			message(_("select some text first."))
		else:

			# For translators: Message to announce the number of words
			message(_("{arg0} words and {arg1} characters").format(arg0 = len(info.text.split()), arg1 = len(info.text)))

	# For translators: Message to be announced during Keyboard Help
	script_wordCount.__doc__ = _("Announces how many words and characters are in the selected text.")
	# For translators: Name of the section in "Input gestures" dialog.
	script_wordCount.category = _("Text editing")

	__gestures = {
		"kb:control+shift+f12": "wordCount",
	}
