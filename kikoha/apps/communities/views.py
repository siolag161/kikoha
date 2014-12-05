
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.template import loader, RequestContext

from braces.views import LoginRequiredMixin  
from endless_pagination.views import AjaxListView
from endless_pagination.decorators import page_template


from core.views import OwnedCreateView
from django.shortcuts import get_object_or_404, render_to_response

from .models import Link, Community
from .forms import CommunityCreateForm, LinkCreateForm

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
        
    
#########################################################################
"""
"""
class LinkCreateView(LoginRequiredMixin, OwnedCreateView):
    model = Link    
    template_name = "links/create_view.html"
    form_class = LinkCreateForm

    def get_context_data(self, **kwargs):
        ctx = super(OwnedCreateView, self).get_context_data(**kwargs)
        ctx['name'] = self.kwargs.get('name')
        return ctx

    def form_valid(self, form):
	link = form.save(commit=False)
        link.author = self.request.user
	comm_name = self.kwargs.get('name')
	community = Community.objects.get(title=comm_name)	
	link.community = community	
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
class LinkUpdateView(LoginRequiredMixin, UpdateView):
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
Links by authors, twitter style
"""
class LinkAuthorListView(AjaxListView):
    model = Link
    context_object_name = 'link_list'
    template_name = 'links/list_by_author_view.html'
    page_template = 'links/list_page_view.html'

    def get_queryset(self):
	Model = self.model
	UserModel = get_user_model()
	qs = []
	user_pk = self.kwargs.get('user_pk')
	#username = self.request.GET.get('username')

	#print user_pk
	if user_pk:
	    self.author = UserModel.objects.get(pk = int(user_pk))
	    qs = self.author.links()	
	#elif username:
	    #self.author = User.objects.get(username = user_pk)	    
	    #qs = self.author.links()	
	return qs
	
	
	
