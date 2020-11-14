from django.contrib import admin
from django.urls import include, path
from weather.views import HomeView

admin.site.site_header = "Web Crawler Admin"
admin.site.site_title = "crawl something!"
admin.site.index_title = "G'day"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(template_name = 'index.html'), name='index'),
    path('weather/', HomeView.as_view(), name='weather'),
    path('apis/', include('apis.urls')),
]
