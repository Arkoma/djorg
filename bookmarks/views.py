from django.shortcuts import render
from .models import Bookmark, PersonalBookmark
from .forms import PersonalBookmarkForm
from django.contrib.auth import authenticate, login

def index(request):

    pbid = PersonalBookmark.objects.values_list('id')

    if request.method == 'POST':
        form = PersonalBookmarkForm(request.POST)
        if form.is_valid():
            if request.user.is_anonymous:
                form.errors['login'] = 'user must log in to save a bookmark'
            else:
                # import pdb; pdb.set_trace() # for debugging purposes
                form.save()
        else:
            
            # TODO error
            pass
            
    context = {}

    context['bookmarks'] = Bookmark.objects.exclude(id__in=pbid)
    # context['bookmarks'] = Bookmark.objects.all()

    if request.user.is_anonymous:
        context['personal_bookmarks'] = PersonalBookmark.objects.none()
    else:
        context['personal_bookmarks'] = PersonalBookmark.objects.filter(user=request.user)

    context['form'] = PersonalBookmarkForm
    
    return render(request, 'bookmarks/index.html', context)

def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, passweord=password)
    if user is not None:
        login(request, user)
    context['form'] = SigninForm

    return render(request, 'signin/index.html', context)
