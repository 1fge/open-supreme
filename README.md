# Open Supreme
*Open Supreme* is a 100% open source requests-based Supreme program  

Created by [@internalises](https://twitter.com/internalises) (nested#1389)  
Join the discord here https://discord.gg/Yfz62NV  

If you encounter any problems feel free to message me on Discord or Twitter. I will continue to fix any issues that arise from Supreme modifying their website, and am planning on implementing a hybrid method soon.

## Features
* **<1 Second Checkout Times**  
* Unlimited Tasks that run concurrently
* Proxy support   
* Ability to have different tasks use different profiles
* Custom checkout delay per task

## Installation
To Install Files:  
```bash
git clone https://github.com/1fge/open-supreme
```
To Install Required Modules:  
```bash
pip install -r requirements.txt
```

  

## Usage
Unlike previous versions, the entire program can be interacted with using one file, osp.py. This script can be accessed by opening the command prompt in the open-supreme folder and typing: 
```bash
python osp.py
```
After successfully getting osp.py to run, make sure you create at least one profile before attempting to make tasks. As mentioned above, you can run with as many tasks and profiles as you want. Note: Don't try to edit **tasks.json** or **profiles.json** without osp.py as it could cause breaking changes.

When you are ready to start your tasks, go to the main menu and input `2` or `Open-Supreme`. Then, type `run` and the bot will start! To get the program to stop, just hit enter.
  

## Important Information 
1. This bot will fail while ticket is enforced as it has no ticket workaround.
2. *Open Supreme* only works in the U.S. Other regions may be added later. 
3. Color names must be exact matches otherwise the program won't find your item (not case-sensitive)
4. For all of the categories and sizes you should use, check out the discord!

## TODO
- [ ] Captcha Harvester
- [ ] Implement Hybrid Ticket Solution
- [ ] Improve Process of Starting and Stopping Tasks
- [ ] Add More Regions
- [ ] More Descriptive Error Handling
