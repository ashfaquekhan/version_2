  
# created by ashfaque ahmed khan
# THE POCKET DATA TRANSFERER
# this thing will download and install every important library and packeges in ur system, if this doesnt works then install the required packages manually.
# navigate to the download folder and type the command "sh install.sh" to download every package.
set -e 
sudo apt-get install -y \
  git-core \
  python-setuptools \
  python-imaging \
  python-dev \
  python-pip
  
  
cd
git clone https://github.com/Gadgetoid/WiringPi2-Python.git
cd WiringPi2-Python/
sudo python setup.py install
./build.sh
cd ..
git clone https://github.com/doceme/py-spidev
cd py-spidev
sudo python setup.py install
cd ..
git clone https://github.com/guyc/py-gaugette.git
cd py-gaugette
sudo python setup.py install
cd
sudo pip install wiringpi
cd OLED/python-examples
wget http://www.ralphmag.org/HS/penguins900x600.jpg 
cd
