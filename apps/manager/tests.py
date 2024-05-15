from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse

from apps.accounts.models import UserModel, GroupModel


class UserListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('user-list')

        non_manager_user = UserModel.objects.create(email='nonmanager@example.com', is_manager=False)
        non_manager_user.set_password('test123')
        non_manager_user.save()

        manager_user = UserModel.objects.create(email='manager@example.com', is_manager=True)
        manager_user.set_password('test123')
        manager_user.save()

    def test_access_for_non_authenticated_users(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_access_for_non_manager(self):
        self.client.login(email='nonmanager@example.com', password='test123')
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_access_for_manager(self):
        self.client.login(email='manager@example.com', password='test123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_queryset_excludes_managers(self):
        self.client.login(email='manager@example.com', password='test123')
        response = self.client.get(self.url)
        self.assertNotIn('manager@example.com', [user.email for user in response.context['users']])

    def test_context_data(self):
        self.client.login(email='manager@example.com', password='test123')
        response = self.client.get(self.url)
        self.assertEqual(response.context['title'], 'List of users')
        self.assertEqual(response.context['button_label'], 'Create user')


class CustomUpdateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        UserModel = get_user_model()

        self.manager_user = UserModel.objects.create(email='manager@example.com', is_manager=True)
        self.manager_user.set_password('test123')
        self.manager_user.save()

        self.normal_user = UserModel.objects.create(email='normal@example.com', is_manager=False)
        self.normal_user.set_password('test123')
        self.normal_user.save()

        self.update_url = reverse('user-edit', kwargs={'pk': self.normal_user.pk})

    def test_access_for_unauthenticated_users(self):
        response = self.client.get(self.update_url)
        self.assertNotEqual(response.status_code, 200)

    def test_access_for_unauthorized_user(self):
        self.client.login(email='normal@example.com', password='test123')
        unauthorized_update_url = reverse('user-edit', kwargs={'pk': self.manager_user.pk})
        response = self.client.get(unauthorized_update_url)
        self.assertNotEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "You don't have permission to edit this profile.")

    def test_access_for_authorized_user(self):
        self.client.login(email='manager@example.com', password='test123')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)


class CustomDeleteViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        UserModel = get_user_model()

        self.manager_user = UserModel.objects.create(email='manager@example.com', is_manager=True)
        self.manager_user.set_password('test123')
        self.manager_user.save()

        self.normal_user = UserModel.objects.create(email='normal@example.com', is_manager=False)
        self.normal_user.set_password('test123')
        self.normal_user.save()

        self.delete_url = reverse('user-delete', kwargs={'pk': self.normal_user.pk})

    def test_access_for_unauthenticated_users(self):
        response = self.client.get(self.delete_url)
        self.assertNotEqual(response.status_code, 200)

    def test_access_for_unauthorized_user(self):
        self.client.login(email='normal@example.com', password='test123')
        unauthorized_delete_url = reverse('user-delete', kwargs={'pk': self.manager_user.pk})
        response = self.client.get(unauthorized_delete_url)
        self.assertNotEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "You don't have permission to edit this profile.")

    def test_access_for_authorized_user(self):
        self.client.login(email='manager@example.com', password='test123')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)

    def test_delete_functionality(self):
        self.client.login(email='manager@example.com', password='test123')
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, reverse('user-list'))
        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(pk=self.normal_user.pk)


class GroupListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('group-list')

        GroupModel.objects.create(name='Group 1', description='Test Group 1')
        GroupModel.objects.create(name='Group 2', description='Test Group 2')

    def test_group_list_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'groups_list.html')

        groups_in_context = response.context['groups']
        self.assertEqual(len(groups_in_context), 2)
        self.assertEqual(groups_in_context[0].name, 'Group 1')
        self.assertEqual(groups_in_context[1].name, 'Group 2')


