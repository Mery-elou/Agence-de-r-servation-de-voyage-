
from django.urls import path
from . import views



urlpatterns = [

    path('couples/',views.voyages_couples,name='couples'),
    path('equipes/',views.voyages_equipes,name='equipes'),
    path('familles/',views.voyages_familles,name='familles'),
    path('haj/',views.voyages_Hajs,name='hajs'),
    path('Voyage/<int:id_voyage>',views.detail,name='detail'),
    path('promo/',views.promo,name='promo'),
    
    path('tousvoyages/',views.tousvoyages,name='tousvoyages'),
    path('deletevoyage/<int:id>/',views.DeleteVoyage,name='deletevoyage'),
    path('updatevoyage<int:voyage_id>/',views.update_voyage,name='updatevoyage'),
    path('ajoutervoyage/',views.ajouter_voyage,name='ajoutervoyage'),
    
    path('hotel/',views.hotel,name='hotel'),
    path('deletehotel/<int:id>/',views.Deletehotel,name='deletehotel'),
    path('updatehotel<int:hotel_id>/',views.update_hotel,name='updatehotel'),
    path('ajouterhotel/',views.ajouter_hotel,name='ajouterhotel'),
    
    path('promotion/',views.promotion,name='promotion'),
    path('deletepromo/<int:id>/',views.deletepromo,name='deletepromo'),
    path('updatepromo<int:promo_id>/',views.update_promo,name='updatepromo'),
    path('ajouterpromo/',views.ajouter_promo,name='ajouterpromo'),
    
 
]

