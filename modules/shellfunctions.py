import modules.shell as s


def getHDDs():
    command:list = ["ls /dev/ | grep -s -E '(sd|hd)[a-z]+$'"]
    output:str = s.execute(command)
    result:list = list(filter(lambda x: x != '', map(lambda x: x.strip(), output.split('\n'))))
    result = list(map(lambda x: "/dev/"+x, result))
    result.sort()
    return result

