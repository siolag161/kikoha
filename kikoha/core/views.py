from django.views.generic import TemplateView, CreateView
from django.views.decorators.cache import cache_page

class HomeView(TemplateView):
    template_name = 'pages/home.html'


class OwnedCreateView(CreateView):    
    def form_valid(self, form):
	object = form.save(commit=False)
        object.author = self.request.user
	object.save()
        return super(OwnedCreateView, self).form_valid(form)

cached_home = cache_page(60 * 60)(HomeView.as_view())
home = HomeView.as_view()
