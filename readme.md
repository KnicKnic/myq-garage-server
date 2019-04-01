# myQ garage door server
This repository provides a webserver for [myq-garage](https://github.com/Einstein42/myq-garage) door project and the necessary setup to host it on your home internet securely. It uses dynamic dns powered by [duckdns](https://duckdns.org) and TLS certificates([Let's Encrypt](https://letsencrypt.org)) obtained by [traefik](https://traefik.io) to accomplish secure communication to a home server. Allowing [IFTTT](https://ifttt.com) using your phone's location to automatically close your garage door when you leave.

## Howto use
1. clone this branch with submodules
    1. `git clone --recurse-submodule https://github.com/KnicKnic/myq-garage-server.git`
    1. cd myq-garage-server
1. overlay https://github.com/KnicKnic/traefik_duckdns ontop this folder
    1. follow all the instructions for setting up [traefik_dns](https://github.com/KnicKnic/traefik_duckdns/blob/master/README.md)
1. update your username and password for myq-garage/config.ini to those in your myq app
1. update password in rules/garage.toml
    1. change `some_password` in `rule = "PathPrefixStrip:/some_password; HostRegexp:garage.{restdomain:[\\-a-z0-9.]+}"` to some other password
    1. ex: `rule = "PathPrefixStrip:/my_secret_password; HostRegexp:garage.{restdomain:[\\-a-z0-9.]+}"`
    1. this serves as security to prevent others from opening and shutting your door.
1. start everything `docker-compose up -d --build`
1. issue GET web requests to your domain of the format
    1. [https://garage.`test`.duckdns.org/`some_password`/`close`/`Garage`](https://garage.test.duckdns.org/some_password/close/Garage)
        1. `test` should be the name of the duckdns subdomain you signed up for
        1. `some_password` should be the password you set in rules/garage.toml
        1. `close` - `close` and `open` are both supported to close and open the garage door
        1. `Garage` should be the "Device Name" of your door in the myq app

## Use IFTTT for control
You can setup geofencing to auto close your garage door using IFTTT when you leave an area (use `location` service). You can also use IFTTT to create buttons to press on your phone (use `button widget` service). For both of these you should connect it to the `webhook` service. Use url of mentioned in step 6 of "Howto use", leave Method as "Get" and then click Save.

See https://www.howtogeek.com/221555/how-to-create-geographic-event-triggers-with-your-smartphone-and-ifttt/ for more info on setting up geofencing for your phone.

## Files expained
files | explanation
--- | ---
flask_prog.py | python webserver that calls open and close garage door
Dockerfile | makes the container that closes and opens garage door
docker-compose.override.yml | extends traefik_duckdns docker-compose to add this project
rules/garage.toml | traefik config file to add webserver & expose it securely to internet
myq-garage/config.ini | config file for https://github.com/Einstein42/myq-garage
myq-garage/myq-garage.py | myq garage controller from https://github.com/Einstein42/myq-garage

