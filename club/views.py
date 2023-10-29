from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.apps import AppConfig
import random
from django.db.models import Q
import datetime

# đăng nhập & đăng ký


def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            return redirect("a_login")
    return render(request, "registrations/login.html")


def Signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        facebook = request.POST.get("facebook")
        zalo = request.POST.get("zalo")
        cls = request.POST.get("class")
        description = request.POST.get("description")
        avatar = request.FILES['avatar']
        thumbnail = request.FILES['thumbnail']

        user = User.objects.filter(username=username).first()
        user2 = Social.objects.filter(zalo=zalo).first()

        if not user and not user2:
            user = User.objects.create_user(username, email, password)
            user.save()
            user = User.objects.get(username=username)
            if user:
                user2 = Social(user=user, facebook=facebook, zalo=zalo, avatar=avatar, thumbnail=thumbnail, cls=cls,
                               email=email, description=description)
                user2.save()
                login(request, user)
                return redirect("home")
        else:
            login(request, user)
            return redirect("home")
    return render(request, "registrations/register.html")

# trang chủ


def index(request):
    return render(request, "index.html")

# list_view


def home(request):
    if request.user.is_authenticated:
        club = Club.objects.all()
        noti = nofitication.objects.filter(user=request.user).all()
        '''
        if request.method == "GET":
            club = Club.objects.filter(
                name__contains=request.GET.get['search']).all()
        '''
        context = {"posts": club[::-1], "notis": noti}
    else:
        return redirect("a_login")
    return render(request, "club/home.html", context)


def member_hire(request):
    if request.user.is_authenticated:
        mem_hire = Member_Hire.objects.all()
        club = Club.objects.filter(user=request.user).all()
        noti = nofitication.objects.filter(user=request.user).all()
        '''
        if request.method == "GET":
            mem_hire = Member_Hire.objects.filter(
                title__contain=request.get['search']).all()
        '''
        context = {"posts": mem_hire[::-1], "clubs": club[::-1], "notis": noti}
    else:
        return redirect("a_login")
    return render(request, "member_hire/member.html", context)


def Post(request):
    if request.user.is_authenticated:
        post = Posts.objects.all()
        p = Posts.objects.filter(pin=1).count()
        noti = nofitication.objects.filter(user=request.user).all()
        '''
        if request.method == "GET":
            post = Posts.objects.filter(
                content__contain=request.get['search']).all()
        '''
        context = {"posts": post[::-1], "p_count": p, 'notis': noti}
    else:
        return redirect("a_login")
    return render(request, "post/post.html", context)


def Alshop(request):
    if request.user.is_authenticated:
        post = Alshop.objects.all()
        noti = nofitication.objects.filter(user=request.user).all()
        '''
        if request.method == "GET":
            post = Alshop.objects.filter(
                name__contain=request.get['search']).all()
        '''
        context = {"posts": post[::-1], "notis": noti}
    else:
        return redirect("a_login")
    return render(request, "shop/shop.html", context)


def Alevent(request):
    if request.user.is_authenticated:
        post = Event.objects.all()
        club = Club.objects.filter(user=request.user).all()
        payment = Payment_method.objects.all()
        noti = nofitication.objects.filter(user=request.user).all()
        '''
        if request.method == "GET":
            post = Alevent.objects.filter(
                name__contain=request.get['search']).all()
        '''
        context = {"posts": post[::-1],
                   "clubs": club[::-1], "payment": payment, "notis": noti}
    else:
        return redirect("a_login")
    return render(request, "event/event.html", context)


def Aldonate(request):
    if not request.user.is_authenticated:
        return redirect('a_login')
    return render(request, "donate/donate.html")

# tạo


def create_Post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            content = request.POST.get("content")
            image = request.FILES.get('image')

            if image:

                avatar = Social.objects.filter(id=request.user.id).first()

                if request.user.is_superuser:
                    pin = 1
                else:
                    pin = 0

                new_post = Posts(content=content, image=image, pin=pin,
                                 user=request.user, avatar=avatar.avatar, comment_count=0)
                new_post.save()
                return redirect("post")
            else:
                avatar = Social.objects.filter(id=request.user.id).first()

                if request.user.is_superuser:
                    pin = 1
                else:
                    pin = 0

                new_post = Posts(content=content, pin=pin, user=request.user,
                                 avatar=avatar.avatar, comment_count=0)
                new_post.save()
                return redirect("post")
    else:
        return redirect('a_login')


