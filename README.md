# <img itemprop="image" class="avatar flex-shrink-0 mb-3 mr-3 mb-md-0 mr-md-4" src="https://avatars.githubusercontent.com/u/89392827?s=200&amp;v=4" width="100" height="100" alt="@CMU-MS-DAS-Vis-Mini Spring 2022"> CMU-MS-DAS-Vis-Flask
CMU MS-DAS Visualization Class course Flask lab

## Quick Start ##

This repo is meant to provide a simple Flask environment for class experiments.
These instructions assume conda is already installed.
To set things up:
1) Clone this repo to your local machine.
2) cd into the repo you've just cloned.
3) Create the virtual environment, as follows:
On Linux or macOS do:
```
$ conda create --name FlaskEnv python=3.8
$ conda activate FlaskEnv
$ pip install -r requirements.txt
```
On Windows do:
```
>conda create -n FlaskEnv python=3.8 anaconda
>activate FlaskEnv
>pip install -r requirements.txt
```
4) Start up the server:
On Linux or macOS do:
```
$ bash init_db.sh
$ bash run_app.sh
```
On Windows do:
```
>set FLASK_APP=myproj
>set FLASK_DEV=development
>flask init-db
>flask run
```
5) The Flask server should now be running in the window where you issued
   the run-app command.  Connect to the server from a web browser. The
   URL should be visible in the window, but it is probably
   http://127.0.0.1:5000/
