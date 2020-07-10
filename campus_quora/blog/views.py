from django.contrib import auth
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import *
from .forms import QuestionForm,AnswerForm
from accounts.models import UserProfile
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

m = {0: 'Department', 1: 'Clubs', 2: 'placements', 3: 'fests', 4: 'hostel', 5: 'general'}
m1 = {'Department': 0, 'Clubs': 1, 'placements': 2, 'fests': 3, 'hostel': 4, 'general': 5}


@login_required
def homepage(request, username):
    questions = Question.objects.all()
    user = User.objects.get(username=username)
    user_ = UserProfile.objects.get(user=user)
    print(type(user_.tags))
    print(user_.tags)
    v = []
    b = []
    size = []
    for ques in questions:
        size.append(len(ques.answer_set.all()))
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)

    for ques in questions:
        a = 1
        for bm in user.bookmark_set.all():
            if bm.Question.id == ques.id:
                b.append(0)
                a = 0
                break
        if a:
            b.append(1)

    return render(request, 'blog/home.html', {'user': user, 'questions': questions,'data': zip(questions, v, b,size)})


@login_required
def sortques(request, username):
    if request.method == 'POST':
        search_tag = request.POST.get("search", False)  # for avoiding multidictionary key error
        print(search_tag)
        if search_tag == "Preferences":

            user = User.objects.get(username=username)
            user_ = UserProfile.objects.get(user=user)
            tags1 = user_.tags
            tags = list(tags1)
            questions = Question.objects.filter(tags__in = tags)
            print('questions')
            print(questions)
            print('questions')
            print(type(tags[0]))
            print('falak')
            print(tags)
            v = []
            b = []
            size = []
            for ques in questions:
                size.append(len(ques.answer_set.all()))
                a = 1
                for votes in user.quesvotes_set.all():
                    if votes.Question.id == ques.id:
                        v.append(0)
                        a = 0
                        break
                if a:
                    v.append(1)

            for ques in questions:
                a = 1
                for bm in user.bookmark_set.all():
                    if bm.Question.id == ques.id:
                        b.append(0)
                        a = 0
                        break
                if a:
                    b.append(1)
            return render(request, 'blog/home.html',{'user': user, 'questions': questions, 'data': zip(questions, v, b, size)})


        else:
            return redirect('blog:home', username)

    else:
        return redirect('blog:home', username)

@login_required
def search(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        # s = request.POST['search']
        # print(s)
        search_tag = request.POST.get("search", False) # for avoiding multidictionary key error

        if search_tag:
            print(search_tag)
            match_ques = Question.objects.filter(Q(tags__icontains=m1[search_tag]))
            v = []
            b = []
            size = []
            for ques in match_ques:
                size.append(len(ques.answer_set.all()))
                a = 1
                for votes in user.quesvotes_set.all():
                    if votes.Question.id == ques.id:
                        v.append(0)
                        a = 0
                        break
                if a:
                    v.append(1)

            for ques in match_ques:
                a = 1
                for bm in user.bookmark_set.all():
                    if bm.Question.id == ques.id:
                        b.append(0)
                        a = 0
                        break
                if a:
                    b.append(1)
            if match_ques:
                return render(request,'blog/search.html',{'user':user,'match_ques':match_ques, 'data': zip(match_ques, v, b, size), "search":search_tag})
            else:
                 return render(request,'blog/search.html',{'user':user,'error_message':'no questions :(', "search":search_tag})
        else:
            print(search_tag)
            return redirect('blog:home',username)

    else:
        return redirect('blog:home', username)

@login_required
def ssearch(request, username, search):
    print("search-------")
    print(type(search))
    print("search--------")
    print("search")
    if len(search) == 1:
        search1 = int(search)
        search = search1
        print(type(search))
        search = m[search]
    user = User.objects.get(username=username)
    match_ques = Question.objects.filter(Q(tags__icontains=m1[search]))
    v = []
    b = []
    size = []
    for ques in match_ques:
        size.append(len(ques.answer_set.all()))
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)

    for ques in match_ques:
        a = 1
        for bm in user.bookmark_set.all():
            if bm.Question.id == ques.id:
                b.append(0)
                a = 0
                break
        if a:
            b.append(1)
    return render(request, 'blog/search.html', {'user': user, 'match_ques': match_ques, 'data': zip(match_ques, v, b,size), "search": search})

