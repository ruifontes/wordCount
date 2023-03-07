# -*- coding: UTF-8 -*-
# Part of wordCount add-on
# Module for add-on settings panel
# written by Rui Fontes <rui.fontes@tiflotecnia.com>, Ângelo Abrantes <ampa4374@gmail.com> and Abel Passos do Nascimento Jr. <abel.passos@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# import the necessary modules
from .update import *
# For translation process
addonHandler.initTranslation()

optionsList = [_("Alphabetically"), _("By number of occurences")]


class wordCountSettingsPanel(gui.SettingsPanel):
	# Translators: Title of the wordCount settings dialog in the NVDA settings.
	title = ourAddon.name

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
		self.orderCB.SetSelection(config.conf[ourAddon.name]["order"])

		# Translators: Checkbox name in the configuration dialog
		self.shouldUpdateChk = sHelper.addItem(wx.CheckBox(self, label=_("Check for updates at startup")))
		self.shouldUpdateChk.SetValue(config.conf[ourAddon.name]["isUpgrade"])
		if config.conf.profiles[-1].name:
			self.shouldUpdateChk.Disable()

	def onSave (self):
		config.conf[ourAddon.name]["order"] = optionsList.index(self.orderCB.GetStringSelection())
		if not config.conf.profiles[-1].name:
			config.conf[ourAddon.name]["isUpgrade"] = self.shouldUpdateChk.GetValue()


