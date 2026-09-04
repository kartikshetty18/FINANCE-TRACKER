"""
URL configuration for finance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('user_home',views.user_home,name='user_home'),
    path('agent_home', views.agent_home, name='agent_home'),
    path('registration',views.registration,name='registration'),
    path('password',views.password,name='password'),
    path('bankTransaction',views.bankTransaction,name='bankTransaction'),
    path('customer/',views.customer,name='customer'),
    path('employee/',views.employee,name='employee'),
    path('loan/',views.loan,name='loan'),
    path('loan_history',views.loan_history,name='loan_history'),
    path('employee_view',views.employee_view,name='employee_view'),
    path('customer_view',views.customer_view,name='customer_view'),
    path('loan_view',views.loan_view,name='loan_view'),
    path('loan_history_view',views.loan_history_view,name='loan_history_view'),
    path('bankTransaction_view',views.bankTransaction_view,name='bankTransaction_view'),
    path('employee_del/<int:pk>', views.employee_del, name='employee_del'),
    path('customer_del/<int:pk>', views.customer_del, name='customer_del'),
    path('loan_del/<int:pk>', views.loan_del, name='loan_del'),
    path('loan_history_del/<int:pk>', views.loan_history_del, name='loan_history_del'),
    path('bankTransaction_del/<int:pk>', views.bankTransaction_del, name='bankTransaction_del'),
    path('forgetpassword',views.forgetpassword,name='forgetpassword'),
    path('resetpassword',views.resetpassword,name='resetpassword'),
    path('otp',views.otp,name='otp'),

    path('cust_wise_collection',views.cust_wise_collection,name='cust_wise_collection'),
    path('total_collection/<str:acc_no>',views.total_collection,name='total_collection'),
    path('datewise_report_admin',views.datewise_report_admin,name='datewise_report_admin'),
    path('loan_report_open',views.loan_report_open,name='loan_report_open'),
    path('loan_report_close',views.loan_report_close,name='loan_report_close'),
    path('loan_report_due',views.loan_report_due,name='loan_report_due'),
    path('loan_report_admin',views.loan_report_admin,name='loan_report_admin'),
    path('approved_loan_view',views.approved_loan_view,name='approved_loan_view'),
    path('loan_history_view_agent',views.loan_history_view_agent,name='loan_history_view_agent'),
    path('update_loan_amount/<str:acc_no>',views.update_loan_amount,name='update_loan_amount'),
    path('approved_transaction',views.approved_transaction,name='approved_transaction'),
    path('employee_edit/<int:pk>',views.employee_edit,name='employee_edit'),
    path('customer_edit/<int:pk>',views.customer_edit,name='customer_edit'),
    path('loan_edit/<int:pk>',views.loan_edit,name='loan_edit'),
    path('loan_view_agent',views.loan_view_agent,name='loan_view_agent'),
    path('loan_history_edit/<int:pk>',views.loan_history_edit,name='loan_history_edit'),
    path('bankTransaction_edit/<int:pk>',views.bankTransaction_edit,name='bankTransaction_edit'),
    #path('approved_transaction/', views.approved_transaction, name='approved_transaction'),
    path('approve_loan/<int:id>/', views.approve_loan, name='approve_loan'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)