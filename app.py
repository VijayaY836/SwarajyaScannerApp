import streamlit as st
from PIL import Image
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Swarajya Scanner Dashboard", layout="wide")

# Theme Toggle
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"  # or 'dark' if you prefer dark mode default

with st.sidebar:
    switch = st.button(
        "🌙 Dark Mode" if st.session_state["theme"] == "light" else "☀️ Light Mode",
        key="theme_toggle",
        help="Toggle light/dark mode"
    )
    if switch:
        st.session_state["theme"] = "dark" if st.session_state["theme"] == "light" else "light"


# Theme color variables
if st.session_state["theme"] == "dark":
    main_bg = "#181922"
    main_fg = "#f5f5f5"
    side_bg = "#232635"
    side_fg = "#f5f5f5"
    heading_color = "#f5f5f5"
    body1_color = "#20253a"
    body2_color = "#f5f5f5"
    chat_bg = "#262844"
    chat_fg = "#fafbfc"
    header_bg = "#134a91"
    header_fg = "#fff"
    chat_input_bg = "#232635"
    chat_input_fg = "#f5f5f5"
    chat_input_border = "#484c64"
else:
    main_bg = "#f5f5f5"
    main_fg = "#181922"
    side_bg = "#fff"
    side_fg = "#232635"
    heading_color = "#181922"
    body1_color = "#36417d"
    body2_color = "#181922"
    chat_bg = "#fff"
    chat_fg = "#262844"
    header_bg = "#007BFF"
    header_fg = "#fff"
    chat_input_bg = "#fff"
    chat_input_fg = "#232635"
    chat_input_border = "#bfc5e0"

theme_css = f"""
<style>
body, .block-container, .main, .appview-container {{
    background: {main_bg} !important;
    color: {main_fg} !important;
}}
[data-testid="stSidebar"], .sidebar-content, .css-1d391kg {{
    background: {side_bg} !important;
    color: {side_fg} !important;
}}
h1, h2, h3, h4, h5, h6, .stTitle, .stHeader, .stSubheader {{
    color: {heading_color} !important;
}}
.chat-popup, .chat-footer, .chat-body, .chat-header {{
    background: {chat_bg} !important;
    color: {chat_fg} !important;
}}
.chat-header {{
    background: {header_bg} !important;
    color: {header_fg} !important;
}}
.chat-footer input {{
    background: {chat_input_bg} !important;
    color: {chat_input_fg} !important;
    border: 1px solid {chat_input_border} !important;
}}
</style>
"""

st.markdown(theme_css, unsafe_allow_html=True)

