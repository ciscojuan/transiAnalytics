from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.transform import factor_cmap
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from math import pi
import pandas as pd
from pprint import pprint
from bokeh.palettes import Spectral6
from bokeh.models.tools import HoverTool


def index(request):
    x = [i for i in range(10)]
    x2 = [i ** 2 for i in range(10)]
    x3 = [i ** 3 for i in range(10)]
    title_ = 'Y = f(x) = x^2'

    plot = figure(title=title_, x_axis_label='Indep.', y_axis_label='Dep')

    plot.line(x, x2, legend='x2', line_width=2, line_color="#666699")
    plot.line(x, x3, legend='x3', line_width=2, line_color='#31B404')
    plot.sizing_mode = 'scale_width'

    bars_ = bars()
    pie_ = pie()
    script, div = components(plot, CDN)
    script_bar, div_bar = components(bars_, CDN)
    script_pie, div_pie = components(pie_, CDN)
    data = {'user_name': 'Camilo',
            'scritp_bar': script_bar,
            'div_bar': div_bar,
            'scritp_': script,
            'div_': div,
            'scritp_pie': script_pie,
            'div_pie': div_pie,
            }
    return render(request, 'analytics/index.html', data)


def bars():
    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    years = ['2015', '2016', '2017']

    data = {'fruits': fruits,
            '2015': [2, 1, 4, 3, 2, 4],
            '2016': [5, 3, 3, 2, 4, 6],
            '2017': [3, 2, 4, 4, 5, 3]}

    palette = ["#c9d9d3", "#718dbf", "#e84d60"]

    # this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
    x = [(fruit, year) for fruit in fruits for year in years]
    counts = sum(zip(data['2015'], data['2016'], data['2017']), ())  # like an hstack

    source = ColumnDataSource(data=dict(x=x, counts=counts))

    p = figure(x_range=FactorRange(*x), title="Fruit Counts by Year",
               toolbar_location=None, tools="")

    p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
           fill_color=factor_cmap('x', palette=palette, factors=years, start=1, end=2))

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.sizing_mode = 'scale_width'
    return p


def pie():
    x = {
        'United States': 157,
        'United Kingdom': 93,
        'Japan': 89
    }

    data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'country'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = Category20c[len(x)]

    p = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
               tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='country', source=data)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    return p


def crashesbyGender(request):
    df = pd.read_excel('analytics/datasets/lesiones-accidentes-transito-2018.xlsx')
    grouped = df.groupby('Sexo')[['Cantidad']].count()
    pprint(df['Sexo'].size)
    pprint(grouped)
    source = ColumnDataSource(grouped)
    genders = source.data['Sexo'].tolist()
    p = figure(x_range=genders)
    color_map = factor_cmap(field_name='Sexo', palette=Spectral6, factors=genders)
    p.vbar(x='Sexo', top='Cantidad', source=source, width=0.70, color=color_map, legend="Sexo")
    p.title.text = 'Accidentes de Transito'
    p.xaxis.axis_label = 'Genero'
    p.yaxis.axis_label = 'Cantidad'

    hover = HoverTool()
    hover.tooltips = [
        ("Edad / Escolaridad / Estado civil", "@Edad / @Escolaridad / @Estado_civil ")]

    hover.mode = 'vline'
    p.add_tools(hover)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = 150
    p.legend.orientation = "vertical"
    p.legend.location = "top_right"
    p.sizing_mode = 'scale_width'
    p.height = 300

    script_gender, div_gender = components(p, CDN)
    data = {'script_gender': script_gender,
            'div_gender': div_gender}
    return render(request, 'analytics/crashesbyGender.html', data)

def diesbyGender(request):
    df = pd.read_excel('analytics/datasets/homicidios-accidentes-transito-2018_1.xls')
    grouped = df.groupby('Sexo')[['Cantidad']].count()
    pprint(df['Sexo'].size)
    pprint(grouped)
    source = ColumnDataSource(grouped)
    genders = source.data['Sexo'].tolist()
    p = figure(x_range=genders)
    color_map = factor_cmap(field_name='Sexo', palette=Spectral6, factors=genders)
    p.vbar(x='Sexo', top='Cantidad', source=source, width=0.70, color=color_map, legend="Sexo")
    p.title.text = 'Homicidios Accidentes de Transito'
    p.xaxis.axis_label = 'Genero'
    p.yaxis.axis_label = 'Cantidad'

    hover = HoverTool()
    hover.tooltips = [
        ("Edad / Escolaridad / Estado civil", "@Edad / @Escolaridad / @Estado_civil ")]

    hover.mode = 'vline'
    p.add_tools(hover)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = 150
    p.legend.orientation = "vertical"
    p.legend.location = "top_right"
    p.sizing_mode = 'scale_width'
    
    script_gender, div_gender = components(p, CDN)
    data = {'script_gender': script_gender,
            'div_gender': div_gender}
    return render(request, 'analytics/diesbyGender.html', data)