@login_required
def ans(request, pk, username):
    pk = int(pk)
    question = Question.objects.get(pk = pk)
    user = User.objects.get(username=username)
    qv = 1
    for votes in user.quesvotes_set.all():
        if votes.Question.id == question.id:
            qv = 0
            break
    size = len(question.answer_set.all())
    qb = 1
    for bm in user.bookmark_set.all():
        if bm.Question.id == question.id:
            qb = 0
            break

    v = []
    answer = []
    for ans in question.answer_set.all():
        a = 1
        answer.append(ans)
        for votes in user.ansvotes_set.all():
            if votes.Answer.id == ans.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)
    print(answer)
    return render(request,'blog/ans.html', {'question':question, 'user':user, 'size':size ,'qv':qv, 'qb':qb,  'data': zip(answer, v)})

@login_required
def sortans(request, pk, username):
    question = Question.objects.get(pk=pk)
    user = User.objects.get(username=username)
    qv = 1
    for votes in user.quesvotes_set.all():
        if votes.Question.id == question.id:
            qv = 0
            break

    qb = 1
    for bm in user.bookmark_set.all():
        if bm.Question.id == question.id:
            qb = 0
            break
    if request.method == 'POST':
        size = len(question.answer_set.all())
        search_tag = request.POST.get("search", False)  # for avoiding multidictionary key error
        print(search_tag)
        if search_tag == "Votes":
            answer = question.answer_set.all().order_by('-votes', '-created_on') # - for decreasing order
            v = []
            for ans in answer:
                a = 1
                for votes in user.ansvotes_set.all():
                    if votes.Answer.id == ans.id:
                        v.append(0)
                        a = 0
                        break
                if a:
                    v.append(1)
            return render(request, 'blog/anssort.html', {'question':question, 'user': user, 'size':size , 'qv':qv, 'qb':qb, 'data': zip(answer, v)})
        else:
            return redirect('blog:ans', pk, username)

    else:
        return redirect('blog:ans', pk, username)

@login_required
def mysearch(request, username):
    print(username)
    print(6)
    user = User.objects.get(username=username)
    if request.method == 'POST':
        # s = request.POST['search']
        # print(s)
        search_tag = request.POST.get("search", False) # for avoiding multidictionary key error

        if search_tag:
            print(search_tag)
            match_ques = Question.objects.filter(Q(tags__icontains=m1[search_tag]), User = user)
            v = []
            b = []
            for ques in match_ques:
                a = 1
                for votes in user.quesvotes_set.all():
                    if votes.Question.id == ques.id:
                        v.append(0)
                        a = 0
                        break
                if a:
                    v.append(1)

            for ques in match_ques:
                a = 1
                for bm in user.bookmark_set.all():
                    if bm.Question.id == ques.id:
                        b.append(0)
                        a = 0
                        break
                if a:
                    b.append(1)
            # print(search_tag)
            if match_ques:
                return render(request,'blog/mysearch.html',{'user': user,'match_ques': match_ques,'data': zip(match_ques, v, b), 'search':search_tag})
            else:
                 return render(request,'blog/mysearch.html',{'user':user,'error_message':'no question','search':search_tag})
        else:
            print(search_tag)
            return redirect('blog:home',username)

    else:
        return redirect('blog:home', username)