# Language dictionary with translations
content = {
    "English": {
        "title": "Welcome to Swarajya Scanner! 📜",
        "tagline": "Give every citizen a Constitution in their pocket, and the guts to use it.",
        "intro": "Swarajya Scanner empowers you with knowledge of your constitutional rights in your vernacular language. Ask questions, get answers, and defend your rights with confidence.",
        "get_started": "Get Started",
        "features_title": "Key Features",
        "features": [
            "📚 Multilingual Q&A: Get answers in your local language.",
            "🛡️ Rights Defense: Equip yourself with constitutional knowledge.",
            "🔍 Easy Search: Find answers quickly and easily.",
            "🤝 Community Support: Connect with others defending their rights.",
            "🔔 Notifications: Stay updated with relevant rights alerts."
        ],
        "footer": "© 2025 Swarajya Scanner. All rights reserved."
    },
    "తెలుగు": {
        "title": "స్వరాజ్య స్కానర్‌కు స్వాగతం! 📜",
        "tagline": "ప్రతి పౌరునికైనా తన జేబులో రాజ్యాంగం ఉండే ధైర్యం ఇవ్వండి.",
        "intro": "స్వరాజ్య స్కానర్ మీకు మీ స్థానిక భాషలో మీ రాజ్యాంగ హక్కుల జ్ఞానాన్ని ఇస్తుంది. ప్రశ్నలు అడగండి, జవాబులు పొందండి, మరియు మీ హక్కులను నమ్మకంతో రక్షించండి.",
        "get_started": "ప్రారంభించండి",
        "features_title": "ప్రధాన లక్షణాలు",
        "features": [
            "📚 బహుభాషా ప్రశ్నలు మరియు జవాబు: మీ స్థానిక భాషలో జవాబులు పొందండి.",
            "🛡️ హక్కుల రక్షణ: రాజ్యాంగ జ్ఞానంతో సుసజ్జితం అవ్వండి.",
            "🔍 సులభమైన శోధన: త్వరగా మరియు సులభంగా జవాబులు కనుగొనండి.",
            "🤝 సమాజ మద్దతు: హక్కులను రక్షిస్తున్న అందరితో కలసి ఉన్నారు.",
            "🔔 నోటిఫికేషన్లు: సంబంధిత హక్కుల తాజావార్తతో అప్‌డేట్ అవ్వండి."
        ],
        "footer": "© 2025 స్వరాజ్య స్కానర్. అన్ని హక్కులు సంరక్షితం."
    },
    "हिन्दी": {
        "title": "स्वराज्य स्कैनर में आपका स्वागत है! 📜",
        "tagline": "हर नागरिक के पास संविधान हो, और उसे इस्तेमाल करने का साहस भी हो।",
        "intro": "स्वराज्य स्कैनर आपको आपकी स्थानीय भाषा में आपके संवैधानिक अधिकारों का ज्ञान देता है। प्रश्न पूछें, उत्तर प्राप्त करें, और अपने अधिकारों की सुरक्षा करें।",
        "get_started": "शुरुआत करें",
        "features_title": "मुख्य विशेषताएँ",
        "features": [
            "📚 बहुभाषी प्रश्नोत्तर: अपनी भाषा में जवाब पाएं।",
            "🛡️ अधिकार रक्षा: संवैधानिक ज्ञान से सुसज्जित हों।",
            "🔍 आसान खोज: जल्दी और आसानी से उत्तर पाएं।",
            "🤝 समुदाय समर्थन: अपने अधिकारों की रक्षा करने वालों से जुड़ें।",
            "🔔 सूचनाएं: संबंधित अधिकारों से अपडेट रहें।"
        ],
        "footer": "© 2025 स्वराज्य स्कैनर। सर्वाधिकार सुरक्षित।"
    },
    # Add other languages similarly (Tamil, Kannada, Malayalam, Urdu) from your previous dictionary
}




# ─────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Homepage",
    "Document Scan",
    "Dashboard",
    "Results",
    "Leaderboard"
])

