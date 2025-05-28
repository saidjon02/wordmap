from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # URL nomlari: urls.py dagi name parametrlari
        return ['home', 'about', 'contact']

    def location(self, item):
        return reverse(item)
