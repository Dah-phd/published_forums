from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from forum.models import discussion, comment
from forum.forms import comment_form
from books.models import book
from login.models import DM
from forum.forms import DMform, adding_friend
from django.core.paginator import Paginator
from login.models import friend_list
from django.http import JsonResponse


def main(request):
    return render(request, 'forum/forum.html', {'books': book.objects.all(), 'discussions': discussion.objects.all()})


def forum_book(request, bk):
    return render(request, 'forum/discussions.html', {'book': book.objects.filter(pk=bk)[0], 'discussions': discussion.objects.filter(book__pk=bk)})


def thread(reqest, bk, trd, pg):
    location = discussion.objects.filter(
        book__pk=bk,
        discussion=trd
    )[0]
    if reqest.method == 'POST':
        if reqest.POST['type'] == 'new':
            form = comment_form(reqest.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.location = location
                if reqest.user.is_authenticated:
                    obj.user = reqest.user
                obj.save()
        elif reqest.POST['type'] == 'edit':
            obj = comment.objects.filter(pk=reqest.POST['id'])
            if reqest.user.is_authenticated and reqest.user.pk == obj[0].user.pk:
                obj.update(
                    post_title=reqest.POST['title'],
                    text=reqest.POST['text']
                )
        elif reqest.POST['type'] == 'delete':
            obj = comment.objects.filter(pk=reqest.POST['id'])
            if reqest.user.is_authenticated and reqest.user.pk == obj[0].user.pk:
                obj.delete()
    pages = Paginator(object_list=comment.objects.filter(
        location=location).order_by('created'), per_page=15
    )
    return render(reqest, 'forum/thread.html',
                  {'location': location,
                   'book': book.objects.filter(pk=bk)[0],
                   'discussions': discussion.objects.filter(book__pk=bk),
                   'comments': pages.get_page(-1 if pg == 0 else pg),
                   'friends_serialized': [fr.friend.pk for fr in friend_list.objects.filter(owner=reqest.user)] if reqest.user.is_authenticated else [0],
                   'form': comment_form,
                   'current': pg if pg != 0 else pages.num_pages,
                   'pages': pages.num_pages,
                   'page': 'last' if pg == 0 or pg == pages.num_pages else 'first' if pg == 1 else 'not'
                   })


def send_DM(reqest):
    if reqest.method == 'POST' and reqest.user.is_authenticated:
        if 'type' in reqest.POST:
            obj = DM.objects.filter(pk=reqest.POST['id'])
            if reqest.POST['type'] == 'delete':
                if reqest.POST['by'] == 'sender' and reqest.user == obj[0].sender:
                    obj.update(
                        deleted_sender=True
                    )
                elif reqest.POST['by'] == 'reciever' and reqest.user == obj[0].reciever:
                    obj.update(
                        deleted_reciever=True
                    )
                if obj[0].deleted_reciever and obj[0].deleted_sender:
                    obj[0].delete()
                return JsonResponse({'result': 'done'})
            elif reqest.POST['type'] == 'read':
                if reqest.user == obj[0].reciever:
                    obj.update(new=False)
                    return JsonResponse({'result': 'done'})
        sender = reqest.user
        reciever = User.objects.filter(pk=reqest.POST['reciever_id'])[0]
        form = DMform(reqest.POST)
        if form.is_valid():
            form.instance.sender = sender
            form.instance.reciever = reciever
            form.save()
            return JsonResponse({'result': 'done'})
    return JsonResponse({'result': 'error'})


def new_friend(reqest):
    if reqest.user.is_authenticated and reqest.method == 'POST':
        if 'delete' in reqest.POST:
            obj = friend_list.objects.filter(
                owner=reqest.user, friend=reqest.POST['friend'])[0].delete()
            return JsonResponse({'result': 'done'})
        if friend_list.objects.filter(owner=reqest.user, friend=reqest.POST['friend']).exists():
            return JsonResponse({'result': 'done'})
        form = adding_friend(reqest.POST)
        form.instance.owner = reqest.user
        if form.is_valid():
            form.save()
            return JsonResponse({'result': 'done'})
    return JsonResponse({'result': 'error'})