@login_required
def bookmarksearch(request, username):
    print(username)
    user = User.objects.get(username=username)
    if request.method == 'POST':
        # s = request.POST['search']
        # print(s)
        search_tag = request.POST.get("search", False) # for avoiding multidictionary key error
        size = []
        if search_tag:
            print(search_tag)
            bookmark = user.bookmark_set.all()
            match_ques = []
            for bm in bookmark:
                size.append(len(bm.Question.answer_set.all()))
                if bm.Question.tags == m1[search_tag]:
                    match_ques.append(bm)
            v = []
            for bm in match_ques:
                ques = bm.Question
                a = 1
                for votes in user.quesvotes_set.all():
                    if votes.Question.id == ques.id:
                        v.append(0)
                        a = 0
                        break
                if a:
                    v.append(1)
            if match_ques:
                return render(request,'blog/Bookmarksearch.html',{'user': user,'bookmark': match_ques,'data': zip(match_ques, v,size), "search":search_tag})
            else:
                 return render(request,'blog/Bookmarksearch.html',{'user':user,'error_message':'no bookmark :(', "search":search_tag})
        else:
            print(search_tag)
            return redirect('blog:home',username)

    else:
        return redirect('blog:home', username)

@login_required
def myques(request, username):
    user = User.objects.get(username = username)
    myques = user.question_set.all()
    v = []
    b = []
    size = []
    for ques in myques:
        size.append(len(ques.answer_set.all()))
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)

    for ques in myques:
        a = 1
        for bm in user.bookmark_set.all():
            if bm.Question.id == ques.id:
                b.append(0)
                a = 0
                break
        if a:
            b.append(1)
    return render(request, 'blog/myques.html', {'user': user, 'myques': myques, 'data': zip(myques, v, b, size)})


@login_required
def merge(list1, list2):
    merged_list = tuple(zip(list1, list2))
    return merged_list

@login_required
def myans(request, username):
    user = User.objects.get(username = username)
    myans = user.answer_set.all()
    size = []
    match_ques = set()
    for ans in myans:
        if not ans.Question.id in match_ques:
            match_ques.add(ans.Question)
    qv = []
    b = []
    aa = []
    qav1 = []
    for ques in match_ques:
        size.append(len(ques.answer_set.all()))
        av = []
        an = []
        t = []
        for ans in ques.answer_set.all():
            if ans.User.username == user.username:
                a = 1
                an.append(ans)
                for votes in user.ansvotes_set.all():
                    if votes.Answer.id == ans.id:
                        av.append(0)
                        a = 0
                        break
                if a:
                    av.append(1)
        merged_list = [[an[i], av[i]] for i in range(0, len(av))]
        qav1.append(merged_list)

    print(qav1)
    for ques in match_ques:
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                qv.append(0)
                a = 0
                break
        if a:
            qv.append(1)

    for ques in match_ques:
        a = 1
        for bm in user.bookmark_set.all():
            if bm.Question.id == ques.id:
                b.append(0)
                a = 0
                break
        if a:
            b.append(1)



    return render(request,'blog/myans.html', {'user':user,'data': zip(match_ques,qv,b,qav1,size)})

@login_required
def QuestionCreate(request, username):
    if request.method == 'POST':
        tags = request.POST['tags']
        question = request.POST['question']
        title = request.POST['title']
        user = User.objects.get(username = username)
        ques = Question()
        ques.question = question
        ques.tags = tags
        ques.title = title
        ques.User = user
        ques.save()
        return redirect('blog:myques', username)

    else:
        form = QuestionForm()
        return render(request, 'blog/question_form.html', {'form': form})

@login_required
def AnswerCreate(request, username, pk, pk2):
    if request.method == 'POST':

        answer = request.POST['answer']
        user = User.objects.get(username=username)
        Ques = Question.objects.get(pk=pk)

        ans = Answer()
        ans.answer = answer
        ans.Question = Ques
        ans.User = user
        ans.save()

        notification = Notifications()
        notification.Question = Ques
        notification.who = user
        notification.User = Ques.User
        notification.Answer = ans
        notification.save()
        i = int(pk2)
        if i == 0:
            return redirect('blog:ans', Ques.id, username)
        elif i==1:
            return redirect('blog:myans', username)


@login_required
def vote(request, pk, username):
    question = Question.objects.get(pk = pk)
    question.votes += 1
    question.save()
    return redirect('blog:home', username)

