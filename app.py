import streamlit as st
import langchain_helper

st.title("🍽️ Restaurant Name & Dish Planner")

cuisine = st.sidebar.selectbox("Pick a Cuisine", ("Indian", "Italian", "Mexican", "Arabic", "American", "Chinese", "Japanese", "Spanish", "Turkish", "Lebanese"))

if cuisine:
    response = langchain_helper.generate_restaurant_name_and_items(cuisine)
    st.header(response['restaurant_name'].strip())
    menu_items = response['menu_items'].strip().split("\n")
    for item in menu_items:
        cleaned_item = item.lstrip("-• ").strip()
        if cleaned_item:
            st.write("-", cleaned_item)