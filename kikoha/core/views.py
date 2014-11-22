from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

class HomeView(TemplateView):
    template_name = 'pages/home.html'

cached_home = cache_page(60 * 60)(HomeView.as_view())
home = HomeView.as_view()
