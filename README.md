# SpendBot
###### Language: Python  
###### Libraries: aiogram, pandas, sqlalchemy, matplotlib
## Features:
### 1.Adding spending
![Cost adding](images/1costs_adding.png)
### 2. View spending as pie charts
![Costs pie graph](images/2pie_view.png)
### 3. Support for family spending
![Family costs](images/3family_support.png)
## Before the beginning
First you need to install the PostgreSQL server  

For Arch Linux:
```
sudo pacman -S postgresql
systemctl start postgresql
systemctl enable postgresql
```
Then you need to clone this repository:
```
git clone https://github.com/akulij/spendstatbot.git
cd spendstatbot
```
## Setup
If you need to setup bot in virtual enviroment, enter in your shell:
```bash
make venv
source venv/bin/activate
```

Then enter:
```
make setup
```
to setup the bot.

You need to enter corect values in fields.  
Some fields have default values. To keep them just hit Enter.

## Start
To start bot just enter:
```
make
```
