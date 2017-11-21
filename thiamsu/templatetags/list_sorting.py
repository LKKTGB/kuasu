from django import template

register = template.Library()


DEFAULT_SORTING_TYPE = 'original'

SORTING_TYPE_LABELS = {
    'original': '歌名（原文）',
    'tailo': '歌名（全羅）',
    'progress': '完成度',
}


@register.simple_tag(takes_context=True)
def sorting_url_of(context, sorting_type):
    request = context['request']
    updated = request.GET.copy()
    updated['sort'] = sorting_type

    return '?{}'.format(updated.urlencode()) if updated else ''


@register.simple_tag()
def sorting_label_of(sorting_type):
    return SORTING_TYPE_LABELS.get(sorting_type, sorting_type)


@register.simple_tag(takes_context=True)
def current_sorting_label(context):
    request = context['request']
    ordering = request.GET.get('sort', DEFAULT_SORTING_TYPE)

    return SORTING_TYPE_LABELS.get(ordering, SORTING_TYPE_LABELS.get(DEFAULT_SORTING_TYPE))


@register.simple_tag()
def all_sorting_types():
    return ['original', 'tailo', 'progress']
