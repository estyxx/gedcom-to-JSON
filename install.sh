# if macos
if [[ $OSTYPE == 'darwin'* ]]; then
  echo "Do you Have brew?"
  if [[ ! brew info cask &>/dev/null; ]] then
    echo "ERROR: You need brew installed to run this script!!"
    echo "QUITTING"
    break
  else
    echo "Installing python"
    brew install python python-pip 
  fi

  if [[ ! type "$node" > /dev/null || if ! type "$npm" > /dev/null]]; then
    echo "You need node and npm installed \n Installing:"
    brew install node npm
  fi

fi

# if linux (currently only supports debian based)
if [[ $OSTYPE == 'linux-gnu' ]]; then
  sudo apt-get install python python-pip

  if [[ ! type "$node" > /dev/null || if ! type "$npm" > /dev/null]]; then
    echo "You need node and npm installed \n Installing:"
    sudo apt-get install nodejs npm
  fi

fi

echo "Installing Node packages"
npm install --save child-process multer body-parser express mongoose mongo
echo "Installed Node packages"

echo "Installing Pip programs"
sudo pip install datetime six
echo "Installed Pip programs"

echo "Installing gecompy"
python gedcompy/setup.py build
python gedcompy/setup.py install
echo "Installed gedcompy"

echo 

