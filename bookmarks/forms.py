from django import forms
from .models import Bookmark, PersonalBookmark

class BookmarkForm(forms.ModelForm):

    class Meta:
        model = Bookmark
        fields = ('url', 'name', 'notes')
        
class PersonalBookmarkForm(forms.ModelForm):

    class Meta:
        model = PersonalBookmark
        fields = ('user','url', 'name', 'notes')

