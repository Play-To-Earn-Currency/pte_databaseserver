# Play To Earn HTTP Server
Creates any http server to handle play to earn database, some games may use this or custom applications

### WARNING
Do not use open ports for this, this is to be used only with local machines, setup a strong firewall in your system, don't let internet have access to this server.

First run requires internet connection to download mysql package, after package installation configure your database in ``./config/database.txt``

### Available Routes:
All routes requires "from": "gamename", in the header

- /getbalance, GET
- > Returns user currently balance
- > Requires "uniqueid" as query parameter

- /getbalanceraw, GET
- > Returns user currently balance in WEI
- > Requires "uniqueid" as query parameter

- /getwallet, GET
- > Returns user currently wallet, returns 404 if not registered
- > Requires "uniqueid" as query parameter

- /increment, PUT
- > Increment some user wallet value
- > Requires "quantity" and "uniqueid" as body parameter

- /register, POST
- > Register a new user in the table
- > Requires "uniqued" as body parameter

- /updatewallet, PUT
- > Updates the user wallet to a new one
- > Requires "walletaddress" and "uniqueid" as body parameter

## Running
- Install mariadb/mysql
- Configure your game specific database
```sql
CREATE TABLE gamename (
    uniqueid VARCHAR(255) NOT NULL PRIMARY KEY,
    walletaddress VARCHAR(255) DEFAULT null,
    value DECIMAL(50, 0) NOT NULL DEFAULT 0
);
```
- Install [python](https://www.python.org/downloads) on your machine

- > Run
- run_linux.sh or run_windows.bat