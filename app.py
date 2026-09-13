import hashlib
import os
import streamlit as st

try:
    from google import genai
except ImportError:
    try:
        import google.genai as genai
    except ImportError:
        genai = None

# ============================================================
# 1. PAGE & STATE INITIALIZATION
# ============================================================
st.set_page_config(
    page_title="UniBridge Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize local session state database if it doesn't exist
if "users" not in st.session_state:
    st.session_state.users = [
        {
            "id": "u1",
            "name": "Alex Johnson",
            "email": "alex@unibridge.edu",
            "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
            "role": "Senior",
            "university": "ITECH College",
            "department": "Artificial Intelligence",
            "bio": "Senior AI student passionate about machine learning and neural networks.",
            "expertise": "Python, Machine Learning, TensorFlow"
        }
    ]

if "questions" not in st.session_state:
    st.session_state.questions = [
        {
            "id": "q1",
            "junior_id": "u2",
            "junior_name": "Sarah Connor",
            "target_senior_id": None,
            "title": "How to structure a Neural Network for image classification?",
            "details": "I'm working on a CNN project and struggling with the layer dimensions.",
            "department": "Artificial Intelligence",
            "status": "Unanswered",
            "created_at": "2026-06-01"
        }
    ]

if "answers" not in st.session_state:
    st.session_state.answers = []

if "auth_user" not in st.session_state:
    st.session_state.auth_user = None
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [{
        "role": "assistant",
        "content": "Hello! I am your UniBridge AI Assistant powered by Gemini. Ask me any question regarding programming, coursework, or career paths!"
    }]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ============================================================
# 2. DYNAMIC THEMING ENGINE
# ============================================================
is_dark = st.session_state.theme == "Dark"

bg_color = "#0F172A" if is_dark else "#F8FAFC"
card_bg = "#1E293B" if is_dark else "#FFFFFF"
text_color = "#F8FAFC" if is_dark else "#0F172A"
border_color = "#334155" if is_dark else "#CBD5E1"
accent_color = "#14B8A6" if is_dark else "#0D9488"
subtext_color = "#94A3B8" if is_dark else "#475569"
input_bg = "#334155" if is_dark else "#F1F5F9"
input_text = "#FFFFFF" if is_dark else "#0F172A"

st.markdown(f"""
<style>
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {card_bg} !important;
        border-right: 1px solid {border_color} !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}
    p, h1, h2, h3, h4, h5, h6, label, span, div {{
        color: {text_color} !important;
    }}
    input, textarea, select, [data-baseweb="select"] > div {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border-color: {border_color} !important;
    }}
    .card {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }}
    .top-header {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        padding: 16px 24px;
        border-radius: 12px;
        margin-bottom: 20px;
    }}
    .brand-name {{ color: {text_color} !important; font-size: 26px; font-weight: 800; display: inline-block; }}
    .brand-name span {{ color: {accent_color} !important; }}
    .stat-card {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }}
    .stat-number {{ font-size: 24px; font-weight: 800; color: {accent_color} !important; }}
    .stat-label {{ font-size: 13px; color: {subtext_color} !important; }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="top-header">
    <div class="brand-name">🎓 Uni<span>Bridge</span></div>
    <span style="float: right; font-size: 13px; margin-top: 8px;">Peer Mentorship & AI Guidance Platform</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🎨 APPEARANCE")
current_theme = st.sidebar.radio("UI Theme Mode", ["Dark", "Light"], index=0 if is_dark else 1, key="theme_radio")
if current_theme != st.session_state.theme:
    st.session_state.theme = current_theme
    st.rerun()

st.sidebar.markdown("---")

# ============================================================
# 3. AUTHENTICATION WORKFLOW
# ============================================================
if not st.session_state.auth_user:
    st.subheader("🔑 Access UniBridge")
    auth_tab1, auth_tab2 = st.tabs(["Login", "Register Account"])

    with auth_tab1:
        st.markdown("##### Existing User Login")
        with st.form("login_form"):
            login_email = st.text_input("Email Address")
            login_pass = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Sign In")

            if submit_login:
                if not login_email or not login_pass:
                    st.error("Please provide both email and password.")
                else:
                    hashed = hash_password(login_pass)
                    matched_user = next(
                        (u for u in st.session_state.users if u["email"] == login_email.strip().lower() and u["password_hash"] == hashed),
                        None
                    )
                    if matched_user:
                        st.session_state.auth_user = matched_user
                        st.success(f"Welcome back, {matched_user['name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid email address or password.")

    with auth_tab2:
        st.markdown("##### Register New Account")
        with st.form("reg_form"):
            reg_name = st.text_input("Full Name")
            reg_email = st.text_input("Email Address")
            reg_pass = st.text_input("Password", type="password")
            reg_role = st.selectbox("I am a:", ["Junior", "Senior"])
            reg_univ = st.text_input("University", value="ITECH College")
            reg_dept = st.text_input("Department", placeholder="e.g., Artificial Intelligence")
            reg_bio = st.text_area("Short Bio / Interests", placeholder="Describe your focus or goals...")
            reg_exp = st.text_input("Skills / Expertise", placeholder="e.g., Python, Web Dev, Data Science")

            submit_reg = st.form_submit_button("Create Account")

            if submit_reg:
                if not reg_name or not reg_email or not reg_pass or not reg_dept:
                    st.error("Please fill in all required fields.")
                else:
                    existing = any(u["email"] == reg_email.strip().lower() for u in st.session_state.users)
                    if existing:
                        st.error("An account with this email address already exists.")
                    else:
                        new_user = {
                            "id": f"u_{len(st.session_state.users) + 1}",
                            "name": reg_name.strip(),
                            "email": reg_email.strip().lower(),
                            "password_hash": hash_password(reg_pass),
                            "role": reg_role,
                            "university": reg_univ.strip(),
                            "department": reg_dept.strip(),
                            "bio": reg_bio.strip(),
                            "expertise": reg_exp.strip()
                        }
                        st.session_state.users.append(new_user)
                        st.success("Account created successfully! Please sign in using the Login tab.")
    st.stop()

# ============================================================
# 4. NAVIGATION & SIDEBAR CONTROL
# ============================================================
user = st.session_state.auth_user

st.sidebar.markdown(f"### 👤 {user['name']}")
st.sidebar.markdown(f"**Role:** `{user['role']}`  \n**Dept:** {user['department']}")
st.sidebar.markdown("---")

if user["role"] == "Junior":
    nav_options = ["Dashboard", "Ask Question", "My Questions & Answers", "Find Seniors", "AI Assistant", "Settings"]
else:
    nav_options = ["Dashboard", "Answer Questions", "Find Seniors", "AI Assistant", "Settings"]

selected_page = st.sidebar.radio("Navigation Menu", nav_options)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.auth_user = None
    st.rerun()

# ============================================================
# 5. DASHBOARDS
# ============================================================
if selected_page == "Dashboard":
    st.subheader(f"👋 Welcome, {user['name']}!")

    q_total = len(st.session_state.questions)
    q_answered = len([q for q in st.session_state.questions if q.get("status") == "Answered"])

    seniors_count = len([u for u in st.session_state.users if u.get("role") == "Senior"])
    juniors_count = len([u for u in st.session_state.users if u.get("role") == "Junior"])

    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f"<div class='stat-card'><div class='stat-number'>{q_total}</div><div class='stat-label'>Total Questions</div></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='stat-card'><div class='stat-number'>{q_answered}</div><div class='stat-label'>Resolved Questions</div></div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='stat-card'><div class='stat-number'>{seniors_count}</div><div class='stat-label'>Available Seniors</div></div>", unsafe_allow_html=True)
    m4.markdown(f"<div class='stat-card'><div class='stat-number'>{juniors_count}</div><div class='stat-label'>Registered Juniors</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if user["role"] == "Junior":
        st.markdown("##### 📌 Recent Community Questions")
        for q_data in st.session_state.questions[:5]:
            st.markdown(f"""
            <div class='card'>
                <b>{q_data.get('title')}</b> <span style='font-size:12px; color:{subtext_color}'>({q_data.get('department')})</span><br>
                <span style='font-size:13px;'>Asked by: {q_data.get('junior_name')} | Status: <code>{q_data.get('status')}</code></span>
            </div>
            """, unsafe_allow_html=True)

    elif user["role"] == "Senior":
        st.markdown("##### 📥 Open Questions Needing Help")
        open_q = [q for q in st.session_state.questions if q.get("status") == "Unanswered"]
        if not open_q:
            st.info("No unanswered questions right now. Great job!")
        else:
            for q_data in open_q:
                st.markdown(f"""
                <div class='card'>
                    <b>{q_data.get('title')}</b> <span style='font-size:12px; color:{subtext_color}'>({q_data.get('department')})</span><br>
                    <p style='font-size:14px; margin: 8px 0;'>{q_data.get('details')}</p>
                    <span style='font-size:12px; color:{subtext_color}'>Asked by {q_data.get('junior_name')}</span>
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# 6. JUNIOR WORKFLOW
# ============================================================
elif selected_page == "Ask Question" and user["role"] == "Junior":
    st.subheader("❓ Ask a Senior")

    seniors_docs = [u for u in st.session_state.users if u.get("role") == "Senior"]
    senior_options = {"General - Any Senior": None}
    for s in seniors_docs:
        senior_options[f"{s.get('name')} (Skills: {s.get('expertise', 'General')})"] = s.get("id")

    with st.form("ask_q_form"):
        q_title = st.text_input("Question Summary / Title")
        q_target = st.selectbox("Target Senior (Optional)", list(senior_options.keys()))
        q_dept = st.text_input("Department / Subject Category", value=user["department"])
        q_details = st.text_area("Detailed Explanation")

        submit_q = st.form_submit_button("Post Question")

        if submit_q:
            if not q_title or not q_details:
                st.error("Please provide both a title and detailed explanation.")
            else:
                new_q = {
                    "id": f"q_{len(st.session_state.questions) + 1}",
                    "junior_id": user["id"],
                    "junior_name": user["name"],
                    "target_senior_id": senior_options[q_target],
                    "title": q_title.strip(),
                    "details": q_details.strip(),
                    "department": q_dept.strip(),
                    "status": "Unanswered",
                    "created_at": "2026-06-01"
                }
                st.session_state.questions.append(new_q)
                st.success("Your question has been posted successfully!")

elif selected_page == "My Questions & Answers" and user["role"] == "Junior":
    st.subheader("📚 My Submitted Questions")

    my_q = [q for q in st.session_state.questions if q.get("junior_id") == user["id"]]

    if not my_q:
        st.info("You haven't asked any questions yet.")
    else:
        for q_data in my_q:
            st.markdown(f"""
            <div class='card'>
                <h4>{q_data.get('title')}</h4>
                <p>{q_data.get('details')}</p>
                <span style='font-size:12px; color:{subtext_color}'>Category: {q_data.get('department')} | Status: <b>{q_data.get('status')}</b></span>
            </div>
            """, unsafe_allow_html=True)

            ans_docs = [a for a in st.session_state.answers if a.get("question_id") == q_data.get("id")]
            if ans_docs:
                for a_data in ans_docs:
                    st.markdown(f"""
                    <div style='margin-left: 30px; background-color:{card_bg}; border-left: 3px solid {accent_color}; padding: 12px; margin-bottom: 10px;'>
                        <b>💬 Answer from {a_data.get('senior_name')}:</b>
                        <p style='margin-top: 6px;'>{a_data.get('answer_text')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("⏳ No answers posted for this question yet.")
            st.markdown("---")

# ============================================================
# 7. SENIOR WORKFLOW
# ============================================================
elif selected_page == "Answer Questions" and user["role"] == "Senior":
    st.subheader("📝 Answer Junior Questions")

    if not st.session_state.questions:
        st.info("No questions currently logged.")
    else:
        for q_data in st.session_state.questions:
            q_id = q_data.get("id")
            with st.expander(f"Q: {q_data.get('title')} (Asked by {q_data.get('junior_name')})"):
                st.write(f"**Details:** {q_data.get('details')}")

                ans_docs = [a for a in st.session_state.answers if a.get("question_id") == q_id]
                if ans_docs:
                    st.markdown("---")
                    st.markdown("**Existing Answers:**")
                    for a in ans_docs:
                        st.markdown(f"- *{a.get('senior_name')}*: {a.get('answer_text')}")

                st.markdown("---")
                with st.form(f"ans_form_{q_id}"):
                    ans_text = st.text_area("Your Response")
                    submit_ans = st.form_submit_button("Submit Response")

                    if submit_ans:
                        if not ans_text.strip():
                            st.error("Response cannot be empty.")
                        else:
                            new_ans = {
                                "question_id": q_id,
                                "senior_id": user["id"],
                                "senior_name": user["name"],
                                "answer_text": ans_text.strip(),
                                "created_at": "2026-06-01"
                            }
                            st.session_state.answers.append(new_ans)
                            q_data["status"] = "Answered"
                            st.success("Your answer has been saved!")
                            st.rerun()

# ============================================================
# 8. SENIOR DISCOVERY
# ============================================================
elif selected_page == "Find Seniors":
    st.subheader("🔍 Discover Seniors & Mentors")

    search_term = st.text_input("Search by Name, Expertise, or Department").strip().lower()
    seniors_docs = [u for u in st.session_state.users if u.get("role") == "Senior"]

    matching_seniors = []
    for s_data in seniors_docs:
        if search_term:
            if search_term in s_data.get('name', '').lower() or search_term in s_data.get('expertise', '').lower() or search_term in s_data.get('department', '').lower():
                matching_seniors.append(s_data)
        else:
            matching_seniors.append(s_data)

    if not matching_seniors:
        st.warning("No Seniors found matching your search criteria.")
    else:
        cols = st.columns(2)
        for idx, s in enumerate(matching_seniors):
            col = cols[idx % 2]
            with col:
                col.markdown(f"""
                <div class='card'>
                    <h4>👨‍🎓 {s.get('name')}</h4>
                    <b>🏫 {s.get('university')} | 📚 {s.get('department')}</b><br>
                    <p style='margin-top: 8px;'><b>Skills:</b> {s.get('expertise', 'General Mentorship')}</p>
                    <p style='font-size:13px; color:{subtext_color};'>{s.get('bio', 'No bio provided.')}</p>
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# 9. AI CHATBOT (GEMINI INTEGRATION)
# ============================================================
elif selected_page == "AI Assistant":
    st.subheader("🤖 Context-Aware AI Study Assistant")

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_prompt := st.chat_input("Type your question here..."):
        st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")

            if api_key and genai is not None:
                try:
                    client = genai.Client(api_key=api_key)
                    formatted_contents = [
                        {"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]}
                        for m in st.session_state.chat_messages
                    ]
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=formatted_contents
                    )
                    ai_response = response.text
                except Exception as e:
                    ai_response = f"⚠️ Gemini API issue: {str(e)}"
            else:
                ai_response = f"### Response for: '{user_prompt}'\n\nTo enable full AI responses, please configure your `GEMINI_API_KEY` under Streamlit Secrets. I see you are studying **{user['department']}**!"

            message_placeholder.markdown(ai_response)
            st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})

# ============================================================
# 10. SETTINGS
# ============================================================
elif selected_page == "Settings":
    st.subheader("⚙️ Account & Application Settings")

    with st.form("settings_form"):
        st.write(f"**Email:** `{user['email']}` (Read-only)")
        up_name = st.text_input("User Name", value=user["name"])
        up_univ = st.text_input("University", value=user["university"])
        up_dept = st.text_input("Department", value=user["department"])
        up_bio = st.text_area("Bio / Interests", value=user.get("bio", ""))
        up_exp = st.text_input("Skills / Expertise", value=user.get("expertise", ""))

        save_settings = st.form_submit_button("Save Settings")

        if save_settings:
            user["name"] = up_name.strip()
            user["university"] = up_univ.strip()
            user["department"] = up_dept.strip()
            user["bio"] = up_bio.strip()
            user["expertise"] = up_exp.strip()

            st.success("Settings updated successfully!")
            st.rerun()
