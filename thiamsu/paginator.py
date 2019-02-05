from django.core.paginator import Page as DjangoPage
from django.core.paginator import Paginator as DjangoPaginator
from django.utils.functional import cached_property


class Paginator(DjangoPaginator):
    def __init__(self, *args, **kwargs):
        self.padding = kwargs.pop("padding", 2)
        super(Paginator, self).__init__(*args, **kwargs)

    def _get_page(self, *args, **kwargs):
        return Page(padding=self.padding, *args, **kwargs)


class Page(DjangoPage):
    def __init__(self, *args, **kwargs):
        padding = kwargs.pop("padding")
        super(Page, self).__init__(*args, **kwargs)
        self.leftmost_page_number = max(1, self.number - padding)
        self.rightmost_page_number = min(
            self.paginator.num_pages, self.number + padding
        )

    @property
    def visible_page_range(self):
        return range(self.leftmost_page_number, self.rightmost_page_number + 1)
