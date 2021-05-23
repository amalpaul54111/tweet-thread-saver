from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from twitter_scripts import thread_fetch, profile_fetch
from .models import Thread

# Create your views here.
def dashboard(request):
    if request.user.username == '':
        return redirect('/user_login')
    else:
        print(request.user.username + " Logged in")
        threads = Thread.objects.filter(user=request.user)
        return render(request=request, template_name="dashboard.html", context={'threads': threads})


def refresh(request):

    # this is where we will run the script to add new mentions to our database 
    # and store them
    threads=thread_fetch.main(request.user.username)
    for thread in threads:
        convId = thread['conversation_id']
        author = thread['thread_author']
        author_username = thread['thread_author_username']
        tweets = thread['thread_tweets']
        twitter_thread=""
        profile_banner = profile_fetch.get_profile_url(author_username)
        for tweet in tweets:
            twitter_thread = twitter_thread +" "+ tweet
        new_thread = Thread(
            user=request.user,
            conversationId=convId,
            thread_author=author,
            thread_author_username=author_username,
            thread_author_banner=profile_banner,
            thread_tweets=twitter_thread
            )
        if not Thread.objects.filter(conversationId=convId).exists():
            new_thread.save()

    return redirect("/dashboard")


def noLogin(request):

    return render(request=request, template_name='login.html')