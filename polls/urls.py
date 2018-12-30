from django.urls import path

from updown.views import AddRatingFromModel
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('new/', views.post_new, name='new'),
    path('<int:pk>/rate/(<object_id>|<score>)', AddRatingFromModel(), {
            'app_label': 'polls',
            'model': 'Choice',
            'field_name': 'rating',
    }, name='like'),
]
