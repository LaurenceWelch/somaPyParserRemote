#Laurence Welch

import subprocess
import re

##################
#                #
# Config Section #
#                #
##################

#   pullMap
#Each entry in this dictionary represents a remote machine. This script requires the configuration of your ~/.ssh/config file.
#key: how this script references the dictionary entry.
#value: an array consisting of: 
#   1. the command used to ssh (ssh).
#   2. the ~/.ssh/config machine name (i.e. if you ssh using the command 'ssh ubuntu1', the value here should be ubuntu1).
#   3. the command used to print data to stdout (cat).
PullMap = {
    'ubuntu1': ['ssh', 'ubuntu1', 'cat']
}

#   logMap
#Each entry represents the path of a log on a remote machine, e.g. /var/log/auth.log. This path will be automatically appended to the command: e.g. 'ssh ubuntu1 "cat /etc/var/auth.log"'.
LogMap = {
    'auth': '/var/log/auth.log'
}

#   reMap
#Each entry represents a regular expression string.
ReMap = {
    #successful ssh logins
    'accepted': 'Accepted',
    #ipv4 address
    'ip': '([0-9]{1,3}\.){3}[0-9]{1,3}'
}

######################
#                    #
# End Config Section #
#                    #
######################

LogObj = {}
CurrentKey = 'tl'

def printResult(l):
    for line in l:
        print(line)

#for testing
def getLocalLog():
    LogObj['tl'] = []
    with open('auth.log') as f:
        for line in f: 
            LogObj['tl'].append(line)

#prints each loop iteration
def printDashboard():
    keyStr = ''
    keys = list(LogObj.keys())
    keyStr = '(none)' if not keys else ', '.join(keys)
    curLog = '(none)' if CurrentKey == '' else CurrentKey
    #print the dashboard
    print('---------- Dashboard ----------')
    print('logs loaded:', keyStr)  
    print('current log:', curLog)
    print('h for help')
    print('-------------------------------')

#cheatsheet
def printHelp():
    print('load data: get <pullMap key> <logMap key>')
    s = 'filter count limit'

#filter based on a regex string
def filterLog(string, log):
    result = []
    for line in log:
        re.search(string, line) and result.append(line)
    return result

#count distinct regex matches
def distinct(string, log, reverseResults=False):
    result = []
    sortFun = lambda x: int(x[0:x.index(' ')])
    d = {}
    for line in log:
        o = re.search(string, line)
        if o:
            val = o.group()
            if val in d:
                d[val] += 1 
            else:
                d[val] = 1
    for k in d:
        result.append(str(d[k]) + ' times ' + str(k))    
    result.sort(key=sortFun, reverse=reverseResults)
    return result

#count results
def printCount(log):
    print('==> rows displayed:', len(log))
    print('==> log total rows:', len(LogObj[CurrentKey]))

#save a temp regex string
def saveReMap(name, string, escape=True):
    if name in ReMap:
        print('error: name already taken')
    else:
        string = re.escape(string)
        ReMap[name] = string
        print('==> saved', string, 'as', name)
    
#parse user input into commands
def parseCommand(command):
    if command == 'h':
        printHelp()
    test1 = '103.180.149.133'
    saveReMap('badip', test1)
    command = 'filter badip'
    cmd = command.split() 
    if len(cmd) < 2:
        return
    numCmds = int(len(cmd) / 2)
    if CurrentKey == '':
        print('error: set a current log first')
        return
    log = LogObj[CurrentKey]
    if not log:
        print('error: key didn\'t seem to work')
    for i in range(numCmds):
        nextCmd = cmd[i * 2: i * 2 + 2]
        first = nextCmd[0]
        second = nextCmd[1]
        if second not in ReMap:
            print('error: regex string', second, 'not found in ReMap')
        regexString = ReMap[second] 
        if first == 'filter':
            log = filterLog(regexString, log)
        elif first == 'distinct':
            log = distinct(regexString, log)
        elif first == 'distinctr':
            log = distinct(regexString, log, reverseResults=True)
   #print results
    printResult(log)
    printCount(log)

def main():
#    cmd = pullMap['ubuntu1']
#    cmd.append(logMap['auth'])
#    print(cmd)
#    out = subprocess.run(cmd, capture_output=True).stdout.decode().strip()
#    lines = out.split('\n')
#    reStr = reMap['authAccept']
#    result = []
#    for line in lines:
#        re.search(reStr, line) and result.append(line)
#        
#    printResult(result)
    getLocalLog()
    printDashboard()
    parseCommand('')
          
main()
