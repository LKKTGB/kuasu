# 歌詞正字

台語歌詞共同編修平台，為非營利及非商業性使用，僅供學習及促進台語用字一致化之教育功能。

## Getting Started

### Requirements

* Python 3.8

### Install Dependencies

```
pip install -r requirements-dev.txt
```

### Setup Local Environment Variables (Optional)

Add .env file to project root with following variables
```
SOCIAL_AUTH_FACEBOOK_KEY=<App ID from Facebook app thiamsu-development>
SOCIAL_AUTH_FACEBOOK_SECRET=<App Secret from Facebook app thiamsu-development>
```

### Setup Database

Migrate

```
python manage.py migrate
```

Load sample data

```
python samples/generate_sample_data.py [num_of_users] [num_of_songs]
python manage.py loaddata samples/sample_data.json
```

Create super user for dev

```
python manage.py createsuperuser
```

### Run server
```
python manage.py runserver
```

## Contributors
* @badboy99tw
* @wancw
* Kate
* Sharon
* Vic
