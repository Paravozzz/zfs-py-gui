import npyscreen

import constants as c
import forms as f
import shell as s
import enums as e

#WIDGETS
class FormSwitchMenu(npyscreen.MultiLineAction):
    ITEMS_AND_ACTIONS_DICT = {} 
    def actionHighlighted(self, act_on_this, key_press):
        if len(self.ITEMS_AND_ACTIONS_DICT) == 0: 
            raise Exception("Fill ITEMS_AND_ACTIONS_DICT first!")
        menu_item:dict = self.ITEMS_AND_ACTIONS_DICT[act_on_this]
        if "Action" not in menu_item.keys():
            f.showPopUp(self, "Error:", "Menu item doesn't contain Action key", e.ColorsEnum.DANGER.name) 
            return 
        menu_action:str = menu_item["Action"]
        if "Arguments" not in menu_item.keys():
            f.showPopUp(self, "Error:", "Menu item doesn't contain Arguments key", e.ColorsEnum.DANGER.name) 
            return
        menu_arguments:list = menu_item["Arguments"]
        if len(menu_arguments) == 0:
            f.showPopUp(self, "Error:", "Action \"" + act_on_this +"\" doesn't contain any arguments", e.ColorsEnum.DANGER.name) 
            return 
        if menu_action == "FormSwitch": 
            if menu_arguments[0] == "Previous":
                self.parent.parentApp.switchFormPrevious()
            else:
                if menu_arguments[0] is not None and menu_arguments[0] not in self.parent.parentApp._Forms:
                    f.showPopUp(self, "Error:", "Form "+ menu_arguments[0] + " not found", e.ColorsEnum.DANGER.name)
                else:
                   self.parent.parentApp.switchForm(menu_arguments[0])
        elif menu_action == "CommandModal":
            command_str:str = ' '.join(map(str, menu_arguments)) 
            frm = self.parent.parentApp.getForm(c.FORM_ID_MODAL_OK)
            frm._clear_all_widgets()
            frm.name = self.parent.name + "->" + act_on_this
            frm.add(npyscreen.TitleFixedText, name="Executed:", value=command_str, editable=False)
            frm.add(npyscreen.TitleFixedText, name="Result:", editable=False)
            frm.add(npyscreen.MultiLineEdit, value=s.execute(menu_arguments), editable=False)
            self.parent.parentApp.switchForm(c.FORM_ID_MODAL_OK)
        else: 
           f.showPopUp(self, "Error:", "Action is not valid: " + menu_action, e.ColorsEnum.DANGER.name) 
