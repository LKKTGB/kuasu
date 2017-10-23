from django.contrib.auth.models import User


def update_profile(backend, response, user, *args, **kwargs):
    if backend.name == 'facebook':
        url = 'http://graph.facebook.com/%s/picture?type=large' % response['id']
        user.profile.avatar_url = url
        user.save()
