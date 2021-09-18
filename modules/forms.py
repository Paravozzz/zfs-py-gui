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
        command:str = "zpool create"
        if self.forceCeckWdgt == True:
             command += " -f"
        command += " -m " + str(self.mountPathWdgt.value)
        command += " " + str(self.nameWdgt.value)
        poolType:str = None
        if len(self.slectPoolTypeWdgt.value)>0: 
            poolType = self.slectPoolTypeWdgt.values[self.slectPoolTypeWdgt.value[0]]
            if poolType != "stripe":
                command += " " + poolType
        if len(self.selectDisksWdgt.value)>0:
            for val_pos in self.selectDisksWdgt.value:
                command += " " + self.selectDisksWdgt.values[val_pos]
        app = getApp(self)
        showCommandConfirm(self, [command], "Do you want to create pool?", afterCommanExecutionFunction=lambda formId=c.FORM_ID_MANAGE_POOLS: app.switchForm(formId))
        
    def beforeEditing(self):
        self.selectDisksWdgt.values = sf.getHDDs() 

class FormOK(npy.ActionFormMinimal):
    formId = None
    okFunction = None 
    def on_ok(self):
        if self.okFunction is None:
            self.parentApp.switchFormPrevious()
        else:
            self.okFunction()

class FormOkCancel(npy.ActionFormV2):
    formId = None
    okFunction = None
    cancelFunction = None
    def on_ok(self):
        if self.okFunction is None:
            self.parentApp.switchFormPrevious()
        else:
            self.okFunction()
    def on_cancel(self):
        if self.cancelFunction is None:
            self.parentApp.switchFormPrevious()
        else:
            self.cancelFunction()
            
##FUNCTIONS
def createDialogOk(self, fullscreen:bool = False, okFunction = None, title:str = ""):
    formId = c.FORM_ID_DIALOG_OK
    app = getApp(self)
    if fullscreen == False:
        frm = app.addForm(formId, FormOK, lines=12, columns=60)
        frm.center_on_display()
    else:
        frm = app.addForm(formId, FormOK)
    if title != "" :
        frm.name = self.name + " -> " + title
    else:
        frm.name = self.name
    frm.formId = formId
    frm.okFunction = okFunction
    return frm

def createDialogOkCancel(self, fullscreen:bool = False, okFunction = None, cancelFunction = None, title:str = ""):
    formId = c.FORM_ID_DIALOG_OK_CANCEL
    app = getApp(self)
    if fullscreen == False:
        frm = app.addForm(formId, FormOkCancel, lines=12, columns=60)
        frm.center_on_display()
    else:
        frm = app.addForm(formId, FormOkCancel)
    if title != "" :
        frm.name = self.name + " -> " + title
    else:
        frm.name = self.name
    frm.formId = formId
    frm.okFunction = okFunction
    frm.cancelFunction = cancelFunction
    return frm

#Shows modal dialog and then return to previous window
def showDialogOk(self, title:str, message:str, colorLabel:str = "DEFAULT", fullscreen:bool = False, okFunction = None):
    frm = createDialogOk(self, fullscreen=fullscreen, okFunction=okFunction) 
    frm.add(npy.TitleFixedText, name=title, editable=False, labelColor=colorLabel)
    frm.add(npy.FixedText, value=message, editable=False)
    frm.parentApp.switchForm(frm.formId)
    
def showDialogOkCancel(self, title:str, message:str, colorLabel:str = "DEFAULT", fullscreen:bool = False, okFunction = None, cancelFunction = None):
    frm = createDialogOkCancel(self, fullscreen=fullscreen, okFunction=okFunction, cancelFunction=cancelFunction) 
    frm.add(npy.TitleFixedText, name=title, editable=False, labelColor=colorLabel)
    frm.add(npy.FixedText, value=message, editable=False)
    frm.parentApp.switchForm(frm.formId)
    
#Shows modal dialog with stdout or stderror of executed command
def showCommandResult(self, command:list, okFunction:str = None, title:str = ""):
    command_str:str = ' '.join(map(str, command)) 
    frm = createDialogOk(self, fullscreen=True, okFunction=okFunction, title=title)
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
    frm.add(npy.Pager, values=text, editable=False)
    frm.parentApp.switchForm(frm.formId)
    
#Shows modal dialog with command confirmation    
def showCommandConfirm(self, command:list, message:str = "Are you sure?", afterCommanExecutionFunction = None):
    frm = createDialogOkCancel(self, fullscreen=False, okFunction = lambda self=self, command=command, okFunction=afterCommanExecutionFunction: showCommandResult(self, command, okFunction), cancelFunction=None)
    frm.add(npy.FixedText, value=message, editable = False)
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