@login_required
def deleteques(request, pk, username, pk2):
    Question.objects.filter(pk=pk).delete()


    i = int(pk2)
    if i == 0:
        return redirect('blog:home', username)
    if i == 1:
        return redirect('blog:myques', username)
    if i == 2:
        return redirect('blog:home',  username)
    if i == 3:
        return redirect('blog:myques', username)
    if i == 4:
        return redirect('blog:notification', username)
    if i == 5:
        return redirect('blog:myans', username)

    return redirect('blog:myques', username)


@login_required
def sdeleteques(request, pk, username, search):
    Question.objects.filter(pk=pk).delete()


    return redirect('blog:ssearch', username, search)

@login_required
def qs_deleteques(request, pk, username,search):
    question = Question.objects.get(pk=pk)
    user = User.objects.get(username=username)
    Question.objects.filter(pk=pk).delete()
    match_ques = Question.objects.filter(Q(tags__icontains=m1[search]), User=user)
    v = []
    b = []
    for ques in match_ques:
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)

    for ques in match_ques:
        a = 1
        for bm in user.bookmark_set.all():
            if bm.Question.id == ques.id:
                b.append(0)
                a = 0
                break
        if a:
            b.append(1)
    return render(request, 'blog/mysearch.html',{'user': user, 'match_ques': match_ques, 'data': zip(match_ques, v, b), 'search': search})


@login_required
def ndelete(request, pk,  username):
    Notifications.objects.filter(pk=pk).delete()
    return redirect('blog:notification', username)

@login_required
def ansdelete(request, pk, username, pk2, pk3):
    Answer.objects.filter(pk=pk).delete()
    pk2 = int(pk2)
    pk3 = int(pk3)
    if pk2 == 0:
        return redirect('blog:myans', username)
    if pk2 == 1:
        return redirect('blog:ans', pk3 , username)

@login_required
def notification(request, username):
    user = User.objects.get(username=username)
    notifications = user.notifications_set.all()
    return render(request, 'blog/notifications.html', {'user':user, 'notifications':notifications})

@login_required
def nques(request, pk, username):
    notification = Notifications.objects.get(pk=pk)
    user = User.objects.get(username=username)
    qv = 1
    size = len(notification.Question.answer_set.all())
    for votes in user.quesvotes_set.all():
        if votes.Question.id == notification.Question.id:
            qv = 0
            break

    b = 1
    for bm in user.bookmark_set.all():
        if bm.Question.id == notification.Question.id:
            b = 0
            break

    av = 1
    for votes in user.ansvotes_set.all():
        if votes.Answer.id == notification.Answer.id:
            av = 0
            break

    return render(request, 'blog/nques.html', {'notification': notification, 'size':size ,'qv': qv, 'b':b, 'user':user, 'av': av})

@login_required
def mybookmark(request, username):
    user = User.objects.get(username=username)
    bookmark = user.bookmark_set.all()
    v = []
    size = []
    for bm in bookmark:
        a = 1
        size.append(len(bm.Question.answer_set.all()))
        for votes in user.quesvotes_set.all():
            if votes.Question.id == bm.Question.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)
    return render(request, 'blog/bookmark.html', {'user':user ,bookmark:'bookmark', 'data': zip(bookmark, v,size)})

@login_required
def bookmark(request, pk, username, pk2):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)

    mybook = user.bookmark_set.all()
    s = set()
    br = 1
    for b in mybook:
        s.add(int(b.Question.pk))

    print(s)
    print(pk)
    t = int(pk)
    if t in s:
        print(1)
        pass
    else:
        print(0)
        book = Bookmark()
        book.User = user
        book.Question = ques
        book.save()
    i = int(pk2)
    if i == 0:
        return redirect('blog:home', username)
    elif i == 1:
        return redirect('blog:myques', username)
    elif i == 3:
        return redirect('blog:myans', username)
    elif i == 4:
        return redirect('blog:ans', ques.id , username)

