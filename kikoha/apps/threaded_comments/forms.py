import re

from django.conf import settings
from django.forms import ModelForm, CharField, IntegerField, HiddenInput, Textarea
from django.core.exceptions import ValidationError
from django.utils.translation import ungettext, ugettext, ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.crypto import salted_hmac, constant_time_compare
from django.utils.encoding import force_text
from django.utils.text import get_text_list

from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions

from django.contrib.comments.forms import CommentForm, CommentSecurityForm

from core.mixins import NoFormTagCrispyFormMixin

#from core.forms import BaseForm
from .models import ThreadedComment

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH', 3000)

"""
"""
class CommentForm(NoFormTagCrispyFormMixin, CommentSecurityForm):
    """@todo: refactor this"""
    parent = IntegerField(required=False, widget= HiddenInput)
    comment  = CharField(label=_('Comment'), widget=Textarea,
			 max_length=COMMENT_MAX_LENGTH, required=True)

    
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_show_labels = False
    # helper.add_input(Submit('submit', 'submit'))

    helper.layout = Layout(
    	Field('comment', rows="3", css_class=''),
     	Field('parent', css_class='parent', type='hidden'),
	Field('content_type', css_class='', type='hidden'),
	Field('object_pk', css_class='', type='hidden'),
	Field('security_hash', css_class='', type='hidden'),
	Field('timestamp', css_class='', type='hidden'),
	
     	FormActions(
             Submit('save_changes', 'Save changes', css_class="btn-primary"),
             Submit('cancel', 'Cancel', css_class="btn-primary"),
         )
     )

    def __init__(self, target_object, parent=None, data=None, initial=None):
	# self.base_fields.insert(
        #     # self.base_fields.keyOrder.index('comment'), 'title',
        #     # forms.CharField(label=_('Title'), required=False, max_length=getattr(settings, 'COMMENTS_TITLE_MAX_LENGTH', 255))
        # )
        self.parent = parent
        if initial is None:
            initial = {}
        initial.update({'parent': self.parent})
        super(CommentForm, self).__init__(target_object, data=data, initial=initial)
    
    #class Meta:
	#model = ThreadedComment
	#fields = ('comment',)

    def get_comment_model(self):
        return ThreadedComment

    def get_comment_create_data(self):
        return dict(
            content_type = ContentType.objects.get_for_model(self.target_object),
            object_pk    = force_text(self.target_object._get_pk_val()),
            comment      = self.cleaned_data["comment"],
            submit_date  = timezone.now(),
            site_id      = settings.SITE_ID,
            is_public    = True,
            is_removed   = False,
        )

    def get_comment_object(self):
        """
        Return a new (unsaved) comment object based on the information in this
        form. Assumes that the form is already validated and will throw a
        ValueError if not.
        Does not set any of the fields that would come from a Request object
        (i.e. ``user`` or ``ip_address``).
        """
        if not self.is_valid():
            raise ValueError("get_comment_object may only be called on valid forms")

        CommentModel = self.get_comment_model()
        new = CommentModel(**self.get_comment_create_data())
        new = self.check_for_duplicate_comment(new)

        return new

    def check_for_duplicate_comment(self, new):
        """
        Check that a submitted comment isn't a duplicate. This might be caused
        by someone posting a comment twice. If it is a dup, silently return the *previous* comment.
        """
        possible_duplicates = ThreadedComment.objects.filter(
            content_type = new.content_type,
            object_pk = new.object_pk,
            user_name = new.user_name,
            #user_email = new.user_email,
            #user_url = new.user_url,
        )
        for old in possible_duplicates:
            if old.submit_date.date() == new.submit_date.date() and old.comment == new.comment:
                return old

        return new

