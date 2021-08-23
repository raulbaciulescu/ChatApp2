from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from account.forms import RegistrationForm, LoginForm, UpdateForm
from account.models import Account
from friend.friend_request_status import FriendRequestStatus
from friend.models import FriendList, FriendRequest
from friend.utils import get_friend_request_or_false


def register_view(request, *args, **kwargs):
     user = request.user
     if user.is_authenticated:
         return HttpResponse(f'You are already authenticated as {user.email}!')

     context = {}

     if request.method == 'POST':
         form = RegistrationForm(request.POST)
         if form.is_valid():
             form.save()
             email = form.cleaned_data.get('email').lower()
             raw_password = form.cleaned_data.get('password1')
             account = authenticate(email=email, password=raw_password)
             login(request, account)
             destination = kwargs.get('next')
             if destination:
                 return redirect(destination)
             else:
                 return redirect('home')
         else:
             context['registration_form'] = form

     return render(request, 'personal/register.html', context)


def login_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f'You are already authenticated as {user.email}!')

    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = kwargs.get('next')
            if destination:
                return redirect(destination)
            else:
                return redirect('home')
        else:
            context['login_form'] = form

    return render(request, 'personal/login.html', context)

def logout_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        logout(request)
    return redirect('home')


def account_view(request, *args, **kwargs):
    '''
    is_self - boolean
    is_friend

    -1: NO_REQUEST_SENT
    0: THEM_SENT_TO_YOU
    1: YOU_SENT_TO_THEM
    '''
    context = {}
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)
    except:
        return HttpResponse("Something went wrong.")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email

        try:
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=account)
            friend_list.save()
        friends = friend_list.friends.all()
        context['friends'] = friends

        # Define template variables
        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value  # range: ENUM -> friend/friend_request_status.FriendRequestStatus
        friend_requests = None
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
            if friends.filter(pk=user.id):
                is_friend = True
            else:
                is_friend = False
                # CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
                if get_friend_request_or_false(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
                # CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                # CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

        elif not user.is_authenticated:
            is_self = False
        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
            except:
                pass

        # Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['request_sent'] = request_sent
        context['friend_requests'] = friend_requests
        context['BASE_URL'] = settings.BASE_URL
        return render(request, "personal/account.html", context)

def search(request, *args, **kwargs):
    context = {}
    accounts = []
    user = request.user

    if request.method == 'GET':
        username = request.GET.get('search')
        status = Account.objects.filter(username__icontains=username)  # returns a list
        if user.is_authenticated:
            auth_user_friends = FriendList.objects.get(user=user)
            # [(account1, True/False), (account2, True/False)...]
            # True if we are friends
            for account in status:
                if account in auth_user_friends.friends.all():
                    accounts.append((account, True))
                else:
                    accounts.append((account, False))
        else:
            for account in status:
                accounts.append((account, False))
        context['accounts'] = accounts
    return render(request, "personal/search.html", context)


def update_view(request, *args, **kwargs):
    pk = kwargs['pk']
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        raise HttpResponse("Something went wrong!")

    if request.user.pk != account.pk:
        return HttpResponse("You cannot edit someone elses profile!")

    context = {}
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            account.profile_image.delete()
            form.save()
            return redirect('account:account', user_id=pk)
        else:
            form = UpdateForm(
                request.POST,
                instance=request.user,
                initial= {
                    'id': account.pk,
                    'email': account.email,
                    'username': account.username,
                    'profile_image': account.profile_image,
                    'hide_email': account.hide_email,
                }
            )
    else:
        form = UpdateForm(
            request.POST,
            initial={
                'id': account.pk,
                'email': account.email,
                'username': account.username,
                'profile_image': account.profile_image,
                'hide_email': account.hide_email,
            }
        )

    context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE

    return render(request, 'personal/update_account.html', context)