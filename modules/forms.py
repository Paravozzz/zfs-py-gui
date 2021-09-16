import os
import npyscreen as npy
from npyscreen.fmPopup import Popup

import modules.menus as m
import modules.constants as c
import modules.shellfunctions as sf
import modules.enums as e
import modules.shell as s

#FORMS
class FormMain(npy.FormBaseNew):
    def create(self):
        self.txtWdgt = self.add(npy.TitleFixedText, name="Main Menu", editable=False)
        self.menuWdgt = self.add(m.FormSwitchMenu, name = "Main Menu", values=list(c.FORM_MENU_MAIN.keys()))

    def beforeEditing(self):
        self.menuWdgt.ITEMS_AND_ACTIONS_DICT = c.FORM_MENU_MAIN

    def afterEditing(self):
        pass

class FormManagePools(npy.FormBaseNew):
    def create(self):
        self.txtWdgt = self.add(npy.TitleFixedText, name="Manage pools", editable=False)
        self.menuWdgt = self.add(m.FormSwitchMenu, name="Manage pools", values=list(c.FORM_MENU_MANAGE_POOLS.keys()))
    
    def beforeEditing(self):
        self.menuWdgt.ITEMS_AND_ACTIONS_DICT = c.FORM_MENU_MANAGE_POOLS
    
    def afterEditing(self):
        pass

class FormPoolInformation(npy.FormBaseNew):
    def create(self):
        self.txtWdgt = self.add(npy.TitleFixedText, name="Pools Info", editable=False)
        self.menuWdgt = self.add(m.FormSwitchMenu, name="Pools Info", values=list(c.FORM_MENU_POOL_INFO.keys()))

    def beforeEditing(self):
        self.menuWdgt.ITEMS_AND_ACTIONS_DICT = c.FORM_MENU_POOL_INFO
    
    def afterEditing(self):
        pass 

class FormCreatePool(npy.FormBaseNew):
    def create(self):
        app = getApp(self)
        self.nameWdgt = self.add(npy.TitleText, name="Pool name:", value="mypool")
        self.selectDisksWdgt = self.add(npy.TitleMultiSelect, name="Select disks:", max_height=8, scroll_exit = True, slow_scroll=True)
        self.slectPoolTypeWdgt = self.add(npy.TitleSelectOne, name="Pool type:", max_height=6, scroll_exit=True, slow_scroll=True, value=[1,], values=["stripe", "mirror", "raidz1", "raidz2", "raidz3"])
        self.forceCeckWdgt = self.add(npy.CheckBox, name="Force (try use disks, even if they appear in use)")
        self.mountPathWdgt = self.add(npy.TitleFilenameCombo, name="Mount point", value="/mnt")
        addOkAndCancel(self, "Create", "Cancel", self.createPool, app.switchFormPrevious)
       
    def createPool(self):
        command:str = "zpool create "
        command += str(self.nameWdgt.value)
        poolType:str = None
        if len(self.slectPoolTypeWdgt.value)>0: 
            poolType = self.slectPoolTypeWdgt.values[self.slectPoolTypeWdgt.value[0]]
            if poolType != "stripe":
                command += " " + poolType
        if len(self.selectDisksWdgt.value)>0:
            for val_pos in self.selectDisksWdgt.value:
                command += " " + self.selectDisksWdgt.values[val_pos]
        showCommandConfirm(self, [command], nextFormId=c.FORM_ID_MANAGE_POOLS)
        
    def beforeEditing(self):
        self.selectDisksWdgt.values = sf.getHDDs() 

class ActionFormMinimalMy(npy.ActionFormMinimal):
    formId = None
    nextFormId = None 
    def on_ok(self):
        if self.nextFormId is None:
            self.parentApp.switchFormPrevious()
        else:
            self.parentApp.switchForm(self.nextFormId)
            
##FUNCTIONS
def createDialogOk(self, fullscreen:bool = False, nextFormId:str = None, title:str = ""):
    formId = c.FORM_ID_DIALOG_OK
    app = getApp(self)
    if fullscreen == False:
        frm = app.addForm(formId, ActionFormMinimalMy, lines=12, columns=60)
        frm.center_on_display()
    else:
        frm = app.addForm(formId, ActionFormMinimalMy)
    if title != "" :
        frm.name = self.name + " -> " + title
    else:
        frm.name = self.name
    frm.formId = formId
    frm.nextFormId = nextFormId
    return frm

#Shows modal dialog and then return to previous window
def showDialogOk(self, title:str, message:str, colorLabel:str = "DEFAULT", fullscreen:bool = False, nextFormId:str = None):
    frm = createDialogOk(self, fullscreen, nextFormId) 
    frm.add(npy.TitleFixedText, name=title, editable=False, labelColor=colorLabel)
    frm.add(npy.FixedText, value=message, editable=False)
    frm.nextFormId = nextFormId
    frm.parentApp.switchForm(frm.formId)
    
#Shows modal dialog with stdout or stderror of executed command
def showCommandResult(self, command:list, nextFormId:str = None, title:str = ""):
    command_str:str = ' '.join(map(str, command)) 
    frm = createDialogOk(self, True, nextFormId, title)
    frm.add(npy.TitleFixedText, name="Executed:", value=command_str, editable=False)
    shell_stdout, shell_stderror = s.execute(command)
    title = None
    text = None
    if len(shell_stderror.strip()) > 0:
        title = "Error:"
        color = e.ColorsEnum.DANGER.name
        text = shell_stderror.strip()
    else:
        title = "Result:"
        color = e.ColorsEnum.LABEL.name
        text = shell_stdout
    frm.add(npy.TitleFixedText, name = title, labelColor = color, editable = False)
    text = text.split("\n")
    frm.add(npy.Pager, values=text, editable=True)
    
    frm.parentApp.switchForm(frm.formId)
    
#Shows modal dialog with command confirmation    
def showCommandConfirm(self, command:list, message:str = "Are you sure?", nextFormId:str = None):
    frm = createDialogOk(self, False, nextFormId)
    frm.add(npy.FixedText, value=message, editable = False)
    addOkAndCancel(frm, okFunction = lambda self=self, command=command, nextFormId=nextFormId: showCommandResult(self, command, nextFormId))
    frm.parentApp.switchForm(frm.formId)

#Put confirm and cancel button to form
def addOkAndCancel(form, okName:str = "Ok", cancelName:str = "Cancel", okFunction = None, cancelFunction = None):
    app = getApp(form)
    if okFunction is None:
        okFunction = app.switchFormPrevious()
    if cancelFunction is None:
        cancelFunction = app.switchFormPrevious()
    form.cancelButton = form.add(npy.ButtonPress, name=cancelName, when_pressed_function=cancelFunction)
    form.okButton = form.add(npy.ButtonPress, name=okName, when_pressed_function=okFunction)
    form.cancelButton.set_relyx(form.max_y - 3, form.max_x - 3 - form.cancelButton.width - form.okButton.width)
    form.okButton.set_relyx(form.cancelButton.rely, form.cancelButton.relx + form.cancelButton.width)

#Tries to get Form depends on self is a wigget or a form    
def getForm(self, formId:str):
    try:
        return self.parentApp.getForm(formId)
    except AttributeError:
        return self.parent.parentApp.getForm(formId)

#Tries to get App depends on self is a widget or a form
def getApp(self):
    try:
        return self.parentApp
    except AttributeError:
        return self.parent.parentApp