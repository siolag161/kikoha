

from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView, ListView
 
from braces.views import LoginRequiredMixin  
from endless_pagination.views import AjaxListView


from .models import Link
from .forms import LinkCreateForm

"""
"""
class LinkCreateView(CreateView, LoginRequiredMixin):
    model = Link    
    template_name = "links/create_view.html"
    form_class = LinkCreateForm

    def form_valid(self, form):
	link = form.save(commit=False)
        link.author = self.request.user
	link.save()
        return super(LinkCreateView, self).form_valid(form)
"""
"""
class LinkDetailView(DetailView):
    model = Link
    context_object_name = 'link'
    template_name = "links/detail_view.html"
    
"""
"""
class LinkUpdateView(UpdateView, LoginRequiredMixin):
    model = Link
    template_name = "links/update_view.html"

"""
All links, twitter style
"""
class LinkListView(AjaxListView):
    model = Link
    context_object_name = 'link_list'
    template_name = 'links/list_view.html'
    page_template = 'links/list_page_view.html'
    

"""
All links, twitter style
"""
class LinkAuthorListView(AjaxListView):
    model = Link
    context_object_name = 'link_list'
    template_name = 'links/list_by_author_view.html'
    page_template = 'links/list_page_view.html'

    def get_query_set(self):
	Model = self.model
	qs = Model.objects.all()
	
	user_pk = int( self.request.GET.get('user_pk') )
	if user_pk:
	    self.user = get_user_model().objects.get(pk = user_pk)	    
	    qs = self.user.links()

	return qs
	
	
	
