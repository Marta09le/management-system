from django.contrib import messages
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View

from apps.accounts.forms import UserRegisterForm, GroupAddForm
from apps.accounts.models import UserModel, GroupModel, NoteModel


# View for choosing between different lists (users or groups).
class ChooseListView(generic.TemplateView):
    template_name = 'choose_lists.html'


# View for displaying a list of regular users.
class UserListView(generic.ListView):
    model = UserModel
    template_name = 'users_list.html'
    context_object_name = 'users'

    # Filter the queryset to only include non-manager users.
    def get_queryset(self):
        return UserModel.objects.filter(is_manager=False)

    # Add additional context to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of users'
        context['button_label'] = 'Create user'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or (request.user.is_authenticated and not request.user.is_manager):
            messages.error(request, "You don't have permission")
            return redirect('error')
        return super().dispatch(request, *args, **kwargs)


# View for displaying a list of managers.
class ManagerListView(generic.ListView):
    model = UserModel
    template_name = 'users_list.html'
    context_object_name = 'users'

    # Filter the queryset to only include manager users.
    def get_queryset(self):
        return UserModel.objects.filter(is_manager=True)

    # Add additional context to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of managers'
        context['button_label'] = 'Create manager'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_manager:
            messages.error(request, "You don't have permission")
            return redirect('error')
        return super().dispatch(request, *args, **kwargs)


# View for updating a user's information.
class CustomUpdateView(generic.UpdateView):
    model = UserModel
    form_class = UserRegisterForm
    template_name = 'edit_user.html'
    success_url = reverse_lazy('user-list')

    # Check permissions before allowing the user to edit.
    def dispatch(self, request, *args, **kwargs):
        user_to_edit = get_object_or_404(UserModel, pk=kwargs['pk'])
        if not request.user.is_authenticated or (not request.user.is_manager and request.user != user_to_edit):
            messages.error(request, "You don't have permission to edit this profile.")
            return redirect('error')
        return super().dispatch(request, *args, **kwargs)


# View for deleting a user.
class CustomDeleteView(generic.DeleteView):
    model = UserModel
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('user-list')

    # Add additional context to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user'] = True
        return context

    # Check permissions before allowing the user to delete.
    def dispatch(self, request, *args, **kwargs):
        user_to_edit = get_object_or_404(UserModel, pk=kwargs['pk'])
        if not request.user.is_authenticated or (not request.user.is_manager and request.user != user_to_edit):
            messages.error(request, "You don't have permission to edit this profile.")
            return redirect('error')
        return super().dispatch(request, *args, **kwargs)


#  ===========  REST URL METHOD  ===========

# View for displaying a list of groups.
class GroupListView(generic.ListView):
    model = GroupModel
    template_name = 'groups_list.html'
    context_object_name = 'groups'


# View for creating a new group.
class GroupCreateView(generic.CreateView):
    model = GroupModel
    form_class = GroupAddForm
    template_name = "edit_event.html"
    success_url = reverse_lazy('group-list')

    # Add additional context to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create event'
        context['button_label'] = 'Create'
        return context


# View for updating a group's information.
class GroupUpdateView(generic.UpdateView):
    model = GroupModel
    form_class = GroupAddForm
    template_name = 'edit_event.html'
    success_url = reverse_lazy('group-list')

    # Add additional context to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit event'
        context['button_label'] = 'Save changes'
        context['notes'] = NoteModel.objects.all()
        return context

    # Check permissions before allowing the user to edit.
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You don't have permission")
            return redirect('error')
        return super().dispatch(request, *args, **kwargs)


# View for deleting a group.
class GroupDeleteView(generic.DeleteView):
    model = GroupModel
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('group-list')

    # Add additional context to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user'] = False
        return context

    # Check permissions and group membership before allowing deletion.
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_manager:
            messages.error(request, "You don't have permission")
            return redirect('error')
        return super().dispatch(request, *args, **kwargs)

    # Prevent deletion of groups with members.
    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "This group cannot be deleted because it is used by other objects.")
            return redirect('some_view')


# # View for displaying an error message.
class ErrorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'error.html', {})


#   ===========  REST HTTP METHOD  ===========

# class EventView(View):
#     template_list = 'groups_list.html'
#     template_edit = 'edit_event.html'
#     template_delete = 'confirm_delete.html'
#     success_url = reverse_lazy('user-list')
#
#     def get(self, request, *args, **kwargs):
#         if 'id' in kwargs:
#             group = get_object_or_404(GroupModel, pk=kwargs['id'])
#             form = GroupAddForm(instance=group)
#             return render(request, self.template_edit, {'form': form, 'group': group})
#
#         groups = GroupModel.objects.all()
#         return render(request, self.template_list, {'groups': groups})
#
#     def post(self, request, *args, **kwargs):
#         if 'id' in kwargs:
#             group = get_object_or_404(GroupModel, pk=kwargs['id'])
#             form = GroupAddForm(request.POST, instance=group)
#         else:
#             form = GroupAddForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             return redirect(self.success_url)
#         return render(request, self.template_edit, {'form': form})
#
#     def delete(self, request, *args, **kwargs):
#         group = get_object_or_404(GroupModel, pk=kwargs['id'])
#         try:
#             group.delete()
#             return redirect(self.success_url)
#         except ProtectedError:
#             messages.error(request, "This group cannot be deleted because it is used by other objects.")
#             return redirect('some_view')
#
#     def patch(self, request, *args, **kwargs):
#         if 'id' in kwargs:
#             group = get_object_or_404(GroupModel, pk=kwargs['id'])
#             form = GroupAddForm(request.POST, instance=group)
#         else:
#             return JsonResponse({'error': 'Invalid request'}, status=400)
#
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'message': 'Group updated successfully.'}, status=200)
#
#         return JsonResponse({'error': 'Invalid data'}, status=400)


