from django.shortcuts import redirect, render, get_object_or_404
from . models import Contact
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.
# def home(request):
#     context = {
#         "contacts" : Contact.objects.all()
#     }
#     return render(request, 'index.html')


# def detail(request, id):
#     context = {
#         'contact':get_object_or_404(contact, pk=id)
#     }
#     return render(request, 'detail.html', context)


@login_required
def search(request):

    print(request.user)
    if request.GET:

        search_term = request.GET['search_term']        
        search_results = Contact.objects.filter(
            Q(name__icontains = search_term) |
            Q(email__icontains = search_term) |
            Q(info__icontains = search_term) |
            Q(phone__icontains = search_term) 
        )

        print(search_results)
        print(search_results.filter(manager = request.user))

        context = {
            "search_term": search_term,
            "contacts" : search_results.filter(manager = request.user)
        }
        
        return render(request, 'search.html', context)
    
    else:
        return redirect('home')


class HomePageView(LoginRequiredMixin, ListView):

    template_name = 'index.html'
    model = Contact
    context_object_name = 'contacts'

    def get_queryset(self):

        contacts = super().get_queryset()
        return contacts.filter(manager = self.request.user)


class ContactDetailView(LoginRequiredMixin, DetailView):

    template_name = 'detail.html'
    model = Contact
    context_object_name = 'contact'


class ContactCreateView(LoginRequiredMixin, CreateView):

    model = Contact
    template_name = 'create.html'
    fields = ['name', 'email', 'phone', 'info', 'gender', 'image']

    def form_valid(self, form):
        
        instance = form.save(commit=False)
        instance.manager = self.request.user
        instance.save()
        messages.success(self.request, 'Your Contact has been created successfully')
        return redirect('home')


class ContactUpdateView(LoginRequiredMixin, UpdateView):

    model = Contact
    template_name = 'update.html'
    fields = ['name', 'email', 'phone', 'info', 'gender', 'image']
    success_url = '/'

    def form_valid(self, form):
        
        instance = form.save()
        messages.success(self.request, 'Your Contact has been updated successfully')
        return redirect('detail', instance.pk)


class ContactDeleteView(LoginRequiredMixin, DeleteView):

    model = Contact
    template_name = 'delete.html'
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request, 'Your contact has been successfully deleted!')
        return super().delete(self, request, *args, **kwargs)

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')


