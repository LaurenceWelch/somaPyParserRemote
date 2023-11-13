#Laurence Welch

import subprocess
import re

#   pullMap
#Each entry in this dictionary represents a remote machine.
#The key is how you reference it from within this script
#index 0: the command used to ssh into the remote machine, i.e. ssh
#index 1: must match the name in ~/.ssh/config e.g. if you SSH using the command: 'ssh ubuntu1', index 1 should be ubuntu1
#index 2: the command to print data to stdout, i.e. cat
pullMap = {
    'ubuntu1': ['ssh', 'ubuntu1', 'cat']
}

#   logMap
#Each entry represents the path of a log on a remote machine, e.g. /var/log/auth.log
#This path will be automatically appended to the command
logMap = {
    'auth': '/var/log/auth.log'
}

#   reMap
#Each entry represents a regular expression string.
reMap = {
    #successful ssh logins
    'authAccept': 'Accepted'
}

def printResult(l):
    for line in l:
        print(line)

def main():
    cmd = pullMap['ubuntu1']
    cmd.append(logMap['auth'])
    print(cmd)
    out = subprocess.run(cmd, capture_output=True).stdout.decode().strip()
    lines = out.split('\n')
    reStr = reMap['authAccept']
    result = []
    for line in lines:
        re.search(reStr, line) and result.append(line)
        
    printResult(result)
          

main()