# ─────────────────────────────────────────
# PAGE: Homepage
# ─────────────────────────────────────────
if page == "Homepage":

    # Custom CSS for enhanced look and feel
    st.markdown("""
    <style>
    body {
        background-color: #f4f4f9;
        color: #333;
    }
    h1, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
    }
    h1 {
        color: #0050b3;
        font-weight: 700;
    }
    h3 {
        color: #0073e6;
        font-style: italic;
    }
    .stButton > button {
        background-color: #0073e6;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0050b3;
    }
    /* Center and set fixed max-width for selectbox container */
    .css-1v0mbdj.edgvbvh3 {
        max-width: 320px;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)

    # Language selection dropdown with reduced width and centered
    language = st.selectbox(
        "Select your language / अपनी भाषा चुनें",
        options=list(content.keys()),
        index=0
    )

    page_content = content[language]

    st.markdown(f"# {page_content['title']}")
    st.markdown(f"### {page_content['tagline']}")
    st.write(page_content['intro'])

    # Image slot below intro, centered
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.image(
            "Image.png",       # <-- Replace with your image path or URL
            use_column_width=True,
            caption="Swarajya Scanner"
        )

    # Get started button (dummy, no action for now)
    if st.button(page_content['get_started'], key="get_started_btn"):
        st.info("Let's get started!")

    st.markdown(f"### {page_content['features_title']}")
    for feature in page_content['features']:
        st.write(f"- {feature}")

    # Infographics - example metrics
    st.markdown("---")
    st.subheader("At a Glance")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Scans", "1045")
    col2.metric("Threats Detected", "3")
    col3.metric("Users Registered", "287")
    col4.metric("Documents Verified", "986")

    st.markdown(f"---\n<footer style='text-align:center; color:gray;'>{page_content['footer']}</footer>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# PAGE: Scan & Chatbot (merged)
# ─────────────────────────────────────────
elif page == "Document Scan":
    st.header("📤 Upload & Scan Documents")

    st.subheader("Upload Documents for Scanning")
    uploaded_file = st.file_uploader(
        "Upload a document or image", type=["png", "jpg", "jpeg", "pdf"])
    if uploaded_file:
        file_details = {"filename": uploaded_file.name, "type": uploaded_file.type}
        st.write("Uploaded File Details:", file_details)
        if uploaded_file.type in ["image/png", "image/jpg", "image/jpeg"]:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Image", use_column_width=True)
        st.success("✅ File uploaded successfully. Starting scan...")
        with st.spinner("Scanning..."):
            time.sleep(2)
            st.balloons()
            st.success("✅ Scan complete. No threats detected.")

# ─────────────────────────────────────────
# PAGE: Dashboard
# ─────────────────────────────────────────


elif page == "Dashboard":
    st.header("📊 Swarajya Scanner Dashboard")

    # Sample user past queries data - replace with real data source
    sample_queries = [
        {"query": "What are fundamental rights?", "url": "https://swarajyscanner.org/queries/1", "date": "2025-07-20"},
        {"query": "How to file a public grievance?", "url": "https://swarajyscanner.org/queries/2", "date": "2025-07-21"},
        {"query": "Right to education information", "url": "https://swarajyscanner.org/queries/3", "date": "2025-07-22"},
        {"query": "Latest constitutional amendments", "url": "https://swarajyscanner.org/queries/4", "date": "2025-07-23"},
        {"query": "Citizen duties overview", "url": "https://swarajyscanner.org/queries/5", "date": "2025-07-24"},
    ]

    # Convert to DataFrame for display
    df_queries = pd.DataFrame(sample_queries)
    df_queries['date'] = pd.to_datetime(df_queries['date'])

    # Simulate user activity data (e.g., queries per day) - replace with real
    today = datetime.today()
    dates = [today - timedelta(days=i) for i in range(15)]
    activity_counts = [1,2,1,3,0,4,2,1,3,2,5,1,0,2,3]
    df_activity = pd.DataFrame({"date": dates, "queries": activity_counts})
    df_activity = df_activity.sort_values("date")

    # --- Layout ---

    # Top: Account Settings button left aligned
    with st.container():
        col1, col2 = st.columns([1, 10])
        with col1:
            if st.button("⚙️ Account Settings"):
                st.info("Account Settings page coming soon!")
        with col2:
            st.markdown("<h1 style='text-align:center;'>Swarajya Scanner Dashboard</h1>", unsafe_allow_html=True)

    st.markdown("---")

    # Main dashboard: two columns
    col_left, col_right = st.columns([3, 5])

    with col_left:
        st.subheader("Your Past Queries")

        def make_clickable(url, text):
            return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'

        df_queries_display = df_queries.copy()
        df_queries_display['Query'] = df_queries_display.apply(lambda row: make_clickable(row['url'], row['query']), axis=1)
        df_queries_display['Date'] = df_queries_display['date'].dt.strftime('%Y-%m-%d')

        st.write(
            df_queries_display[['Query', 'Date']].to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

        st.markdown("---")

        # Additional metric or stats widgets
        total_queries = len(df_queries)
        most_recent_date = df_queries['date'].max().strftime('%Y-%m-%d')

        st.metric(label="Total Queries", value=total_queries)
        st.metric(label="Most Recent Query Date", value=most_recent_date)

    with col_right:
        st.subheader("Your Activity Over Time")
        fig = px.line(df_activity, x='date', y='queries', markers=True,
                      title='Queries Submitted Per Day',
                      labels={"date": "Date", "queries": "Number of Queries"})
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        st.subheader("Recent Activity")
        if activity_counts[-1] > 0:
            st.success(f"You submitted {activity_counts[-1]} queries today. Keep it up!")
        else:
            st.info("No queries submitted today. How about exploring some topics?")

        st.markdown("""
        ### Welcome to Swarajya Scanner!
        Explore the Constitution in your pocket, raise issues and track public discourse.
        - Use the 'Account Settings' to manage your profile.
        - Check your query history on the left.
        - View your activity trends on the right.
        """)

# ─────────────────────────────────────────
# PAGE: Results
# ─────────────────────────────────────────
elif page == "Results":
    st.header("📁 Scan Results")
    st.write("Previous scan data will appear here (simulated for now).")
    results_data = {
        "Document": ["ID_001.png", "Doc_002.pdf", "Visa_003.jpg"],
        "Status": ["Clean", "Clean", "Suspected Tampering"],
        "Confidence": ["99%", "98.5%", "76%"]
    }
    st.table(pd.DataFrame(results_data))

# ─────────────────────────────────────────
# PAGE: Leaderboard
# ─────────────────────────────────────────
elif page == "Leaderboard":
    st.title("🏆 Swarajya Scanner Leaderboard")

    # Example data for leaderboard (replace with real data from your backend)
    data = [
        {"Rank": 1, "Username": "raj_swaraj", "Points": 1500, "Profile": "https://swarajyscanner.org/users/raj_swaraj"},
        {"Rank": 2, "Username": "anita_jain", "Points": 1420, "Profile": "https://swarajyscanner.org/users/anita_jain"},
        {"Rank": 3, "Username": "vikram88", "Points": 1300, "Profile": "https://swarajyscanner.org/users/vikram88"},
        {"Rank": 4, "Username": "mira_das", "Points": 1200, "Profile": "https://swarajyscanner.org/users/mira_das"},
        {"Rank": 5, "Username": "suresh_k", "Points": 1150, "Profile": "https://swarajyscanner.org/users/suresh_k"},
        {"Rank": 6, "Username": "deepa_shah", "Points": 1100, "Profile": "https://swarajyscanner.org/users/deepa_shah"},
        {"Rank": 7, "Username": "prateek", "Points": 1050, "Profile": "https://swarajyscanner.org/users/prateek"},
        {"Rank": 8, "Username": "neha_verma", "Points": 930, "Profile": "https://swarajyscanner.org/users/neha_verma"},
        {"Rank": 9, "Username": "arvind_nair", "Points": 850, "Profile": "https://swarajyscanner.org/users/arvind_nair"},
        {"Rank": 10, "Username": "jyoti_m", "Points": 800, "Profile": "https://swarajyscanner.org/users/jyoti_m"},
    ]

    df = pd.DataFrame(data)

    # Search filter
    search_username = st.text_input("Search username", "")

    if search_username.strip():
        df_filtered = df[df['Username'].str.contains(search_username.strip(), case=False)]
    else:
        df_filtered = df.copy()

    # Sortable Table with clickable profile links
    def make_clickable(url, text):
        return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'

    df_filtered['Profile Link'] = df_filtered.apply(lambda row: make_clickable(row['Profile'], 'View Profile'), axis=1)
    df_display = df_filtered[['Rank', 'Username', 'Points', 'Profile Link']]

    st.markdown("### Leaderboard Table")
    st.write(
        df_display.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Summary stats
    total_users = len(df)
    top_user = df.loc[df['Points'].idxmax()]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users on Leaderboard", total_users)
    col2.metric("Top Scorer", top_user['Username'])
    col3.metric("Top Score", top_user['Points'])

    st.markdown("---")

    # Visual leaderboard - Bar chart of top 10
    st.markdown("### Top 10 Users by Points")
    fig = px.bar(
        df.sort_values('Points', ascending=False),
        x='Points',
        y='Username',
        orientation='h',
        text='Points',
        height=400,
        labels={'Points': 'Points', 'Username': 'User'},
        title="Top 10 Swarajya Scanner Contributors"
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis=dict(autorange="reversed"), margin=dict(l=100, r=20, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ---
    *Leaderboard ranks users based on points accumulated through contributions such as raising public issues, contributing to discussions, and community engagement.*
    """)

    # Optional: Add any other features/features like badges, filters for timeframe etc. here

