# -*- coding: UTF-8 -*-
# WordCount add-on: Module for settings panel
# written by Rui Fontes <rui.fontes@tiflotecnia.com>, Ângelo Abrantes <ampa4374@gmail.com> and Abel Passos do Nascimento Jr. <abel.passos@gmail.com>
# Copyright (C) 2022-2023 Rui Fontes <rui.fontes@tiflotecnia.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# import the necessary modules
import config
import wx
import gui
from gui.settingsDialogs import NVDASettingsDialog, SettingsPanel
from gui import guiHelper
import addonHandler

# To start the translation process
addonHandler.initTranslation()

def initConfiguration():
	confspec = {
		"order": "boolean(default=False)",
	}
	config.conf.spec["wordCount"] = confspec

initConfiguration()

# Constants:
optionsList = [_("Alphabetically"), _("By number of occurences")]


class wordCountSettingsPanel(gui.settingsDialogs.SettingsPanel):
	# Translators: Title of the wordCount settings dialog in the NVDA settings.
	title = _("Wordcount")

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer = settingsSizer)

		# Translators: Label of a  combobox used to choose the sort order
		orderLabel = _("&Order by:")
		self.orderCB = sHelper.addLabeledControl(
			orderLabel,
			wx.Choice,
			choices = optionsList,
			style = wx.CB_SORT
		)
		self.orderCB.SetSelection(config.conf["wordCount"]["order"])

	def onSave (self):
		config.conf["wordCount"]["order"] = optionsList.index(self.orderCB.GetStringSelection())
		# Reactivate profiles triggers
		config.conf.enableProfileTriggers()
		self.Hide()

	def onPanelActivated(self):
		# Deactivate all profile triggers and active profiles
		config.conf.disableProfileTriggers()
		self.Show()

	def onPanelDeactivated(self):
		# Reactivate profiles triggers
		config.conf.enableProfileTriggers()
		self.Hide()

