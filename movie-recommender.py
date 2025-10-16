!pip install --upgrade pip
import streamlit as st
import pickle
import pandas as pd
import os
import gdown

file_id = "1o7QynCjtAklI5-9ANEiFQiYIj5qkT9rs" 
url = f"https://drive.google.com/uc?id={file_id}"

if not os.path.exists("similarity.pkl"):
    with st.spinner("Downloading similarity data from Google Drive..."):
        gdown.download(url, "similarity.pkl", quiet=False)

def recommend(search):
    results = {}
    for item in new_data.title:
        if item.lower() == search.lower():

            movie_index = new_data[new_data.title == item].index[0]

            similar = similarity[movie_index]
            movies_list = sorted(list(enumerate(similar)), reverse=True, key=lambda x: x[1])[1:6]

            results['Similar Movies'] = [new_data.iloc[i[0]].title for i in movies_list]
            break

    if any(films.crew.str.contains(search, case=False, na=False)):
        crew = films.crew[films[films.crew.str.contains(r'\b{}\b'.format(search), case=False, na=False)].index[0:5]]
        title = films.title[films[films.crew.str.contains(r'\b{}\b'.format(search), case=False, na=False)].index[0:5]]
        results['By Crew'] = title.head(5)

    elif any(films.cast.str.contains(search, case=False, na=False)):
        cast = films.cast[films[films.cast.str.contains(r'\b{}\b'.format(search), case=False, na=False)].index[0:5]]
        title = films.title[films[films.cast.str.contains(r'\b{}\b'.format(search), case=False, na=False)].index[0:5]]
        results['By Cast'] = title.head(5)

    elif any(films.genres.str.contains(search, case=False, na=False)):
        genres = films.genres[films[films.genres.str.contains(r'\b{}\b'.format(search), case=False, na=False)].index[0:5]]
        title = films.title[films[films.genres.str.contains(r'\b{}\b'.format(search), case=False, na=False)].index[0:5]]
        results['By Genre'] = title.head(5)

    return results
movies_dict= pickle.load(open('movies_dict.pkl', 'rb'))
new_data= pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
films=pickle.load(open('films.pkl', 'rb'))

st.title("Movie Recommender")


search = st.text_input("Enter a movie title, actor, director, or genre:")

if search:
    output = recommend(search)

    if not output:
        st.warning("No results found.")
    else:
        for key, value in output.items():
            st.subheader(key)
            if isinstance(value, list):
                for v in value:
                    st.write(f"• {v}")
            else:

                st.dataframe(value)

