def update_profile(backend, response, user, *args, **kwargs):
    # pylint: disable=unused-argument
    if backend.name == "facebook":
        url = "https://graph.facebook.com/%s/picture?type=large" % response["id"]
        user.profile.avatar_url = url
        user.save()
