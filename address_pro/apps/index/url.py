from rest_framework.routers import SimpleRouter
from . import views
from django.urls import path

router = SimpleRouter()

# router.register('get_all_store', views.GetAllStoreDataView, 'get_all_store')
# router.register('get_flower_data', views.GetFlowerDataView, 'get_flower_data')
# router.register('get_category', views.GetCategoryView, 'get_category')
# router.register('get_category2', views.GetCategory2View, 'get_category2')

urlpatterns = [
    # path('get_flower_data/', views.GetFlowerDataView.as_view()),

]

urlpatterns += router.urls




