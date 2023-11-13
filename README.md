# somaPyParserRemote

## Summary
Pull and parse data using SSH and regex. Customize and save commands for rapid log analysis.

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

## Parser Setup


