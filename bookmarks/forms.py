from django import forms
from .models import Bookmark, PersonalBookmark
from allauth.account.forms import SignupForm;

class BookmarkForm(forms.ModelForm):

    class Meta:
        model = Bookmark
        fields = ('url', 'name', 'notes')
        
class PersonalBookmarkForm(forms.ModelForm):

    class Meta:
        model = PersonalBookmark
        fields = ('user','url', 'name', 'notes')

class BookmarkSignupForm(SignupForm):

    def save(self):

        user = super(BookmarkSignupForm, self).save()

        return user
