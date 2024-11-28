# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
import pandas as pd
from snowflake.snowpark.functions import col

cnx=st.connection("snowflake")
session=cnx.session()
#import matplotlib.pyplot as plt
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw: ")
st.write( 
    """Choose the fruits you want in your custom smoothie
    """
)
#option = st.selectbox(
#    "What is your favourite fruit?",
#    ("Banana","Strawberries", "Peaches"),
#    index=None,
#    placeholder="Select your favourite fruit",
#)
#st.write("Your favourite fruit is:", option)

name_on_order = st.text_input("Name on Smoothie")
st.write("The on your Smoothie will be", name_on_order)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list =st.multiselect('Choose upt to 5 ingredients:'
                                 ,my_dataframe,
                                max_selections=5)

#st.write( 
#    f"""
#    {type(my_dataframe)}"""
#)
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+ ' '
    st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order+ """')"""

    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button('Submit Order')
    if(time_to_insert):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        #st.write("the histogram is")
        #table = session.table("smoothies.public.orders")
        #df = table.to_pandas()
        #st.dataframe(data=table, use_container_width=True)
        #st.title("Smoothies Price Distribution")

        # Plot histogram using Streamlit
        #st.write("Histogram of smoothie prices:")
        #st.write("Columns in the DataFrame:", table.columns)
        #st.bar_chart(df["ingredients"].value_counts().sort_index())
    
