from django.db import router
from rest_framework import urlpatterns
from wishlists.views import WishlistsViewSet
from rest_framework.routers import DefaultRouter

app_name = 'wishlists'

router = DefaultRouter()
router.register('', WishlistsViewSet, basename='wishlist')
urlpatterns = router.urls
