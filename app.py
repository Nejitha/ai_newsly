import os
import streamlit as st
import feedparser
from openai import OpenAI

# ================= OPENAI CLIENT =================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ================= PAGE SETUP =================
st.set_page_config(
    page_title="Newsly",
    page_icon="📰",
    layout="wide"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
/* App background */
.stApp {
    background-color: #111827;
    color: #F3F4F6;
    font-family: 'Segoe UI', sans-serif;
}

/* Title */
.title {
    font-size: 48px;
    font-weight: 800;
    color: #F9FAFB;
    margin-bottom: 5px;
}

/* Description */
.description {
    font-size: 20px;
    color: #9CA3AF;
    margin-bottom: 35px;
}

/* Selectbox */
.stSelectbox > div > div {
    background-color: #1F2937;
    border-radius: 10px;
    color: #F3F4F6;
}

/* News card */
.summary {
    background-color: #1F2937;
    padding: 22px;
    border-radius: 14px;
    margin-bottom: 22px;
    border: 1px solid #374151;
}

/* Article link */
.article-link {
    color: #60A5FA;
    font-weight: 600;
    text-decoration: none;
}

/* Footer */
.footer {
    color: #6B7280;
    text-align: center;
    font-size: 14px;
    margin-top: 60px;
    padding-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown('<h1 class="title">📰 Newsly</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="description">'
    'Your AI-powered personal news curator. '
    'Choose a topic and language to get concise, readable news summaries instantly.'
    '</p>',
    unsafe_allow_html=True
)

# ================= INPUT SECTIONS =================
col1, col2 = st.columns(2)

with col1:
    category = st.selectbox(
        "Choose a topic",
        ["technology", "business", "sports", "science", "health", "entertainment"]
    )

with col2:
    language = st.selectbox(
        "Choose language",
        ["English", "Hindi", "Malayalam", "Tamil"]
    )

# ================= LANGUAGE MAP =================
language_map = {
    "English": {"hl": "en-IN", "ceid": "IN:en", "name": "English"},
    "Hindi": {"hl": "hi", "ceid": "IN:hi", "name": "Hindi"},
    "Malayalam": {"hl": "ml", "ceid": "IN:ml", "name": "Malayalam"},
    "Tamil": {"hl": "ta", "ceid": "IN:ta", "name": "Tamil"}
}

# ================= ACTION BUTTON =================
if st.button("Get News"):

    st.info("Fetching latest news articles...")

    lang = language_map[language]

    rss_url = (
        f"https://news.google.com/rss/search?"
        f"q={category}&hl={lang['hl']}&gl=IN&ceid={lang['ceid']}"
    )

    feed = feedparser.parse(rss_url)

    if not feed.entries:
        st.error("No articles found. Please try another topic.")
        st.stop()

    st.success(f"Found {len(feed.entries[:10])} articles. Summarizing with AI...")

    # ================= AI SUMMARIZATION =================
    for i, entry in enumerate(feed.entries[:10], 1):

        prompt = f"""
        Summarize the following news headline in 2–3 simple sentences.
        Write the summary in {lang['name']} language.

        Headline: {entry.title}
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful news summarizer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.4
            )

            summary = response.choices[0].message.content

        except Exception as e:
            summary = f"AI error: {e}"

        # ================= DISPLAY =================
        st.markdown(
            f'''
            <div class="summary">
                <h3>{i}. {entry.title}</h3>
                <p>{summary}</p>
                <a class="article-link" href="{entry.link}" target="_blank">
                    Read full article →
                </a>
            </div>
            ''',
            unsafe_allow_html=True
        )

# ================= FOOTER =================
st.markdown(
    '''
    <div class="footer">
        © 2025 <b>Newsly</b> · Built with ❤️ by Nejitha using Streamlit & OpenAI GPT<br>
        <a href="https://github.com/Nejitha/ai_newsly" target="_blank" style="color:#60A5FA;">
            View Source on GitHub
        </a>
    </div>
    ''',
    unsafe_allow_html=True
)
