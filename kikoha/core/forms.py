
from django.forms import ModelForm

from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Submit, Div

from crispy_forms.helper import FormHelper
#from crispy_forms.bootstrap import FormAction

from .mixins import NoFormTagCrispyFormMixin

"""
"""
class BaseForm(NoFormTagCrispyFormMixin,ModelForm):    
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-xs-2'
    helper.field_class = 'col-xs-8'
    helper.add_input(Submit('submit', 'submit'))

