import subprocess

def execute(commandList: list):
    command:str = ' '.join(map(str, commandList))
    result = None
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
    except Exception as e:
        return (str(""), str(e))
    return (result.stdout, result.stderr)