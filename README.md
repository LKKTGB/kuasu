# 歌詞好正

## Install
```
pip install -r requirements.txt
python manage.py migrate
```

## Develop

### Setup Env

Add .env file to project root with following variables
```
SOCIAL_AUTH_FACEBOOK_KEY=<App ID from Facebook>
SOCIAL_AUTH_FACEBOOK_SECRET=<App Secret from Facebook>
```

### Run server
```
python manage.py runserver
```

Then you can login at
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
