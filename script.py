import streamlit as st
import openai
from docx import Document
from io import BytesIO
import base64

def generate_testimonials_local(test_name, city_name):
    # prompt = f"Generate 10 user reviews for a {test_name} test in {city_name}. Include grammatical and typographical errors in the reviews so that it can look more authentic. The service provider is PharmEasy, a healthcare company known for its home sample collection service. Do not mention the company name in 5 review, but include it in other 5 reviews. Ensure that the reviews are unique and do not repeat any previously generated content."

    prompt = f"Consider the scenario, Our company name is PharmEasy, a healthcare provider we provide diagnostic test facility and we need users testimonial or reviews for our web page for {test_name} in {city_name} so your task is to generate 10 reviews keep in mind to include grammatical and typographical errors in the reviews so that it can look more authentic. Do not mention the company name and its USP in all the ten reviews but mention these some of the reviews. Ensue that the reviews are unique and do not repeat any previously generated content. Keep in mind do not mention home sample collection in every review, use this in some reviews only for rest show some creativity"
    
    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content":  prompt,
            },
        ],
        max_tokens=500,
        n=10,
        stop=None,
        temperature=0.5,
    )
    response = gpt_response["choices"][0]["message"]["content"].strip()
    response = response
    return response


def generate_testimonials_generics(test_name):

    prompt = f"Consider the scenario, Our company name is PharmEasy, a healthcare provider we provide diagnostic test facility and we need users testimonial or reviews for our web page for {test_name} so your task is to generate 10 reviews keep in mind to include grammatical and typographical errors in the reviews so that it can look more authentic. Do not mention the company name and its USP in all the ten reviews but mention these some of the reviews. Ensue that the reviews are unique and do not repeat any previously generated content. Keep in mind do not mention home sample collection in every review, use this in some reviews only for rest show some creativity"
    
    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content":  prompt,
            },
        ],
        max_tokens=500,
        n=10,
        stop=None,
        temperature=0.5,
    )
    response = gpt_response["choices"][0]["message"]["content"].strip()
    response = response
    return response


def create_download_link(string, file_name, link_text):
    doc = Document()

    doc.add_paragraph(string)

    doc_io = BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)

    doc_base64 = base64.b64encode(doc_io.read()).decode()


    href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{doc_base64}" download="{file_name}">{link_text}</a>'

    return href


def dummy(test_name, page_type, city_name = "Unknown"):
    
    if page_type == "Local":
        st.write(f"""
             Test name: {test_name}
             City name: {city_name}
             Testimonial Creation is in Progress""")
        
        result = generate_testimonials_local(test_name, city_name)

    else:
        st.write(f"""
            Test name: {test_name}
            Generic page Testimonial Creation is in Progress""")

        result = generate_testimonials_generics(test_name)    

    st.write(result)
    file_name = f"{test_name}_in_{city_name}_reviews.docx"
    download_link = create_download_link(result, file_name, "Click to here to download the Word file for these reviews")
    st.markdown(download_link, unsafe_allow_html=True)


def main():
   
    st.write("<h1 style='color: #10847E;'>Diag Testimonial Creator</h1>", unsafe_allow_html=True)    
    
    test_name = st.text_input("Enter Test Name", placeholder= "CBC Test")
    openai_key = st.text_input("Enter your open Ai key", type = "password")

    option = st.radio(
    "Please Select the type of diagnostic page",
    ("Local", "Non-Local (Generic page)")
)
    if option == "Local":
        city_name = st.text_input("Enter City Name", placeholder="Delhi")

    if st.button("Create Testimonials"):
        if test_name and openai_key:
            openai.api_key = openai_key
            with st.spinner("Creating Testimonials ...."):
                if option == "Local":
                    dummy(test_name, option, city_name)
                else:
                    dummy(test_name, option)    
        else:
            st.warning("Please give the appropriate inputs")    


if __name__ == "__main__":
    main()
