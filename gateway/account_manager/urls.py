from gateway.account_manager import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"account_manager", views.AccountManager, basename="account_manager")
urlpatterns = router.urls
