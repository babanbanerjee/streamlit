import streamlit as st

st.write("Addition of Two numbers")
st.header("Enter the Two numbers")
num1 = st.number_input("Enter the 1st number")
num2 = st.number_input("Enter the 2nd number")
clicked = st.button("Add")
sum = 0
if clicked:
    sum = num1+num2
st.write("Addition of Two numbers is :" + str(sum))


