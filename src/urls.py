from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Bank API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('accounts.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', schema_view),
    url(r'^api-token-auth/', obtain_jwt_token),
]
