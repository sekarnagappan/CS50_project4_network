from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError, transaction
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.utils import timezone
import json
import math, decimal, sys, logging, os

from .models import User, Postings, Followings, Likes


# Python logger, for logging error
logger = logging.getLogger(__name__)


def index(request):
    # Only display index page if user is logged in.

    context = {}
    if request.user.is_authenticated:
        request, context = view_postings(request, context, "All")
        return render(request, "network/index.html", context)
    else:
        return HttpResponseRedirect(reverse("login"))


# Add a new posting to the DB, or update an existing posting if the post_id is
# present in the request.
@login_required
def make_posting(request):

    # A make_posting request must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient e-mails
    data = json.loads(request.body)
    text = data.get('text', "")
    post_id = data.get('post_id', "")

    if text == "":
        return JsonResponse({
            "error": "Your post is empty."
        }, status=400)

    user = get_object_or_404(User, username=request.user)

    if (post_id):
        original_post = get_object_or_404(Postings, pk=post_id)
        original_post.post_superceded = True
        original_post.supercede_ts = timezone.now()
        print(f"Update Post ID: {original_post.id}")

    posting = Postings(
                        posting_user=user,
                        post_text=text,
                        likes_count=0,
                        dislikes_count=0,
                        previous_post=original_post if post_id else None
                        )

    try:
        with transaction.atomic():
            posting.save()
            if (post_id):
                original_post.save()
                print(f"Posted Update. {original_post.id}")
    except IntegrityError:
        messages.error(request, "Sorry, I am not able to update the post, a technical error has occured.")

    return JsonResponse({"message": "Posting Done."}, status=201)


@login_required
def view_profile(request):
    profile_id = request.GET.get('profile_id', '')
    if (profile_id != ''):
        context = {}
        request, context = view_postings(request, context, "Profile", profile_id)

    return render(request, "network/index.html", context)


@login_required
def view_all_post(request):
    context = {}
    request, context = view_postings(request, context, "All")

    return render(request, "network/index.html", context)


