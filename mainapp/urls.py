from django.urls import path

from mainapp.views import ClientCreateView, CSVUploadView, ClientCSVDataView


urlpatterns = [
    path('get_clients/', ClientCreateView.as_view()),
    path('post_csv/', CSVUploadView.as_view()),
    path('get_data/', ClientCSVDataView.as_view())
]
