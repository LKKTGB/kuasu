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
SOCIAL_AUTH_FACEBOOK_KEY=<App ID from Facebook app thiamsu-development>
SOCIAL_AUTH_FACEBOOK_SECRET=<App Secret from Facebook app thiamsu-development>
```

### Run server
```
python manage.py runserver
```

Then you can login at
```
http://localhost:8000/login
```

### Import sample data to local db
```
python tools/import_sample_data.py
```

## Deploy

* setup
```shell
brew install heroku
```

### Testing (Heroku)
```
heroku login
heroku git:remote -a thiamsu-testing
git push heroku-testing <local_branch>:master
```

### Staging (Heroku)
```
heroku login
heroku git:remote -a thiamsu-staging
git push heroku-staging <local_branch>:master
```

### Heroku Notes
* other useful commands
```
heroku ps
heroku ps:scale web=1
heroku logs --tail
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```
