from django.urls import reverse, resolve
from recipes import views
from unittest import skip # funçao para pular os teste

from .test_recipe_base import RecipeTestBase

class RecipeViewsTest(RecipeTestBase):
    def test_recipe_home_views_function_is_corrert(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_views_function_is_corrert(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id':1})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_detail_views_function_is_corrert(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id':1})
        )
        self.assertIs(view.func, views.recipe)
    
    @skip('teste')
    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf-8'))

    # testes populando dados
    def test_recipe_home_template_loads_recipes(self):
        # teste passando parametro para o objeto
        self.make_recipe(author_data={
            'first_name':'joazinho'
        })

        response = self.client.get(reverse('recipes:home'))
        # response_recipes = response.context['recipes']
        # self.assertEqual(response_recipes.first().title, 'Recipe Title')
        content = response.content.decode('utf-8')

        #verificar se a string esta na tela
        response_context_recipes = response.context['recipes']
        self.assertIn('Recipe Title', content)
        self.assertIn('joazinho', content)
        self.assertEqual(len(response_context_recipes), 1)

    @skip('validar novamente o teste')
    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load one recipe'

        self.make_recipe(title=needed_title)
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id':1
                }
            )
        )
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    @skip('teste que tem valor fixo')
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1> No recipes found here </h1>',
            response.content.decode('utf-8')
        )