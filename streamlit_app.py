# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas

# Write directly to the app
st.title(":cup_with_straw: Customize your Smothie :cup_with_straw:")
st.write(
    """Choose fruits to cutomize your Smoothie!
    """
   )
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop

options = st.multiselect(
    "Choose your Ingredients",my_dataframe
    )

#st.dataframe(data=my_dataframe, use_container_width=True)

if options:
    #st.write(options)
    #st.text( options)
    ingredients_string = ""
    for fruit_chosen in options:
        st.subheader(fruit_chosen + 'Nurtritional Information ')
        ingredients_string += fruit_chosen + ' '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    #st.text( ingredients_string)    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


#st.text(fruityvice_response.json())


