# Import python packages
import streamlit as st
import os
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f"Custom Smoothie Order Form :cup_with_straw:")
st.write(
  """Chose up to five fruits!
  """
)

cnx = st.connection('snowflake')
session = cnx.session()
session.use_database("SMOOTHIES")
session.use_schema("PUBLIC")
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruits_list = st.multiselect('Make you choice below:', my_dataframe)
if fruits_list:
    #fruits_string = ''
    for fruit in fruits_list:
        #fruits_string += fruit + ' '
        st.subheader(fruit + ' Nutrition information')
        url = 'https://my.smoothiefroot.com/api/fruit/' + fruit.lower()
        #st.write(url)
        smoothiefroot_response = requests.get(url)
        sf_sf = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    if len(fruits_list) < 6:
        name_on_order = st.text_input('Your Name:')
        if name_on_order:
            order_line = ''.join([c + ', ' for c in fruits_list])
            sql_insert = """insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + order_line[:-2] + """', '""" + name_on_order + """')"""
            time_to_insert = st.button('Submit Order')
            if time_to_insert:
                result = session.sql(sql_insert).collect()
                st.success('Your order has been submitted.', icon="✅")
    elif len(fruits_list) > 5:
        st.write('Too many fruits chosen!')
