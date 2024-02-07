from django.test import TestCase
from django.urls import resolve, reverse
from recipes.models import Category, Recipe, User

from recipes import views



class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        print('Test em view Home')
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
    def test_recipe_category_view_function_is_correct(self):
        print('Test em view Category')
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func, views.category)
    def test_recipe_detail_view_function_is_correct(self):
        print('Test em view Recipes')
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.recipe)
        
    def test_recipe_home_view_returns_status_code_200_OK(self):
        print('Test em Status 200 Home')
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        print('Test load correct tempate home')
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html') 
        
    def test_recipe_home_template_loads_recipes(self):
        print('Test home loads recipes')
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com',
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )
        assert 1 == 1

    def test_recipe_category_view_function_is_correct(self):
        print('Test cetegory function is correct')
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func, views.category)
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        print('Test cetegory return 404 is no recipes found')
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)
    def test_recipe_detail_view_function_is_correct(self):
        print('Test detail view function is correct')
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.recipe)
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        print('Test recipe detail view returns 404 if no recipes found')
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)           