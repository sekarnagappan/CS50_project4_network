import math, decimal, sys, logging, os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError, transaction
from django.db.models import Count, Q

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

import json
from django.http import JsonResponse

from .models import User, Postings, Followings, Likes

#Python logger, for logging error
logger = logging.getLogger(__name__)

def index(request):
    #Only display index page if user is logged in.
    context = {}
    if request.user.is_authenticated:
        request, context = view_postings(request, context, "All")
        return render(request, "network/index.html", context)
    else:
        return HttpResponseRedirect(reverse("login"))

@login_required
def make_posting(request):

    # A make_posting request must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
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
        print(f"Update Post ID: {original_post.id}")

    posting = Postings(
                        posting_user = user,
                        post_text = text,
                        likes_count = 0,
                        dislikes_count = 0,
                        previous_post = original_post if post_id else null
                        )

    try:
        with transaction.atomic():
            posting.save()
            if (post_id):
                original_post.save()
                print(f"Posted Update. {original_post.id}")
    except IntegrityError:
        messages.error("Sorry, I am not able to update the post, a technical error has occured.")

    return JsonResponse({"message": "Posting Done."}, status=201)

@login_required
def view_all_post(request):
    context = {}
    request, context = view_postings(request, context, "All")

    return render(request, "network/index.html", context)


@login_required
def view_postings(request, context, filter="All", profile_user=""):
    # This functions retrives a list of post for a user and displays 10 post
    # per page, using a paginator.
    if (filter == "All" ):
        heading = "All Posts"
    elif (filter == "Followings"):
        heading == "Postings You Follow"
    elif (filter == "Profile"):
        heading == f"Posting By user {profile_user}"
    else:
        heading == ""


    list_page = request.GET.get('page', 1)

    try:
        usr = User.objects.get(username=request.user)
        list = Postings.objects.all().filter(post_superceded=False).order_by('-post_ts')
    except Exception as e:
        logger.error(f"{type(e)} : {e}")
        messages.error(request, "Sorry, I am not able to retrive any postings!")
    else:
        paginator = Paginator(list, 10)
        try:
            postlist = paginator.page(list_page)
        except PageNotAnInteger:
            postlist = paginator.page(1)
        except EmptyPage:
            postlist = paginator.page(paginator.num_pages)

        context = {'postlist': postlist, 'heading': heading, 'count': paginator.count }
        return (request, context)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


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
