#somaPyParserRemote
#Laurence Welch

import subprocess
import re

##########################################################
#                                                        #
# Config Section                                         #
#                                                        #
# Brief Description of Variables                         #
#   1. HostMap:  used to reference remote machines.      #
#                                                        #
#   2. LogMap:   used to reference logs within a remote  #
#                machine.                                #
#                                                        #
#   3. ReMap:    used to pull 'fields' from log entries. #
#                                                        #
#   4. MacroMap: map strings to commands.                #
#                                                        #
#   3. Startup:  run commands as soon as you execute     #
#                this script.                            #
#                                                        #
##########################################################

#   HostMap
#Edit this to add remote hosts. This script requires the configuration of your ~/.ssh/config file.
#key: how this script references the dictionary entry.
#value: an array consisting of: 
#   1. the command used to ssh (ssh).
#   2. the ~/.ssh/config machine name (i.e. if you ssh using the command 'ssh ubuntu1', the value here should be ubuntu1).
#   3. the command used to print data to stdout (cat).
HostMap = {
    'ubuntu1': ['ssh', 'ubuntu1', 'cat']
}

#   LogMap
#Edit this to add log references. Each entry represents the path of a log on a remote machine, e.g. /var/log/auth.log. This path will be automatically appended to the command: e.g. 'ssh ubuntu1 "cat /etc/var/auth.log"'.
LogMap = {
    'auth': '/var/log/auth.log'
}

#   ReMap
#Edit this to add regex strings which can be used to filter logs, and pull specific fields from logs. Each entry represents a regular expression string.
#You can create dynamic (temporary) entries using the command: save <key name> <regex string>
#The above command will, for convenience, escape special regex characters.
#If you don't want special characters escaped, use the command: saveraw <key name> <regex string>
ReMap = {
    #successful ssh logins
    'accepted': 'Accepted',
    #invalid login attempt
    'invalid': 'Invalid',
    #ip address (ipv4)
    'ip': '([0-9]{1,3}\.){3}[0-9]{1,3}',
}

#   MacroMap
#Edit this to map a string to a command. After you input something and press enter, this script first checks if you entered a macro, if so, it grabs that macro and inputs it into the main parser.
#A good use case for this feature would be to load local logs with paths that are annoying to type out.
#Another good use would be to execute long, commonly used queries.
MacroMap = {
    #'loadubu1': 'loadlocal auth.log ubu1'
}

#   StartupCommands
#Commands in this list will be run, in order, upon starting this script. If you always pull the same logs, loading them at startup might be a good idea.
Startup = [
    #'loadubu1',
    'd'
] 

#########################
#                       #
# End of Config Section #
#                       #
#########################

#Globals
LogObj = {}
CurrentKey = ''

#print log contents
def printResult(l):
    print('-----results-----')
    for line in l:
        print(line)

#print informative message
def printSys(label, value):
    print('<>', label, ':', value)

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
    print('dashboard:       d')
    print('quit:            q')
    print('load data:       load <LogMap key> <HostMap key> <pick a name>')
    print('load local data: loadlocal <fileName> <pick a name>')
    print('switch logs:     use <log>')
    print('print all:       all')
    print('filter:          filter <ReMap key>')
    print('distinct:        distinct <Remap key>')
    print('save to ReMap:   save|saveraw <regex string> <pick a name>')

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
    printSys('rows displayed', len(log))
    printSys('log total rows', len(LogObj[CurrentKey]))

#save a temp regex string
def saveReMap(name, string, escape=True):
    if name in ReMap:
        print('error: name already taken')
    else:
        string = re.escape(string)
        ReMap[name] = string
        printSys('temporarily saved', string + ' as ' + name)

#used while parsing a save command
def branchSave(cmdList):
    if len(cmdList) != 3:
        print('error: try: save|saveraw <regex string> <pick a name>')
        return
    first,second,third = cmdList
    #escape special chars unless saveraw
    shouldEscape = first == 'save'
    saveReMap(third, second)

