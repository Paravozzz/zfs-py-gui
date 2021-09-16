import npyscreen

import modules.constants as c
import modules.forms as f


class AppClass(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm(c.FORM_ID_MAIN, f.FormMain, name=c.APP_NAME +" -> "+ c.FORM_TITLE_MAIN)
        self.addForm(c.FORM_ID_MANAGE_POOLS, f.FormManagePools, name=c.APP_NAME + " -> " + c.FORM_TITLE_MANAGE_POOLS)
        self.addForm(c.FORM_ID_POOL_INFO, f.FormPoolInformation, name=c.APP_NAME + " -> " + c.FORM_TITLE_POOL_INFO)
        self.addForm(c.FORM_ID_CREATE_POOL, f.FormCreatePool, name=c.APP_NAME + " -> " + c.FORM_TITLE_CREATE_POOL)

#MAIN
if __name__ == '__main__':
    App = AppClass()
    App.run()