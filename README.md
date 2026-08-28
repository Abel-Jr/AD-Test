# AD-Test Lab

Just a personal lab I set up to learn more about Active Directory security - how it breaks, how attacks actually work in practice, and how you'd go about detecting them. Everything runs in an isolated environment, nothing here touches a real network.

Disclaimer: this is for learning only. Don't run any of this against systems you don't own or don't have permission to test on. Unauthorized access is illegal, full stop.

What's in here

I'm using BadBlood to populate the domain with a bunch of fake users, groups, OUs, and permissions. It's basically a script that trashes an otherwise clean AD install and makes it look like a real (messy) company environment - broken ACLs, weird delegations, the usual stuff you'd find on an actual pentest.

Setup

You'll need:

A hypervisor (I'm using VirtualBox, but VMware/Hyper-V/Proxmox all work)
A Windows Server VM promoted to a domain controller
The network fully isolated - no internet, no bridging to anything else
BadBlood cloned onto the DC

Once the DC is up and running:
- git clone https://github.com/davidprowe/BadBlood.git
- cd BadBlood
- .\Invoke-BadBlood.ps1

Let it run, it'll take a while. When it's done you'll have hundreds of users/groups/OUs and a bunch of intentional misconfigurations scattered around the domain.

To check it worked, just poke around in ADUC or run a few Get-ADUser / Get-ADGroup commands. Better yet, point BloodHound at it and see what attack paths show up.

Tools I'm using alongside this
BloodHound - to visualize attack paths in the domain
PingCastle - quick AD security audit/scoring
Impacket - various AD attack scripts
Rubeus - Kerberos stuff (roasting, ticket abuse, etc.)
Why

Mostly to get more comfortable with AD enumeration and common attack techniques (Kerberoasting, AS-REP roasting, ACL abuse, unconstrained delegation...) without needing an actual company's infra to mess with. Also useful for testing detection rules on the blue team side once I get a SIEM hooked up.