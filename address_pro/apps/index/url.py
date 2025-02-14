from rest_framework.routers import SimpleRouter
from . import views
from django.urls import path

router = SimpleRouter()

router.register('get_login_img', views.GetLoginImgView, 'get_login_img')
router.register('juese', views.JueSeView, 'juese')
router.register('user_info', views.GetUserInfoView, 'user_info')
router.register('get_all_order', views.GetAllOrderView, 'get_all_order')
router.register('get_order', views.GetUserOrderView, 'get_order')
router.register('get_common_user', views.GetAllCommonUserView, 'get_common_user')
router.register('get_one_order', views.GetOneOrderView, 'get_one_order')
router.register('get_null_order', views.NullOrderView, 'get_null_order')
router.register('get_order_type', views.GetOrderTypeView, 'get_order_type')
router.register('get_update_order', views.GetUpdateOrderView, 'get_update_order')
router.register('get_all_service_type', views.GetAllServiceTypeView, 'get_all_service_type')
router.register('get_all_address', views.GetAllAddressView, 'get_all_address')
router.register('get_all_service', views.GetAllServiceView, 'get_all_service')


urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('search_address/', views.SearchAddressView.as_view()),
    path('get_add_order/', views.GetDayAddOrderView.as_view()),
    path('get_complete_order/', views.GetDayCompleteOrderView.as_view()),
    path('get_juese_fenbu/', views.GetJueSeView.as_view()),
    path('get_order_state/', views.GetOrderStateView.as_view()),
    path('create_order/', views.CreateOrderView.as_view()),
    path('start_order/', views.StartOrderView.as_view()),
    path('end_order/', views.EndOrderView.as_view()),
    path('update_order/', views.UpdateOrderView.as_view()),
    path('pai_update_order/', views.PaiUpdateOrderView.as_view()),
    path('get_max/', views.GetMaxView.as_view()),
    path('confirm_order/', views.ConfirmOrderView.as_view()),
    path('get_service/', views.GetServiceView.as_view()),
    path('update_service_type/', views.UpdateServiceTypeView.as_view()),
    path('create_service_type/', views.CreateServiceTypeView.as_view()),
    path('create_new_service/', views.CreateNewServiceView.as_view()),
    path('delete_service/', views.DeleteView.as_view()),
    path('delete_order/', views.DeleteOrderView.as_view()),


]

urlpatterns += router.urls




