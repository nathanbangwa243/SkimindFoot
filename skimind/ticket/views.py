from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

# Create your views here.
import psycopg2
import sqlite3

#from ..skimindmaster.setup import ski_usecases
from skimind.skimindmaster.setup import ski_usecases

#with psycopg2._connect()

with sqlite3.connect("../../skimind.db") as conn:
    response = ski_usecases.sort_home_view(conn)

#with psycopg2.connect(database="skimind",user="jeanluc",password="MotDePasse") as conn:
#    response = ski_usecases.sort_home_view(conn)


class HomeView(View):

    def get(self, request):
        return HttpResponse(response)