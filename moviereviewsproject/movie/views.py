from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

def home(request):
    searchTerm = request.GET.get('searchMovie')

    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    
    else:
        movies = Movie.objects.all()


    return render(request,'home.html',{'searchTerm':searchTerm,'movies':movies})


def about(request):
    return render(request,'about.html',{'name':'Jacobo Montes'})


def statistics_view(request):
    matplotlib.use('Agg') # Permite la generación de gráficos sin necesidad de una interfaz gráfica
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year') # Obtener los años de las películas de la base de datos
    movie_counts_by_year = {} # Crear un diccionario para almacenar la cantidad de películas por año
    
    for year in years: # Contar la cantidad de películas por año
        if year:
            movies_in_year = Movie.objects.filter(year=year) # Filtrar películas por año
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True) # Filtrar películas sin año especificado
            year = "None" # Asignar "None" para años nulos
        count = movies_in_year.count() # Contar el número de películas en ese año
        movie_counts_by_year[year] = count # Almacenar el conteo en el diccionario
    
    bar_width = 0.5 # Ancho de las barras en la gráfica
    bar_spacing = 0.5 # Separación entre las barras
    bar_positions = range(len(movie_counts_by_year)) # Posiciones de las barras

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    # Personalizar la gráfica
    plt.title('Movies per year') # Título de la gráfica
    plt.xlabel('Year') # Etiqueta del eje X
    plt.ylabel('Number of movies') # Etiqueta del eje Y
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90) # Etiquetas del eje X con rotación de 90 grados
    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png') # Guardar la gráfica en formato PNG
    buffer.seek(0) # Mover el puntero al inicio del buffer
    plt.close() # Cerrar la gráfica

    # Convertir la gráfica a base64
    image_png = buffer.getvalue() # Obtener los datos de la imagen en formato PNG
    buffer.close() # Cerrar el buffer
    graphic = base64.b64encode(image_png) # Codificar la imagen en base64
    graphic = graphic.decode('utf-8') # Decodificar la imagen a una cadena de texto

    return render(request, 'statistics.html', {'graphic': graphic}) # Renderizar la plantilla con la gráfica



def genre_statistics_view(request):
    matplotlib.use('Agg') # Permite la generación de gráficos sin necesidad de una interfaz gráfica
    genres = Movie.objects.values_list('genre', flat=True).distinct().order_by('genre') # Obtener los géneros de las películas de la base de datos
    movie_counts_by_genre = {} # Crear un diccionario para almacenar la cantidad de películas por año
    
    for genre in genres: # Contar la cantidad de películas por género
        if genre:
            movies_in_genre = Movie.objects.filter(genre=genre) # Filtrar películas por género
        else:
            movies_in_genre = Movie.objects.filter(genre__isnull=True) # Filtrar películas sin género especificado especificado
            genre = "None" # Asignar "None" para genres nulos
        count = movies_in_genre.count() # Contar el número de películas por género
        movie_counts_by_genre[genre] = count # Almacenar el conteo en el diccionario
    
    bar_width = 0.5 # Ancho de las barras en la gráfica
    bar_spacing = 0.5 # Separación entre las barras
    bar_positions = range(len(movie_counts_by_genre)) # Posiciones de las barras

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')
    # Personalizar la gráfica
    plt.title('Movies per genre') # Título de la gráfica
    plt.xlabel('Genre') # Etiqueta del eje X
    plt.ylabel('Number of movies') # Etiqueta del eje Y
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=90) # Etiquetas del eje X con rotación de 90 grados
    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png') # Guardar la gráfica en formato PNG
    buffer.seek(0) # Mover el puntero al inicio del buffer
    plt.close() # Cerrar la gráfica

    # Convertir la gráfica a base64
    image_png = buffer.getvalue() # Obtener los datos de la imagen en formato PNG
    buffer.close() # Cerrar el buffer
    graphic = base64.b64encode(image_png) # Codificar la imagen en base64
    graphic = graphic.decode('utf-8') # Decodificar la imagen a una cadena de texto

    return render(request, 'genre_statistics.html', {'graphic': graphic}) # Renderizar la plantilla con la gráfica



