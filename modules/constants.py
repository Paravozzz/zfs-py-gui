##Name of App 
APP_NAME = "ZFS Py GUI"

##Form Modal
FORM_ID_MODAL_OK = "FORM_MODAL"

##Form Popup 
FORM_ID_POPUP_OK = "FORM_POPUP"

##Form Create Pool
FORM_ID_CREATE_POOL = "FORM_CREATE_POOL"
FORM_TITLE_CREATE_POOL = "Create pool"

##Manage pools Form
FORM_ID_MANAGE_POOLS = "MANAGE_POOLS"
FORM_TITLE_MANAGE_POOLS = "Manage pools"
FORM_MENU_MANAGE_POOLS = {
    "Create pool":{ 
        "Action":"FormSwitch",
        "Arguments": [FORM_ID_CREATE_POOL]
    },
    "Import pool":{ 
        "Action":"FormSwitch",
        "Arguments": []
    },
    "Export pool":{ 
        "Action":"FormSwitch",
        "Arguments": []
    },
    "Destroy pool":{ 
        "Action":"FormSwitch",
        "Arguments": []
    },
    "Back":{ 
        "Action":"FormSwitch",
        "Arguments": ["Previous"]
    }
}

##Pool information Form
FORM_ID_POOL_INFO = "POOL_INFO"
FORM_TITLE_POOL_INFO = "Pools information"
FORM_MENU_POOL_INFO = {
    "Pool health":{
        "Action":"CommandModal",
        "Arguments":["zpool", "get", "health", "-p"] 
    },
    "Pool status":{
        "Action":"CommandModal",
        "Arguments":["zpool", "status", "-p"] 
    },
    "Back":{ 
        "Action":"FormSwitch",
        "Arguments": ["Previous"]
    }
}

##Main Form
FORM_ID_MAIN = "MAIN"
FORM_TITLE_MAIN = "Main menu"
FORM_MENU_MAIN = {
    "Pool info": {
        "Action":"FormSwitch",
        "Arguments": [FORM_ID_POOL_INFO]
        },
    "Manage pools": {
        "Action":"FormSwitch",
        "Arguments": [FORM_ID_MANAGE_POOLS]
        },
    "Exit": {
        "Action":"FormSwitch",
        "Arguments":[None]
    } 
}