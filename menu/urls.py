from rest_framework.routers import DefaultRouter

from menu import views

app_name = 'menu'

router = DefaultRouter()
router.register(r"dishes", views.DishViewSet, basename="dishes")
router.register(r"cards", views.MenuViewSet, basename="cards")

urlpatterns = router.urls
