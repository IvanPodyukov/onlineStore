from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, AccessMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from myauth.models import Dialog, Message


def index(request):
    return render(request, 'myauth/index.html')


class RegisterView(CreateView):
    template_name = 'myauth/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('myauth:main')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        return response


class ChatView(LoginRequiredMixin, AccessMixin, View):
    def get(self, request, pk):
        user1 = get_object_or_404(User, pk=pk)
        user2 = request.user
        if user1 == user2:
            self.handle_no_permission()
        if Dialog.objects.filter(user1=user1, user2=user2).exists():
            dialog = Dialog.objects.get(user1=user1, user2=user2)
        elif Dialog.objects.filter(user2=user1, user1=user2).exists():
            dialog = Dialog.objects.get(user1=user2, user2=user1)
        else:
            dialog = Dialog.objects.create(user1=user1, user2=user2)
        return render(request, 'myauth/chat.html', context={'dialog': dialog})

    def post(self, request, pk):
        user1 = get_object_or_404(User, pk=pk)
        user2 = request.user
        if user1 == user2:
            self.handle_no_permission()
        if Dialog.objects.filter(user1=user1, user2=user2).exists():
            dialog = Dialog.objects.get(user1=user1, user2=user2)
        else:
            dialog = Dialog.objects.get(user1=user2, user2=user1)
        Message.objects.create(sender=user2, content=request.POST['message'], dialog=dialog)
        return redirect(reverse('myauth:chat', kwargs={'pk': pk}))


class ProfileView(DetailView):
    model = User
    template_name = 'myauth/profile.html'
    context_object_name = 'user'


class ProfileEditView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    model = User
    template_name = 'myauth/profile_edit.html'
    context_object_name = 'user'
    fields = 'username', 'first_name', 'last_name', 'email'

    def get_success_url(self):
        return reverse('myauth:profile', kwargs={'pk': self.object.pk})


class ProfileDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    model = User
    success_url = reverse_lazy('myauth:main')
    template_name = 'myauth/profile_confirm_delete.html'
