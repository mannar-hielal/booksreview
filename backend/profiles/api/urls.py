from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProfileViewSet,
                    ProfileStatusViewSet,
                    AvatarUpdateViewAPI)

# we still need to specifiy which endpoint we want to use
# profile_list = ProfileViewSet.as_view({'get': 'list'})
# profile_detail = ProfileViewSet.as_view({'get': 'retrieve'})

# initialize router
# router will automatically generate links of endpoints for this viewset
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
# we need basename because we overwritten the get_query method
router.register(r'status', ProfileStatusViewSet, basename='status')

urlpatterns = [
    # path('profiles/', profile_list,
    #      name='profile_list'),
    # path('profiles/<int:pk>/', profile_detail,
    #      name='profile_detail')
    path('', include(router.urls)),
    path('avatar/',AvatarUpdateViewAPI.as_view(), name='avatar_update')
]
