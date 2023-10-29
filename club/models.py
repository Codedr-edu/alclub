from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class nofitication(models.Model):
    content = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Social(models.Model):
    facebook = models.CharField(max_length=1000)
    zalo = models.CharField(max_length=1000)
    description = models.TextField()
    good = models.CharField(max_length=1000, null=True)
    like = models.CharField(max_length=1000, null=True)
    bad = models.CharField(max_length=1000, null=True)
    cls = models.IntegerField(null=True)
    avatar = models.ImageField(upload_to="images/")
    thumnail = models.ImageField(upload_to="images/")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(
        User, related_name='follower', on_delete=models.CASCADE, null=True, blank=True)
    nofitication = models.ForeignKey(
        nofitication, related_name='nofitication', on_delete=models.CASCADE, null=True, blank=True)

    def nofitication_count(self):
        return self.nofitication.count()

    def follower_count(self):
        return self.follower.count()


class Club(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    type_club = models.CharField(max_length=100)
    skill = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/")
    user = models.ForeignKey(Social, on_delete=models.CASCADE, null=True)
    comment_counter = models.IntegerField()
    like = models.ManyToManyField(
        User, related_name='like_set', blank=True)
    dislike = models.ManyToManyField(
        User, related_name='dislike_set', blank=True)
    down = models.ManyToManyField(
        User, related_name='down_set', blank=True)
    member = models.ManyToManyField(
        User, related_name='member_set', blank=True)
    date = models.DateField(auto_now_add=True)

    def count_like(self):
        return self.like.count()

    def count_dislike(self):
        return self.dislike.count()

    def count_down(self):
        return self.like.count()


class Posts(models.Model):
    content = models.TextField()
    username = models.CharField(max_length=1000)
    user = models.ForeignKey(Social, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    pin = models.IntegerField()
    comment_count = models.IntegerField()
    like = models.ManyToManyField(
        User, related_name='post_liked_set', blank=True)
    dislike = models.ManyToManyField(
        User, related_name='post_disliked_set', blank=True)
    down = models.ManyToManyField(
        User, related_name='post_downed_set', blank=True)
    date = models.DateField(auto_now_add=True)

    def count_like(self):
        return self.like.count()

    def count_dislike(self):
        return self.dislike.count()

    def count_down(self):
        return self.like.count()


class Alshop(models.Model):
    name = models.CharField(max_length=255)
    type_shop = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    link = models.CharField(max_length=400)
    like = models.ManyToManyField(
        User, related_name='shop_like', blank=True)
    dislike = models.ManyToManyField(
        User, related_name='shop_dislike', blank=True)
    down = models.ManyToManyField(
        User, related_name='shop_down', blank=True)

    def count_like(self):
        return self.like.count()

    def count_dislike(self):
        return self.dislike.count()

    def count_down(self):
        return self.like.count()


class Payment_method(models.Model):
    name = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)


class Event(models.Model):
    name = models.CharField(max_length=1000)
    user = models.ForeignKey(Social, on_delete=models.CASCADE, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to="images/")
    ticket = models.IntegerField()
    donate = models.IntegerField()
    comment_count = models.IntegerField()
    like = models.ManyToManyField(
        User, related_name='event_liked', blank=True)
    dislike = models.ManyToManyField(
        User, related_name='event_disliked', blank=True)
    down = models.ManyToManyField(
        User, related_name='event_downed', blank=True)
    ticket_counter = models.IntegerField()
    ticker_sold = models.IntegerField()
    payment_method = models.ForeignKey(
        Payment_method, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    joiner = models.ManyToManyField(
        User, related_name="event_joiner", null=True, blank=True)

    def count_like(self):
        return self.like.count()

    def count_dislike(self):
        return self.dislike.count()

    def count_down(self):
        return self.like.count()


class Member_Hire(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    main_skill = models.CharField(max_length=1000)
    skill = models.CharField(max_length=1000)
    cls = models.IntegerField()
    user = models.ForeignKey(Social, on_delete=models.CASCADE, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True)
    apply_count = models.IntegerField()
    comment_count = models.IntegerField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    like = models.ManyToManyField(
        User, related_name='member_hire_like', blank=True)
    dislike = models.ManyToManyField(
        User, related_name='member_hire_disliked', blank=True)
    down = models.ManyToManyField(
        User, related_name='member_hire_down', blank=True)
    avatar = models.ImageField()
    create_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def count_like(self):
        return self.like.count()

    def count_dislike(self):
        return self.dislike.count()

    def count_down(self):
        return self.like.count()


class Apply_from_Hire(models.Model):
    letter = models.TextField()
    user = models.ForeignKey(
        User, related_name='apply_hire_user', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Member_Hire, related_name='apply_hire', on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(
        User, related_name='apply_hire_admin', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=1000)


class Apply_from_You(models.Model):
    letter = models.TextField()
    user = models.ForeignKey(
        User, related_name='apply_club_user', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Club, related_name='apply_club', on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(
        User, related_name='apply_club_admin', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=1000)


class Comment_Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        Social, related_name='comment_post_user', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Posts, related_name='comment_post', on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name="post_reply")


class Comment_Club(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        Social, related_name='comment_club_user', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Member_Hire, related_name='comment_club', on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name="club_reply")


class Comment_Hire(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        Social, related_name='comment_hire_user', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Member_Hire, related_name='comment_hire', on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name="member_hire_reply")


class Comment_Event(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        Social, related_name='comment_event_user', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Event, related_name='comment_event', on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name="event_reply")


class Event_book(models.Model):
    user = models.ForeignKey(
        User, related_name='event_user', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Event, related_name='event',
                             on_delete=models.CASCADE, null=True)
    letter = models.TextField()
    Payment_method = models.ForeignKey(
        Payment_method, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=1000)
