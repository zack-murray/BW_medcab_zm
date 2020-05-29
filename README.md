# DS

## Installing and running API app:

1) Install python 3.8

2) install pipenv with ```pip3 install pipenv``` or ```pip install pipenv``` (whichever works)

3) CD into DS directory

4) Install pipenv requirements with ```pipenv install```

5) Activate pipenv shell with ```pipenv shell```

6) Run app with ```FLASK_APP=web_app flask run```(mac) or ```export FLASK_APP=web_app``` then ```flask run``` (windows)

7) When done, exit pipenv shell with ```exit```

## Testing server status:

Go to ```http://localhost:5000/jsontest```

## Getting all names:

Go to ```http://localhost:5000/names```