def crashesbymovilKind(request):

        df = pd.read_excel('analytics/datasets/lesiones-accidentes-transito-2018.xlsx')

        grouped = df.groupby('Movil Victima')['Cantidad', 'Edad', 'Sexo', 'Estado civil'].sum()

        print(grouped)

        source = ColumnDataSource(grouped)
        countries = source.data['Movil Victima'].tolist()
        p = figure(x_range=countries)

        color_map = factor_cmap(field_name='Movil Victima', palette=Spectral6, factors=countries)

        p.vbar(x='Movil Victima', top='Cantidad', source=source, width=0.70, color=color_map ,legend="Movil Victima")

        p.title.text ='Mortalidad en Accidentes de Transito'
        p.xaxis.axis_label = 'Estado Victima'
        p.yaxis.axis_label = 'Cantidad'

        hover = HoverTool()
        hover.tooltips = [
        ("Edad / Escolaridad / Estado civil", "@Edad / @Escolaridad / @Estado_civil ")]

        hover.mode = 'vline'

        p.add_tools(hover)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.y_range.end = 150
        p.legend.orientation = "vertical"
        p.legend.location = "top_right"

        script_gender, div_gender = components(p, CDN)
        data = {'script_gender': script_gender,
            'div_gender': div_gender}

        return render(request, 'analytics/crashesbymovilKind.html', data)

def diesbymovilKind(request):

        df = pd.read_excel('analytics\datasets\homicidios-accidentes-transito-2018_1.xls')

        grouped = df.groupby('Movil Victima')['Cantidad', 'Edad', 'Sexo', 'Estado civil'].sum()

        print(grouped)

        source = ColumnDataSource(grouped)
        countries = source.data['Movil Victima'].tolist()
        p = figure(x_range=countries)

        color_map = factor_cmap(field_name='Movil Victima', palette=Spectral6, factors=countries)

        p.vbar(x='Movil Victima', top='Cantidad', source=source, width=0.70, color=color_map ,legend="Movil Victima")

        p.title.text ='Mortalidad en Accidentes de Transito'
        p.xaxis.axis_label = 'Estado Victima'
        p.yaxis.axis_label = 'Cantidad'

        hover = HoverTool()
        hover.tooltips = [
        ("Edad / Escolaridad / Estado civil", "@Edad / @Escolaridad / @Estado_civil ")]

        hover.mode = 'vline'

        p.add_tools(hover)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.y_range.end = 150
        p.legend.orientation = "vertical"
        p.legend.location = "top_right"

        dies_ = diesbymovilKind_Agresor()

        script_gender, div_gender = components(p, CDN)
        script_dies_Agresor, div_dies_Agresor = components(dies_, CDN)
        

        data = {
        'user_name': 'Camilo',
        'script_gender': script_gender,
        'div_gender': div_gender,
        'script_dies_Agresor': script_dies_Agresor,
        'div_dies_Agresor': div_dies_Agresor,
        }

        return render(request, 'analytics/diesbymovilKind.html', data)

def diesbymovilKind_Agresor():

        df = pd.read_excel('analytics\datasets\homicidios-accidentes-transito-2018_1.xls')

        grouped = df.groupby('Movil Agresor')['Cantidad', 'Edad', 'Sexo', 'Movil Victima'].sum()

        print(grouped)

        source = ColumnDataSource(grouped)
        countries = source.data['Movil Agresor'].tolist()
        p = figure(x_range=countries)

        color_map = factor_cmap(field_name='Movil Agresor', palette=Spectral6, factors=countries)

        p.vbar(x='Movil Agresor', top='Cantidad', source=source, width=0.70, color=color_map ,legend="Movil Agresor")

        p.title.text ='Mortalidad en Accidentes de Transito'
        p.xaxis.axis_label = 'Estado Agresor'
        p.yaxis.axis_label = 'Cantidad'

        hover = HoverTool()
        hover.tooltips = [
        ("Edad / Escolaridad / Estado civil", "@Edad / @Escolaridad / @Estado_civil ")]

        hover.mode = 'vline'

        p.add_tools(hover)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.y_range.end = 150
        p.legend.orientation = "vertical"
        p.legend.location = "top_right"

        return p

def diesByEscolaridad(request):
        df = pd.read_excel('analytics\datasets\homicidios-accidentes-transito-2018_1.xls')

        grouped = df.groupby('Escolaridad')['Cantidad'].sum()
        grouped *100

        print(grouped)

        data = pd.Series(grouped).reset_index(name='value').rename(columns={'index':'Escolaridad'})
        data['angle'] = data['value']/data['value'].sum() * 2*pi
        data['color'] = Category20c[len(grouped)]

        p = figure(plot_height=350, title="Escolaridad", toolbar_location=None,
                tools="hover", tooltips="Escolaridad: @value", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='Escolaridad', source=data)

        p.axis.axis_label=None
        p.axis.visible=False
        p.grid.grid_line_color = None

        script_gender, div_gender = components(p, CDN)
        data = {'script_gender': script_gender,
            'div_gender': div_gender}

        return render(request, 'analytics/diesByEscolaridad.html', data)

