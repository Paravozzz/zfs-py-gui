import npyscreen

import modules.forms as f
import modules.enums as e

#WIDGETS
class FormSwitchMenu(npyscreen.MultiLineAction):
    ITEMS_AND_ACTIONS_DICT = {} 
    def actionHighlighted(self, act_on_this, key_press):
        if len(self.ITEMS_AND_ACTIONS_DICT) == 0: 
            raise Exception("Fill ITEMS_AND_ACTIONS_DICT first!")
        menu_item:dict = self.ITEMS_AND_ACTIONS_DICT[act_on_this]
        if "Action" not in menu_item.keys():
            f.showDialogOk(self, "Error:", "Menu item doesn't contain Action key", e.ColorsEnum.DANGER.name) 
            return 
        menu_action:str = menu_item["Action"]
        if "Arguments" not in menu_item.keys():
            f.showDialogOk(self, "Error:", "Menu item doesn't contain Arguments key", e.ColorsEnum.DANGER.name) 
            return
        menu_command:list = menu_item["Arguments"]
        if len(menu_command) == 0:
            f.showDialogOk(self, "Error:", "Action \"" + act_on_this +"\" doesn't contain any arguments", e.ColorsEnum.DANGER.name) 
            return 
        if menu_action == "FormSwitch": 
            if menu_command[0] == "Previous":
                self.parent.parentApp.switchFormPrevious()
            else:
                if menu_command[0] is not None and menu_command[0] not in self.parent.parentApp._Forms:
                    f.showDialogOk(self, "Error:", "Form "+ menu_command[0] + " not found", e.ColorsEnum.DANGER.name)
                else:
                   self.parent.parentApp.switchForm(menu_command[0])
        elif menu_action == "ShowCommandResult":
            f.showCommandResult(self, menu_command, title=act_on_this)
        else: 
           f.showDialogOk(self, "Error:", "Action is not valid: " + menu_action, e.ColorsEnum.DANGER.name) 
