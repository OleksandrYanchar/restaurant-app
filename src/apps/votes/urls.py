from django.urls import path
from apps.votes.views import TodayMenusWithVotesView, VoteView

urlpatterns = [

    path('restaurants/menus/vote/', VoteView.as_view(), name='vote-menu'),
    path('restaurants/menus/today/votes/', TodayMenusWithVotesView.as_view(), name='today-menus-votes'),

]
