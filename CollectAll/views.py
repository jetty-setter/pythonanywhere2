from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from .forms import CollectionCreate, CollectionItemCreate, CommentForm
from .models import Collection, SiteUser, CollectionItem, Category, Comment


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
	collections = Collection.objects.filter(siteUser=request.user)
	for collection in collections:
		collection.favorite = True
		collection.save()
		request.user.favorite_collections.add(collection)
	return redirect('favorites_list')


def favorites_list(request):
	collections = Collection.objects.filter(siteUser=request.user, favorite=True)
	return render(request, 'CollectAll/favorites_list.html', {'collections': collections})

class CollectionDetailView(generic.DetailView):
    model = Collection
    template_name = 'CollectAll/collection_detail.html'
    context_object_name = 'collection'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection = self.get_object()
        comments = Comment.objects.filter(collection=collection)
        context['comments'] = comments
        return context


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
		form = CollectionItemCreate(initial={'collection': collection})
		print(form.errors)
	context = {'form': form}

	return render(request, 'CollectAll/collectionitem_form.html', context)


class CollectionItemUpdate(LoginRequiredMixin, UpdateView):
	model = CollectionItem
	fields = ['name', 'quantity', 'value', 'notes', 'collectedDate', 'collectionItem_image']


def collectionItem_delete(request, pk):
	collectionItem = get_object_or_404(CollectionItem, pk=pk)
	try:
		collectionItem.delete()
		messages.success(request, (collectionItem.name + " has been deleted"))
	except:
		messages.success(request, (collectionItem.name + " cannot be deleted"))
	return redirect('personal_list')

	return render(request, 'CollectAll/collectionItem_form.html', context)

from django.contrib.auth.decorators import login_required

@login_required
def add_comment(request, pk):
    collection = get_object_or_404(Collection, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.collection = collection
            comment.siteUser = request.user
            comment.comments = form.cleaned_data['comments']  # Assign the comment content from the form
            comment.save()
            return redirect('collection_detail', pk=collection.pk)
    else:
        form = CommentForm()

    return render(request, 'CollectAll/add_comment.html', {'form': form})

@login_required()
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        # Update the comment with the new data
        comment.comments = request.POST['comments']
        comment.save()
        return redirect(reverse('collection_detail', kwargs={'pk': comment.collection.pk}))

    context = {'comment': comment}
    return render(request, 'CollectAll/edit_comment.html', context)




@login_required()
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        collection_pk = comment.collection.pk
        comment.delete()
        return redirect(reverse('collection_detail', kwargs={'pk': collection_pk}))

    context = {'comment': comment}
    return render(request, 'CollectAll/delete_comment.html', context)


