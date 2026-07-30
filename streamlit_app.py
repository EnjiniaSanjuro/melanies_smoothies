# Import python packages
import streamlit as st
import os
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched
import requests

# Write directly to the app
st.title(f'Pending Smoothie Orders')
st.write(
  """
  """
)

#smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text('watermelon')#'smoothiefroot_response)

cnx = st.connection('snowflake')
session = cnx.session() #get_active_session()
my_dataframe = session.table('smoothies.public.orders').filter(col('order_filled') == 0).collect()
current_dataset = session.table('smoothies.public.orders')
if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    if submitted:
        try:
            edited_dataset = session.create_dataframe(editable_df)
            current_dataset.merge(edited_dataset,
                                  (current_dataset['ORDER_UID'] == edited_dataset['ORDER_UID']),
                                  [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})])
            st.success('Your orders has been updated.', icon="✅")
        except:
            st.write('Something went wrong, try again.')
else:
    st.success('There are no pending orders.')
