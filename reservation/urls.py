from django.urls import include, path

from Voyages.models import Voyages
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.Logout, name='log_out'),
    path('updateProfil/',views.ClientupdateProfil,name='updateclient'),
    path('add_to_cart/<int:id_voyage>/',views.add_to_Cart,name='add_to_cart'),
    path('panie/',views.panier,name='panier'),
    path('reser/',views.reservation,name='reservation'),
    path('DeleteVoyageCart/<int:id>/',views.DeleteVoyageCart,name='deleteCart'),
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('payement/',views.payment,name='payment'),
    path('payementsuccess/',views.payment_success,name='payment_success'),
    path('payementcancel/',views.payment_cancel,name='payment_cancel'),
    path('signupadmin/', views.signupadmin, name='signupadmin'),
    path('dashboardAdmin/',views.dashboardAdmin,name='dashboardAdmin'),
    path('clients/',views.clients,name='clients'),
    path('tousreser/',views.tousreservation,name='tousreservation'),
    path('deleteclient/<int:id>/',views.Deleteclient,name='deleteclient'),
    path('deletereservation/<int:id>/',views.Deletereservation,name='deletereservation'),
    path('notification/',views.notification,name='notification'),
    path('addnotification/<int:user_id>/',views.notify_user_about_upcoming_voyage,name='notfier'),
    path('deletenotif/<int:id>',views.deletenotif,name='deletenotif'),
    path('readnotif/<int:id>/',views.mark_notifications_as_read,name='read'),
    path('deletefavoris/<int:id>/',views.deletefavoris,name='deletefavoris'),
    path('favoris/',views.favoris,name='favoris'),
    path('ajoutfavoris/<int:voyage_id>/',views.toggle_favorite,name='ajouterfavoris'),
    path('updateA/<int:id>',views.updateAdulte,name='update'),
    path('updateE/<int:id>',views.updateEnfants,name='updateE'),
    path('contacter/',views.contacter,name='contacter'),
    path('deletecontact/<int:id>',views.Deletecontact,name='deletecontact'),
    path('readc/<int:id>/',views.mark__as_read,name='readc'),
    path('cantact/',views.contact,name='contact'),
    path('forgot_password/',views.forgot_password, name='forgot_password') ,
    path('update_password/<str:token>/<str:uid>/', views.update_password, name='update_password'),
    path('com/',views.com,name="com"),
   
]

# from django.urls import reverse

# # Update this line in your code
# url = reverse('add_to_cart', kwargs={'id_voyage': Voyages.id})