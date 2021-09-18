# #Name of App
APP_NAME = "ZFS Py GUI"

# #Form Dialog Ok
FORM_ID_DIALOG_OK = "FORM_DIALOG_OK"

# #Form Dialog Ok Cancel
FORM_ID_DIALOG_OK_CANCEL = "FORM_DIALOG_OK_CANCEL"

# #Form Create Pool
FORM_ID_CREATE_POOL = "FORM_CREATE_POOL"
FORM_TITLE_CREATE_POOL = "Create pool"

# #Manage pools Form
FORM_ID_MANAGE_POOLS = "MANAGE_POOLS"
FORM_TITLE_MANAGE_POOLS = "Manage pools"
FORM_MENU_MANAGE_POOLS = {
    "Create pool": {
        "Action": "FormSwitch",
        "Arguments": [FORM_ID_CREATE_POOL]
    },
    "Import pool": {
        "Action": "FormSwitch",
        "Arguments": []
    },
    "Export pool": {
        "Action": "FormSwitch",
        "Arguments": []
    },
    "Destroy pool": {
        "Action": "FormSwitch",
        "Arguments": []
    },
    "Back": {
        "Action": "FormSwitch",
        "Arguments": ["MAIN"]
    }
}

# #Pool information Form
FORM_ID_POOL_INFO = "POOL_INFO"
FORM_TITLE_POOL_INFO = "Pools information"
FORM_MENU_POOL_INFO = {
    "Pools health": {
        "Action": "ShowCommandResult",
        "Arguments": ["zpool", "status", "-x", "-p"]
    },
    "Pools status": {
        "Action": "ShowCommandResult",
        "Arguments": ["zpool", "status", "-p"]
    },
    "Back": {
        "Action": "FormSwitch",
        "Arguments": ["MAIN"]
    }
}

# #Main Form
FORM_ID_MAIN = "MAIN"
FORM_TITLE_MAIN = "Main menu"
FORM_MENU_MAIN = {
    "Pool info": {
        "Action": "FormSwitch",
        "Arguments": [FORM_ID_POOL_INFO]
    },
    "Manage pools": {
        "Action": "FormSwitch",
        "Arguments": [FORM_ID_MANAGE_POOLS]
    },
    "Exit": {
        "Action": "FormSwitch",
        "Arguments": [None]
    }
}