@login_required
def sbookmark(request, pk, username, search):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)

    mybook = user.bookmark_set.all()
    s = set()
    br = 1
    for b in mybook:
        s.add(int(b.Question.pk))

    print(s)
    print(pk)
    t = int(pk)
    if t in s:
        print(1)
        pass
    else:
        print(0)
        book = Bookmark()
        book.User = user
        book.Question = ques
        book.save()
    print(search)
    question = Question.objects.filter(tags=m1[search])
    v = []
    b = []
    for ques in question:
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)

    for ques in question:
        a = 1
        for bm in user.bookmark_set.all():
            if bm.Question.id == ques.id:
                b.append(0)
                a = 0
                break
        if a:
            b.append(1)

    return render(request, 'blog/search.html',{'user': user, 'question': question, 'data': zip(question, v, b), "search": search})

@login_required
def qs_bookmark(request, pk, username, search):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)

    mybook = user.bookmark_set.all()
    s = set()
    br = 1
    for b in mybook:
        s.add(int(b.Question.pk))

    print(s)
    print(pk)
    t = int(pk)
    if t in s:
        print(1)
        pass
    else:
        print(0)
        book = Bookmark()
        book.User = user
        book.Question = ques
        book.save()
    match_ques = Question.objects.filter(Q(tags__icontains=m1[search]), User=user)
    v = []
    b = []
    for ques in match_ques:
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)

    for ques in match_ques:
        a = 1
        for bm in user.bookmark_set.all():
            if bm.Question.id == ques.id:
                b.append(0)
                a = 0
                break
        if a:
            b.append(1)

    return render(request, 'blog/mysearch.html',{'user': user, 'match_ques': match_ques, 'data': zip(match_ques, v, b), 'search': search})


@login_required
def nbookmark(request, pk, username):
    notification = Notifications.objects.get(pk=pk)
    user = User.objects.get(username=username)
    ques = notification.Question
    mybook = user.bookmark_set.all()
    s = set()
    br = 1
    for b in mybook:
        s.add(int(b.Question.pk))

    print(s)
    print(pk)
    t = int(pk)
    if t in s:
        print(1)
        pass
    else:
        print(0)
        book = Bookmark()
        book.User = user
        book.Question = ques
        book.save()
    return redirect('blog:nques', pk, username)

@login_required
def removebookmark(request, pk, username, pk2):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)

    Bookmark.objects.filter(Question=ques, User=user).delete()
    i = int(pk2)
    if i == 0:

        return redirect('blog:home', username)
    elif i == 1:
        return redirect('blog:myques', username)
    elif i == 2:
        return redirect('blog:mybookmark', username)
    elif i==3:
        return redirect('blog:myans', username)
    elif i == 4:
        return redirect('blog:ans', ques.id , username)

@login_required
def sremovebookmark(request, pk, username, search):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)

    Bookmark.objects.filter(Question=ques, User=user).delete()
    question = Question.objects.filter(tags=m1[search])
    v = []
    b = []
    for ques in question:
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)

    for ques in question:
        a = 1
        for bm in user.bookmark_set.all():
            if bm.Question.id == ques.id:
                b.append(0)
                a = 0
                break
        if a:
            b.append(1)

    return render(request, 'blog/search.html',{'user': user, 'question': question, 'data': zip(question, v, b), "search": search})

@login_required
def qs_removebookmark(request, pk, username, search):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)

    Bookmark.objects.filter(Question=ques, User=user).delete()
    match_ques = Question.objects.filter(Q(tags__icontains=m1[search]), User=user)
    v = []
    b = []
    for ques in match_ques:
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)

    for ques in match_ques:
        a = 1
        for bm in user.bookmark_set.all():
            if bm.Question.id == ques.id:
                b.append(0)
                a = 0
                break
        if a:
            b.append(1)

    return render(request, 'blog/mysearch.html',{'user': user, 'match_ques': match_ques, 'data': zip(match_ques, v, b), 'search': search})


