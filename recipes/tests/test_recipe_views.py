
from django.urls import resolve, reverse
from recipes import views
from utils.recipes.factory import make_recipe
from unittest.mock import patch

from .test_recipe_base import RecipeTestBase



class RecipeViewsTest(RecipeTestBase):
    def tearDown(self) -> None:
        return super().tearDown()


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
        
    def test_recipe_home_template_loads_recipes(self):
        print('Test recipe home tamplate loads recipes')
       
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
        self.assertEqual(len(response_context_recipes), 1)
    
    def test_recipe_search_uses_correct_view_function(self):
        print('Test search_uses_correct_view_function')
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        print('Test recipe_search_loads_correct_template')
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        print('Test recipe_search_raises_404_if_no_search_term')
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    

    # def test_recipe_search_term_is_on_page_title_and_escaped(self):
    #      url = reverse('recipes:search') + '?q=<Teste>'
    #      response = self.client.get(url)
    #      self.assertIn(
    #          'Search for &quot;&lt;Teste&gt;&quot;',
    #          response.content.decode('utf-8')
    #      )
    
    # def test_recipe_search_can_find_recipe_by_title(self):
    #     print('Test recipe_search_can_find_recipe_by_title')
    #     title1 = 'This is recipe one'
    #     title2 = 'This is recipe two'

    #     recipe1 = self.make_recipe(
    #         slug='one', title=title1, author_data={'username': 'one'}
    #     )
    #     recipe2 = self.make_recipe(
    #         slug='two', title=title2, author_data={'username': 'two'}
    #     )

    #     search_url = reverse('recipes:search')
    #     response1 = self.client.get(f'{search_url}?q={title1}')
    #     response2 = self.client.get(f'{search_url}?q={title2}')
    #     response_both = self.client.get(f'{search_url}?q=this')

    #     self.assertIn(recipe1, response1.context['recipes'])
    #     self.assertNotIn(recipe2, response1.context['recipes'])

    #     self.assertIn(recipe2, response2.context['recipes'])
    #     self.assertNotIn(recipe1, response2.context['recipes'])

    #     self.assertIn(recipe1, response_both.context['recipes'])
    #     self.assertIn(recipe2, response_both.context['recipes'])             