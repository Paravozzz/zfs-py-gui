import npyscreen

import menus as m
import constants as c

#FORMS
class FormMain(npyscreen.FormBaseNew):
    def create(self):
        self.txtWdgt = self.add(npyscreen.TitleFixedText, name="Main Menu", editable=False)
        self.menuWdgt = self.add(m.FormSwitchMenu, values=list(c.FORM_MENU_MAIN.keys()))

    def beforeEditing(self):
        self.menuWdgt.ITEMS_AND_ACTIONS_DICT = c.FORM_MENU_MAIN

    def afterEditing(self):
        pass

class FormManagePools(npyscreen.FormBaseNew):
    def create(self):
        self.txtWdgt = self.add(npyscreen.TitleFixedText, name="Manage pools", editable=False)
        self.menuWdgt = self.add(m.FormSwitchMenu, values=list(c.FORM_MENU_MANAGE_POOLS.keys()))
    
    def beforeEditing(self):
        self.menuWdgt.ITEMS_AND_ACTIONS_DICT = c.FORM_MENU_MANAGE_POOLS
    
    def afterEditing(self):
        pass

class FormPoolInformation(npyscreen.FormBaseNew):
    def create(self):
        self.txtWdgt = self.add(npyscreen.TitleFixedText, name="Pools Info", editable=False)
        self.menuWdgt = self.add(m.FormSwitchMenu, values=list(c.FORM_MENU_POOL_INFO.keys()))

    def beforeEditing(self):
        self.menuWdgt.ITEMS_AND_ACTIONS_DICT = c.FORM_MENU_POOL_INFO
    
    def afterEditing(self):
        pass 

class FormModal(npyscreen.Form):
    def create(self):
        pass
    
    def afterEditing(self):
        self.parentApp.switchFormPrevious()

class FormPopup(npyscreen.Popup):
    def create(self):
        pass

    def afterEditing(self):
        self.parentApp.switchFormPrevious()

#FUNCTIONS
#Shows modal dialog and then return to previous window
def showPopUp(self, title:str, message:str, colorLabel:str = "DEFAULT"):
    frm = self.parent.parentApp.getForm(c.FORM_ID_POPUP_OK)
    frm._clear_all_widgets()
    frm.name = self.parent.name
    frm.add(npyscreen.TitleFixedText, name=title, editable=False, labelColor=colorLabel)
    frm.add(npyscreen.FixedText, value=message, editable=False)
    self.parent.parentApp.switchForm(c.FORM_ID_POPUP_OK)