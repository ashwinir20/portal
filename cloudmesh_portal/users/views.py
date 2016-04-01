from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from models import PortalUser
from django.views.decorators.cache import never_cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

# Name of the session key which stores user id
YUBIKEY_SESSION_USER_ID = getattr(settings, 'YUBICO_SESSION_USER_ID',
                                  'yubicodjango_user_id')

# Name of the session key which stores the name of the backend user used to log
# in.
YUBIKEY_SESSION_AUTH_BACKEND = getattr(settings, 'YUBICO_SESSION_AUTH_BACKEND',
                                       'yubicodjango_auth_backend')

# Name of the session key which stores attempt counter
YUBIKEY_SESSION_ATTEMPT_COUNTER = getattr(settings,
                                          'YUBIKEY_SESSION_ATTEMPT_COUNTER',
                                          'yubicodjango_counter')

# Django Yubico session keys
SESSION_KEYS = [YUBIKEY_SESSION_USER_ID, YUBIKEY_SESSION_AUTH_BACKEND,
                YUBIKEY_SESSION_ATTEMPT_COUNTER]

@never_cache
def register(request, template_name='cloudmesh_portal/users/register.html',
             redirect_field_name=REDIRECT_FIELD_NAME):
    redirect_to = settings.LOGIN_REDIRECT_URL
    if request.method == 'POST':
        # POST request to send form
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            print form.username
            # TODO add validation error if user is already there.
            user = User.objects.create_user(form.cleaned_data['username'],
                                            form.cleaned_data['email'],
                                            form.cleaned_data['password'])
            user.last_name = form.cleaned_data['lastname']
            user.first_name = form.cleaned_data['firstname']
            user.save()
            p = PortalUser(user=user, address=form.cleaned_data['address'],
                           additional_info=form.cleaned_data['additional_info'],
                           citizen=form.cleaned_data['citizen'],
                           country=form.cleaned_data['country'])
            p.save()

        else:
            # Not a valid form, open Register form with an error message.
            form = RegisterForm()
    else:
        # GET request to get form
        form = RegisterForm()

    dictionary = {'form': form, redirect_field_name: redirect_to}
    return render_to_response(template_name, dictionary,
                              context_instance=RequestContext(request))


@never_cache
def login(request, template_name='cloudmesh_portal/users/register.html',
             redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = redirect_field_name
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    user = form.user
                else:
                    return HttpResponseRedirect(reverse('yubico_django_login'))
            
