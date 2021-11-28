from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers_count   = models.PositiveIntegerField(default=0, help_text="Number of Followers", verbose_name="Followers Count")
    followings_count = models.PositiveIntegerField(default=0, help_text="Number of people you follow", verbose_name="Followerings Count")

class Postings(models.Model):
    posting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster", related_query_name="poster", verbose_name='Poster')
    post_text = models.TextField(help_text="Posting Text", verbose_name="Post Text")
    post_ts = models.DateTimeField(auto_now_add=True, verbose_name="Posting Timestamp")
    likes_count = models.PositiveIntegerField(default=0, help_text="Number of likes", verbose_name="Likes Count")
    dislikes_count = models.PositiveIntegerField(default=0, help_text="Number of dislikes", verbose_name="Dislikes Count")
    post_superceded = models.BooleanField(default=False, help_text="This post superceded by another post.",verbose_name='Superceded')
    supercede_ts = models.DateTimeField(blank=True, null=True, verbose_name="Supercede Timestamp")
    previous_post = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="replaced_post", related_query_name="replaced_post", verbose_name='Suceeding Post')

    def __str__(this):
        return (f'Post ID: {this.id}')

class Followings(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower", related_query_name="follower", verbose_name='Follower')
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follows", related_query_name="follows", verbose_name='Follows')
    following_active = models.BooleanField(default=True, help_text="The following is active.",verbose_name='Following Active')
    follow_start = models.DateTimeField(auto_now_add=True, verbose_name="Following Start Timestamp")
    follow_end = models.DateTimeField(blank=True, null=True, verbose_name="Following End Timestamp")

    def __str__(this):
        return (f'{this.follower} follows {this.follows}')

class Likes(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liker", related_query_name="liker", verbose_name='Liker')
    post_id = models.ForeignKey(Postings, on_delete=models.CASCADE, related_name="liked_post", related_query_name="liked_post", verbose_name='Liked Post')
    likes = models.BooleanField(default=True, help_text="Like or Dislike",verbose_name='Likes?')
    likes_active = models.BooleanField(default=True, help_text="This like is Active",verbose_name='Active Likes?')
    likes_starts_ts = models.DateTimeField(auto_now_add=True, verbose_name="Likes Timestamp")
    likes_ends_ts = models.DateTimeField(blank=True, null=True, verbose_name="Like End Timestamp")

    def __str__(this):
        if this.likes:
            return (f'{this.liker} likes {this.post_id}')
        else:
            return (f'{this.liker} dislikes {this.post_id}')
