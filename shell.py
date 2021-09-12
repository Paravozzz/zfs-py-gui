import subprocess

def execute(commandList: list):
    try:
        result = subprocess.run(commandList, stdout=subprocess.PIPE, text=True)
    except:
        return "Error"
    return result.stdout