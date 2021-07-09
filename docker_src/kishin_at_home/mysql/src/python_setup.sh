sleep 60

apt update
apt upgrade -y

apt-get install python3 -y
apt install python3-pip -y

python3 --version
pip3 install -r /src/requirements.txt

python3 /src/initial_book_insert.py