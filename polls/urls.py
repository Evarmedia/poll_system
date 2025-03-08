# polls/urls.py
from django.urls import path
from .views import RegisterView, LoginView, PollListCreateView, PollDetailView, VoteView, PollResultsView, PollDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('polls/', PollListCreateView.as_view(), name='poll_list_create'),
    path('polls/<int:pk>/', PollDetailView.as_view(), name='poll_detail'),
    path('polls/<int:poll_id>/vote/<int:option_id>/',
         VoteView.as_view(), name='vote'),
    path('polls/<int:poll_id>/results/', PollResultsView.as_view(), name='poll_results'),
    path('polls/<int:poll_id>/delete/', PollDeleteView.as_view(), name='poll_delete'),


]
