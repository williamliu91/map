import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date
from datetime import timedelta

# Load the data
@st.cache_data
def load_data():
    data = {
        'country': ['Austria', 'Czechoslovakia', 'Poland', 'Denmark', 'Norway', 'Belgium', 'Netherlands', 
                    'Luxembourg', 'France', 'Serbia', 'Croatia', 'Bosnia and Herzegovina', 
                    'North Macedonia', 'Montenegro', 'Slovenia', 'Greece', 'Soviet Union'],
        'code': ['AUT', 'CZE', 'POL', 'DNK', 'NOR', 'BEL', 'NLD', 'LUX', 'FRA', 
                 'SRB', 'HRV', 'BIH', 'MKD', 'MNE', 'SVN', 'GRC', 'SUN'],
        'date': ['1938-03-12', '1939-03-15', '1939-09-01', '1940-04-09', '1940-04-09', '1940-05-10', 
                 '1940-05-10', '1940-05-10', '1940-05-10', '1941-04-06', '1941-04-06', '1941-04-06', 
                 '1941-04-06', '1941-04-06', '1941-04-06', '1941-04-06', '1941-06-22'],
        'end_date': ['1945-05-08', '1945-05-08', '1945-05-08', '1945-05-05', '1945-05-08', '1944-09-30', 
                     '1945-05-05', '1944-09-30', '1944-08-25', '1945-05-08', '1945-05-08', '1945-05-08', 
                     '1945-05-08', '1945-05-08', '1945-05-08', '1944-10-31', '1945-05-08']
    }
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['end_date'] = pd.to_datetime(df['end_date']).dt.date
    return df

# App
st.title('German Invasions in World War II')

df = load_data()

# Create a slider for the date
min_date = df['date'].min() - timedelta(days=365)
max_date = df['end_date'].max()
selected_date = st.slider('Select a date', min_value=min_date, max_value=max_date, 
                          value=min_date, format="YYYY-MM-DD")

# Filter the data based on the selected date
invaded = df[(df['date'] <= selected_date) & (df['end_date'] >= selected_date)]

# Prepare data for the map
all_countries = df['code'].tolist() + ['DEU']  # Include Germany
all_country_names = df['country'].tolist() + ['Germany']
colors = ['red' if code in invaded['code'].tolist() or code == 'DEU' else 'lightgrey' for code in all_countries]

# Create the map
fig = go.Figure(data=go.Choropleth(
    locations = all_countries,
    z = [1 if color == 'red' else 0 for color in colors],  # 1 for invaded, 0 for not invaded
    text = all_country_names,
    colorscale = [[0, 'lightgrey'], [1, 'red']],
    autocolorscale = False,
    reversescale = False,
    marker_line_color = 'darkgray',
    marker_line_width = 0.5,
    colorbar_title = 'Invaded',
))

fig.update_layout(
    title_text = f'German Invasions in World War II (as of {selected_date})',
    geo = dict(
        showframe = False,
        showcoastlines = True,
        projection_type = 'equirectangular',
        center = dict(lon=15, lat=55),  # Center on Europe
        lonaxis = dict(range=[-10, 40]),  # Adjust these values to zoom on Europe
        lataxis = dict(range=[35, 70]),
    ),
    width = 800,
    height = 500
)

# Display the map
st.plotly_chart(fig)

# Display the list of invaded countries
if not invaded.empty:
    st.write(f"Countries under German occupation on {selected_date}:")
    for country in invaded['country']:
        st.write(f"- {country}")
else:
    st.write("No countries under German occupation on this date.")

# Add some context
st.markdown("""
This map shows the progression of German invasions during World War II. 
Use the slider to change the date and see which countries were under German occupation at that time.

Red countries are those under German control, including Germany itself.

Note: The map uses historical borders from the World War II era, but Yugoslavia has been replaced with its present-day countries, 
representing Serbia, Croatia, Bosnia and Herzegovina, North Macedonia, Montenegro, and Slovenia.
""")
