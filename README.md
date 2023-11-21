# somaPyParserRemote

## Purpose and Goals
1. Analyze the log files of remote linux machines in a convenient fashion via a psuedo console.
2. Lightweight: Data transfer happens via SSH, doesn't require any extra software.
3. Flexible: Can handle non-normalized logs because it uses regex not column numbers.
4. Customizable: Add hosts, log paths, and regex strings easily.
5. Ease of Use: Can be configured via the Startup list to automatically pull multiple logs upon executing the script. Macros can be set via the MacroMap.

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
As detailed via comments in somaPyParser.py, edit the HostMap, LogMap, and ReMap dictionaries as per your needs, then open a terminal and run the script using:
```bash
python3 somaPyParserRemote.py
```

## Examples

## Load data
Load a remote file:
```
load auth ubuntu1 ubu1
```
Load a local file:
```
loadlocal auth.log ubu2
```

## Show the UI
Check the Dashboard:
```
d
```
Check the help screen:
```
h
```

## Switch between logs
switch to log ubu1
```
use ubu1
```
switch to log ubu2
```
use ubu2
```

## Dynamically entered Regex strings
Save a temporary regex string (escape special characters)
```
save 127.0.0.1 myip
```
Save a temporary regex string (keep regex special characters)
```
saveraw [0-9]{10} numchunk
```

## Analysis
Filter by accepted SSH logins:
```
filter accepted
```
Count distinct ips
```
distinct ip
```
Filter by accepted, then count distinct ips
```
filter accepted distinct ip
```
