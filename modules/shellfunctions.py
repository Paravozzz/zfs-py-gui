import modules.shell as s


def getHDDs():
    command: list = ["ls /dev/ | grep -s -E '(sd|hd)[a-z]+$'"]
    command_stdout, command_stderror = s.execute(command)
    result: list = list(map(lambda x: x.strip(), command_stdout.split('\n')))
    result = list(filter(lambda x: x != '', result))
    result = list(map(lambda x: "/dev/" + x, result))
    result.sort()
    return result
