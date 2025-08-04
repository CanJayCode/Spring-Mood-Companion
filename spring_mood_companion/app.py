import streamlit as st
from mood_utils import analyze_mood, get_spring_tip, save_log, suggest_activity, recommend_web_activity, get_log, random_spring_quote, random_activity
import requests
import pandas as pd

st.set_page_config(page_title="Spring Mood Companion", page_icon="🌸", layout="centered")

# --- Custom CSS for spring theme and animated flowers ---
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #f9f6e7 0%, #e0f7fa 100%) !important;
    }
    .stApp {
        background: linear-gradient(135deg, #f9f6e7 0%, #e0f7fa 100%) !important;
        border-radius: 20px;
        border: 4px solid #ffe0b2;
        box-shadow: 0 0 40px #e1bee7;
    }
    .spring-border {
        border: 2px dashed #a5d6a7;
        border-radius: 16px;
        padding: 1.5em;
        background: #fffde7cc;
        margin-bottom: 1.5em;
    }
    .spring-btn {
        background: #e1bee7;
        color: #388e3c;
        border-radius: 8px;
        border: none;
        padding: 0.5em 1.5em;
        font-size: 1.1em;
        margin: 0.5em 0;
        cursor: pointer;
        transition: background 0.2s;
    }
    .spring-btn:hover {
        background: #b2dfdb;
        color: #6d4c41;
    }
    .progress-bar {
        height: 18px;
        background: #c8e6c9;
        border-radius: 9px;
        margin-bottom: 1em;
        overflow: hidden;
    }
    .progress {
        height: 100%;
        background: linear-gradient(90deg, #a5d6a7, #ffe082);
        border-radius: 9px;
        transition: width 0.5s;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Lottie animation loader ---
@st.cache_data(show_spinner=False)
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_spring = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_8ygi2vrc.json")
lottie_mood = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_0yfsb3a1.json")
lottie_activity = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_2ks3pjua.json")

# --- Sidebar: Mood Log History ---
st.sidebar.header("🌱 Mood Log History")
log = get_log()
if log:
    df = pd.DataFrame(log)
    df = df[["timestamp", "entry", "mood", "polarity"]]
    st.sidebar.dataframe(df.tail(10), use_container_width=True, hide_index=True)
    st.sidebar.download_button("Download Log as CSV", df.to_csv(index=False), file_name="mood_log.csv")
else:
    st.sidebar.info("No mood logs yet!")

st.sidebar.markdown("---")
st.sidebar.markdown("<div style='text-align:center;font-size:1.5em;'>🌸🌷🌼🐝🌱</div>", unsafe_allow_html=True)

# --- Main UI ---
st.markdown('<div style="text-align:center">', unsafe_allow_html=True)
if lottie_spring:
    st.components.v1.html(
        f'<lottie-player src="https://assets2.lottiefiles.com/packages/lf20_8ygi2vrc.json"  background="transparent"  speed="1"  style="width: 300px; height: 300px; margin:auto;"  loop  autoplay></lottie-player>',
        height=320,
    )
else:
    st.markdown("🌸🌷🌼🐝", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.title("🌸 Spring Mood Companion")
st.markdown('<div class="spring-border">Hi! I\'m your spring wellness agent. Let\'s chat and I\'ll suggest something fun and uplifting! 🌱🌷</div>', unsafe_allow_html=True)

# --- Agent conversation state ---
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'show_summary' not in st.session_state:
    st.session_state.show_summary = False

questions = [
    {"key": "mood", "q": "How are you feeling today? 🌼", "type": "text"},
    {"key": "energy", "q": "How is your energy right now? (Low/Medium/High)", "type": "select", "options": ["Low", "Medium", "High"]},
    {"key": "social", "q": "Do you feel like being social or solo?", "type": "select", "options": ["Social", "Solo", "Either"]},
]

# --- Progress bar ---
progress = int((st.session_state.step / (len(questions)+1)) * 100)
st.markdown(f'''<div class="progress-bar"><div class="progress" style="width:{progress}%"></div></div>''', unsafe_allow_html=True)

if st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    st.markdown(f'<div class="spring-border">{q["q"]}</div>', unsafe_allow_html=True)
    if q["type"] == "text":
        ans = st.text_input("Your answer:", key=f"q{st.session_state.step}")
    else:
        ans = st.selectbox("Choose one:", q["options"], key=f"q{st.session_state.step}")
    if st.button("Next", key=f"next{st.session_state.step}", help="Continue to next question"):
        if ans:
            st.session_state.answers[q["key"]] = ans
            st.session_state.step += 1
        else:
            st.warning("Please answer before continuing.")
elif not st.session_state.show_summary:
    # Show summary before suggestions
    st.markdown('<div class="spring-border"><b>Here\'s what you shared:</b><ul>' + ''.join([f'<li><b>{q["q"]}</b> <span style="color:#388e3c;">{st.session_state.answers[q["key"]]}</span></li>' for q in questions]) + '</ul></div>', unsafe_allow_html=True)
    if st.button("See Suggestions!", key="see_suggestions", help="Get your personalized spring suggestions"):
        st.session_state.show_summary = True
else:
    # Analyze and suggest
    user_input = st.session_state.answers["mood"]
    sentiment, polarity = analyze_mood(user_input)
    tip = get_spring_tip(sentiment)
    activity = suggest_activity(sentiment, st.session_state.answers["energy"], st.session_state.answers["social"])
    web_activity, web_url = recommend_web_activity(sentiment, st.session_state.answers["energy"], st.session_state.answers["social"])
    save_log(user_input, sentiment, polarity)
    st.balloons()
    if lottie_mood:
        st.components.v1.html(
            f'<lottie-player src="https://assets2.lottiefiles.com/packages/lf20_0yfsb3a1.json"  background="transparent"  speed="1"  style="width: 180px; height: 180px; margin:auto;"  loop  autoplay></lottie-player>',
            height=200,
        )
    st.markdown(f"<div class='spring-border'><b>Detected Mood</b>: <span style='color:#43a047;'>{sentiment}</span> ({round(polarity, 2)})<br>🌼 <b>Tip:</b> {tip}</div>", unsafe_allow_html=True)
    if lottie_activity:
        st.components.v1.html(
            f'<lottie-player src="https://assets2.lottiefiles.com/packages/lf20_2ks3pjua.json"  background="transparent"  speed="1"  style="width: 180px; height: 180px; margin:auto;"  loop  autoplay></lottie-player>',
            height=200,
        )
    st.markdown(f"<div class='spring-border'>🌷 <b>Personalized Spring Activity:</b> {activity}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='spring-border'>🌱 <b>Try this web activity:</b> <a href='{web_url}' target='_blank'>{web_activity}</a></div>", unsafe_allow_html=True)
    st.info(f"🌸 Spring Quote: {random_spring_quote()}")
    if st.button("Surprise me!", key="surprise"):
        st.success(f"🌼 Try this: {random_activity()}")
    if st.button("Restart Conversation"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.show_summary = False

st.markdown('<div style="text-align:center; font-size: 1.5em; margin-top:2em;">🌸🌷🌼🐝🌱</div>', unsafe_allow_html=True)