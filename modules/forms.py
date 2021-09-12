import npyscreen as npy

import modules.menus as m
import modules.constants as c
import modules.shellfunctions as sf
import modules.enums as e

#FORMS
class FormMain(npy.FormBaseNew):
    def create(self):
        self.txtWdgt = self.add(npy.TitleFixedText, name="Main Menu", editable=False)
        self.menuWdgt = self.add(m.FormSwitchMenu, values=list(c.FORM_MENU_MAIN.keys()))

    def beforeEditing(self):
        self.menuWdgt.ITEMS_AND_ACTIONS_DICT = c.FORM_MENU_MAIN

    def afterEditing(self):
        pass

class FormManagePools(npy.FormBaseNew):
    def create(self):
        self.txtWdgt = self.add(npy.TitleFixedText, name="Manage pools", editable=False)
        self.menuWdgt = self.add(m.FormSwitchMenu, values=list(c.FORM_MENU_MANAGE_POOLS.keys()))
    
    def beforeEditing(self):
        self.menuWdgt.ITEMS_AND_ACTIONS_DICT = c.FORM_MENU_MANAGE_POOLS
    
    def afterEditing(self):
        pass

class FormPoolInformation(npy.FormBaseNew):
    def create(self):
        self.txtWdgt = self.add(npy.TitleFixedText, name="Pools Info", editable=False)
        self.menuWdgt = self.add(m.FormSwitchMenu, values=list(c.FORM_MENU_POOL_INFO.keys()))

    def beforeEditing(self):
        self.menuWdgt.ITEMS_AND_ACTIONS_DICT = c.FORM_MENU_POOL_INFO
    
    def afterEditing(self):
        pass 

class FormCreatePool(npy.FormBaseNew):
    def create(self):
        self.nameWdgt = self.add(npy.TitleText, name="Pool name:", value="mypool")
        self.selectDisksWdgt = self.add(npy.TitleMultiSelect, name="Select disks:", max_height=8, scroll_exit = True, slow_scroll=True)
        self.slectPoolTypeWdgt = self.add(npy.TitleSelectOne, name="Pool type:", max_height=6, scroll_exit=True, slow_scroll=True, values=["stripe", "mirror", "raidz1", "raidz2", "raidz3"])
        self.forceCeckWdgt = self.add(npy.CheckBox, name="Force (try use disks, even if they appear in use)")
        self.mountPathWdgt = self.add(npy.TitleFilenameCombo, name="Mount point", value="/mnt")
        addOkAndCancel(self, "Create", "Cancel", self.parentApp.switchFormPrevious, self.parentApp.switchFormPrevious)
        
    def beforeEditing(self):
        self.selectDisksWdgt.values = sf.getHDDs() 
        
    def afterEditing(self):
        self.parentApp.switchFormPrevious()

class FormModal(npy.Form):
    def create(self):
        pass
    
    def afterEditing(self):
        self.parentApp.switchFormPrevious()

class FormPopup(npy.Popup):
    def create(self):
        pass

    def afterEditing(self):
        self.parentApp.switchFormPrevious()

##FUNCTIONS
#Shows modal dialog and then return to previous window
def showPopUp(self, title:str, message:str, colorLabel:str = "DEFAULT"):
    frm = self.parent.parentApp.getForm(c.FORM_ID_POPUP_OK)
    frm._clear_all_widgets()
    frm.name = self.parent.name
    frm.add(npy.TitleFixedText, name=title, editable=False, labelColor=colorLabel)
    frm.add(npy.FixedText, value=message, editable=False)
    self.parent.parentApp.switchForm(c.FORM_ID_POPUP_OK)
    
def addOkAndCancel(self, okName:str="Ok", cancelName:str = "Cancel", okFunction = None, cancelFunction = None):
    self.cancelButton = self.add(npy.ButtonPress, name=cancelName, when_pressed_function=cancelFunction)
    self.okButton = self.add(npy.ButtonPress, name=okName, when_pressed_function=okFunction)
    self.cancelButton.set_relyx(self.max_y - 3, self.max_x - 3 - self.cancelButton.width - self.okButton.width)
    self.okButton.set_relyx(self.cancelButton.rely, self.cancelButton.relx + self.cancelButton.width)