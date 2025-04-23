import streamlit as st
import pandas as pd
import random

# --- load data ---
@st.cache_data
def load_data():
    df = pd.read_csv('q_and_answer.csv')
    qlist = df.to_dict(orient='records')
    random.shuffle(qlist)
    return qlist

questions = load_data()

# --- init session state ---
if 'idx' not in st.session_state:
    st.session_state.idx = 0
    st.session_state.correct = 0
    st.session_state.wrong = 0

# --- UI ---
st.title("X‑Ray AI Detector")
q = questions[st.session_state.idx]
st.image(f"static/images/{q['Image_Name']}", use_container_width=True)
st.write("Is this radiograph AI‑generated or authentic (real)?")

col1, col2 = st.columns(2)
with col1:
    if st.button("🤖 AI"):
        if q['RealOrAI'] == 'AI':
            st.session_state.correct += 1
        else:
            st.session_state.wrong += 1
        st.session_state.idx += 1
with col2:
    if st.button("✅ Real"):
        if q['RealOrAI'] == 'Real':
            st.session_state.correct += 1
        else:
            st.session_state.wrong += 1
        st.session_state.idx += 1

# --- show stats or final ---
if st.session_state.idx < len(questions):
    st.write(f"**Correct:** {st.session_state.correct} | **Wrong:** {st.session_state.wrong}")
    if (st.session_state.correct+st.session_state.wrong) > 0:
        st.write(f"**Accuracy:** {st.session_state.correct/(st.session_state.correct+st.session_state.wrong)*100:.1f}%")
    else:
        st.write("**Accuracy:** 0%")
    st.write(f"**Remaining:** {len(questions)-st.session_state.idx}")
else:
    st.header("Thank You!")
    st.write("Your participation helps advance medical AI research.")
    st.write(f"**Final Score:** {st.session_state.correct}/{len(questions)}")
    st.write(f"**Accuracy:** {st.session_state.correct/len(questions)*100:.1f}%")
    if st.button("🔄 Restart"):
        for k in ['idx','correct','wrong']:
            del st.session_state[k]
        st.experimental_rerun()
