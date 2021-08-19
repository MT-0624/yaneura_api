apt-get update -y
apt-get upgrade -y

echo "update completed"

apt-get install iputils-ping net-tools -y
echo "net-tools are ready"

apt install python3 python3-pip -y
pip3 install -r /src/requirements.txt
pip3 install --upgrade pip
pip3 install --upgrade setuptools
pip3 install -r requirements.txt