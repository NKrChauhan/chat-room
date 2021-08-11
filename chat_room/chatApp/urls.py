from django.urls import path
from .views import home,InboxView,ThreadView

app_name = 'chat_app'

urlpatterns = [
    path('',home,name='home'),
    path('thread/<username>/',ThreadView.as_view(),name='threads'),
    path('inbox/',InboxView.as_view(),name='inbox'),
]
