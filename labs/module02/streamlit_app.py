import streamlit as st
from backend import predict, load_model

st.set_page_config(page_title="Review desk", page_icon="📝")
st.title("Review desk")
st.caption("A tiny teaching model. Predictions require human review.")

@st.cache_resource
def cached_model():
    return load_model()

cached_model()
if "count" not in st.session_state:
    st.session_state.count = 0
with st.form("review_form"):
    review = st.text_area("Course review", max_chars=2000)
    threshold = st.slider("Human-review threshold", 0.5, 0.95, 0.6, 0.05)
    display = st.selectbox("Output format", ["Detailed", "Label only"])
    submitted = st.form_submit_button("Analyse review")
if submitted:
    with st.spinner("Analysing…"):
        st.session_state.result = predict(review, threshold, display)
        st.session_state.count += 1
if "result" in st.session_state:
    st.info(st.session_state.result)
st.metric("Requests in this session", st.session_state.count)