@login_required
def bs_removebookmark(request, pk, username, search):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)

    Bookmark.objects.filter(Question=ques, User=user).delete()
    bookmark = user.bookmark_set.all()
    match_ques = []
    for bm in bookmark:
        if bm.Question.tags == m1[search]:
            match_ques.append(bm)

    v = []
    for bm in match_ques:
        ques = bm.Question
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)
    return render(request, 'blog/Bookmarksearch.html',{'user': user, 'bookmark': match_ques, 'data': zip(match_ques, v), "search": search})


@login_required
def nremovebookmark(request, pk, username):
    notification = Notifications.objects.get(pk=pk)
    user = User.objects.get(username=username)
    ques = notification.Question
    Bookmark.objects.filter(Question=ques, User=user).delete()
    return redirect('blog:nques', pk, username)

@login_required
def quesvote(request, pk, username, pk2):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)
    votes = ques.quesvotes_set.all()
    s = set()
    for v in votes:
        s.add(str(v.User.username))
    # print(s)
    if user.username in s:
        pass
    else:
        votes = Quesvotes()
        votes.Question = ques
        votes.User = user
        ques.votes += 1;
        ques.save()
        votes.save()
    i = int(pk2)
    if i == 0:
        return redirect('blog:home', username)
    elif i == 1:
        return redirect('blog:myques', username)
    elif i == 2:
        return redirect('blog:mybookmark', username)
    elif i==3:
        return redirect('blog:myans', username)
    elif i == 4:
        return redirect('blog:ans', ques.id , username)

@login_required
def squesvote(request, pk, username, search):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)
    votes = ques.quesvotes_set.all()
    s = set()
    for v in votes:
        s.add(str(v.User.username))
    # print(s)
    if user.username in s:
        pass
    else:
        votes = Quesvotes()
        votes.Question = ques
        votes.User = user
        ques.votes += 1;
        ques.save()
        votes.save()

    question = Question.objects.filter(tags=m1[search])
    v = []
    b = []
    for ques in question:
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)

    for ques in question:
        a = 1
        for bm in user.bookmark_set.all():
            if bm.Question.id == ques.id:
                b.append(0)
                a = 0
                break
        if a:
            b.append(1)

    return render(request, 'blog/search.html',{'user': user, 'question': question, 'data': zip(question, v, b), "search": search})

@login_required
def bs_quesvote(request, pk, username, search):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)
    votes = ques.quesvotes_set.all()
    s = set()
    for v in votes:
        s.add(str(v.User.username))
    # print(s)
    if user.username in s:
        pass
    else:
        votes = Quesvotes()
        votes.Question = ques
        votes.User = user
        ques.votes += 1;
        ques.save()
        votes.save()
    bookmark = user.bookmark_set.all()
    match_ques = []
    for bm in bookmark:
        if bm.Question.tags == m1[search]:
            match_ques.append(bm)

    v = []
    for bm in match_ques:
        ques = bm.Question
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)
    return render(request, 'blog/Bookmarksearch.html',{'user': user, 'bookmark': match_ques, 'data': zip(match_ques, v), "search": search})

@login_required
def qs_quesvote(request, pk, username, search):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)
    votes = ques.quesvotes_set.all()
    s = set()
    for v in votes:
        s.add(str(v.User.username))
    # print(s)
    if user.username in s:
        pass
    else:
        votes = Quesvotes()
        votes.Question = ques
        votes.User = user
        ques.votes += 1;
        ques.save()
        votes.save()
    match_ques = Question.objects.filter(Q(tags__icontains=m1[search]), User=user)
    v = []
    b = []
    for ques in match_ques:
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)

    for ques in match_ques:
        a = 1
        for bm in user.bookmark_set.all():
            if bm.Question.id == ques.id:
                b.append(0)
                a = 0
                break
        if a:
            b.append(1)

    return render(request, 'blog/mysearch.html', {'user': user, 'match_ques': match_ques, 'data': zip(match_ques, v, b), 'search': search})


