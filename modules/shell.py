import subprocess

def execute(commandList: list):
    command:str = ' '.join(map(str, commandList))
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
    except:
        return "Error"
    return result.stdout