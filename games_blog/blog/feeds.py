from blog.models import Article
from django.contrib.syndication.views import Feed


class LatestArticleFeed(Feed):
    title = "Game blog Django "
    link = "/feeds/"
    description = "NON description"

    def items(self):
        return Article.published.order_by("-updated_at")[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.full_description

    def item_link(self, item):
        return item.get_absolute_url()