@login_required
def nquesvote(request, pk, username):
    notification = Notifications.objects.get(pk=pk)
    user = User.objects.get(username=username)
    ques = notification.Question
    votes = ques.quesvotes_set.all()
    s = set()
    for v in votes:
        s.add(str(v.User.username))
    # print(s)
    if user.username in s:
        pass
    else:
        votes = Quesvotes()
        votes.Question = ques
        votes.User = user
        ques.votes += 1;
        ques.save()
        votes.save()
    return redirect('blog:nques', pk, username)

@login_required
def nansvote(request, pk, username):
    notification = Notifications.objects.get(pk=pk)
    user = User.objects.get(username=username)
    ans = notification.Answer
    votes = ans.ansvotes_set.all()
    s = set()
    for v in votes:
        s.add(str(v.User.username))
    # print(s)
    if user.username in s:
        pass
    else:
        votes = Ansvotes()
        votes.Answer = ans
        votes.User = user
        ans.votes += 1;
        ans.save()
        votes.save()
    return redirect('blog:nques', pk, username)

@login_required
def quesdownvote(request, pk, username, pk2):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)
    votes = ques.quesvotes_set.all()

    Quesvotes.objects.filter(Question=ques, User=user).delete()

    ques.votes -= 1
    ques.save()
    i = int(pk2)
    if i == 0:
        return redirect('blog:home', username)
    elif i == 1:
        return redirect('blog:myques', username)
    elif i == 2:
        return redirect('blog:mybookmark', username)
    elif i == 3:
        return redirect('blog:myans', username)
    elif i == 4:
        return redirect('blog:ans', ques.id , username)

@login_required
def squesdownvote(request, pk, username, search):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)
    votes = ques.quesvotes_set.all()
    Quesvotes.objects.filter(Question=ques, User=user).delete()

    ques.votes -= 1
    ques.save()
    question = Question.objects.filter(tags=m1[search])
    v = []
    b = []
    for ques in question:
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)

    for ques in question:
        a = 1
        for bm in user.bookmark_set.all():
            if bm.Question.id == ques.id:
                b.append(0)
                a = 0
                break
        if a:
            b.append(1)

    return render(request, 'blog/search.html',{'user': user, 'question': question, 'data': zip(question, v, b), "search": search})

@login_required
def bs_quesdownvote(request, pk, username, search):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)
    votes = ques.quesvotes_set.all()
    Quesvotes.objects.filter(Question=ques, User=user).delete()
    ques.votes -= 1
    ques.save()
    bookmark = user.bookmark_set.all()
    match_ques = []
    for bm in bookmark:
        if bm.Question.tags == m1[search]:
            match_ques.append(bm)

    v = []
    for bm in match_ques:
        ques = bm.Question
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)
    return render(request, 'blog/Bookmarksearch.html', {'user': user, 'bookmark': match_ques, 'data': zip(match_ques, v), "search": search})

@login_required
def qs_quesdownvote(request, pk, username, search):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)
    votes = ques.quesvotes_set.all()
    Quesvotes.objects.filter(Question=ques, User=user).delete()
    ques.votes -= 1
    ques.save()
    match_ques = Question.objects.filter(Q(tags__icontains=m1[search]), User=user)
    v = []
    b = []
    for ques in match_ques:
        a = 1
        for votes in user.quesvotes_set.all():
            if votes.Question.id == ques.id:
                v.append(0)
                a = 0
                break
        if a:
            v.append(1)

    for ques in match_ques:
        a = 1
        for bm in user.bookmark_set.all():
            if bm.Question.id == ques.id:
                b.append(0)
                a = 0
                break
        if a:
            b.append(1)

    return render(request, 'blog/mysearch.html', {'user': user, 'match_ques': match_ques, 'data': zip(match_ques, v, b), 'search': search})


@login_required
def nquesdownvote(request, pk, username):
    notification = Notifications.objects.get(pk=pk)
    user = User.objects.get(username=username)
    ques = notification.Question
    votes = ques.quesvotes_set.all()
    Quesvotes.objects.filter(Question=ques, User=user).delete()

    ques.votes -= 1
    ques.save()
    return redirect('blog:nques', pk, username)

