from unittest.mock import patch



from selenium.webdriver.common.keys import Keys

from base import RecipeBaseFunctionalTest

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By


class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 🥲', body.text)
        
    
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        print('test funcional recipe_search_input_can_find_correct_recipes')
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'

        recipes[0].title = title_needed
        recipes[0].save()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê um campo de busca com o texto "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )

        # Clica neste input e digita o termo de busca
        # para encontrar a receita o título desejado
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # O usuário vê o que estava procurando na página
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )    
    
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        print('test funcional test_recipe_home_page_pagination')
        self.make_recipe_in_batch()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê que tem uma paginação e clica na página 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # Vê que tem mais 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
    
# functional tests authors here

    
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        
        callback(form)
        return form

        
    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Ex.: John')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Write your first name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Ex.: Doe')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_callback(callback)

        
    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Your username')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field must not be empty', form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'Your e-mail')
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('The e-mail must be valid.', form.text)
        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, 'Type your password')
            password2 = self.get_by_placeholder(form, 'Repeat your password')
            password1.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd_Different')
            password2.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Password and password2 must be equal', form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(form, 'Ex.: John').send_keys('First Name')
        self.get_by_placeholder(form, 'Ex.: Doe').send_keys('Last Name')
        self.get_by_placeholder(form, 'Your username').send_keys('my_username')
        self.get_by_placeholder(
            form, 'Your e-mail').send_keys('email@valid.com')
        self.get_by_placeholder(
            form, 'Type your password').send_keys('P@ssw0rd1')
        self.get_by_placeholder(
            form, 'Repeat your password').send_keys('P@ssw0rd1')

        form.submit()

        self.assertIn(
            'Your user is created, please log in.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        
# functional tests for login here    

    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password
        )

        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # Usuário digita seu usuário e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Usuário envia o formulário
        form.submit()

        # Usuário vê a mensagem de login com sucesso e seu nome
        self.assertIn(
            f'Your are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )   
    
    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url +
            reverse('authors:login_create')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )      
        
    def test_form_login_invalid_credentials(self):
        # Usuário abre a página de login
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # Usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # E tenta enviar valores com dados que não correspondem
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys('invalid_user')
        password.send_keys('invalid_password')

        # Envia o formulário
        form.submit()

        # Vê uma mensagem de erro na tela
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )  

# Testes funcionais de ogout 
    
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.get(
            reverse('authors:logout'),
            follow=True
        )

        self.assertIn(
            'Invalid logout request',
            response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'another_user'
            },
            follow=True
        )

        self.assertIn(
            'Invalid logout user',
            response.content.decode('utf-8')
        )

    def test_user_can_logout_successfully(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'my_user'
            },
            follow=True
        )

        self.assertIn(
            'Logged out successfully',
            response.content.decode('utf-8')
        )          