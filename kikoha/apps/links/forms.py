import re

from django.forms import ModelForm
from django.core.exceptions import ValidationError

from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Submit, Div
from crispy_forms.helper import FormHelper

from core.forms import BaseForm
from .models import Link

class LinkCreateForm(BaseForm):
    class Meta:
	model = Link
	fields = ('title', 'url')