# ─────────────────────────────────────────
# FOOTER / Aesthetic (remains the same)
# ─────────────────────────────────────────
st.markdown("""
<style>
    .css-1rs6os.edgvbvh3 {
        background: #0f1116;
        color: #fff;
    }
    .stButton>button {
        background-color: #e63946;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #ff595e;
        color: #000;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# FLOATING CHATBOT (Injected via HTML)
# ─────────────────────────────────────────

chat_html = """
<style>
.chat-icon {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    background-color: #007BFF;
    color: white;
    font-size: 28px;
    border-radius: 50%;
    border: none;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    cursor: pointer;
    z-index: 2147483647 !important;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.3s;
}
.chat-icon:hover {
    background-color: #0056b3;
}
/* Overlap guaranteed, never hidden */
.chat-popup {
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 350px;
    max-width: 96vw;
    height: 450px;
    max-height: 70vh;
    background: #fff;
    border-radius: 16px 16px 8px 16px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.20);
    display: none;
    flex-direction: column;
    overflow: hidden;
    z-index: 2147483647 !important;
    font-family: 'Segoe UI', Arial, sans-serif;
}
.chat-popup.active { display: flex; }
.chat-header {
    background-color: #007BFF;
    color: white;
    padding: 15px;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-align: left;
    border-bottom: 1px solid #0070df33;
    position: relative;
}
.chat-header .close-btn {
    position: absolute;
    right: 12px; top: 12px;
    color: white;
    background: transparent;
    font-size: 19px;
    border: none;
    cursor: pointer;
}
.chat-body {
    flex: 1;
    padding: 12px;
    overflow-y: auto;
    background: #f7f7fa;
    font-size: 15px;
}
.chat-footer {
    display: flex;
    padding: 10px 9px;
    border-top: 1px solid #eee;
    background: #fff;
}
.chat-footer input {
    flex: 1;
    padding: 9px 12px;
    border: 1px solid #ccc;
    border-radius: 13px;
    font-size: 15px;
    outline: none;
    margin-right: 6px;
}
.chat-footer button {
    padding: 8px 17px;
    background: #007BFF;
    border: none;
    border-radius: 11px;
    color: white;
    font-weight: 600;
    cursor: pointer;
    font-size: 15px;
    transition: background 0.2s;
}
.chat-footer button:hover { background: #0056b3; }
@media screen and (max-width:510px){
    .chat-popup { width: 97vw; height: 85vw; min-height: 290px; }
}
.chat-body::-webkit-scrollbar { width: 0; background: transparent;}
</style>

<button class="chat-icon" id="floatingBtn" title="Open chat" onclick="toggleChat()">💬</button>
<div class="chat-popup" id="chatPopup">
    <div class="chat-header">
        Swarajya Chatbot
        <button class="close-btn" onclick="toggleChat()" title="Close">&times;</button>
    </div>
    <div class="chat-body" id="chatBody"></div>
    <div class="chat-footer">
        <input type="text" id="chatInput" placeholder="Type a message..." autocomplete="off"
            onkeydown="if(event.key==='Enter'){sendMessage(); return false;}" />
        <button onclick="sendMessage()">Send</button>
    </div>
</div>
<script>
function toggleChat() {
    var popup = document.getElementById("chatPopup");
    if(!popup.classList.contains("active")) {
        popup.classList.add("active");
        document.getElementById("chatInput").focus();
    } else {
        popup.classList.remove("active");
    }
}
function scrollChatToBottom() {
    var body = document.getElementById("chatBody");
    setTimeout(function(){
        body.scrollTop = body.scrollHeight;
    },15);
}
function sendMessage() {
    var input = document.getElementById("chatInput");
    var msg = input.value.trim();
    if(msg) {
        var body = document.getElementById("chatBody");
        var userMsg = document.createElement("div");
        userMsg.innerHTML = "<span style='color:#267afe;font-weight:600'>You:</span> " + 
                    msg.replace(/</g,'&lt;').replace(/>/g,'&gt;');
        userMsg.style.marginBottom = "6px";
        body.appendChild(userMsg);

        input.value = '';

        // Bot echoes back
        setTimeout(function(){
            var botMsg = document.createElement("div");
            botMsg.innerHTML = "<span style='color:#ff4a4a;font-weight:600'>Bot:</span> I'm a chatbot with no integrated backend. You said “" + 
                    msg.replace(/</g,'&lt;').replace(/>/g,'&gt;') + "”";
            botMsg.style.marginBottom = "12px";
            body.appendChild(botMsg);
            scrollChatToBottom();
        }, 220);
        scrollChatToBottom();
    }
}
</script>
"""

# Ensure this is the LAST Streamlit command
components.html(chat_html, height=360)