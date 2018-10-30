#install packages
pip3 install --user -r requirements.txt

#start flask
cd dcha
export FLASK_APP=main.py
export FLASK_DEBUG=true
flask run --host 0.0.0.0 --port 8001
