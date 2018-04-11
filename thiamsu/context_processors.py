from django.conf import settings


def ga_tracking_id(request):
    try:
        return {'ga_tracking_id': settings.GA_TRACKING_ID}
    except AttributeError:
        return ''
