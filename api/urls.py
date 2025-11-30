from django.urls import path
from .views import *
from .stats import *
from .statis2 import *
from .marque1 import *
from .statagent import *
from .etatsupport import *
from .filtre import *
from .filtreg import *
from .importdata import*

urlpatterns = [
    path('importerdonneesexcel/', importer_donnees_de_excel, name='importer_donnees_excel'),
    path('donneescollectees/', DonneeCollecteeList.as_view(), name='donnee-collectee-list'), #Ok
    path('agent/', DonneeCollecteeListAgent.as_view(), name='all-collectee-list'),
    path('agent/<int:pk>/', DonneeCollecteeDetailView1.as_view(), name='all-collectee-list1'),
    path('donneescollecteesall/', DonneeCollecteeListAll.as_view(), name='donnee-collectee-list'),
    path('statbyetat/', StatByEtat.as_view(), name='stat-collectee-list'),
    path('statbyetatall/', StatByEtatAll.as_view(), name='stat-collectee-list'),
    path('all/', Allcollecte.as_view(), name='all-collectee-list'),

    path('donneescollectees/<int:pk>/', DonneeCollecteeDetailView.as_view(), name='donnee-collectee-detail'),
    path('collectedata/', DonneeCollecteeCreate.as_view(), name='donnee-collectee-create'),
    path('commune/', CommuneL.as_view(), name='commune-collectee-create'),
    path('commune/<int:pk>/', CommuneDetail.as_view(), name='commune-collectee-detail'),
    path('etat/', EtatListView.as_view(), name='etat'),
    path('visibilite/', VisibiliteListView.as_view(), name='visibilite'),
    path('canal/', CanalListView.as_view(), name='canal'),
    path('marque/', MarqueListView.as_view(), name='marque'),
    path('site/', SiteListView.as_view(), name='site'),
    path('etat/<int:pk>/', EtatListViewD.as_view(), name='etat'),
    path('visibilite/<int:pk>/', VisibiliteListViewD.as_view(), name='visibilite'),
    path('canal/<int:pk>/', CanalListViewD.as_view(), name='canal'),
    path('marque/<int:pk>/', MarqueListViewD.as_view(), name='marque'),
    path('site/<int:pk>/', SiteListViewD.as_view(), name='site'),
    path('supports/', SupportPublicitaireListView.as_view(), name='support-publicitaire-list'),
    path('supports/<int:pk>/', SupportPublicitaireDetailView.as_view(), name= 'support-publicitaire-detail'),
    
    # # Statistiques générales
    path('statagent/<str:start_date>/<str:end_date>/', StatsByAgent.as_view(), name='general-agent'),
    path('deletedata/<str:start_date>/<str:end_date>/', DeleData.as_view(), name='delete-data'),
    path('statagentid/<str:start_date>/<str:end_date>/<int:agent_id>/', StatsByAgent.as_view(), name='general-agents'),
    path('gcollecte/', GTotalCollectedDataView.as_view(), name='general-statistics'), #Ok
    path('collecte/<str:start_date>/<str:end_date>/', TotalCollectedDataView.as_view(), name='statistics-etat'),
    path('collectem/<str:start_date>/<str:end_date>/', GTotalCollectedDataViewM.as_view(), name='statistics-marque'),
    path('filtregeneral/', TotalCollectedDataView.as_view(), name='statistics-marque'),

    # Filtre
    path('fetat/', EtatListViewF.as_view(), name='etat'),
    path('fvisibilite/', VisibiliteListViewF.as_view(), name='visibilite'),
    path('fcanal/', CanalListViewF.as_view(), name='canal'),
    path('fmarque/', MarqueListViewF.as_view(), name='marque'),
    path('fsite/', SiteListViewF.as_view(), name='site'),
    path('fsupports/', SupportPublicitaireListViewF.as_view(), name='support-publicitaire-list'),
    path('fville/', VilleListe.as_view(), name='ville-collectee-app'),
    path('ville/', VilleListeP.as_view(), name='ville-collectee-app'),
    path('ville/<int:pk>/', VilleDetail.as_view(), name='ville-collecteed-app'),
    path('communeapp/', CommuneApp.as_view(), name='commune-collectee-app'),
    path('fcommune/', CommuneApp.as_view(), name='commune-collectee-app'),
    path('fquartier/', QuartierListe.as_view(), name='quartier1'),
    path('quartier/', QuartierCommune.as_view(), name='quartier2'),
    path('quartier/<int:pk>/', QuartierCommuneDetail.as_view(), name='quartier3'),

    path('region/', RegionApp.as_view(), name='region'),
    path('fregion/', RegionAppFiltre.as_view(), name='fregion'),
    path('district/', DistrictApp.as_view(), name='district'),
    path('fdistrict/', DistrictAppFiltre.as_view(), name='fdistrict'),
    path('affectation/', AffectationApp.as_view(), name='affectation'),

    path('dregion/<int:pk>/', RegionAppDetail.as_view(), name='region'),
    path('dfregion/<int:pk>/', RegionAppFiltreDetail.as_view(), name='fregion'),
    path('ddistrict/<int:pk>/', DistrictAppDetail.as_view(), name='district'),
    path('dfdistrict/<int:pk>/', DistrictAppFiltreDetail.as_view(), name='fdistrict'),
    path('daffectation/<int:pk>/', AffectationAppDetail.as_view(), name='affectation'),

    path('village/', VillageApp.as_view(), name='village'),
    path('fvillage/', VillageAppFiltre.as_view(), name='fvillage'),
    path('dvillage/<int:pk>/', VillageAppFiltreDetail.as_view(), name='dvillage'),
    path('quartiersco/', QuartiersByCommuneView.as_view(), name='quartiers_by_commune'),
]

