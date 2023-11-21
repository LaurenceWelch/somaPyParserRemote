# somaPyParserRemote

## Purpose and Goals
1. Analyze the log files of remote linux machines in a convenient fashion.
2. Lightweight: Data transfer happens via SSH, doesn't require any extra software.
3. Flexible: Can handle non-normalized logs because it uses regex not column numbers.
4. Customizable: Add hosts, log paths, and regex strings easily.

## Security Considerations
This script uses the subprocess module to run bash commands. Anyone with write access could modify said commands for nefarious purposes. If the remote user has root privileges, users running this script will have root privileges on the remote machine.

## Guide

## SSH Setup
1. Ensure the remote host(s) allows key-based authentication.
2. Edit/Create your ~/.ssh/config file to include your remote host, for example:

```
Host [pick a name]
    HostName [host]
    User [user]
    IdentityFile [path to key, example: ~/.ssh/key.pem]
```

3. Test connection using:

```bash
ssh [name you picked]
```
4. Celebrate!

## Running the parser

Look at somaPyParserRemote.py to learn what to edit. When everything is in order, open a terminal and enter:
```bash
python3 somaPyParserRemote.py
```

## Examples

```bash
#load a remote log into a variable
#load <LogMap key> <HostMap key> <pick a name>
load auth ubuntu1 ubu1

#load a local log
#loadlocal <fileName> <pick a name>
load auth.log ubu2

#filter by accepted logins
#filter <ReMap key>
filter accepted

#filter by accepted than count distinct ips
#filter accepted distinct ip
```
