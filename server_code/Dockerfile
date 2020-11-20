FROM ubuntu
run apt update -y && apt upgrade -y
run apt install python3 -y
run apt install python3-pip -y
run pip3 install anvil-uplink
run apt install python3-dev libpq-dev -y
run pip3 install psycopg2
add . .
env uplinkkey="QDYIJLYLCRW762NRFKH6Z3EY-B4CFZ34JETACVQWU"
cmd python3 ServerModule1.py
