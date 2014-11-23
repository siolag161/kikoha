import re

from django.forms import ModelForm
from django.core.exceptions import ValidationError

from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Submit, Div
from crispy_forms.helper import FormHelper

from core.forms import BaseForm
from .models import Community, Link

"""
"""

class CommunityCreateForm(BaseForm):
    """@todo: refactor this"""
    def clean(self):
	cleaned_data = super(BaseForm, self).clean()
	name = cleaned_data['title']
	
	if not re.match(r'[A-z0-9]+$', name):
            raise ValidationError('AlphaNumeric characters only, son!')
	    
	if Community.objects.filter(title=cleaned_data['title']).exists():
	    self._errors['title'] =  self.error_class(['name exists'])
	    del cleaned_data['title']
	return cleaned_data
    
    class Meta:
	model = Community
	fields = ('title',)
"""
"""
class LinkCreateForm(BaseForm):
    class Meta:
	model = Link
	fields = ('title', 'url')
