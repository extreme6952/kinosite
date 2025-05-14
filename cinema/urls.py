from django.urls import path
from . import views



urlpatterns = [
    path('',views.SeriesCinemaListView.as_view(),name='list_series'),
    path('detail-series/<int:pk>/<slug:slug>/',views.SeriesDetailView.as_view(),name='series_detail'),
    path('list-series-user/',views.SeriesUserListView.as_view(),name='list_user_series'),
    path('add-series-user/',views.SeriesAddFormView.as_view(),name='add_series_user'),
    path('delete-series/<pk>',views.DeleteSeriesUser.as_view(),name="delete_series"),
    path('add-season-to-series/<int:pk>/',views.AddSeasonSeriesView.as_view(),name='add_season_user_series'),
    path('video-create/<model_name>/content/<int:season_id>/create/',views.VideoSeriesSeasonCreateUpdateView.as_view(),
         name='content_video_create'),
    path('video-update/<model_name>/content/<int:season_id>/<int:id>/update/',views.VideoSeriesSeasonCreateUpdateView.as_view(),
         name='content_video_update'),
    path('season-series/<int:season_id>/',views.SeasonVideoView.as_view(),name='series_season_user'),
    path('delete-video/<int:id>/delete/',views.DeleteVideoSeriesView.as_view(),name='delete_video_season_series'),
    path('raiting-series/<int:series_id>/',views.AddCommentRatingForm.as_view(),name='add_raitng_series')
]
