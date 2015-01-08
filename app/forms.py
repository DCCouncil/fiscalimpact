from django import forms
from app.models import Document

class DocumentForm(forms.ModelForm):
    CHOICES = [('draft','Draft'), ('review','Review')]
    # status = forms.CharField(max_length=10, widget=forms.Select(choices=CHOICES))
    class Meta:
        model = Document
        exclude = ['id','employee','publish_date', 'slug']

        widgets = {
            'amendment_number': forms.TextInput(attrs={'class': 'hidden'}),
        }