def create_club(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get("name")
            description = request.POST.get("description")
            type_club = request.POST.get("type")
            skill = request.POST.get("skill")
            image = request.FILES.get('image')

            club = Club.objects.get(name=name, user=request.user)

            if not club:
                if image:
                    new_club = Club(name=name, description=description, type_club=type_club,
                                    user=request.user, skill=skill, image=image, comment_counter=0)
                    new_club.save()
                    new_club = Club.objects.filter(
                        name=name, user=request.user).first()
                    return redirect("Club_view", id=new_club.id)
                else:
                    new_club = Club(name=name, description=description, type_club=type_club,
                                    user=request.user, skill=skill, comment_counter=0)
                    new_club.save()
                    new_club = Club.objects.filter(
                        name=name, user=request.user).first()
                    return redirect("Club_view", id=new_club.id)
            else:
                return redirect("Error")
    else:
        return redirect('a_login')


def create_hire_news(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            main_skill = request.POST.get("main_skill")
            skill = request.POST.get("skill")
            cls = request.POST.get("cls")
            club = request.POST.get("club_select")
            image = request.FILES.get('image')
            date = request.POST.get("date")

            date = date.strftime("%d/%m/%Y")

            club = Club.objects.get(id=club)

            if club:
                if image:

                    avatar = Social.objects.filter(
                        user__id=request.user.id).first()

                    new_hire_news = Member_Hire(title=title, description=description, main_skill=main_skill, skill=skill, cls=cls,
                                                image=image, like=0, comment_counter=0, disliked=0, down=0, user=request.user, apply_count=0, avatar=avatar.avatar, end_date=date)
                    new_hire_news.save()
                    m = Member_Hire.objects.filter(
                        title=title, user=request.user).first()
                    return redirect("Member_Hire_View", id=m.id)
                else:
                    avatar = Social.objects.filter(
                        user__id=request.user.id).first()

                    new_hire_news = Member_Hire(title=title, description=description, main_skill=main_skill, skill=skill, cls=cls, end_date=date,
                                                like=0, comment_counter=0, disliked=0, down=0, user=request.user, apply_count=0, avatar=avatar.avatar)
                    new_hire_news.save()
                    m = Member_Hire.objects.filter(
                        title=title, user=request.user).first()
                    return redirect("Member_Hire_View", id=m.id)
            else:
                return redirect("error")
    else:
        return redirect('a_login')


def create_event(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get("name")
            standby = request.POST.get("standby")
            description = request.POST.get("description")
            image = request.FILES.get('image')
            ticket = request.POST.get("ticket")
            date = request.POST.get("date")
            date = date.strftime("%d/%m/%Y")
            if image:

                avatar = Social.objects.filter(
                    user__id=request.user.id).first()

                if ticket > 0:
                    new_event = Event(name=name, standby=standby, description=description, donate=10,
                                      image=image, ticket=ticket, user=request.user, like=0, comment_counter=0, disliked=0, down=0, avatar=avatar.avatar, date=date)
                    new_event.save()
                    event = Event.objects.filter(
                        name=name, standby=standby, user=request.user).first()
                    return redirect("Event_view", id=event.id)
                else:
                    new_event = Event(name=name, standby=standby, description=description, donate=0,
                                      image=image, ticket=ticket, user=request.user, like=0, comment_counter=0, disliked=0, down=0, avatar=avatar.avatar, date=date)
                    new_event.save()
                    event = Event.objects.filter(
                        name=name, standby=standby, user=request.user).first()
                    return redirect("Event_view", id=event.id)
            else:
                avatar = Social.objects.filter(
                    user__id=request.user.id).first()

                if ticket > 0:
                    new_event = Event(name=name, standby=standby, description=description, donate=10, ticket=ticket,
                                      user=request.user, like=0, comment_counter=0, disliked=0, down=0, avatar=avatar.avatar, date=date)
                    new_event.save()
                    event = Event.objects.filter(
                        name=name, standby=standby, user=request.user).first()
                    return redirect("Event_view", id=event.id)
                else:
                    new_event = Event(name=name, standby=standby, description=description, donate=0,
                                      ticket=ticket, user=request.user, like=0, comment_counter=0, disliked=0, down=0, avatar=avatar.avatar, date=date)
                    new_event.save()
                    event = Event.objects.filter(
                        name=name, standby=standby, user=request.user).first()
                    return redirect("Event_view", id=event.id)
    else:
        return redirect('a_login')


def create_shop(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get('name')
            type_shop = request.POST.get('type')
            description = request.POST.get('description')
            image = request.FILES['image']
            if image:

                new_shop = Alshop(name=name, type_shop=type_shop, description=description,
                                  image=image, like=0, comment_counter=0, disliked=0, down=0, user=request.user)
                new_shop.save()
                return redirect("Alshop")
            else:
                new_shop = Alshop(name=name, type_shop=type_shop, description=description,
                                  image=image, like=0, comment_counter=0, disliked=0, down=0, user=request.user)
                new_shop.save()
                return redirect("Alshop")
    else:
        return redirect('a_login')

# comment


def comment_post(request, id):
    if request.user.is_authenticated:
        post = Posts.objects.get(id=id).first()
        if request.method == "POST" and post:
            content = request.POST.get("content")

            new_comment = Comment_Post(
                content=content, post=post, user=request.user)
            new_comment.save()
            content = request.user.username, "đã bình luận vào bài viết của bạn"
            link = '/view/post/'+str(post.id)
            noti = nofitication(content=content, link=link, user=post.user)
            noti.save()
            post.comment_counter += 1
            post.save()
            return redirect("Post")
    else:
        return redirect('a_login')


def comment_club(request, id):
    if request.user.is_authenticated:
        post = Club.objects.filter(id=id).first()
        if request.method == "POST" and post:
            content = request.POST.get("content")

            new_comment = Comment_Club(
                content=content, post=post, user=request.user)
            new_comment.save()
            content = request.user.username, "đã bình luận vào bài viết của bạn"
            link = '/view/club/'+str(post.id)
            noti = nofitication(content=content, link=link, user=post.user)
            noti.save()
            post.comment_counter += 1
            post.save()
            return redirect("Club")
    else:
        return redirect('a_login')


def comment_hire(request, id):
    if request.user.is_authenticated:
        post = Member_Hire.objects.filter(id=id).first()
        if request.method == "POST" and post:
            content = request.POST.get("content")

            new_comment = Comment_Hire(
                content=content, post=post, user=request.user)
            new_comment.save()
            content = request.user.username, "đã bình luận vào bài viết của bạn"
            link = '/view/member/hire/'+str(post.id)
            noti = nofitication(content=content, link=link, user=post.user)
            noti.save()
            post.comment_counter += 1
            post.save()
            return redirect("Hire")
    else:
        return redirect('a_login')


def comment_event(request, id):
    if request.user.is_authenticated:
        post = Event.objects.filter(id=id).first()
        if request.method == "POST" and post:
            content = request.POST.get("content")

            new_comment = Comment_Event(
                content=content, post=post, user=request.user)
            new_comment.save()
            content = request.user.username, "đã bình luận vào bài viết của bạn"
            link = '/view/event/'+str(post.id)
            noti = nofitication(content=content, link=link, user=post.user)
            noti.save()
            post.comment_counter += 1
            post.save()
            return redirect("Event")
    else:
        return redirect('a_login')


def reply_comment_post(request, post_id, comment_id):
    if request.user.is_authenticated:
        post = Posts.objects.get(id=post_id).first()
        cmt = Comment_Post.objects.filter(id=comment_id).first()
        if request.method == "POST" and post and cmt:
            content = request.POST.get("content")

            new_comment = Comment_Post(
                content=content, post=post, user=request.user, reply=cmt)
            new_comment.save()
            content = request.user.username, "đã phản hồi lại bình luận vào bài viết của bạn"
            link = '/view/post/'+str(post.id)
            noti = nofitication(content=content, link=link, user=cmt.user)
            noti.save()
            post.comment_counter += 1
            post.save()
            return redirect("Post")
    else:
        return redirect('a_login')


def reply_comment_club(request, post_id, comment_id):
    if request.user.is_authenticated:
        post = Club.objects.get(id=post_id).first()
        cmt = Comment_Club.objects.filter(id=comment_id).first()
        if request.method == "POST" and post and cmt:
            content = request.POST.get("content")

            new_comment = Comment_Club(
                content=content, post=post, user=request.user, reply=cmt)
            new_comment.save()
            content = request.user.username, "đã phản hồi lại bình luận vào bài viết của bạn"
            link = '/view/club/'+str(post.id)
            noti = nofitication(content=content, link=link, user=cmt.user)
            noti.save()
            post.comment_counter += 1
            post.save()
            return redirect("Club")
    else:
        return redirect('a_login')


def reply_comment_hire(request, post_id, comment_id):
    if request.user.is_authenticated:
        post = Member_Hire.objects.get(id=post_id).first()
        cmt = Comment_Hire.objects.filter(id=comment_id).first()
        if request.method == "POST" and post and cmt:
            content = request.POST.get("content")

            new_comment = Comment_Hire(
                content=content, post=post, user=request.user, reply=cmt)
            new_comment.save()
            content = request.user.username, "đã phản hồi lại bình luận vào bài viết của bạn"
            link = '/view/member/hire/'+str(post.id)
            noti = nofitication(content=content, link=link, user=cmt.user)
            noti.save()
            post.comment_counter += 1
            post.save()
            return redirect("Hire")
    else:
        return redirect('a_login')


def reply_comment_event(request, post_id, comment_id):
    if request.user.is_authenticated:
        post = Event.objects.get(id=post_id).first()
        cmt = Comment_Event.objects.filter(id=comment_id).first()
        if request.method == "POST" and post and cmt:
            content = request.POST.get("content")

            new_comment = Comment_Event(
                content=content, post=post, user=request.user, reply=cmt)
            new_comment.save()
            content = request.user.username, "đã phản hồi lại bình luận vào bài viết của bạn"
            link = '/view/event/'+str(post.id)
            noti = nofitication(content=content, link=link, user=cmt.user)
            noti.save()
            post.comment_counter += 1
            post.save()
            return redirect("Event")
    else:
        return redirect('a_login')

# Xóa


def delete_club(request, id):
    if request.user.is_authenticated:
        club = Club.objects.filter(id=id).first()

        club.delete()
        return redirect("home")
    else:
        return redirect('a_login')


def delete_post(request, id):
    if request.user.is_authenticated:
        club = Posts.objects.filter(id=id).first()

        club.delete()
        return redirect("home")
    else:
        return redirect('a_login')


def delete_hire_news(request, id):
    if request.user.is_authenticated:
        club = Member_Hire.objects.filter(id=id).first()

        club.delete()
        return redirect("home")
    else:
        return redirect('a_login')


def delete_shop(request, id):
    if request.user.is_authenticated:
        club = Alshop.objects.filter(id=id).first()

        club.delete()
        return redirect("home")
    else:
        return redirect('a_login')


def delete_event(request, id):
    if request.user.is_authenticated:
        club = Event.objects.filter(id=id).first()

        club.delete()
        return redirect("home")
    else:
        return redirect('a_login')


def delete_comment_post(request, id):
    if request.user.is_authenticated:
        comment = Comment_Post.objects.filter(id=id).first()
        comment.delete()
        return redirect("home")
    else:
        return redirect('a_login')


def delete_comment_club(request, id):
    if request.user.is_authenticated:
        comment = Comment_Club.objects.filter(id=id).first()
        comment.delete()
        return redirect("home")
    else:
        return redirect('a_login')


def delete_comment_hire(request, id):
    if request.user.is_authenticated:
        comment = Comment_Hire.objects.filter(id=id).first()
        comment.delete()
        return redirect("home")
    else:
        return redirect('a_login')


def delete_comment_event(request, id):
    if request.user.is_authenticated:
        comment = Comment_Event.objects.filter(id=id).first()
        comment.delete()
        return redirect("home")
    else:
        return redirect('a_login')


def delete_apply_from_hire(request, id):
    if request.user.is_authenticated:
        apply = Apply_from_Hire.objects.filter(id=id).first()
        apply.delete()
        return redirect("home")
    else:
        return redirect('a_login')


def delete_apply_from_you(request, id):
    if request.user.is_authenticated:
        apply = Apply_from_You.objects.filter(id=id).first()
        apply.delete()
        return redirect("home")
    else:
        return redirect('a_login')


def Apply_from_hire(request, id):
    if request.user.is_authenticated:
        hire = Member_Hire.objects.get(id=id).first()
        if request.method == "POST" and hire:
            letter = request.POST.get("letter")

            new_apply = Apply_from_Hire(
                letter=letter, user=request.user, post=hire, status="Chờ xử lý")
            new_apply.save()
            return redirect("Hire_View", id=id)
    else:
        return redirect('a_login')
    return render(request, "apply/apply_from_hire.html")

# Apply


def Apply_from_you(request, id):
    if request.user.is_authenticated:
        hire = Club.objects.get(id=id).first()
        if request.method == "POST" and hire:
            letter = request.POST.get("letter")

            new_apply = Apply_from_You(
                letter=letter, user=request.user, post=hire, status="Chờ xử lý")
            new_apply.save()
            return redirect("Club_View", id=id)
    else:
        return redirect('a_login')
    return render(request, "apply/apply_from_hire.html")


def delete_user(request, id):
    if request.user.is_authenticated:
        if request.user.id == id:
            user = User.objects.filter(id=id).first()
            post_id = Posts.objects.filter(user_id=id).all()
            event = Alevent.objects.filter(user_id=id).all()
            club = Club.objects.filter(user_id=id).all()
            user.delete()

            for i in post_id:
                i.delete()
            for item in event:
                item.delete()
            for j in club:
                j.delete()
            return redirect('index')
        else:
            return redirect("home")
    else:
        return redirect('a_login')

# Like


def like_post_views(request, id):
    if request.user.is_authenticated:
        post = Posts.objects.get(id=id)
        user = request.user
        if not user in post.like:
            post.like.add(user)
            link = "/post/"+str(id)+"/"
            content = str(request.user.username)+" đã like bài viết của bạn"
            noti = nofitication(content=content, link=link, user=post.user)
            noti.save()
        else:
            post.like.remove(user)
        return HttpResponseRedirect(reverse('post'), args=[id])
    else:
        return redirect('a_login')


def like_club_views(request, id):
    if request.user.is_authenticated:
        post = Club.objects.get(id=id)
        user = request.user
        if not user in post.like:
            post.like.add(user)
            link = "/home/"+str(id)+"/"
            content = str(request.user.username)+" đã like bài viết của bạn"
            noti = nofitication(content=content, link=link, user=post.user)
            noti.save()
        else:
            post.like.remove(user)
        return HttpResponseRedirect(reverse('club'), args=[id])
    else:
        return redirect('a_login')


def like_event_views(request, id):
    if request.user.is_authenticated:
        post = Alevent.objects.get(id=id)
        user = request.user
        if not user in post.like:
            post.like.add(user)
            link = "/event/"+str(id)+"/"
            content = str(request.user.username)+" đã like bài viết của bạn"
            noti = nofitication(content=content, link=link, user=post.user)
            noti.save()
        else:
            post.like.remove(user)
        return HttpResponseRedirect(reverse('event'), args=[id])
    else:
        return redirect('a_login')


def like_shop_views(request, id):
    if request.user.is_authenticated:
        post = Alshop.objects.get(id=id)
        user = request.user
        if not user in post.like:
            post.like.add(user)
        else:
            post.like.remove(user)
        return HttpResponseRedirect(reverse('shop'), args=[id])
    else:
        return redirect('a_login')


def like_hire_views(request, id):
    if request.user.is_authenticated:
        post = Member_Hire.objects.get(id=id)
        user = request.user
        if not user in post.like:
            post.like.add(user)
            link = "/member/hire/"+str(id)+"/"
            content = str(request.user.username)+" đã like bài viết của bạn"
            noti = nofitication(content=content, link=link, user=post.user)
            noti.save()
        else:
            post.like.remove(user)
        return HttpResponseRedirect(reverse('member_hire'), args=[id])
    else:
        return redirect('a_login')

# dislike


def dislike_post_views(request, id):
    if request.user.is_authenticated:
        post = Posts.objects.get(id=id)
        user = request.user
        if not user in post.dislike:
            post.dislike.add(user)
        else:
            post.dislike.remove(user)
        return HttpResponseRedirect(reverse('post'), args=[id])
    else:
        return redirect('a_login')


def dislike_club_views(request, id):
    if request.user.is_authenticated:
        post = Club.objects.get(id=id)
        user = request.user
        if not user in post.dislike:
            post.dislike.add(user)
        else:
            post.dislike.remove(user)
        return HttpResponseRedirect(reverse('post'), args=[id])
    else:
        return redirect('a_login')


def dislike_event_views(request, id):
    if request.user.is_authenticated:
        post = Alevent.objects.get(id=id)
        user = request.user
        if not user in post.dislike:
            post.dislike.add(user)
        else:
            post.dislike.remove(user)
        return HttpResponseRedirect(reverse('post'), args=[id])
    else:
        return redirect('a_login')


def dislike_shop_views(request, id):
    if request.user.is_authenticated:
        post = Alshop.objects.get(id=id)
        user = request.user
        if not user in post.dislike:
            post.dislike.add(user)
        else:
            post.dislike.remove(user)
        return HttpResponseRedirect(reverse('post'), args=[id])
    else:
        return redirect('a_login')


def dislike_hire_views(request, id):
    if request.user.is_authenticated:
        post = Member_Hire.objects.get(id=id)
        user = request.user
        if not user in post.dislike:
            post.dislike.add(user)
        else:
            post.like.remove(user)
        return HttpResponseRedirect(reverse('post'), args=[id])
    else:
        return redirect('a_login')


# Báo cáo

def down_post_views(request, id):
    if request.user.is_authenticated:
        post = Posts.objects.get(id=id)
        user = request.user
        if not user in post.down:
            post.down.add(user)
        else:
            post.down.remove(user)
        return HttpResponseRedirect(reverse('post'), args=[id])
    else:
        return redirect('a_login')


def down_club_views(request, id):
    if request.user.is_authenticated:
        post = Club.objects.get(id=id)
        user = request.user
        if not user in post.down:
            post.down.add(user)
        else:
            post.down.remove(user)
        return HttpResponseRedirect(reverse('post'), args=[id])
    else:
        return redirect('a_login')


def down_event_views(request, id):
    if request.user.is_authenticated:
        post = Alevent.objects.get(id=id)
        user = request.user
        if not user in post.down:
            post.down.add(user)
        else:
            post.down.remove(user)
        return HttpResponseRedirect(reverse('post'), args=[id])
    else:
        return redirect('a_login')


def down_shop_views(request, id):
    if request.user.is_authenticated:
        post = Alshop.objects.get(id=id)
        user = request.user
        if not user in post.down:
            post.down.add(user)
        else:
            post.down.remove(user)
        return HttpResponseRedirect(reverse('post'), args=[id])
    else:
        return redirect('a_login')


def down_hire_views(request, id):
    if request.user.is_authenticated:
        post = Member_Hire.objects.get(id=id)
        user = request.user
        if not user in post.down:
            post.down.add(user)
        else:
            post.down.remove(user)
        return HttpResponseRedirect(reverse('post'), args=[id])
    else:
        return redirect('a_login')


# Xem chi tiết

def club_view(request, id):
    if request.user.is_authenticated:
        club = Club.objects.filter(id=id).first()
        noti = nofitication.objects.filter(user=request.user).all()
        context = {'post': club, "notis": noti}
    else:
        return redirect('a_login')
    return render(request, 'club/club_view.html', context)


def event_view(request, id):
    if request.user.is_authenticated:
        club = Alevent.objects.filter(id=id).first()
        noti = nofitication.objects.filter(user=request.user).all()
        context = {'post': club, "notis": noti}
    else:
        return redirect('a_login')
    return render(request, 'event/event_view.html', context)


def member_hire_view(request, id):
    if request.user.is_authenticated:
        club = Member_Hire.objects.filter(id=id).first()
        noti = nofitication.objects.filter(user=request.user).all()
        context = {'post': club, "notis": noti}
    else:
        return redirect('a_login')
    return render(request, 'member_hire/member_hire_view.html', context)


def view_post(request, id):
    if request.user.is_authenticated:
        post = Posts.objects.filter(id=id).first()
        noti = nofitication.objects.filter(user=request.user).all()
        context = {'post': post, "notis": noti}
    else:
        return redirect('a_login')
    return render(request, 'post/post_view.html', context)


def profile_view(request, id):
    if request.user.is_authenticated:
        user = User.objects.filter(id=id).first()
        user2 = Social.objects.filter(user=user).first()
        noti = nofitication.objects.filter(user=request.user).all()
        context = {'user': user, 'user2': user2, "notis": noti}
    else:
        return redirect('a_login')
    return render(request, 'profile/profile.html', context)

# Đăng xuất


def logout(request):
    if request.user.is_authenticated:
        logout(request.user)
        return redirect('index')
    else:
        return redirect('a_login')

# leader view


def leader_view(request):
    if not request.user.is_authenticated:
        return redirect('a_login')
    return render(request, 'leader/leader_list_view.html')


def leader_club_list_view(request):
    if request.user.is_authenticated:
        club = Club.objects.filter(user__user=request.user).all()
        if club:
            context = {'posts': club}
        else:
            return redirect('home')
    else:
        return redirect('a_login')
    return render(request, 'club/home.html', context)


def leader_event_list_view(request):
    if request.user.is_authenticated:
        club = Event.objects.filter(user__id=request.user.id).all()
        if club:
            context = {'posts': club}
        else:
            return redirect('home')
    else:
        return redirect('a_login')
    return render(request, 'event/event.html', context)


def leader_member_hire_list_view(request):
    if request.user.is_authenticated:
        club = Member_Hire.objects.filter(user__id=request.user.id).all()
        if club:
            context = {'posts': club}
        else:
            return redirect('home')
    else:
        return redirect('a_login')
    return render(request, 'member_hire/member_hire.html', context)


def leader_club_member_list_view(request):
    if request.user.is_authenticated:
        club = Club.objects.filter(user__id=request.user.id).first()
        if club:
            context = {'club': club}
        else:
            return redirect('home')
    else:
        return redirect('a_login')
    return render(request, 'leader/club_member.html', context)


def leader_club_apply_list_view(request):
    if request.user.is_authenticated:
        club = Club.objects.filter(user__id=request.user.id).first()
        member = Apply_from_You.objects.filter(club__id=club.id).all()
        if club:
            context = {'posts': member, 'club': club}
        else:
            return redirect('home')
    else:
        return redirect('a_login')
    return render(request, 'leader/club_apply_view.html', context)


def leader_member_hire_apply_list_view(request):
    if request.user.is_authenticated:
        club = Member_Hire.objects.filter(user__id=request.user.id).first()
        member = Apply_from_hire.objects.filter(club__id=club.id).all()
        if club:
            context = {'posts': member, 'club': club}
        else:
            return redirect('home')
    else:
        return redirect('a_login')
    return render(request, 'leader/member_hire_apply_view.html', context)


# Follow

def follow(request, id):
    if request.user.is_authenticated:
        if request.user.id != id:
            follow = Social.objects.get(user__id=id).first()
            follow.follower.add(request.user)
            follow.save()
            return redirect('profile', id=id)
        else:
            return redirect('profile', id=id)
    else:
        return redirect('a_login')

# Bài ghim


def pin_post(request):
    if request.user.is_authenticated:
        post = Posts.objects.filter(pin=1).all()
        context = {'posts': post}
    else:
        return redirect('a_login')
    return render(request, 'post/post.html', context)

# Search


def search_shop(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            search = request.GET.get("search")

            q = Alshop.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search))
            if q:
                return redirect('search_post_result', q=q)
            else:
                return redirect("Error")
    else:
        return redirect("a_login")


def search_post(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            search = request.GET.get("search")

            q = Posts.objects.filter(Q(content__icontains=search))
            if q:
                return redirect('search_post_result', q=q)
            else:
                return redirect("Error")
    else:
        return redirect("a_login")


def search_club(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            search = request.GET.get("search")

            q = Club.objects.filter(Q(name__icontains=search) | Q(
                description__icontains=search) | Q(type_club__icontains=search) | Q(skill__icontains=search))
            if q:
                return redirect('search_club_result', q=q)
            else:
                return redirect("Error")
    else:
        return redirect("a_login")


def search_member_hire(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            search = request.GET.get("search")

            q = Member_Hire.objects.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(
                main_skill__icontains=search) | Q(skill__icontains=search) | Q(cls__icontains=search))
            if q:
                return redirect('search_member_hire_result', q=q)
            else:
                return redirect("Error")
    else:
        return redirect("a_login")


def search_event(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            search = request.GET.get("search")

            q = Event.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search))
            if q:
                return redirect('search_post_result', q=q)
            else:
                return redirect("Error")
    else:
        return redirect("a_login")


def leader_search_club_member(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            search = request.GET.get("search")

            q = Club.objects.filter(Q(user__username__icontains=search) | Q(club__name__icontains=search) | Q(
                club__description__icontains=search) | Q(club__skill__icontains=search) | Q(club__type_club__icontains=search), admin=request.user)
            if q:
                return redirect('search_post_result', q=q)
            else:
                return redirect("Error")
    else:
        return redirect("a_login")


def leader_search_apply_from_hire(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            search = request.GET.get("search")

            q = Apply_from_hire.objects.filter(Q(user__username__icontains=search) | Q(club__name__icontains=search) | Q(
                club__description__icontains=search) | Q(club__skill__icontains=search) | Q(club__type_club__icontains=search), admin=request.user)
            if q:
                return redirect('search_post_result', q=q)
            else:
                return redirect("Error")
    else:
        return redirect("a_login")


def leader_search_apply_from_you(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            search = request.GET.get("search")

            q = Apply_from_you.objects.filter(Q(user__username__icontains=search) | Q(club__name__icontains=search) | Q(
                club__description__icontains=search) | Q(club__skill__icontains=search) | Q(club__type_club__icontains=search), admin=request.user)
            if q:
                return redirect('search_post_result', q=q)
            else:
                return redirect("Error")
    else:
        return redirect("a_login")


def search_post_result(request, q):
    if request.user.is_authenticated:
        post = Posts.objects.filter(Q(content__icontains=q)).all()
        context = {"posts": post}
    else:
        return redirect("a_login")
    return render(request, "post/post.html", context)


def search_club_result(request, q):
    if request.user.is_authenticated:
        post = Club.objects.filter(Q(name__icontains=q) | Q(
            description__icontains=q) | Q(type_club__icontains=q) | Q(skill__icontains=q)).all()
        context = {"posts": post}
    else:
        return redirect("a_login")
    return render(request, "club/home.html", context)


def search_member_hire_result(request, q):
    if request.user.is_authenticated:
        post = Member_Hire.objects.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(
            main_skill__icontains=q) | Q(skill__icontains=q) | Q(cls__icontains=q)).all()
        context = {"posts": post}
    else:
        return redirect("a_login")
    return render(request, "member_hire/member_hire.html", context)


def search_event_result(request, q):
    if request.user.is_authenticated:
        post = Event.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q)).all()
        context = {"posts": post}
    else:
        return redirect("a_login")
    return render(request, "event/event.html", context)


def search_shop_result(request, q):
    if request.user.is_authenticated:
        post = Alshop.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q)).all()
        context = {"posts": post}
    else:
        return redirect("a_login")
    return render(request, "shop/shop.html", context)


def search_member_hire_result(request, q):
    if request.user.is_authenticated:
        post = Member_Hire.objects.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(
            main_skill__icontains=q) | Q(skill__icontains=q) | Q(cls__icontains=q)).all()
        context = {"posts": post}
    else:
        return redirect("a_login")
    return render(request, "member_hire/member_hire.html", context)


def leader_search_club_member_result(request, q):
    if request.user.is_authenticated:
        post = Club.objects.filter(Q(user__username__icontains=q) | Q(name__icontains=q) | Q(
            description__icontains=q) | Q(skill__icontains=q) | Q(type_club__icontains=q), admin=request.user).all()
        context = {"posts": post}
    else:
        return redirect("a_login")
    return render(request, "leader/club_member.html", context)


def leader_search_apply_from_hire_result(request, q):
    if request.user.is_authenticated:
        post = Club.objects.filter(Q(user__username__icontains=q) | Q(name__icontains=q) | Q(
            description__icontains=q) | Q(skill__icontains=q) | Q(type_club__icontains=q), admin=request.user).all()
        context = {"posts": post}
    else:
        return redirect("a_login")
    return render(request, "leader/club_apply_view.html", context)


def leader_search_apply_from_you_result(request, q):
    if request.user.is_authenticated:
        post = Apply_from_You.objects.filter(Q(user__username__icontains=q) | Q(club__name__icontains=q) | Q(
            club__description__icontains=q) | Q(club__skill__icontains=q) | Q(club__type_club__icontains=q), admin=request.user).all()
        context = {"posts": post}
    else:
        return redirect("a_login")
    return render(request, "leader/member_hire_apply_view.html", context)


def nofitication_readed(request, id):
    if request.user.is_authenticated:
        noti = nofitication.objects.filter(id=id, user=request.user).first()
        link = noti.link
        noti.delete()
        return redirect(link)
    else:
        return redirect("a_login")


def all_nofitication_readed(request, back_link):
    if request.user.is_authenticated:
        noti = nofitication.objects.filter(user=request.user).all()
        noti.delete()
        return redirect(back_link)
    else:
        return redirect("a_login")
