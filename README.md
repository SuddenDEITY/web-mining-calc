# Web Mining Calculator
Hello! This is application that shows actual mining profitability on most GPU's.

It uses django for backend and playwright for parsing.

This application also shows:
- USD price
- EUR price
- ETH price
- TON price


## Instalation
First of all, you need to git clone this repo:
```
git clone https://github.com/SuddenDEITY/web-mining-calc <directory_you_want>
```
Since this app is containerized with docker, all you need is:
```
docker-compose up --build (you can use -d to run it in dedicated mode)
```
Now we need to make migrations:
```
docker-compose exec web python3 manage.py makemigrations
```
Then, migrate:
```
docker-compose exec web python3 manage.py migrate
```
And last step is preload data with gpu parameters like hashrate and so on:
```
docker-compose exec web python3 loaddata data.json
```
Now we can restart container with:
```
docker-compose down
docker-compose up
```
That's it!
