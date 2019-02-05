from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def page_url_of(context, page):
    request = context["request"]
    updated = request.GET.copy()
    updated["page"] = page

    return "?{}".format(updated.urlencode()) if updated else ""
