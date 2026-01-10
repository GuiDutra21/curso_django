from django.contrib import admin
from django.urls import path, include
from core import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'editoras',views.EditoraViewSet)
router.register(r'autores', views.AutoresViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('teste/',views.teste),
    path('categorias-class/',views.CategoriaView.as_view()),
    path('categorias-class/<int:id>/',views.CategoriaView.as_view()),
    path('categorias-apiview/',views.CategoriasList.as_view()),
    path('categorias-apiview/<int:id>/',views.CategoriaDetail.as_view()),
    path('categorias-generics/',views.CategoriasListGeneric.as_view()),
    path('categorias-generics/<int:id>/',views.CategoriasDetailGeneric.as_view()),
    path('',include(router.urls)) # Essa linha já inclui TODAS as ViewSets registradas no router
]
