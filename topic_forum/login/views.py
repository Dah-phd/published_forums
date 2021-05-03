from django.shortcuts import render, redirect
from django.contrib import messages
from login.forms import new_user, change_user
from login.models import DM
from forum.models import comment
from django.contrib.auth.views import PasswordChangeForm, PasswordResetForm
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from django.http import JsonResponse
from django.middleware.csrf import get_token
from login.models import friend_list


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'result': 'done'})
    else:
        return redirect('topics')


def user_page(request):
    if request.method == "POST":
        form = new_user(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"{form.cleaned_data['username']} created!")
            return redirect('forum')
    else:
        form = new_user()
    return render(request, 'login/create.html', {'form': form})


def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed!')
        friends = friend_list.objects.filter(owner=request.user)
        return render(request, 'login/profile.html',
                      {
                          'form': PasswordChangeForm,
                          'inbox': DM.objects.filter(reciever=request.user).order_by('-created'),
                          'outbox': DM.objects.filter(sender=request.user).order_by('-created'),
                          'friends': friends,
                          'friends_serialized': [fr.friend.pk for fr in friends],
                          'comments': comment.objects.filter(user=request.user)
                      }
                      )
    else:
        return redirect('topics')


def pass_reset(request):
    if request.user.is_authenticated:
        return redirect('topics')
    elif request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return JsonResponse({'result': 'done'})
        else:
            return JsonResponse({'result': 'failed'})


def modal_login(request):
    if request.method == 'POST':
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return JsonResponse({'token': get_token(request), 'result': request.POST['username']})
        else:
            return JsonResponse({'result': 'failed'})
    else:
        return redirect('games')


def edit_comment(request):
    if request.method == 'POST':
        obj = comment.objects.filter(pk=request.POST['id'])
        if request.user.is_authenticated and request.user.pk == obj[0].user.pk:
            obj.update(
                post_title=request.POST['title'],
                text=request.POST['text']
            )
            return JsonResponse({'result': 'done'})
    return JsonResponse({'result': 'error'})
