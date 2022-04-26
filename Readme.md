# LSTS
## _Local Stock Tracking System_

[![Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org/)

Tracks the stock of local pharmacies to help people find their medicine easier

- Track items availability in drug stores near you
- Spend less time searching for the right place to get your meds
- Helps you use your time with more efficiency

## Valuable information
- The default username and password for UPA-SUL is "admin"
- The default username and password for UPA-LESTE is "leste"

## Features

- Automagically gets the latest availability data and prices
- Export your items list with prices as a text file

## Warning
> :warning: **This is a PoC project for educational purposes only**: We don't provide any support, use at your own risk!

## Installation

- LSTS requires Python 3.9.7 or later

### Linux

#### Ubuntu

```sh
git clone https://github.com/Gater73/LSTS.git
pip3 install -r requirements.txt 
```

#### Other distros

```sh
git clone https://github.com/Gater73/LSTS.git
pip install -r requirements.txt 
```

#### Windows (Git Bash)
```sh
git clone https://github.com/Gater73/LSTS.git
pip install -r requirements.txt 
```

## Run

### Linux

#### Ubuntu
```sh
python3 main.py
```

```sh
python3 admin/main.py
```

#### Other distros
```sh
python main.py
```

```sh
python admin/main.py
```

#### Windows
> You can run LSTS in windows simply by running _start.bat_ in the repository folder you cloned to your PC.

> Start _start-admin.bat_ to open the admin UI.

## License

[GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)

[//]: # (Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [Name]: <Link>
