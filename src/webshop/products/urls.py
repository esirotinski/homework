from products.views import ProductsViewSet
from rest_framework.routers import DefaultRouter

app_name = 'products'

router = DefaultRouter()
router.register('', ProductsViewSet, basename='product')
urlpatterns = router.urls
