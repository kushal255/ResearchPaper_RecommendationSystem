# pip install tensorflow==2.11.0
# pip install sentence_transformers==4.0.2
# pip install streamlit

# import tools==================================
import streamlit as st
import torch
from sentence_transformers import util
import pickle

# load save recommendation models===================================

embeddings = pickle.load(open('models/embeddings.pkl','rb'))
sentences = pickle.load(open('models/sentences.pkl','rb'))
rec_model = pickle.load(open('models/rec_model.pkl','rb'))


# custom functions====================================

def recommendation(input_paper):
    # Calculate cosine similarity scores between the embeddings of input_paper and all papers in the dataset.
    cosine_scores = util.cos_sim(embeddings, rec_model.encode(input_paper))

    # Get the indices of the top-k most similar papers based on cosine similarity.
    top_similar_papers = torch.topk(cosine_scores, dim=0, k=5, sorted=True)

    # Retrieve the titles of the top similar papers.
    papers_list = []
    for i in top_similar_papers.indices:
        papers_list.append(sentences[i.item()])

    return papers_list







# create app=========================================

st.title('Research Papers Recommendation and Subject Area Prediction App')
input_paper = st.text_input("Enter Paper title.....")
if st.button("Recommend"):
    # recommendation part
    recommend_papers = recommendation(input_paper)
    st.subheader("Recommended Papers")
    st.write(recommend_papers)