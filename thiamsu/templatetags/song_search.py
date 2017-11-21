from django import template

register = template.Library()


DEFAULT_SEARCH_TYPE = 'performer'

SEARCH_TYPE_LABELS = {
    'performer': '演唱人',
    'song-title': '歌名',
}


@register.simple_tag()
def search_type_label_of(search_type):
    return SEARCH_TYPE_LABELS.get(search_type, search_type)


@register.simple_tag(takes_context=True)
def current_search_type_label(context):
    request = context['request']
    search_type = request.GET.get('type', DEFAULT_SEARCH_TYPE)

    return SEARCH_TYPE_LABELS.get(search_type, SEARCH_TYPE_LABELS.get(DEFAULT_SEARCH_TYPE))


@register.simple_tag()
def all_search_types():
    return ['performer', 'song-title']
