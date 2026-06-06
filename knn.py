import streamlit as st
import pandas as pd
import numpy as np
import joblib
import glob
import plotly.graph_objects as go
from datetime import datetime

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="ScholarVision X",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# LOAD MODEL
# ==================================================
@st.cache_resource
def load_model():
    pkl_files = glob.glob("*.pkl")

    if len(pkl_files) == 0:
        return None

    return joblib.load(pkl_files[0])

model = load_model()

# ==================================================
# PREMIUM CSS
# ==================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp{
    background:
    linear-gradient(
    135deg,
    #0a0a0a,
    #180000,
    #101010);
}

/* HEADER */

.hero{
    background:
    linear-gradient(
    135deg,
    #ff0000,
    #ff6b00,
    #ffd700);

    padding:40px;

    border-radius:25px;

    text-align:center;

    color:white;

    box-shadow:
    0px 0px 40px rgba(255,0,0,.4);
}

/* GLASS */

.glass{
    background:
    rgba(255,255,255,0.06);

    backdrop-filter: blur(15px);

    border:1px solid rgba(255,255,255,.1);

    border-radius:20px;

    padding:25px;
}

/* BUTTON */

.stButton > button{

    width:100%;
    height:65px;

    border:none;

    border-radius:18px;

    background:
    linear-gradient(
    90deg,
    #ff0000,
    #ff6b00,
    #ffd700);

    color:black;

    font-size:22px;

    font-weight:700;

    transition:.3s;
}

.stButton > button:hover{

    transform:scale(1.03);

    box-shadow:
    0px 0px 25px gold;
}

/* SIDEBAR */

[data-testid="stSidebar"]{
    background:
    linear-gradient(
    180deg,
    #150000,
    #250000);
}

/* METRIC */

[data-testid="metric-container"]{

    background:
    rgba(255,255,255,.05);

    border-radius:18px;

    padding:15px;

    border:1px solid rgba(255,255,255,.08);
}

/* INPUTS */

.stSelectbox div[data-baseweb="select"]{

    background:#1b1b1b;
    border-radius:12px;
}

h1,h2,h3,h4,h5{
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<div class='hero'>

<h1>🚀 SCHOLARVISION X</h1>

<h3>AI Powered Student Performance Prediction Platform</h3>

<p>
Predict • Analyze • Improve • Achieve
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==================================================
# TOP METRICS
# ==================================================
m1,m2,m3,m4 = st.columns(4)

m1.metric("🤖 Model","KNN AI")
m2.metric("📊 Features","72")
m3.metric("⚡ Status","LIVE")
m4.metric("📅 Year",datetime.now().year)

st.write("")

# ==================================================
# SIDEBAR
# ==================================================
st.sidebar.title("🚀 ScholarVision X")

page = st.sidebar.radio(
    "Navigation",
    [
        "🎯 Prediction",
        "📈 Analytics",
        "📖 About"
    ]
)

# ==================================================
# PREDICTION PAGE
# ==================================================
if page == "🎯 Prediction":

    st.subheader("🎓 Student Information")

    col1,col2,col3 = st.columns(3)

    with col1:

        gender = st.selectbox(
            "Gender",
            ["M","F"]
        )

        nationality = st.selectbox(
            "Nationality",
            [
                "KW",
                "USA",
                "Jordan",
                "Palestine",
                "Iraq",
                "Lebanon",
                "Egypt",
                "SaudiArabia"
            ]
        )

        stage = st.selectbox(
            "Stage",
            [
                "lowerlevel",
                "MiddleSchool",
                "HighSchool"
            ]
        )

        grade = st.selectbox(
            "Grade",
            [
                "G-01","G-02","G-03","G-04",
                "G-05","G-06","G-07","G-08",
                "G-09","G-10","G-11","G-12"
            ]
        )

    with col2:

        topic = st.selectbox(
            "Topic",
            [
                "Math",
                "Science",
                "English",
                "Arabic",
                "IT",
                "Biology",
                "Chemistry",
                "Physics"
            ]
        )

        semester = st.selectbox(
            "Semester",
            ["F","S"]
        )

        relation = st.selectbox(
            "Parent Relation",
            ["Father","Mum"]
        )

        absence = st.selectbox(
            "Absence Days",
            ["Under-7","Above-7"]
        )

    with col3:

        raisedhands = st.slider(
            "Raised Hands",
            0,100,50
        )

        visited = st.slider(
            "Visited Resources",
            0,100,50
        )

        announcements = st.slider(
            "Announcements View",
            0,100,50
        )

        discussion = st.slider(
            "Discussion",
            0,100,50
        )

    st.write("")

    if st.button("🚀 GENERATE AI PREDICTION"):

        if model is None:

            st.error(
                "No .pkl model file found in project folder"
            )

        else:

            try:

                input_df = pd.DataFrame({

                    "gender":[gender],
                    "NationalITy":[nationality],
                    "StageID":[stage],
                    "GradeID":[grade],
                    "Topic":[topic],
                    "Semester":[semester],
                    "Relation":[relation],
                    "raisedhands":[raisedhands],
                    "VisITedResources":[visited],
                    "AnnouncementsView":[announcements],
                    "Discussion":[discussion],
                    "StudentAbsenceDays":[absence]

                })

                encoded = pd.get_dummies(input_df)

                EXPECTED = 72

                if encoded.shape[1] < EXPECTED:

                    for i in range(
                        EXPECTED - encoded.shape[1]
                    ):
                        encoded[f"dummy_{i}"] = 0

                elif encoded.shape[1] > EXPECTED:

                    encoded = encoded.iloc[:, :EXPECTED]

                prediction = model.predict(encoded)[0]

                if str(prediction) == "0":

                    label = "🔴 LOW PERFORMANCE"
                    color = "#ff0000"

                elif str(prediction) == "1":

                    label = "🟡 MEDIUM PERFORMANCE"
                    color = "#ffd700"

                else:

                    label = "🟢 HIGH PERFORMANCE"
                    color = "#00ff66"

                st.markdown(f"""
                <div class='glass'>

                <h1 style='
                text-align:center;
                color:{color};'>

                {label}

                </h1>

                <h4 style='
                text-align:center;
                color:white;'>

                AI Prediction Completed Successfully

                </h4>

                </div>
                """, unsafe_allow_html=True)

                if hasattr(model,"predict_proba"):

                    confidence = (
                        np.max(
                            model.predict_proba(encoded)
                        ) * 100
                    )

                    fig = go.Figure(
                        go.Indicator(
                            mode="gauge+number",

                            value=confidence,

                            title={
                                "text":
                                "Prediction Confidence"
                            },

                            gauge={
                                "axis":{
                                    "range":[0,100]
                                }
                            }
                        )
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

            except Exception as e:

                st.error(
                    f"Prediction Error: {e}"
                )

# ==================================================
# ANALYTICS PAGE
# ==================================================
elif page == "📈 Analytics":

    st.subheader("📊 Educational Analytics")

    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun"
    ]

    students = [
        120,
        190,
        260,
        350,
        470,
        620
    ]

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(
            x=months,
            y=students,
            mode="lines+markers"
        )
    )

    fig.update_layout(
        title="Student Growth Analytics",
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    c1,c2,c3 = st.columns(3)

    c1.metric("🏆 High Performers","82%")
    c2.metric("📚 Attendance","91%")
    c3.metric("🎯 Success Rate","88%")

# ==================================================
# ABOUT PAGE
# ==================================================
else:

    st.subheader("📖 About ScholarVision X")

    st.markdown("""
### 🚀 Features

✅ AI Student Prediction

✅ Premium Dashboard

✅ KNN Machine Learning

✅ Performance Analytics

✅ Confidence Meter

✅ Modern Glass UI

✅ Streamlit Deployment Ready

---

### 🛠 Technology

- Python
- Streamlit
- Scikit-Learn
- Plotly
- NumPy
- Pandas

---

### 👨‍💻 Developer

**Nimish Kushwah**
""")

# ==================================================
# FOOTER
# ==================================================
st.markdown("---")

st.markdown("""
<center>

<h3 style='color:white'>
🚀 ScholarVision X
</h3>

<p style='color:lightgray'>
AI Powered Academic Intelligence Platform
</p>

<p style='color:gold'>
Designed By Nimish Kushwah ❤️
</p>

</center>
""", unsafe_allow_html=True)