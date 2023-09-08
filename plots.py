import plotly.graph_objects as go
import plotly.express as px
from shapely import wkt

class MyPlots:
    
    def __init__(self, df) -> None:
        self.df = df

    def providers_donut_chart(self):
        
        donut = px.pie(self.df, values='user', names='provider',
                            color_discrete_sequence=[
                                        px.colors.qualitative.Bold[3],      # yellow
                                        px.colors.qualitative.Dark24[5],    # black
                                        px.colors.qualitative.Dark2[6],     # brown
                                        px.colors.qualitative.Set1[8],      # grey
                            ],
                            hole=0.3
                            )
        donut.update_traces(textposition='inside', textinfo='percent+label')
        return donut

    def gender_age_histo(self):
        
        histo = px.histogram(self.df, 
                            x="age_groups", 
                            color='gender',
                            barmode='group',
                            color_discrete_sequence=[
                                        px.colors.qualitative.Dark2[5],             # yellow
                                        px.colors.qualitative.Set1[8]               # grey #.Dark24[5],   # black
                            ]
                            )
        histo.update_layout(bargap=0.15)
        # histo.update_traces(xbins_size = 5)
        
        return histo
    
    def income_hist(self):
        
        income_hist = px.histogram(self.df, 
                            x="income_groups", 
                            barmode='group',
                            color_discrete_sequence=[
                                        px.colors.qualitative.Dark2[5],     # yellow
                                        px.colors.qualitative.Dark24[5],    # black
                            ]
                            )
        income_hist.update_layout(bargap=0.15)
        
        return income_hist

    def score_v_hist(self):
        score_hist = px.histogram(self.df, 
                            y="score", 
                            barmode='group',
                            orientation="h",
                            color_discrete_sequence=[
                                        px.colors.qualitative.Dark2[5],      # yellow
                                        px.colors.qualitative.Dark24[5],    # black
                            ],
                            )
        score_hist.update_layout(bargap=0.15)
        return score_hist
        
    def products_pie(self):
        top_pie = px.pie(self.df, 
                        names='product_renamed', 
                        values='user',
                        color_discrete_sequence=[
                            px.colors.qualitative.Bold[3],      # yellow
                            px.colors.qualitative.Dark24[5],    # black
                            px.colors.qualitative.Dark2[6],     # brown
                            px.colors.qualitative.Set1[8],      # grey
                            ],
                            )
        top_pie.update_traces(textposition='outside', textinfo='percent+label')

        top_pie.update_layout(legend=dict(
                                        orientation="v",
                                        yanchor="bottom",
                                        y=0.7,
                                        xanchor="left",
                                        x=0.2,)                                            
                            )
        return top_pie

    def wkt_polygon(self):
        
        # Ваш WKT полигон
        wkt_polygon = 'POLYGON ((69.2903599002471 41.348032979648,69.2963005350507 41.3477068192585,69.2958675590802 41.3432301939366,69.2899273262056 41.3435563032847,69.2903599002471 41.348032979648))'

        # Преобразование WKT полигона в объект Polygon
        polygon = wkt.loads(wkt_polygon)

        # Получение координат полигона
        coordinates = list(polygon.exterior.coords)
        lons, lats = zip(*coordinates)

        # Создание объекта полигона
        polygon = go.Scattermapbox(
            mode="lines",
            lon=lons,
            lat=lats,
            fill="toself",
            fillcolor="rgba(0, 0, 255, 0.2)",  # Цвет заливки полигона (в данном случае синий с прозрачностью)
            hoverinfo="none"
        )

        # Создание фигуры карты
        fig = go.Figure(data=[polygon])

        # Настройка параметров карты
        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_zoom=15,  # Масштаб карты
            mapbox_center={"lat": lats[0], "lon": lons[0]},  # Центрирование карты на полигоне
            margin={"r": 0, "t": 0, "l": 0, "b": 0},  # Удаление отступов вокруг карты
        )

        # Отображение карты
        return fig

    def roaming_plot(self, version):
        """Map of USA as an example of the User to be a roaming person

        Args:
            version (str, optional): Choropleth or Scattermapbox.

        Returns:
            plotly graph_objects: figure with map. Could be passed to streamlit.plotly_chart method
        """
        country_name = 'USA'
        title = {}# {'text': f"Roaming country: {country_name}", 'x': 0.5, "y": 0.9}
        
        if version=='Choropleth':
            

            # Создание объекта данных для страны
            data = [go.Choropleth(
                locationmode='country names',
                locations=[country_name],
                z=[1],  # Значение для подсветки страны (в данном случае 1)
                colorscale='Reds',  # Цветовая шкала для подсветки
                autocolorscale=False,
                marker_line_color='darkgray',  # Цвет границы страны
                marker_line_width=0.5,  # Толщина границы страны
                text=[country_name],  # Подписи стран
                hovertemplate='%{text}<extra></extra>',  # Формат подсказки при наведении
                showscale=False,  # Убрать шкалу справа
            )]
            layout = go.Layout(
                mapbox_style="open-street-map",
                mapbox_zoom=3,  # Adjust the zoom level as needed
                mapbox_center={"lat": 37.0902, "lon": -95.7129},  # Center on the USA
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                title=title
            )
            # Создание фигуры карты
            fig = go.Figure(data=data, layout=layout)

            # Настройка параметров карты
            fig.update_geos(
                projection_type="natural earth",  # Тип проекции карты
                showocean=True,  # Отображение океана на карте
                oceancolor='rgba(0, 255, 255, 0.1)',  # Цвет океана (в данном случае голубой с прозрачностью)
                showland=True,  # Отображение суши на карте
                landcolor='rgba(240, 240, 240, 0.9)',  # Цвет суши (в данном случае светло-серый с прозрачностью)
                showcountries=True,  # Отображение границ стран на карте
                countrycolor='rgba(0, 0, 0, 0.2)',  # Цвет границ стран (в данном случае черный с прозрачностью)
                showlakes=False,  # Отображение озер на карте
                lakecolor='rgba(0, 255, 255, 0.1)',  # Цвет озер (в данном случае голубой с прозрачностью)
            )
            return fig
        
                
        if version=="Scattermapbox":
            usa_bbox = [
                [-125.00, 24.396308],  # Southwest corner (longitude, latitude)
                [-66.934570, 49.345786],  # Northeast corner (longitude, latitude)
            ]

            # Create a Scattermapbox trace for the USA bounding box
            usa_bbox_trace = go.Scattermapbox(
                mode="lines",
                lon=[usa_bbox[0][0], usa_bbox[1][0], usa_bbox[1][0], usa_bbox[0][0], usa_bbox[0][0]],
                lat=[usa_bbox[0][1], usa_bbox[0][1], usa_bbox[1][1], usa_bbox[1][1], usa_bbox[0][1]],
                fill="toself",
                fillcolor="rgba(0, 0, 255, 0.2)",  # Blue with transparency
                hoverinfo="none"
            )

            # Create a layout for the map
            layout = go.Layout(
                mapbox_style="open-street-map",
                mapbox_zoom=3,  # Adjust the zoom level as needed
                mapbox_center={"lat": 37.0902, "lon": -95.7129},  # Center on the USA
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                title=title
            )

            # Create a figure and add the USA bounding box trace
            fig = go.Figure(data=[usa_bbox_trace], layout=layout)
        
            return fig