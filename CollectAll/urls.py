from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('collection_list/', views.CollectionListView.as_view(), name='collection_list'),
	path('collection_detail/<int:pk>/', views.CollectionDetailView.as_view(), name='collection_detail'),
	path('personal_list/', views.PersonalCollectionListView.as_view(), name='personal_list'),
	path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
	path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
	path('collection/create/', views.create_collection, name='collection_create'),
	path('collection/<int:pk>/update/', views.CollectionUpdate.as_view(), name='collection_update'),
	path('collection/<int:pk>/delete/', views.collection_delete, name='collection_delete'),
	path('search_collections/', views.search_collections, name='search_collections'),
	path('collectionItem/create/<int:pk>/', views.add_collection_item, name='add_collection_item'),
	path('favorite/', views.favorite, name='favorite'),
]
