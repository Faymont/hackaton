from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse
from django.urls import path, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.static import serve


admin.autodiscover()

urlpatterns = [
    path('api/', include(([
        path('get-csrf-token/', ensure_csrf_cookie(lambda r: HttpResponse('OK')), name='get-csrf-token'),
        path('', include('rest_framework.urls', namespace='rest_framework')),
        path('for_people/', include('apps.for_people.urls', namespace='for_people')),
    ], 'api'), namespace='api')),

    path('for_people_admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ] + staticfiles_urlpatterns() + urlpatterns

if settings.ENVIRONMENT == 'development':
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
