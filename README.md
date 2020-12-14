# dynamic_inventory_generator

Let's say you have a host file that looks similar to this:

```
XXX.XX.X.XXX            SITE-u00-os-01a         ## OWNER:  UNIT NAME

XXX.XX.X.XXX            SITE-u00-os-01b         ## OWNER:  UNIT NAME
```

And you want to make every host in the file automatable with Ansible.

Moreover, chance are, that host file changes over time. How do you make Ansible aware of those hosts as the hosts file changes?

This is known as [dynamic inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_dynamic_inventory.html) and Ansible has a few methods for dealing with it.

This repo uses a Python script to take the hosts file and make an Ansible parsable yaml file.

It's currently a work in progress and we look forward to continuing to improve it.

## Useful Resources on Dynamic Inventory in Ansible

For an introduction to dynamic inventory and how it differs from static inventory, check out these resources

* [Ansible Dynamic Inventory: Is It So Hard?](https://blog.opstree.com/2019/05/14/ansible-dynamic-inventory-is-it-so-hard/)
* [Quick Introduction to Static and Dynamic Inventory](https://www.youtube.com/watch?v=VlIl2gyF7kA)

## Usage

* You need Python 3 installed on your workstation. To check whether you have Python3 installed (NOTE: it must be Python 3, not Python 2), run this command in your terminal:

```bash
$ python3 --version
```

* You also need pip3 installed on your workstation. To check, run:

```bash
$ pip3 --version
```

* Then you will need to clone this repository using git

```bash
$ git clone https://github.com/injectedfusion/dynamic_inventory_generator.git
```

* Then change directories into the repo and install the requirements using pip3

```bash
$ cd dynamic_inventory_generator
$ pip3 install -r requirements.txt
```

## Creating the required files

You will need three additional files to run this script:
* hosts file (sample [here](tmp/hosts))
* site names mapping file (sample [here](mappings/sites.json))
* device names mapping file (sample [here](mappings/devices.json))

### Hosts File

The hosts file container the informations for the hosts you want to automate with Ansible.

We have provided a sample hosts file in /tmp/hosts, which looks similar to this:

In this sample, we pretend that we are tracking hosts for various Disneyland resorts all in one hosts file. (You can access the full file [here](tmp/hosts)).

**/tmp/hosts**
```bash
172.18.0.128             DR13-u00-os-01a         ## OWNER:  Rescue Rangers
172.18.0.129             DR13-u00-os-01b         ## OWNER:  Rescue Rangers
172.16.0.128             DLCA-u00-os-01a         ## OWNER:  Mouseketeers
172.16.0.129             DLCA-u00-os-01b         ## OWNER:  Mouseketeers
172.19.0.128             DLFR-u00-os-01a         ## OWNER:  7 Dwarves
172.19.0.129             DLFR-u00-os-01b         ## OWNER:  7 Dwarves
172.18.8.128             DR13-u00-os-02a         ## OWNER:  Lost Boys
172.18.8.129             DR13-u00-os-02b         ## OWNER:  Lost Boys
172.18.16.128            DR13-u00-os-03a         ## OWNER:  King Tritons Daughters
172.18.16.129            DR13-u00-os-03b         ## OWNER:  King Tritons Daughters
172.17.0.128             WDWR-u00-os-01a         ## OWNER:  The Flying Dutchman
172.17.0.129             WDWR-u00-os-01b         ## OWNER:  The Flying Dutchman
```

As you can see, each entry has an IP address, followed by a site designation, and an owner

**Site Designations**

Let's take a closer look at one of the hosts:

```
172.18.0.128             DR13-u00-os-01a         ## OWNER:  Rescue Rangers
```

And let's focus on the site designation:

```
DR13-u00-os-01a 
```

In this example, we have made up abbreviations for each Disneyland resort - "DLCA" represents "Disneyland Resort Anaheim", "WDWR" represents "Walt Disney World Resort Orlando", etc.

To help with translating site abbreviations into site names in the Ansible yaml file, we have created a legend for the abbreviations in [this file](mappings/sites.json).

### Site Names Mapping File

You will need a file which maps your site abbreviations to the full name for the site. We have created a sample on in this repo:

**mappings/sites.json**
```
{
    "DLCA":"Disneyland Resort Anaheim",
    "WDWR":"Walt Disney World Resort Orlando",
    "DR13":"Tokyo Disney Resort",
    "DLFR":"Disneyland Paris",
    "DLHK":"Hong Kong Disneyland Resort",
    "DRCN":"Shanghai Disney Resort"
}
```

So the host with this designation:

```
DR13-u00-os-01a
```

is in the Tokyo Disney Resort.

Continuing our examination of the site designation:

```
u00
```
* Means the device is public.

```
os
```
* means the device type is an outer switch

### Device Types Mapping File

You will need a Device Types Mapping file as well, which maps device type abbreviations to the full name for that device type.

We have created a sample in this repo:

**mappings/devices.json**

```
{
{
    "os":"outer_switches",
    "is":"inner_switches",
    "as":"access_switches",
    "cs":"core_switches",
    "ds":"distro_switches"
}
```

Now let's look at the next part of the host designation `DR13-u00-os-01a`

```
01a
```
* Means the device is the first of that kind in its site and a or b indicates it is in a pair.

So, when we put it all together, we can gain this information from the site designation:

```
DR13-u00-os-01a
```
* **DR13** means the device is in the Tokyo Disneyland Resort
* **u00** means it is a public device
* **os** indicates that it is an outer switch
* **01a** indicates that it is the first device of its kind at that site and is in a pair

## Running the script

Now, let's run the script.

```bash
$ python3 parser.py

Starting the dynamic inventory generator...
```


You will be prompted for the path to your hosts file (the sample one in this repo is at `./tmp/hosts`).

```bash
Please enter the path to your hostfile (for example, ./tmp/hosts):
```

Then you will be prompted for the path to your sites name mapping file (the sample one in this repo is at `./mappings/sites.json`).

```bash
Please enter the path to your sites name mapping file (for example, ./mappings/sites.json):
```

Finally, you will be prompted for the path to your device mapping file (the sample one in this repo is at `./mappings/devices.json`).

```bash
Please enter the path to your device mapping file (for example, ./mappings/devices.json):
```

After you provide the required input, you will see:

```bash
Generating output.yml file...
Finished generating output.yaml
```

And you will now have a file called output.yaml in your local directory.

If I open it up, you will see output similar to this:

```bash
all:
  children:
    disneyland_paris:
      7_dwarves:
        outer_switches:
        - DLFR-u00-os-01a:
            ansible_host: 172.19.0.128
        - DLFR-u00-os-01b:
            ansible_host: 172.19.0.129
      gargoyles:
        outer_switches:
        - DLFR-u00-os-02a:
            ansible_host: 172.19.8.128
        - DLFR-u00-os-02b:
            ansible_host: 172.19.8.129
      prince_johns_guards:
        outer_switches:
        - DLFR-u00-os-03a:
            ansible_host: 172.19.16.129
        - DLFR-u00-os-03b:
            ansible_host: 172.19.16.129
    disneyland_resort_anaheim:
      mighty_ducks:
        outer_switches:
        - DLCA-u00-os-03a:
            ansible_host: 172.16.16.128
        - DLCA-u00-os-03b:
            ansible_host: 172.16.16.128
      mouseketeers:
        outer_switches:
        - DLCA-u00-os-01a:
            ansible_host: 172.16.0.128
        - DLCA-u00-os-01b:
            ansible_host: 172.16.0.129
      nutcracker_sentries:
        outer_switches:
        - DLCA-u00-os-02a:
            ansible_host: 172.16.8.128
        - DLCA-u00-os-02b:
            ansible_host: 172.16.8.128
    hong_kong_disneyland_resort:
      muppets:
        outer_switches:
        - DLHK-u00-os-01a:
            ansible_host: 172.20.0.128
        - DLHK-u00-os-01b:
            ansible_host: 172.20.0.129
    shanghai_disney_resort:
      zurg_bots:
        outer_switches:
        - DRCN-u00-os-01a:
            ansible_host: 172.21.0.128
        - DRCN-u00-os-01b:
            ansible_host: 172.21.0.128
```

**More coming soon!**

