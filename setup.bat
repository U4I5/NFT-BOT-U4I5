@ECHO OFF
start https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe

cls

echo "-------------------------------------------------------------"
timeout /t 60

python3 -m pip install -r requirements.txt

echo "-------------------------------------------------------------"
timeout /t 60


echo "Maintenant tu fais ''Windows + R'' tu écrit cmd, puis tu fais ''CD le chemain d'acces au fichier'' et enfin ''python3 main.py"> start.txt