def crashesByEscolaridad(request):
        df = pd.read_excel('analytics\datasets\lesiones-accidentes-transito-2018.xlsx')

        grouped = df.groupby('Escolaridad')['Cantidad'].sum()
        grouped *100

        print(grouped)

        data = pd.Series(grouped).reset_index(name='value').rename(columns={'index':'Escolaridad'})
        data['angle'] = data['value']/data['value'].sum() * 2*pi
        data['color'] = Category20c[len(grouped)]

        p = figure(plot_height=350, title="Escolaridad", toolbar_location=None,
                tools="hover", tooltips="Escolaridad: @value", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='Escolaridad', source=data)

        p.axis.axis_label=None
        p.axis.visible=False
        p.grid.grid_line_color = None

        script_gender, div_gender = components(p, CDN)
        data = {'script_gender': script_gender,
            'div_gender': div_gender}

        return render(request, 'analytics/crashesByEscolaridad.html', data)

def crashesbyEdad(request):
        df = pd.read_excel('analytics\datasets\lesiones-accidentes-transito-2018.xlsx')

        grouped = df.groupby('Edad')['Cantidad', 'Sexo'].sum()
        print(grouped)

        source = ColumnDataSource(grouped)
        countries = source.data['Edad'].tolist()
        p = figure(x_range=countries)

        color_map = factor_cmap(field_name='Edad', palette=Spectral6, factors=countries)
        p.vbar(x='Edad', top='Cantidad', source=source, width=0.70, color=color_map ,legend="Edad")

        p.title.text ='Mortalidad en Accidentes de Transito'
        p.xaxis.axis_label = 'Edad'
        p.yaxis.axis_label = 'Cantidad'

        hover = HoverTool()
        hover.tooltips = [
        ("Edad :", "@Edad  ")]

        hover.mode = 'vline'

        p.add_tools(hover)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.y_range.end = 150
        p.legend.orientation = "vertical"
        p.legend.location = "top_right"

        script_gender, div_gender = components(p, CDN)
        data = {'script_gender': script_gender,
            'div_gender': div_gender}

        return render(request, 'analytics/crashesByEdad.html', data)

def diesByEdad(request):
        df = pd.read_excel('analytics\datasets\homicidios-accidentes-transito-2018_1.xls')

        grouped = df.groupby('Edad')['Cantidad', 'Sexo'].sum()

        print(grouped)

        source = ColumnDataSource(grouped)
        countries = source.data['Edad'].tolist()
        p = figure(x_range=countries)

        color_map = factor_cmap(field_name='Edad', palette=Spectral6, factors=countries)

        p.vbar(x='Edad', top='Cantidad', source=source, width=0.70, color=color_map ,legend="Edad")

        p.title.text ='Mortalidad en Accidentes de Transito'
        p.xaxis.axis_label = 'Edad'
        p.yaxis.axis_label = 'Cantidad'

        hover = HoverTool()
        hover.tooltips = [
        ("Edad :", "@Edad  ")]

        hover.mode = 'vline'

        p.add_tools(hover)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.y_range.end = 150
        p.legend.orientation = "vertical"
        p.legend.location = "top_right"

        script_gender, div_gender = components(p, CDN)
        data = {'script_gender': script_gender,
            'div_gender': div_gender}

        return render(request, 'analytics/diesByEdad.html', data)

def crashesbyCivil(request):
        df = pd.read_excel('analytics\datasets\lesiones-accidentes-transito-2018.xlsx')

        grouped = df.groupby('Estado civil')['Cantidad'].sum()
        grouped *100

        print(grouped)

        data = pd.Series(grouped).reset_index(name='value').rename(columns={'index':'Escolaridad'})
        data['angle'] = data['value']/data['value'].sum() * 2*pi
        data['color'] = Category20c[len(grouped)]

        p = figure(plot_height=350, title="Estado civil", toolbar_location=None,
                tools="hover", tooltips="Estado civil: @value", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='Estado civil', source=data)

        p.axis.axis_label=None
        p.axis.visible=False
        p.grid.grid_line_color = None

        script_gender, div_gender = components(p, CDN)
        data = {'script_gender': script_gender,
            'div_gender': div_gender}

        return render(request, 'analytics/crashesbyCivil.html', data)

def diesbyCivil(request):
        df = pd.read_excel('analytics\datasets\homicidios-accidentes-transito-2018_1.xls')

        grouped = df.groupby('Estado civil')['Cantidad'].sum()
        grouped *100

        print(grouped)

        data = pd.Series(grouped).reset_index(name='value').rename(columns={'index':'Escolaridad'})
        data['angle'] = data['value']/data['value'].sum() * 2*pi
        data['color'] = Category20c[len(grouped)]

        p = figure(plot_height=350, title="Estado civil", toolbar_location=None,
                tools="hover", tooltips="Estado civil: @value", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='Estado civil', source=data)

        p.axis.axis_label=None
        p.axis.visible=False
        p.grid.grid_line_color = None

        script_gender, div_gender = components(p, CDN)
        data = {'script_gender': script_gender,
            'div_gender': div_gender}

        return render(request, 'analytics/diesByCivil.html', data)