#used while parsing <operator> <regex string> commands
def branchOperator(cmdList):
    #exit conditions
    if CurrentKey == '':
        print('error: set a current log first: set <name of loaded log>')
        return
    log = LogObj[CurrentKey]
    if not log:
        print('fatal error in: def branchOperator')
        return
    if len(cmdList) < 2:
        print('error: expected: <command> <regex string>')
    #calculate number of queries
    numCmds = int(len(cmdList) / 2)
    #parsing starts here
    for i in range(numCmds):
        #pull two words i.e. <command> <regex string>
        nextCmd = cmdList[i * 2: i * 2 + 2]
        first,second = nextCmd
        #check if regex string exists
        if second not in ReMap:
            print('error: key', second, 'not found in ReMap')
            return
        regexString = ReMap[second] 
        if first == 'filter':
            log = filterLog(regexString, log)
        elif first == 'distinct':
            log = distinct(regexString, log)
        elif first == 'distinctr':
            log = distinct(regexString, log, reverseResults=True)
    printResult(log)
    printCount(log)

#modify this for testing local logs
def getLocalLog(cmdList):
    if len(cmdList) != 3:
        print('error: expected: loadlocal <fileName> <pick a name>')
        return
    try:
        _,fileName,key = cmdList
        global CurrentKey
        if key in LogObj:
            print('error: that name already exists')
            return
        LogObj[key] = []
        #read the file
        with open(fileName) as f:
            for line in f: 
                LogObj[key].append(line.strip())
        CurrentKey = key
        printSys('loaded', fileName + ' as ' + key)
        printSys('set', fileName + ' as ' + key)
    except:
        print('error: failed loading local file: ' + fileName)

#pull remote log using SSH
def getLog(cmdList):
    #exit conditions
    cmdError = 'error: expected: load <LogMap key> <HostMap key> <pick a name>'
    if len(cmdList) != 4:
        print(cmdError)
        return
    _,path,host,key = cmdList
    if key in LogObj:
        print('error: ' + key + ' already exists') 
    #key error
    if path not in LogMap or host not in HostMap:
        errorP1 = 'error: LogMap key or HostMap key is invalid:'
        errorP2 = cmdError
        print(errorP1, errorP2)
        return
    #pull the file using SSH
    global CurrentKey
    cmd = HostMap[host]
    cmd.append(LogMap[path])
    out = subprocess.run(cmd, capture_output=True).stdout.decode().strip()
    lines = out.split('\n')
    LogObj[key] = lines    
    CurrentKey = key
    printSys('loaded', path + ' from ' + host + ' as ' + key) 
    printSys('set', key + ' as current log')

#grabs log using SSH or grabs a local log
def branchLoad(cmdList):
    if cmdList[0] == 'load':
        getLog(cmdList)
    else:
        getLocalLog(cmdList)

#switch current log
def branchUse(cmdList):
    global CurrentKey
    if len(cmdList) != 2:
        print('error: expected: use <log key>')
        return
    key = cmdList[1]
    if key not in LogObj:
        print('error: key not found, type d to view loaded logs')
        return
    CurrentKey = key
    printSys('set', 'switching current log to: ' + key)

#print the whole log
def branchAll():
    if CurrentKey not in LogObj:
        print('error: no current log, type d to view dashboard')
        return
    log = LogObj[CurrentKey]
    printResult(log)    
    printCount(log)

#parse user input into commands
def parseCommand(command):
    cmdList = command.split()
    if len(cmdList) == 0:
        return
    first = cmdList[0]
    #parsing starts here
    if first in ['h', 'help']:
        printHelp()
    elif first == 'd':
        printDashboard()
    elif first in ['load', 'loadlocal']:
        branchLoad(cmdList)
    elif first == 'use':
        branchUse(cmdList)
    elif first == 'all':
        branchAll()
    elif first in ['save', 'saveraw']:
        branchSave(cmdList) 
    elif first in ['filter', 'distinct']:
        branchOperator(cmdList)
    else:
        print('command failed, type: h for help')

#main
def main():
    #startup tasks 
    #You can add/remove startup tasks by editing the Startup list in the config section
    for i in Startup:
        cmd = MacroMap[i] if i in MacroMap else i
        parseCommand(cmd) 
    while True:
        ui = input('>')
        #check if macro
        if ui in MacroMap:
            ui = MacroMap[ui]
        if ui in ['q', 'exit']:
            break
        parseCommand(ui)

main()
