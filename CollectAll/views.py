from .models import Collection, CollectionType, SiteUser, CollectionItem, UserComment, Category
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from .forms import CollectionCreate, CollectionItemCreate
from django.http import HttpResponseRedirect
from django.urls import reverse

def search_collections(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        collections = Collection.objects.filter(name__icontains=searched)
        return render(request, 'CollectAll/search_collections.html', {'searched': searched, "collections": collections})
    else:
        return render(request, 'CollectAll/search_collections.html')


def index(request):
    return render(request, 'CollectAll/index.html')


class CollectionListView(generic.ListView):
    model = Collection
    fields = ['collection.name', 'collection_image']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return HttpResponseRedirect(reverse('collection_list'))

    def get_queryset(self):
        return Collection.objects.filter(private=False).filter(parent=None)
def favorite(request):
    favorite_collections = Collection.objects.filter(favorite=True)
    context = {'favorite_collections': favorite_collections}
    return render(request,'CollectAll/favorite.html', context)

class CollectionDetailView(generic.DetailView):
    model = Collection
    fields = ['collection.name', 'collection_image']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return HttpResponseRedirect(reverse('collection_list'))


class PersonalCollectionListView(LoginRequiredMixin, generic.ListView):
    model = Collection
    template_name = 'CollectAll/personal_list.html'

    def get_queryset(self):
        return Collection.objects.filter(siteUser=self.request.user).filter(parent=None)


class ProfileView(generic.DetailView):
    model = SiteUser
    fields = ['description', 'first_name', 'last_name', 'user_image']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return HttpResponseRedirect(reverse('collection_list'))

    def user_profile(self):
        return self.request.user == SiteUser


def create_collection(request):
    if request.method == 'POST':
        form = CollectionCreate(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personal_list')
    else:
        form = CollectionCreate(initial={"siteUser": request.user})
    return render(request, "CollectAll/collection_form.html", {"form": form})

class ProfileCreate(CreateView):
    model = SiteUser
    fields = ['first_name', 'last_name', 'user_image']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return self.request.user == SiteUser


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = SiteUser
    fields = ['first_name', 'last_name', 'user_image', 'email', 'description']

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.save()
    #     return self.request.user == SiteUser


class CollectionUpdate(LoginRequiredMixin, UpdateView):
    model = Collection
    fields = ['name', 'private', 'favorite', 'notes', 'collectionType', 'collection_image']


def collection_delete(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    try:
        collection.delete()
        messages.success(request, (collection.name + " has been deleted"))
    except:
        messages.success(request, (collection.name + " cannot be deleted"))
    return redirect('personal_list')


def add_to_category(request, item_id, category_id):
    item = CollectionItem.objects.get(pk=item_id)
    category = Category.objects.get(pk=category_id)
    category.items.add(item)
    return redirect('item_detail', item_id)


def add_collection_item(request, pk):
    collection = Collection.objects.get(pk=pk)

    if request.method == 'POST':
        form = CollectionItemCreate(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.collection = collection
            instance.save()
            return HttpResponseRedirect(reverse('collection_detail', args=[collection.pk]))
    else:
        form = CollectionItemCreate()
        print(form.errors)
    context = {'form': form, 'collection': collection}
    return render(request, 'CollectAll/collectionItem_form.html', context)


