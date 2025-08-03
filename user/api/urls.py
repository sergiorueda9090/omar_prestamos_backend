from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .view import create_user, update_user, get_user, delete_user, get_users, get_user_info, get_users_filter

urlpatterns = [
    path('api/token/',                      TokenObtainPairView.as_view(),      name='token_obtain_pair'),
    path('api/token/refresh/',              TokenRefreshView.as_view(),         name='token_refresh'),
    path('api/createuser/',                  create_user,                       name="create_user"),
    path('api/updateuser/<int:user_id>',    update_user,                        name="update_user"),
    path('api/getuser/<int:user_id>',       get_user,                           name="get_user"),
    path('api/getusers/',                   get_users,                          name="get_user"),
     path('api/getusersfilter/',            get_users_filter,                   name="get_users_filter"),
    path('api/delete/<int:user_id>',        delete_user,                        name='delete_user'),
    path('api/infouser/',                   get_user_info,                      name='get_user_info'),
]