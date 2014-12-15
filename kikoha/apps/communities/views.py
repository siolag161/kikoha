
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.template import loader, RequestContext

from braces.views import LoginRequiredMixin  
from endless_pagination.views import AjaxListView
from endless_pagination.decorators import page_template


from core.views import OwnedCreateView
from django.shortcuts import get_object_or_404, render_to_response

from .models import Community
from .forms import CommunityCreateForm

@page_template('communities/link_pagination_template.html') 
def community_detail(request, name, template='communities/detail_view.html', extra_context=None):
    community = get_object_or_404(Community, title=name)
    context = {
	'community': community,
        'link_list': community.links.all(),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response( template, context, context_instance=RequestContext(request))

class CommunityCreateView(LoginRequiredMixin, OwnedCreateView):
    model = Community
    template_name = "communities/create_view.html"
    form_class = CommunityCreateForm

# """
# """
# class CommunityByNameDetailView(DetailView):
#     model = Community
#     context_object_name = 'community'
#     template_name = "communities/detail_view.html"
#     pagination_template = "communities/link_pagination_template.html"

#     def get_context_data(self, **kwargs):
#         ctx = super(CommunityByNameDetailView, self).get_context_data(**kwargs)
#         return ctx


    # def get_object(self):
    # 	Model = self.model
    # 	ComminityModel = get_user_model()
    # 	community = None
    # 	comm_name = self.kwargs.get('name')
    # 	if comm_name:
    # 	    community = Model.objects.get(title=comm_name)
    # 	return community

"""
All links, twitter style
"""
class CommunityListView(AjaxListView):
    model = Community
    context_object_name = 'community_list'
    template_name = 'communities/list_view.html'
    page_template = 'communities/list_page_view.html'
        
