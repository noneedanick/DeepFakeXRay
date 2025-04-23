import streamlit as st
import pandas as pd
import random

# 1) Page config
st.set_page_config(page_title="X‑Ray AI Detector", layout="centered")

# 2) Inline your CSS
with open("static/css/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3) Load & shuffle data
@st.cache_data
def load_questions():
    df = pd.read_csv("q_and_answer.csv")
    records = df.to_dict(orient="records")
    random.shuffle(records)
    return records

questions = load_questions()
total_q = len(questions)

# 4) Init session state
if "idx" not in st.session_state:
    st.session_state.idx = 0
    st.session_state.correct = 0
    st.session_state.wrong = 0

# 5) HOME SCREEN
if st.session_state.idx == 0:
    st.markdown("""
    <section class="hero">
      <div class="hero-content">
        <h1>Sharpen Your Radiograph Radar</h1>
        <p>Detect AI fakes before they reach the clinic.</p>
        <button class="btn btn-cta" id="start-btn">Start the Exercise</button>
      </div>
    </section>
    """, unsafe_allow_html=True)
    if st.button("Start the Exercise"):
        st.session_state.idx = 1
        st.experimental_rerun()
    st.stop()

# 6) QUIZ SCREEN
if 1 <= st.session_state.idx <= total_q:
    q = questions[st.session_state.idx - 1]
    st.image(f"static/images/{q['Image_Name']}", use_column_width=True)
    st.markdown("### Is this radiograph AI‑generated or authentic (real)?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤖 AI"):
            if q["Real_or_AI"] == "AI":
                st.session_state.correct += 1
            else:
                st.session_state.wrong += 1
            st.session_state.idx += 1
            st.experimental_rerun()
    with col2:
        if st.button("✅ Real"):
            if q["Real_or_AI"] == "Real":
                st.session_state.correct += 1
            else:
                st.session_state.wrong += 1
            st.session_state.idx += 1
            st.experimental_rerun()
    # stats bar
    if (st.session_state.correct + st.session_state.wrong) > 0:
        acc = st.session_state.correct / (st.session_state.correct + st.session_state.wrong) * 100
    else:
        acc = 0
    st.markdown(f"""
    <div class="stats">
      <span>Correct: {st.session_state.correct}</span>
      <span>Wrong: {st.session_state.wrong}</span>
      <span>Accuracy: {acc:.1f}%</span>
      <span>Remaining: {total_q - st.session_state.idx + 1}</span>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# 7) FINAL SCREEN
st.header("Thank You!")
st.write("Your participation helps advance medical AI research.")
st.markdown(f"**Final Score:** {st.session_state.correct}/{total_q}")
st.markdown(f"**Accuracy:** {st.session_state.correct/total_q*100:.1f}%")
if st.button("🔄 Restart"):
    for key in ("idx", "correct", "wrong"):
        del st.session_state[key]
    st.experimental_rerun()
