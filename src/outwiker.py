#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Tue Mar 23 21:59:58 2010

import gettext
import os

#import wxversion
#wxversion.select("2.8")

import wx

from core.config import getConfigPath
from core.application import Application

if os.name != "nt":
	# Активируем pygkt под Linux
	import gobject
	gobject.threads_init()

	import pygtk
	pygtk.require('2.0')
	import gtk, gtk.gdk


class OutWiker(wx.App):
	def __init__(self, *args, **kwds):
		wx.App.__init__ (self, *args, **kwds)


	def OnInit(self):
		self._configFileName = getConfigPath (u".outwiker", u"outwiker.ini")
		Application.init(self._configFileName)

		from gui.MainWindow import MainWindow
		wx.InitAllImageHandlers()
		self.mainWnd = MainWindow(None, -1, "")
		self.SetTopWindow (self.mainWnd)
		#self.mainWnd.Show()

		self.bindActivateApp()

		return 1


	def bindActivateApp (self):
		"""
		Подключиться к событию при потере фокуса приложением
		"""
		self.Bind (wx.EVT_ACTIVATE_APP, self.onActivate)


	def unbindActivateApp (self):
		"""
		Отключиться от события при потере фокуса приложением
		"""
		self.Unbind (wx.EVT_ACTIVATE_APP)


	def onActivate (self, event):
		if not event.GetActive():
			Application.onForceSave()


# end of class OutWiker

if __name__ == "__main__":
	outwiker = OutWiker(0)
	outwiker.MainLoop()
