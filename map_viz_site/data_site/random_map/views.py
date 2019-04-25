from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Order

import folium as fm
# Create your views here.

def base_map():
    m = fm.Map([35.6762, 139.6503],
            tiles='CartoDB Positron',
            zoom_start=10)

    return m

def render_map(m):
    m.save(r'C:/Users/reeves/Desktop/test_site/data_site/random_map/static/random_map/map.html')

def test_function(m):
    m.get_root().render()
    m_head = m.get_root().header.render()
    m_body = m.get_root().html.render()
    m_script = m.get_root().script.render()
    return m_head, m_body, m_script

def index(request):
    m = base_map()
    render_map(m)
    return render(request, 'random_map/index.html')
    
