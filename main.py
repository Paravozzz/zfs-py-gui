import npyscreen

import constants as c
import forms


class AppClass(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm(c.FORM_ID_MAIN, forms.FormMain, name=c.APP_NAME +"->"+ c.FORM_TITLE_MAIN)
        self.addForm(c.FORM_ID_MANAGE_POOLS, forms.FormManagePools, name=c.APP_NAME + "->" + c.FORM_TITLE_MANAGE_POOLS)
        self.addForm(c.FORM_ID_POOL_INFO, forms.FormPoolInformation, name=c.APP_NAME + "->" + c.FORM_TITLE_POOL_INFO)
        self.addForm(c.FORM_ID_MODAL_OK, forms.FormModal)
        self.addForm(c.FORM_ID_POPUP_OK, forms.FormPopup)
        
#MAIN
if __name__ == '__main__':
    App = AppClass()
    App.run()