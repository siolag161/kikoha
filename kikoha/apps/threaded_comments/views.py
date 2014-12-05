from __future__ import absolute_import

import json

from django import http
from django.http import HttpResponse

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

import django.contrib.comments as django_comments
from django.contrib.comments import signals
from django.contrib.comments.views.utils import next_redirect, confirmation_view

CRISPY_TEMPLATE_PACK = getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap3')


class CommentPostBadRequest(http.HttpResponseBadRequest):
    """
    Response returned when a comment post is invalid. If ``DEBUG`` is on a
    nice-ish error message will be displayed (for debugging purposes), but in
    production mode a simple opaque 400 page will be displayed.
    """
    def __init__(self, why):
        super(CommentPostBadRequest, self).__init__()
        if settings.DEBUG:
            self.content = render_to_string("comments/400-debug.html", {"why": why})


@csrf_protect
@require_POST
def post_comment_ajax(request, next=None, using=None):
    """
    Post a comment.
    HTTP POST is required. If ``POST['submit'] == "preview"`` or if there are
    errors a preview template, ``comments/preview.html``, will be rendered.
    """
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    if request.user.is_authenticated():
        if not data.get('name', ''):
            data["name"] = request.user.get_full_name() or request.user.get_username()
        if not data.get('email', ''):
            data["email"] = request.user.email

    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    if ctype is None or object_pk is None:
        return CommentPostBadRequest("Missing content_type or object_pk field.")
    try:
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.using(using).get(pk=object_pk)
    except TypeError:
        return CommentPostBadRequest(
            "Invalid content_type value: %r" % escape(ctype))
    except AttributeError:
        return CommentPostBadRequest(
            "The given content-type %r does not resolve to a valid model." % \
                escape(ctype))
    except ObjectDoesNotExist:
        return CommentPostBadRequest(
            "No object matching content-type %r and object PK %r exists." % \
                (escape(ctype), escape(object_pk)))
    except (ValueError, ValidationError) as e:
        return CommentPostBadRequest(
            "Attempting go get content-type %r and object PK %r exists raised %s" % \
                (escape(ctype), escape(object_pk), e.__class__.__name__))

    # Do we want to preview the comment?
    preview = "preview" in data

    # Construct the comment form
    form = django_comments.get_form()(target, data=data)

    # Check security information
    if form.security_errors():
        return CommentPostBadRequest(
            "The comment form failed security verification: %s" % \
                escape(str(form.security_errors())))

    
    if preview:
        comment = form.get_comment_object() if not form.errors else None
        return _ajax_result(request, form, "preview", comment, object_id=object_pk)
    if form.errors:
        return _ajax_result(request, form, "post", object_id=object_pk)
    # If there are errors or if we requested a preview show the comment


    # Otherwise create the comment
    CommentModel = form.get_comment_model()
    comment = CommentModel(**form.get_comment_create_data())
    # comment = form.get_comment_object()
    
    comment.ip_address = request.META.get("REMOTE_ADDR", None)
    if request.user.is_authenticated():
	comment.user = request.user
	print comment.user
    else: 
	'bunbun'

    # Signal that the comment is about to be saved
    responses = signals.comment_will_be_posted.send(
        sender=comment.__class__,
        comment=comment,
        request=request
    )

    for (receiver, response) in responses:
        if response == False:
            return CommentPostBadRequest(
                "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)

    # Save the comment and signal that it was saved
    parent = form.cleaned_data['parent']
    if not parent:
	django_comments.get_model().add_root(instance=comment)
    else:
	parent = django_comments.get_model().objects.get(pk=parent)
	parent.add_child(instance=comment)
    signals.comment_was_posted.send(
        sender=comment.__class__,
        comment=comment,
        request=request
    )

    return _ajax_result(request, form, "post", comment, object_id=object_pk)
    
comment_done = confirmation_view( template="comments/posted.html",
    doc="""Display a "comment was posted" success page."""
)



def _ajax_result(request, form, action, comment=None, object_id=None):
    # Based on django-ajaxcomments, BSD licensed.
    # Copyright (c) 2009 Brandon Konkle and individual contributors.
    #
    # This code was extracted out of django-ajaxcomments because
    # django-ajaxcomments is not threadsafe, and it was refactored afterwards.

    success = True
    json_errors = {}

    if form.errors:
        for field_name in form.errors:
            field = form[field_name]
            json_errors[field_name] = _render_errors(field)
        success = False

    json_return = {
        'success': success,
        'action': action,
        'errors': json_errors,
        'object_id': object_id,
        # 'use_threadedcomments': True,
    }

    if comment is not None:
        context = {
            'comment': comment,
            'action': action,
            'preview': (action == 'preview'),
            # 'USE_THREADEDCOMMENTS': true,
        }
        comment_html = render_to_string('comments/comment.html', context, context_instance=RequestContext(request))

        json_return.update({
            'html': comment_html,
            'comment_id': comment.id,
            'parent_id': None,
            'is_moderated': not comment.is_public,   # is_public flags changes in comment_will_be_posted
        })

	if comment.get_parent() is not None:
	    json_return['parent_id'] = comment.get_parent().pk
	else:
	    json_return['parent_id'] = None

    json_response = json.dumps(json_return)
    return HttpResponse(json_response, content_type="application/json")


def _render_errors(field):
    """
    Render form errors in crispy-forms style.
    """
    template = '{0}/layout/field_errors.html'.format(CRISPY_TEMPLATE_PACK)
    return render_to_string(template, {
        'field': field,
        'form_show_errors': True,
    })
