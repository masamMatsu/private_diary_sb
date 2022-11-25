from django.urls import path

from . import views


app_name = 'diary'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),

    path('diary-list/', views.DiaryListView.as_view(), name="diary_list"),
    path('diary-detail/<int:pk>/', views.DiaryDetailView.as_view(), name="diary_detail"),
    path('diary-create/', views.DiaryCreateView.as_view(), name="diary_create"),
    path('diary-update/<int:pk>/', views.DiaryUpdateView.as_view(), name="diary_update"),
    path('diary-delete/<int:pk>/', views.DiaryDeleteView.as_view(), name="diary_delete"),

    path('sukashi-timeline/', views.SukashiTimelineView.as_view(), name="sukashi_timeline"),
    path('sukashi-list/', views.SukashiList.as_view(), name="sukashi_list"),
    path('sukashi-detail/<int:pk>/', views.SukashiDetailView.as_view(), name="sukashi_detail"),
    path('sukashi-create/', views.SukashiCreateView.as_view(), name="sukashi_create"),
    path('sukashi-update/<int:pk>/', views.SukashiUpdateView.as_view(), name="sukashi_update"),
    path('sukashi-delete/<int:pk>/', views.SukashiDeleteView.as_view(), name="sukashi_delete"),
    path('sukashi-rarelist/', views.SukashiRareListView.as_view(), name="sukashi_rarelist"),
]