@login_required
def view_postings(request, context, filter="All", profile_id=""):
    # This functions retrieves a list of post for a user and displays 10 post
    # per page, using a paginator.

    heading = ""
    profile_follows = 0
    profile_followings = 0
    profile_usr = None
    user_follows = 0

    list_page = request.GET.get('page', 1)

    try:
        usr = get_object_or_404(User, username=request.user)
        if (filter == "Profile"):
            heading = f"Posting By user {profile_id}"

            profile_usr = get_object_or_404(User, username=profile_id)

            profile_follows = profile_usr.follower.filter(following_active=True).count()  # the number of people the profiled user follows.
            profile_followings = profile_usr.follows.filter(following_active=True).count()  # the number people following the profiled user
            user_follows = profile_usr.follows.filter(following_active=True).filter(follower=usr).count()
            # print(f"Followings count {profile_id}{profile_follows}, {profile_followings}")
            # list = Postings.objects.all().filter(posting_user=profile_usr).filter(post_superceded=False).order_by('-post_ts')
            list = Postings.objects.raw('select * from network_postings left outer join network_likes on ' \
                                        ' ( network_postings.id = network_likes.post_id_id AND network_likes.likes_active = True ' \
                                        ' and (network_likes.liker_id = %s)) ' \
                                        ' where network_postings.post_superceded = False AND network_postings.posting_user_id = %s ' \
                                        ' ORDER BY post_ts DESC', [usr.id, profile_usr.id])
        elif (filter == "Followings"):
            heading = "Postings You Follow"
            list = Postings.objects.filter(posting_user__in=Followings.objects.filter(following_active=True).filter(follower=usr).values_list('follows')).filter(post_superceded=False)

        else:
            heading = "All Posts"

            # list = Postings.objects.all().filter(post_superceded=False).order_by('-post_ts')
            list = Postings.objects.raw('select * from network_postings left outer join network_likes on ' \
                                        ' ( network_postings.id = network_likes.post_id_id AND network_likes.likes_active = True ' \
                                        ' and (network_likes.liker_id = %s )) '\
                                        ' where network_postings.post_superceded = False   ORDER BY post_ts DESC',
                                        [usr.id])
    except Exception as e:
        logger.error(f"{type(e)} : {e}")
        messages.error(request, "Sorry, I am not able to retrieve any postings!")
    else:
        paginator = Paginator(list, 10)
        try:
            postlist = paginator.page(list_page)
        except PageNotAnInteger:
            postlist = paginator.page(1)
        except EmptyPage:
            postlist = paginator.page(paginator.num_pages)
        
        context = {     'postlist': postlist,
                        'heading': heading,
                        'count': paginator.count,
                        'follows': profile_follows,
                        'followings': profile_followings,
                        'profile_usr': profile_id,
                        'user_follows': user_follows,
                        'sections' : filter,
                        'start_index': paginator.page(postlist.number).start_index(),
                        'end_index': paginator.page(postlist.number).end_index(),
                    }
        return (request, context)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def thumbs_click(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    thumbs_up = data.get('thumbs', "")  # True = Likes post, False = Dislikes Post, None = Netural.
    post_id = data.get('post_id', "")

    user = get_object_or_404(User, username=request.user)
    post = get_object_or_404(Postings, pk=post_id)
    likes = post.liked_post.filter(likes_active=True).filter(liker=user).first()

    if (thumbs_up is None and likes is None):
        print("Messages should not be here, most like so db record corruption")
        return JsonResponse({"message": "Shouldn't be here, nothing to register"}, status=201)

    if (thumbs_up is None):
        if (likes.likes == True):
            post.likes_count -= 1
        if (likes.likes == False):
            post.dislikes_count -= 1
        likes.likes_active = False
        likes.likes_ends_ts = timezone.now()

        try:
            with transaction.atomic():
                post.save()
                likes.save()
        except IntegrityError:
            messages.error(request, "Sorry, I am not able to update the likes, a technical error has occured.")

        print("Exiting thumbs up - True")
        return JsonResponse({"message": "Likes Cleared.",
                            'likes_count': post.likes_count,
                            'dislikes_count': post.dislikes_count }, status=201)

    if (thumbs_up is True):
        post.likes_count += 1
        new_likes = Likes(
                            liker=user,
                            post_id=post,
                            likes=True,
                            likes_active=True,
                        )
        if (likes is not None):
            post.dislikes_count -= 1
            likes.likes_active = False

        try:
            with transaction.atomic():
                post.save()
                new_likes.save()
                if (likes is not None):
                    likes.save()
        except IntegrityError:
            messages.error(request, "Sorry, I am not able to update the likes, a technical error has occured.")

        print("Exiting thumbs up - True")
        return JsonResponse({"message": "Likes Registered.",
                            'likes_count': post.likes_count,
                            'dislikes_count': post.dislikes_count }, status=201)

    if (thumbs_up is False):
        post.dislikes_count += 1
        new_likes = Likes(
                            liker=user,
                            post_id=post,
                            likes=False,
                            likes_active=True,
                        )
        if (likes is not None):
            post.likes_count -= 1
            likes.likes_active = False

        try:
            with transaction.atomic():
                post.save()
                new_likes.save()
                if (likes is not None):
                    likes.save()
        except IntegrityError:
            messages.error(request, "Sorry, I am not able to update the likes, a technical error has occured.")

        print("Exiting thumbs up - False")
        return JsonResponse({"message": "Dislike Registered.",
                            'likes_count': post.likes_count,
                            'dislikes_count': post.dislikes_count }, status=201)

    return JsonResponse({"message": "Thumbs Up - should not reach here!"}, status=400)


@login_required
def follows(request):

    breakpoint()
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    profile_id = data.get('profile_id', "")  # True = Likes post, False = Dislikes Post, None = Netural.
    follows = data.get('follow', "")

    user = get_object_or_404(User, username=request.user)
    profile_user = get_object_or_404(User, username=profile_id)

    try:
        following = Followings.objects.filter(follower=user).filter(follows=profile_user).filter(following_active=True)
        user_follows = profile_user.follows.filter(following_active=True).filter(follower=user).count()
    except IntegrityError:
        messages.error(request, "Sorry, I am not able to retrieve followings information, a technical error has occurred.")

    if len(following) > 1:
        return JsonResponse({"message": "Database integrity Error, nothing done!"}, status=400)

    if (follows == False):
        if (len(following) == 0):
            return JsonResponse({"message": "Not Following Anyway, nothing done!"}, status=201)

        user_follows -= 1
        user.followings_count -= 1
        profile_user.followers_count -= 1
        following = following[0]
        following.following_active = False
        following.follow_end = timezone.now()
         
        try:
            with transaction.atomic():
                user.save()
                profile_user.save()
                following.save()
        except IntegrityError:
            messages.error(request, "Sorry, I am not able to update the followings, a technical error has occurred.")

        return JsonResponse({   "message": "Following removed!",
                                "followings_count": profile_user.followings_count,
                                "followers_count": profile_user.followers_count,
                                "user_follows": user_follows,

                            },
                            status=201)
    else:
        if (len(following) == 1):
            return JsonResponse({"message": "Following Anyway, nothing done!"}, status=201)

        user_follows += 1
        user.followings_count += 1
        profile_user.followers_count += 1
        following = Followings(follower=user,
                                 follows=profile_user,
                                 following_active=True
                              )

        try:
            with transaction.atomic():
                user.save()
                profile_user.save()
                following.save()
        except IntegrityError:
            messages.error(request, "Sorry, I am not able to update the followings, a technical error has occured.")

        return JsonResponse({   "message": "Following updated!",
                                "followings_count": profile_user.followings_count,
                                "followers_count": profile_user.followers_count,
                                "user_follows": user_follows,
                            },
                            status=201)

    return JsonResponse({"message": "Follow - something wrong, should not reach here!"}, status=400)


@login_required
def followings(request):

    context = {}
    request, context = view_postings(request, context, "Followings")

    return render(request, "network/index.html", context)



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            print(f'User logged in: {username}')
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
