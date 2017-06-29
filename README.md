Hydra
=========================

* [What is this?](#what-is-this)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage & Useful Commands](#usage-&-useful-commands)

What is this?
-------------------
Our Revolution's event promotion & events management tool, complete with other goodies.

Prerequisites
-------------------
1. [Pip](https://pip.pypa.io/en/stable/installing/)
2. [Postgres](https://www.postgresql.org/download/)
3. [Our Revolution's Main Site](https://github.com/Our-Revolution/site) running locally
3. **Recommended** - [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

Installation
-------------------
Clone this repository and navigate to the project directory.
```
git clone git@github.com:Our-Revolution/hydra.git
cd hydra
```
Optionally, make a [virtualenv](https://pypi.python.org/pypi/virtualenv) and activate it using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
```
mkvirtualenv hydra
workon hydra
```
Install required packages.
```
pip install -r requirements.txt
```
#### Populate Zip Code Data
Download zip code data and extract all files to `data/zipcodes/`

[2015 cartographic boundary file, 5-digit ZIP code tabulation area for United States, 1:500,000 from data.gov](http://www2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_us_zcta510_500k.zip)

#### Main Site Database
Hydra utilizes the database from [Our Revolution's Main Site](https://github.com/Our-Revolution/site). Make sure you set `GROUP_DATABASE_URL` to that local database in your `.env`.

Usage & Useful Commands
-------------------
From the working directory:

```
# Run Local Server
./manage.py runserver

# Make Migrations
./manage.py makemigrations

# Run Migrations
./manage.py migrate
```
