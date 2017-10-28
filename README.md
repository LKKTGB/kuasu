# 歌詞好正

## Install
```
pip install -r requirements.txt
python manage.py migrate
```

## Run
```
python manage.py runserver
```

## Login
```
http://localhost:8000/login
```

## Deploy
### Staging (Heroku)

* setup
```shell
brew install heroku
heroku login
heroku git:remote -a thiamsu-tw
```

* deploy
```
git push heroku <local_branch>:master
```

* other commands
```
heroku ps
heroku ps:scale web=1
heroku logs --tail
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```
