from django.contrib import admin
from .models import User, Postings, Followings, Likes

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email",
                    "is_active", "is_staff", "is_superuser",
                    "last_login", "date_joined", "followers_count", "followings_count"
                    )

class PostingsAdmin(admin.ModelAdmin):
    list_display = ('posting_user', 'post_text', 'post_ts', 'likes_count',
                    'dislikes_count', 'post_superceded', 'supercede_ts', 'previous_post')

class FollowingsAdmin(admin.ModelAdmin):
    list_display = ('follower', 'follows', 'following_active', 'follow_start', 'follow_end')


class LikesAdmin(admin.ModelAdmin):
    list_display = ('liker', 'post_id', 'likes', 'likes_active', 'likes_starts_ts', 'likes_ends_ts')

admin.site.register(User, UserAdmin)
admin.site.register(Postings, PostingsAdmin)
admin.site.register(Followings, FollowingsAdmin)
admin.site.register(Likes, LikesAdmin)
