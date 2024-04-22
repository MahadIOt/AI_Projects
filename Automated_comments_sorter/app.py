import streamlit as st
from transformers import pipeline
 
if 'all_comments' not in st.session_state:
    st.session_state['all_comments'] = []
 
model_path = ("Models/models--distilbert--distilbert-base-uncased-finetuned-sst-2-english/"
              "snapshots/714eb0fa89d2f80546fda750413ed43d93601a13")
classifier = pipeline("text-classification", model=model_path)
 
st.title("Comments Analyzer")
st.video("https://youtu.be/jSgdL1zX4h8?si=PLXncne9ga_gGIWq")
comment = st.text_input("Enter your comment", value="Amazing Video")
 
# Add select box for sorting
sort_option = st.selectbox("Sort Comments by Sentiment:", [ "None","Positive", "Negative"])
 
def display_comments(comments):
    for idx, comment in enumerate(comments):
        # Determine background color based on sentiment
        if comment['classification'] == 'POSITIVE':
            background_color = '#DFF0D8'  # Light green
        elif comment['classification'] == ('NEGATIVE'):
            background_color = '#F2DEDE'  # Light red
        else:
            background_color = '#FFFFFF'  # Default white
 
        # HTML template for comment display
        comment_html = f"""
        <div style="margin: 10px; padding: 10px; 
        border-radius: 5px; box-shadow: 0px 2px 5px 0px rgba(0, 0, 0, 0.1);
         background-color: {background_color}; padding-left:25px; padding-top:20px; padding-bottom:20px">
            <div style="font-weight: bold;"> Username </div>
            <div>{comment['comment']}</div>
        </div>
        """
        # Display comment using st.write with unsafe_allow_html=True
        st.write(comment_html, unsafe_allow_html=True)
 
 
def classify_comment(classifier, comment):
    result = classifier(comment)[0]['label']
    return result
 
 
if st.button("Add Comment"):
    comment_dic = {'comment': comment, 'classification': classify_comment(classifier, comment)}
    st.session_state['all_comments'].append(comment_dic)
 
# Filter comments based on selected option
filtered_comments = st.session_state['all_comments']
if sort_option == "Positive":
    filtered_comments = [c for c in filtered_comments if c['classification'] == 'POSITIVE']
elif sort_option == "Negative":
    filtered_comments = [c for c in filtered_comments if c['classification'] == 'NEGATIVE']
 
display_comments(filtered_comments)