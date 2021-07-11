apt-get update -y
apt-get upgrade -y

echo "update completed"

apt-get install iputils-ping net-tools -y
echo "nettools is ready"

pip3 install -r /src/requirements.txt
