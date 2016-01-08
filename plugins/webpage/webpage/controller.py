# -*- coding: UTF-8 -*-

import os
import os.path
import sys

import wx

from outwiker.core.factoryselector import FactorySelector
from outwiker.core.system import getOS

from webnotepage import WebPageFactory, WebNotePage
from actions.downloadaction import (CreateChildWebPageAction,
                                    CreateSiblingWebPageAction)
from actions.opensourceurl import OpenSourceURLAction
from actions.showpageinfo import ShowPageInfoAction


class Controller (object):

    """General plugin controller."""

    def __init__ (self, plugin, application):
        self._plugin = plugin
        self._application = application
        self._addedWebPageMenuItems = False

        self.MENU_INDEX = 5


    def initialize (self):
        self._menuName = _(u"Web page")
        self._createGui()

        self._correctSysPath()

        self._application.onPageDialogPageFactoriesNeeded += self.__onPageDialogPageFactoriesNeeded
        self._application.onPageSelect += self.__onPageSelect
        FactorySelector.addFactory (WebPageFactory())


    def _correctSysPath (self):
        cmd_folder = unicode (os.path.dirname(os.path.abspath(__file__)),
                              getOS().filesEncoding)
        cmd_folder = os.path.join (cmd_folder, u'libs')

        syspath = [unicode (item, getOS().filesEncoding)
                   if not isinstance (item, unicode)
                   else item for item in sys.path]

        if cmd_folder not in syspath:
            sys.path.insert(0, cmd_folder)


    def destroy (self):
        self._removeGui()

        self._application.onPageDialogPageFactoriesNeeded -= self.__onPageDialogPageFactoriesNeeded
        self._application.onPageSelect -= self.__onPageSelect

        FactorySelector.removeFactory (WebPageFactory().getTypeString())


    def _createGui (self):
        if self._application.mainWindow is not None:
            self._createMenu()
            self._createSiblingWebPageAction()
            self._createChildWebPageAction()


    def _removeGui (self):
        mainWindow = self._application.mainWindow
        if (mainWindow is not None and
                mainWindow.PLUGINS_TOOLBAR_STR in mainWindow.toolbars):
            actionController = self._application.actionController
            actionController.removeMenuItem (CreateChildWebPageAction.stringId)
            actionController.removeToolbarButton (CreateChildWebPageAction.stringId)
            actionController.removeAction (CreateChildWebPageAction.stringId)

            actionController.removeMenuItem (CreateSiblingWebPageAction.stringId)
            actionController.removeToolbarButton (CreateSiblingWebPageAction.stringId)
            actionController.removeAction (CreateSiblingWebPageAction.stringId)

            if (self._application.selectedPage is not None and
                    self._application.selectedPage.getTypeString() == WebNotePage.getTypeString()):
                self._removeWebPageMenuItems()

            index = mainWindow.mainMenu.FindMenu (self._menuName)
            assert index != wx.NOT_FOUND

            mainWindow.mainMenu.Remove (index)


    def __onPageDialogPageFactoriesNeeded (self, page, params):
        if (params.pageForEdit is not None and
                params.pageForEdit.getTypeString() == WebNotePage.getTypeString()):
            params.addPageFactory (WebPageFactory())


    def __onPageSelect (self, page):
        if (page is not None and
                page.getTypeString() == WebNotePage.getTypeString()):
            self._addWebPageMenuItems()
        else:
            self._removeWebPageMenuItems()


    def _addWebPageMenuItems (self):
        mainWindow = self._application.mainWindow

        if (mainWindow is not None and not self._addedWebPageMenuItems):
            controller = self._application.actionController

            openSourceAction = OpenSourceURLAction(self._application)
            controller.register (openSourceAction, hotkey=None)
            controller.appendMenuItem (openSourceAction.stringId, self.menu)

            showInfoAction = ShowPageInfoAction(self._application)
            controller.register (showInfoAction, hotkey=None)
            controller.appendMenuItem (showInfoAction.stringId, self.menu)

            self._addedWebPageMenuItems = True


    def _removeWebPageMenuItems (self):
        if self._addedWebPageMenuItems:
            actionController = self._application.actionController

            actionController.removeMenuItem (OpenSourceURLAction.stringId)
            actionController.removeAction (OpenSourceURLAction.stringId)

            actionController.removeMenuItem (ShowPageInfoAction.stringId)
            actionController.removeAction (ShowPageInfoAction.stringId)

            self._addedWebPageMenuItems = False


    def _createMenu (self):
        self.menu = wx.Menu (u'')
        self._application.mainWindow.mainMenu.Insert (self.MENU_INDEX,
                                                      self.menu,
                                                      self._menuName)


    def _createChildWebPageAction (self):
        mainWindow = self._application.mainWindow

        if (mainWindow is not None and
                mainWindow.PLUGINS_TOOLBAR_STR in mainWindow.toolbars):
            action = CreateChildWebPageAction(self._application)
            toolbar = mainWindow.treePanel.panel.toolbar
            image = self.getImagePath (u'create-child.png')

            controller = self._application.actionController

            controller.register (action, hotkey=None)
            controller.appendMenuItem (action.stringId, self.menu)
            controller.appendToolbarButton (action.stringId,
                                            toolbar,
                                            image)


    def _createSiblingWebPageAction (self):
        mainWindow = self._application.mainWindow

        if (mainWindow is not None and
                mainWindow.PLUGINS_TOOLBAR_STR in mainWindow.toolbars):
            action = CreateSiblingWebPageAction(self._application)
            toolbar = mainWindow.treePanel.panel.toolbar
            image = self.getImagePath (u'create-sibling.png')

            controller = self._application.actionController

            controller.register (action, hotkey=None)
            controller.appendMenuItem (action.stringId, self.menu)
            controller.appendToolbarButton (action.stringId,
                                            toolbar,
                                            image)


    def getImagePath (self, imageName):
        """Return path to images directory."""
        imagedir = unicode (os.path.join (os.path.dirname (__file__), "images"), getOS().filesEncoding)
        fname = os.path.join (imagedir, imageName)
        return fname