from django.urls import path
from . import views

urlpatterns = [
	path('', views.render_home, name = "home"),
	path('login', views.render_home, name = "home"),
	path('sign_up', views.sign_up, name = "sign_up_page"),
	path('logout', views.logout_user, name = "logout"),
	path('transact', views.make_transaction, name = "transaction_executor"),
	path('statements', views.get_statement, name = "transactions_test")
	]
