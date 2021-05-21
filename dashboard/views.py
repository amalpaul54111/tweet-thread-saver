from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from twitter_scripts import thread_fetch
from .models import Thread

# Create your views here.
def dashboard(request):
    print(request.user.username)
    threads = Thread.objects.all()
    return render(request=request, template_name="dashboard.html", context={'threads': threads})


def refresh(request):
    threads=thread_fetch.main(request.user.username)
    for thread in threads:
        convId = thread['conversation_id']
        author = thread['thread_author']
        author_username = thread['thread_author_username']
        tweets = thread['thread_tweets']
        twitter_thread=""
        for tweet in tweets:
            twitter_thread = twitter_thread + tweet
        new_thread = Thread(
            user=request.user,
            conversationId=convId,
            thread_author=author,
            thread_author_username=author_username,
            thread_tweets=twitter_thread
            )
        new_thread.save()

    return redirect("/dashboard")