@login_required
def nansdownvote(request, pk, username):
    notification = Notifications.objects.get(pk=pk)
    user = User.objects.get(username=username)
    ans = notification.Answer
    votes = ans.ansvotes_set.all()
    Ansvotes.objects.filter(Answer=ans, User=user).delete()

    ans.votes -= 1
    ans.save()
    return redirect('blog:nques', pk, username)

@login_required
def ansdownvote(request, pk, username, pk2):
    user = User.objects.get(username=username)
    ans = Answer.objects.get(pk=pk)
    votes = ans.ansvotes_set.all()

    Ansvotes.objects.filter(Answer=ans, User=user).delete()

    ans.votes -= 1
    ans.save()

    i = int(pk2)
    if i == 0:
        return redirect('blog:ans', ans.Question.id, username)
    else:
        return redirect('blog:myans', username)

@login_required
def ansvote(request, pk, username, pk2):
    user = User.objects.get(username=username)
    ans = Answer.objects.get(pk=pk)
    votes = ans.ansvotes_set.all()
    s = set()
    for v in votes:
        s.add(str(v.User.username))
    # print(s)
    if user.username in s:
        pass
    else:
        votes = Ansvotes()
        votes.Answer = ans
        votes.User = user
        ans.votes += 1
        ans.save()
        votes.save()
    #return redirect('blog:home', username)
    i = int(pk2)
    if i == 0:
        return redirect('blog:ans', ans.Question.id , username)
    else:
        return redirect('blog:myans', username)

@login_required
def allvote(request, pk, username):
    user = User.objects.get(username=username)
    ques = Question.objects.get(pk=pk)
    votes = ques.quesvotes_set.all()
    print(votes)
    return render(request, 'blog/votes.html', {'user': user, 'votes': votes})

@login_required
def allansvote(request, pk, username):
    user = User.objects.get(username=username)
    ans = Answer.objects.get(pk=pk)
    votes = ans.ansvotes_set.all()
    print(votes)
    return render(request, 'blog/votes.html', {'user': user, 'votes': votes})

@login_required
def userinfo(request, username, username2):
    user1 = User.objects.get(username=username2)
    user1_ = UserProfile.objects.get(user=user1)
    tags1 = user1_.tags
    tags2 = list(tags1)
    tags = [int(i) for i in tags2]
    user = User.objects.get(username=username)
    username = user.username
    return render(request, 'blog/userinfo.html', {'user1_': user1_, 'user1': user1, 'tags': tags, 'username':username })

@login_required
def settings(request, username):
    user = User.objects.get(username=username)
    user_ = UserProfile.objects.get(user=user)
    tags1 = user_.tags
    tags2 = list(tags1)
    tags = [int(i) for i in tags2]
    return render(request, 'blog/settings.html', {'user_': user_, 'user': user , 'tags':tags})

def preferences(request, username):
    user = User.objects.get(username=username)
    user_ = UserProfile.objects.get(user=user)
    tags1 = user_.tags
    tags2 = list(tags1)
    tags = [int(i) for i in tags2]
    return render(request, 'blog/preferences.html', {'user_': user_, 'user': user , 'tags':tags})


def updatepreferences(request, username):
    user = User.objects.get(username=username)
    user_ = UserProfile.objects.get(user=user)
    temp = []
    if request.POST.get('0'):
        print(request.POST.get('0'))
        temp.append('0')
        print(0)
    if request.POST.get('1'):
        print(request.POST.get('1'))
        temp.append('1')
        print(1)
    if request.POST.get('2'):
        print(request.POST.get('2'))
        temp.append('2')
        print(2)
    if request.POST.get('3'):
        print(request.POST.get('3'))
        temp.append('3')
        print(3)
    if request.POST.get('4'):
        print(request.POST.get('4'))
        temp.append('4')
        print(4)
    if request.POST.get('5'):
        print(request.POST.get('5'))
        temp.append('5')
        print(5)
    user_.tags = temp
    user_.save()
    return redirect('blog:settings', username)