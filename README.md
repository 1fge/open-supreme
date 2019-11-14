# Open Supreme
*Open Supreme* is a 100% open source requests-based Supreme program  

Created by [@qwkinn](https://twitter.com/qwkinn) (nested#1389)  
Join the discord here https://discord.gg/Yfz62NV  
**Watch the video tutorial from Drops by Mitch [here](https://www.youtube.com/watch?v=aNO_1Oxs0RY)**  

If you encounter any problems feel free to message me on Discord or Twitter. I will continue to fix any issues that arise from Supreme modifying their website, but I most likely will not be adding anymore features to the program (including a pooky solution). Your contribution is very much encouraged! 

## Features
* **1 Second Checkout Time**  
* Unlimited Tasks that run concurrently
* Proxy support
* Captcha Bypass    
* Ability to have different tasks use different profiles

## Installation
type 
```bash
git clone https://github.com/1fge/open-supreme
```
Ensure Python 3 with the requests library is installed 
  

## Usage 
*Open Supreme* comes with two files titled ***addRemoveProfiles.py*** and ***addRemoveTasks.py***. As their names suggest, this is how you will add, remove, view, or delete profiles and tasks. Feel free to run them in an IDE of your choice or simply from the command line. I highly recommend you DO NOT try and edit  ***profiles.json*** or ***tasks.json*** without the above scripts as it could break the program.

Once all of your tasks are created, open command prompt in the folder and enter:
```bash
python main.py
```
This will start all tasks and they will run until a slug is generated or the product is found (with the exception of some error handling) Unfortunately, I didn't implement a way to stop a task while still letting others run. This is where *Open Supreme* could use help from the community.  

## Important Information 
1. This bot will fail while pooky is enabled as it has no pooky workaround.
2. *Open Supreme* only works in the U.S. Other regions may be added later. 
3. I haven't implemented proxy support. This will *probably* get added
4. Try to be case-sensitive for categories, and for tops and sweaters use ***'Tops/Sweaters'***
5. Color names must be exact matches otherwise the program won't find your item (not case-sensitive)
6. For items that don't have sizes, enter ***'N/A'*** for size
7. If you want an extra-large item, enter ***'XLarge'***
