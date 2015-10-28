from django.forms import ModelForm
from webcanlendar.models import Entry

class EntryForm(ModelForm):

	class Meta:
		model = Entry
		fields = ('title', 'snippet', 'remind', 'body')