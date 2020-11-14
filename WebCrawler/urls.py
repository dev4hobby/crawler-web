from django.contrib import admin
from django.urls import include, path
from finder.views import HomeView

admin.site.site_header = "Web Crawler Admin"
admin.site.site_title = "crawl something!"
admin.site.index_title = "G'day"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(template_name = 'index.html'), name='finder'),
    path('finder/', HomeView.as_view(), name='finder'),
    path('apis/', include('apis.urls')),
]
