# coding=utf-8
# Copyright (C) 2019 Oriol Gómez <ogomez.s92@gmail.com> and Rui Fontes <rui.fontes@tiflotecnia.com>
# This file is covered by the GNU General Public License.

import globalPluginHandler
import scriptHandler
import textInfos
import NVDAObjects
from ui import message
import api
import winUser
from globalCommands import SCRCAT_CONFIG
import addonHandler
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def script_wordCount(self,gesture):
		obj=api.getFocusObject()
		treeInterceptor=obj.treeInterceptor
		if hasattr(treeInterceptor,'TextInfo') and not treeInterceptor.passThrough:
			obj=treeInterceptor
		try:
			info=obj.makeTextInfo(textInfos.POSITION_SELECTION)
		except (RuntimeError, NotImplementedError):
			info=None
		if not info or info.isCollapsed:
			message(_("select some text first."))
		else:
			wordcount=0
			str=info.text
			words=str.split()
			wordcount+=len(words)
			message(_("%s words")%wordcount)

	script_wordCount.__doc__ = _("Announces how many words are in the selected text.")
	script_wordCount.category = _("Word count")

	__gestures={
		"kb:NVDA+control+w": "wordCount",
	}