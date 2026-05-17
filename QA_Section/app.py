# # import streamlit as st
# # from query_pipeline import ask_question

# # # ======================================
# # # PAGE CONFIG
# # # ======================================
# # st.set_page_config(
# #     page_title="SBC QA System",
# #     layout="wide"
# # )

# # # ======================================
# # # TITLE
# # # ======================================
# # st.title("Health Insurance SBC QA System")

# # st.write("Ask questions about the SBC document.")

# # # ======================================
# # # QUESTION INPUT
# # # ======================================
# # question = st.text_input(
# #     "Enter your question:"
# # )

# # # ======================================
# # # ASK BUTTON
# # # ======================================
# # if st.button("Get Answer"):

# #     if question.strip() == "":
# #         st.warning("Please enter a question.")

# #     else:

# #         with st.spinner("Generating answer..."):

# #             try:

# #                 # ======================================
# #                 # RUN PIPELINE
# #                 # ======================================
# #                 result = ask_question(question)

# #                 # ======================================
# #                 # DISPLAY RESULTS
# #                 # ======================================
# #                 st.success("Answer Generated")

# #                 st.subheader("Answer")

# #                 st.write(result["answer"])

# #                 # ======================================
# #                 # METRICS
# #                 # ======================================
# #                 st.subheader("LLM Metrics")

# #                 col1, col2, col3 = st.columns(3)

# #                 col1.metric(
# #                     "Input Tokens",
# #                     result["prompt_tokens"]
# #                 )

# #                 col2.metric(
# #                     "Output Tokens",
# #                     result["completion_tokens"]
# #                 )

# #                 col3.metric(
# #                     "Total Tokens",
# #                     result["total_tokens"]
# #                 )

# #                 st.subheader("Performance")

# #                 col4, col5 = st.columns(2)

# #                 col4.metric(
# #                     "Response Time (s)",
# #                     result["total_time"]
# #                 )

# #                 col5.metric(
# #                     "Total Cost ($)",
# #                     result["total_cost"]
# #                 )

# #             except Exception as e:

# #                 st.error(f"Error: {e}")






# import streamlit as st
# from query_pipeline import ask_question

# # ======================================
# # PAGE CONFIG
# # ======================================
# st.set_page_config(
#     page_title="SBC QA System",
#     layout="wide"
# )

# st.title("Health Insurance SBC QA System")

# # ======================================
# # SESSION STATE
# # ======================================
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # ======================================
# # DISPLAY CHAT HISTORY
# # ======================================
# for message in st.session_state.messages:

#     with st.chat_message(message["role"]):

#         st.markdown(message["content"])

#         # Show metrics for assistant only
#         if message["role"] == "assistant":

#             if "metrics" in message:

#                 metrics = message["metrics"]

#                 st.divider()

#                 col1, col2, col3 = st.columns(3)

#                 col1.metric(
#                     "Input Tokens",
#                     metrics["prompt_tokens"]
#                 )

#                 col2.metric(
#                     "Output Tokens",
#                     metrics["completion_tokens"]
#                 )

#                 col3.metric(
#                     "Total Tokens",
#                     metrics["total_tokens"]
#                 )

#                 col4, col5 = st.columns(2)

#                 col4.metric(
#                     "Response Time (s)",
#                     metrics["total_time"]
#                 )

#                 col5.metric(
#                     "Total Cost ($)",
#                     metrics["total_cost"]
#                 )

# # ======================================
# # CHAT INPUT
# # ======================================
# question = st.chat_input(
#     "Ask a question about the SBC document..."
# )

# # ======================================
# # PROCESS QUESTION
# # ======================================
# if question:

#     # USER MESSAGE
#     st.session_state.messages.append({
#         "role": "user",
#         "content": question
#     })

#     with st.chat_message("user"):
#         st.markdown(question)

#     # ASSISTANT MESSAGE
#     with st.chat_message("assistant"):

#         with st.spinner("Generating answer..."):

#             try:

#                 result = ask_question(question)

#                 answer = result["answer"]
#                 answer = answer.replace("`", "")
#                 st.markdown(answer)

#                 st.divider()

#                 col1, col2, col3 = st.columns(3)

#                 col1.metric(
#                     "Input Tokens",
#                     result["prompt_tokens"]
#                 )

#                 col2.metric(
#                     "Output Tokens",
#                     result["completion_tokens"]
#                 )

#                 col3.metric(
#                     "Total Tokens",
#                     result["total_tokens"]
#                 )

#                 col4, col5 = st.columns(2)

#                 col4.metric(
#                     "Response Time (s)",
#                     result["total_time"]
#                 )

#                 col5.metric(
#                     "Total Cost ($)",
#                     result["total_cost"]
#                 )

#                 # SAVE CHAT HISTORY
#                 st.session_state.messages.append({
#                     "role": "assistant",
#                     "content": answer,
#                     "metrics": {
#                         "prompt_tokens": result["prompt_tokens"],
#                         "completion_tokens": result["completion_tokens"],
#                         "total_tokens": result["total_tokens"],
#                         "total_time": result["total_time"],
#                         "total_cost": result["total_cost"]
#                     }
#                 })

#             except Exception as e:

#                 st.error(f"Error: {e}")












# import streamlit as st
# from datetime import datetime

# # ======================================
# # PAGE CONFIG
# # ======================================
# st.set_page_config(
#     page_title="SBC QA System",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ======================================
# # CUSTOM CSS — Vibrant Glassmorphism Theme
# # ======================================
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

# /* ---- ROOT VARIABLES ---- */
# :root {
#     --bg-dark:       #0d0f1a;
#     --bg-card:       rgba(255,255,255,0.05);
#     --accent-1:      #7c3aed;
#     --accent-2:      #06b6d4;
#     --accent-3:      #f59e0b;
#     --accent-4:      #ec4899;
#     --text-main:     #e2e8f0;
#     --text-muted:    #94a3b8;
#     --border:        rgba(255,255,255,0.08);
#     --glow-purple:   rgba(124,58,237,0.4);
#     --glow-cyan:     rgba(6,182,212,0.3);
# }

# /* ---- GLOBAL ---- */
# html, body, .stApp {
#     background: var(--bg-dark) !important;
#     font-family: 'Space Grotesk', sans-serif !important;
#     color: var(--text-main) !important;
# }

# .stApp {
#     background: radial-gradient(ellipse at 20% 10%, rgba(124,58,237,0.18) 0%, transparent 55%),
#                 radial-gradient(ellipse at 80% 80%, rgba(6,182,212,0.12) 0%, transparent 55%),
#                 radial-gradient(ellipse at 50% 50%, rgba(236,72,153,0.06) 0%, transparent 70%),
#                 #0d0f1a !important;
# }

# /* ---- SIDEBAR ---- */
# [data-testid="stSidebar"] {
#     background: rgba(13,15,26,0.95) !important;
#     border-right: 1px solid var(--border) !important;
#     backdrop-filter: blur(20px) !important;
# }

# [data-testid="stSidebar"] > div:first-child {
#     padding: 1.5rem 1rem !important;
# }

# /* ---- SIDEBAR TITLE ---- */
# .sidebar-brand {
#     font-family: 'Syne', sans-serif;
#     font-size: 1.4rem;
#     font-weight: 800;
#     background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
#     margin-bottom: 0.25rem;
# }

# .sidebar-subtitle {
#     font-size: 0.72rem;
#     color: var(--text-muted);
#     letter-spacing: 0.12em;
#     text-transform: uppercase;
#     margin-bottom: 1.5rem;
# }

# /* ---- HISTORY ITEMS ---- */
# .history-item {
#     background: var(--bg-card);
#     border: 1px solid var(--border);
#     border-radius: 10px;
#     padding: 0.65rem 0.85rem;
#     margin-bottom: 0.5rem;
#     cursor: pointer;
#     transition: all 0.2s ease;
#     position: relative;
#     overflow: hidden;
# }

# .history-item::before {
#     content: '';
#     position: absolute;
#     left: 0; top: 0; bottom: 0;
#     width: 3px;
#     background: linear-gradient(180deg, var(--accent-1), var(--accent-2));
#     border-radius: 3px 0 0 3px;
# }

# .history-item:hover {
#     background: rgba(124,58,237,0.12);
#     border-color: rgba(124,58,237,0.35);
#     transform: translateX(2px);
# }

# .history-question {
#     font-size: 0.8rem;
#     color: var(--text-main);
#     font-weight: 500;
#     white-space: nowrap;
#     overflow: hidden;
#     text-overflow: ellipsis;
#     max-width: 200px;
# }

# .history-time {
#     font-size: 0.65rem;
#     color: var(--text-muted);
#     margin-top: 0.15rem;
# }

# .history-badge {
#     display: inline-block;
#     font-size: 0.6rem;
#     background: rgba(6,182,212,0.15);
#     color: var(--accent-2);
#     border: 1px solid rgba(6,182,212,0.3);
#     border-radius: 99px;
#     padding: 1px 7px;
#     margin-top: 0.3rem;
# }

# /* ---- MAIN HEADER ---- */
# .main-header {
#     text-align: center;
#     padding: 2rem 1rem 1.5rem;
#     margin-bottom: 1rem;
# }

# .main-title {
#     font-family: 'Syne', sans-serif;
#     font-size: 2.6rem;
#     font-weight: 800;
#     background: linear-gradient(135deg, #a78bfa 0%, #38bdf8 50%, #f472b6 100%);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
#     line-height: 1.1;
#     margin-bottom: 0.5rem;
# }

# .main-tagline {
#     font-size: 0.9rem;
#     color: var(--text-muted);
#     letter-spacing: 0.05em;
# }

# /* ---- DIVIDER ---- */
# .gradient-divider {
#     height: 2px;
#     background: linear-gradient(90deg, transparent, var(--accent-1), var(--accent-2), var(--accent-4), transparent);
#     border: none;
#     margin: 0.5rem 0 1.5rem;
#     border-radius: 2px;
# }

# /* ---- CHAT MESSAGES ---- */
# [data-testid="stChatMessage"] {
#     background: var(--bg-card) !important;
#     border: 1px solid var(--border) !important;
#     border-radius: 16px !important;
#     backdrop-filter: blur(12px) !important;
#     margin-bottom: 1rem !important;
#     padding: 1rem 1.25rem !important;
# }

# /* USER bubble accent */
# [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
#     border-color: rgba(124,58,237,0.35) !important;
#     box-shadow: 0 0 20px rgba(124,58,237,0.12) !important;
# }

# /* ASSISTANT bubble accent */
# [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
#     border-color: rgba(6,182,212,0.25) !important;
#     box-shadow: 0 0 20px rgba(6,182,212,0.08) !important;
# }

# /* ---- METRICS ---- */
# [data-testid="stMetric"] {
#     background: rgba(255,255,255,0.03) !important;
#     border: 1px solid var(--border) !important;
#     border-radius: 12px !important;
#     padding: 0.75rem 1rem !important;
# }

# [data-testid="stMetricLabel"] {
#     font-size: 0.7rem !important;
#     color: var(--text-muted) !important;
#     letter-spacing: 0.08em !important;
#     text-transform: uppercase !important;
# }

# [data-testid="stMetricValue"] {
#     font-family: 'Space Grotesk', sans-serif !important;
#     font-weight: 600 !important;
#     font-size: 1.1rem !important;
#     color: var(--text-main) !important;
# }

# /* Color-code individual metrics */
# div[data-testid="column"]:nth-child(1) [data-testid="stMetricValue"] { color: #a78bfa !important; }
# div[data-testid="column"]:nth-child(2) [data-testid="stMetricValue"] { color: #38bdf8 !important; }
# div[data-testid="column"]:nth-child(3) [data-testid="stMetricValue"] { color: #34d399 !important; }
# div[data-testid="column"]:nth-child(4) [data-testid="stMetricValue"] { color: #f59e0b !important; }
# div[data-testid="column"]:nth-child(5) [data-testid="stMetricValue"] { color: #f472b6 !important; }

# /* ---- CHAT INPUT ---- */
# [data-testid="stChatInput"] {
#     border-radius: 14px !important;
#     background: rgba(255,255,255,0.04) !important;
#     border: 1px solid rgba(124,58,237,0.4) !important;
#     box-shadow: 0 0 0 0 transparent;
#     transition: box-shadow 0.3s;
# }

# [data-testid="stChatInput"]:focus-within {
#     box-shadow: 0 0 0 3px rgba(124,58,237,0.25) !important;
#     border-color: rgba(124,58,237,0.7) !important;
# }

# [data-testid="stChatInput"] textarea {
#     color: var(--text-main) !important;
#     font-family: 'Space Grotesk', sans-serif !important;
# }

# /* ---- SPINNER ---- */
# .stSpinner > div {
#     border-top-color: var(--accent-1) !important;
# }

# /* ---- SCROLLBAR ---- */
# ::-webkit-scrollbar { width: 5px; height: 5px; }
# ::-webkit-scrollbar-track { background: transparent; }
# ::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.4); border-radius: 99px; }
# ::-webkit-scrollbar-thumb:hover { background: var(--accent-1); }

# /* ---- DIVIDER inside chat ---- */
# hr {
#     border-color: var(--border) !important;
#     margin: 0.75rem 0 !important;
# }

# /* ---- BUTTONS ---- */
# .stButton > button {
#     background: linear-gradient(135deg, var(--accent-1), var(--accent-2)) !important;
#     color: #fff !important;
#     border: none !important;
#     border-radius: 10px !important;
#     font-family: 'Space Grotesk', sans-serif !important;
#     font-weight: 600 !important;
#     font-size: 0.8rem !important;
#     padding: 0.4rem 1rem !important;
#     transition: opacity 0.2s, transform 0.1s !important;
#     width: 100%;
# }

# .stButton > button:hover {
#     opacity: 0.85 !important;
#     transform: translateY(-1px) !important;
# }

# /* Stats summary banner */
# .stats-banner {
#     display: flex;
#     gap: 1rem;
#     padding: 0.65rem 1rem;
#     background: rgba(255,255,255,0.03);
#     border: 1px solid var(--border);
#     border-radius: 12px;
#     margin-bottom: 1.2rem;
#     flex-wrap: wrap;
# }

# .stat-chip {
#     font-size: 0.72rem;
#     color: var(--text-muted);
# }

# .stat-chip span {
#     font-weight: 700;
#     color: var(--text-main);
# }

# /* Empty state */
# .empty-state {
#     text-align: center;
#     padding: 3rem 1rem;
#     color: var(--text-muted);
# }

# .empty-icon {
#     font-size: 3rem;
#     margin-bottom: 1rem;
#     opacity: 0.5;
# }

# .empty-title {
#     font-family: 'Syne', sans-serif;
#     font-size: 1.2rem;
#     color: var(--text-main);
#     margin-bottom: 0.4rem;
# }

# .section-label {
#     font-size: 0.65rem;
#     letter-spacing: 0.14em;
#     text-transform: uppercase;
#     color: var(--text-muted);
#     margin: 1rem 0 0.5rem 0.25rem;
# }
# </style>
# """, unsafe_allow_html=True)


# # ======================================
# # SESSION STATE
# # ======================================
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "search_history" not in st.session_state:
#     st.session_state.search_history = []

# if "total_cost_all" not in st.session_state:
#     st.session_state.total_cost_all = 0.0

# if "total_tokens_all" not in st.session_state:
#     st.session_state.total_tokens_all = 0

# if "selected_history" not in st.session_state:
#     st.session_state.selected_history = None


# # ======================================
# # SIDEBAR — SEARCH HISTORY
# # ======================================
# with st.sidebar:
#     st.markdown('<div class="sidebar-brand">⚡ SBC QA</div>', unsafe_allow_html=True)
#     st.markdown('<div class="sidebar-subtitle">Health Insurance Assistant</div>', unsafe_allow_html=True)

#     # Clear history button
#     if st.session_state.search_history:
#         if st.button("🗑️ Clear History"):
#             st.session_state.messages = []
#             st.session_state.search_history = []
#             st.session_state.total_cost_all = 0.0
#             st.session_state.total_tokens_all = 0
#             st.rerun()

#     st.markdown('<div class="section-label">📋 Search History</div>', unsafe_allow_html=True)

#     if not st.session_state.search_history:
#         st.markdown("""
#         <div style="text-align:center; padding: 1.5rem 0; color: #475569; font-size: 0.8rem;">
#             No searches yet.<br>Ask your first question!
#         </div>
#         """, unsafe_allow_html=True)
#     else:
#         for i, item in enumerate(reversed(st.session_state.search_history)):
#             idx = len(st.session_state.search_history) - 1 - i
#             q_short = item["question"][:45] + "…" if len(item["question"]) > 45 else item["question"]
#             st.markdown(f"""
#             <div class="history-item">
#                 <div class="history-question">💬 {q_short}</div>
#                 <div class="history-time">🕒 {item['timestamp']}</div>
#                 <div class="history-badge">⚡ {item.get('total_tokens', '—')} tokens</div>
#             </div>
#             """, unsafe_allow_html=True)

#     # Session summary at bottom of sidebar
#     if st.session_state.search_history:
#         st.markdown("---")
#         st.markdown('<div class="section-label">📊 Session Stats</div>', unsafe_allow_html=True)
#         st.markdown(f"""
#         <div style="font-size:0.78rem; color:#94a3b8; line-height:1.8;">
#             🔢 <b style="color:#e2e8f0;">{len(st.session_state.search_history)}</b> questions asked<br>
#             🪙 <b style="color:#a78bfa;">{st.session_state.total_tokens_all:,}</b> total tokens<br>
#             💵 <b style="color:#34d399;">${st.session_state.total_cost_all:.4f}</b> total cost
#         </div>
#         """, unsafe_allow_html=True)


# # ======================================
# # MAIN CONTENT
# # ======================================
# st.markdown("""
# <div class="main-header">
#     <div class="main-title">Health Insurance SBC QA</div>
#     <div class="main-tagline">Ask anything about your Summary of Benefits and Coverage document</div>
# </div>
# <div class="gradient-divider"></div>
# """, unsafe_allow_html=True)


# # ======================================
# # DISPLAY CHAT HISTORY
# # ======================================
# if not st.session_state.messages:
#     st.markdown("""
#     <div class="empty-state">
#         <div class="empty-icon">🏥</div>
#         <div class="empty-title">Ready to Answer Your Questions</div>
#         <p style="font-size:0.85rem;">Type a question below about deductibles, copays, network coverage, and more.</p>
#     </div>
#     """, unsafe_allow_html=True)
# else:
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#             if message["role"] == "assistant" and "metrics" in message:
#                 metrics = message["metrics"]
#                 st.divider()
#                 col1, col2, col3 = st.columns(3)
#                 col1.metric("📥 Input Tokens",  metrics["prompt_tokens"])
#                 col2.metric("📤 Output Tokens", metrics["completion_tokens"])
#                 col3.metric("🔢 Total Tokens",  metrics["total_tokens"])
#                 col4, col5 = st.columns(2)
#                 col4.metric("⏱️ Response Time (s)", metrics["total_time"])
#                 col5.metric("💵 Cost ($)",          metrics["total_cost"])


# # ======================================
# # CHAT INPUT
# # ======================================
# question = st.chat_input("Ask about deductibles, copays, network coverage…")

# # ======================================
# # PROCESS QUESTION
# # ======================================
# if question:
#     # USER MESSAGE
#     st.session_state.messages.append({"role": "user", "content": question})
#     with st.chat_message("user"):
#         st.markdown(question)

#     # ASSISTANT MESSAGE
#     with st.chat_message("assistant"):
#         with st.spinner("✨ Searching through your SBC document…"):
#             try:
#                 from query_pipeline import ask_question
#                 result = ask_question(question)

#                 answer = result["answer"].replace("`", "")
#                 st.markdown(answer)

#                 st.divider()
#                 col1, col2, col3 = st.columns(3)
#                 col1.metric("📥 Input Tokens",  result["prompt_tokens"])
#                 col2.metric("📤 Output Tokens", result["completion_tokens"])
#                 col3.metric("🔢 Total Tokens",  result["total_tokens"])
#                 col4, col5 = st.columns(2)
#                 col4.metric("⏱️ Response Time (s)", result["total_time"])
#                 col5.metric("💵 Cost ($)",          result["total_cost"])

#                 # SAVE TO CHAT HISTORY
#                 st.session_state.messages.append({
#                     "role": "assistant",
#                     "content": answer,
#                     "metrics": {
#                         "prompt_tokens":    result["prompt_tokens"],
#                         "completion_tokens": result["completion_tokens"],
#                         "total_tokens":     result["total_tokens"],
#                         "total_time":       result["total_time"],
#                         "total_cost":       result["total_cost"]
#                     }
#                 })

#                 # SAVE TO SEARCH HISTORY
#                 st.session_state.search_history.append({
#                     "question":    question,
#                     "answer":      answer,
#                     "timestamp":   datetime.now().strftime("%b %d, %H:%M"),
#                     "total_tokens": result["total_tokens"],
#                     "total_cost":  result["total_cost"]
#                 })

#                 # UPDATE SESSION TOTALS
#                 try:
#                     st.session_state.total_tokens_all += int(result["total_tokens"])
#                     st.session_state.total_cost_all   += float(result["total_cost"])
#                 except Exception:
#                     pass

#                 st.rerun()

#             except ImportError:
#                 # Demo mode when query_pipeline is not available
#                 demo_answer = f"*(Demo mode — `query_pipeline` not found)*\n\nYou asked: **{question}**"
#                 st.markdown(demo_answer)
#                 st.session_state.messages.append({
#                     "role": "assistant",
#                     "content": demo_answer
#                 })
#                 st.session_state.search_history.append({
#                     "question":    question,
#                     "answer":      demo_answer,
#                     "timestamp":   datetime.now().strftime("%b %d, %H:%M"),
#                     "total_tokens": 0,
#                     "total_cost":  0.0
#                 })
#                 st.rerun()

#             except Exception as e:
#                 st.error(f"❌ Error: {e}")







import streamlit as st
from datetime import datetime
import time
# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="SBC QA System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================
# CUSTOM CSS — Vibrant Glassmorphism Theme
# ======================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

/* ---- ROOT VARIABLES ---- */
:root {
    --bg-dark:       #081210;
    --bg-card:       rgba(255,255,255,0.05);
    --accent-1:      #16a34a;
    --accent-2:      #4ade80;
    --accent-3:      #86efac;
    --accent-4:      #bbf7d0;
    --text-main:     #e2e8f0;
    --text-muted:    #94a3b8;
    --border:        rgba(255,255,255,0.08);
    --glow-green1:   rgba(22,163,74,0.4);
    --glow-green2:   rgba(74,222,128,0.3);
}

/* ---- GLOBAL ---- */
html, body, .stApp {
    background: var(--bg-dark) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-main) !important;
}

.stApp {
    background: radial-gradient(ellipse at 20% 10%, rgba(22,163,74,0.18) 0%, transparent 55%),
                radial-gradient(ellipse at 80% 80%, rgba(74,222,128,0.12) 0%, transparent 55%),
                radial-gradient(ellipse at 50% 50%, rgba(134,239,172,0.06) 0%, transparent 70%),
                #081210 !important;
}

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: rgba(8,18,16,0.97) !important;
    border-right: 1px solid var(--border) !important;
    backdrop-filter: blur(20px) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1rem !important;
}

/* ---- SIDEBAR TITLE ---- */
.sidebar-brand {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}

.sidebar-subtitle {
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* ---- HISTORY ITEMS ---- */
.history-item {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.65rem 0.85rem;
    margin-bottom: 0.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}

.history-item::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--accent-1), var(--accent-2));
    border-radius: 3px 0 0 3px;
}

.history-item:hover {
    background: rgba(22,163,74,0.12);
    border-color: rgba(22,163,74,0.35);
    transform: translateX(2px);
}

.history-question {
    font-size: 0.8rem;
    color: var(--text-main);
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 200px;
}

.history-time {
    font-size: 0.65rem;
    color: var(--text-muted);
    margin-top: 0.15rem;
}

.history-badge {
    display: inline-block;
    font-size: 0.6rem;
    background: rgba(74,222,128,0.12);
    color: var(--accent-2);
    border: 1px solid rgba(74,222,128,0.3);
    border-radius: 99px;
    padding: 1px 7px;
    margin-top: 0.3rem;
}

/* ---- MAIN HEADER ---- */
.main-header {
    text-align: center;
    padding: 2rem 1rem 1.5rem;
    margin-bottom: 1rem;
}

.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #4ade80 0%, #16a34a 50%, #86efac 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}

.main-tagline {
    font-size: 0.9rem;
    color: var(--text-muted);
    letter-spacing: 0.05em;
}

/* ---- DIVIDER ---- */
.gradient-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-1), var(--accent-2), var(--accent-3), transparent);
    border: none;
    margin: 0.5rem 0 1.5rem;
    border-radius: 2px;
}

/* ---- CHAT MESSAGES ---- */
[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(12px) !important;
    margin-bottom: 1rem !important;
    padding: 1rem 1.25rem !important;
}

/* USER bubble accent */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    border-color: rgba(22,163,74,0.4) !important;
    box-shadow: 0 0 20px rgba(22,163,74,0.12) !important;
}

/* ASSISTANT bubble accent */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-color: rgba(74,222,128,0.3) !important;
    box-shadow: 0 0 20px rgba(74,222,128,0.1) !important;
}

/* ---- METRICS ---- */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.7rem !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    color: var(--text-main) !important;
}

/* Color-code individual metrics */
div[data-testid="column"]:nth-child(1) [data-testid="stMetricValue"] { color: #4ade80 !important; }
div[data-testid="column"]:nth-child(2) [data-testid="stMetricValue"] { color: #86efac !important; }
div[data-testid="column"]:nth-child(3) [data-testid="stMetricValue"] { color: #16a34a !important; }
div[data-testid="column"]:nth-child(4) [data-testid="stMetricValue"] { color: #bbf7d0 !important; }
div[data-testid="column"]:nth-child(5) [data-testid="stMetricValue"] { color: #34d399 !important; }

/* ---- CHAT INPUT ---- */
[data-testid="stChatInput"] {
    border-radius: 14px !important;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(22,163,74,0.4) !important;
    box-shadow: 0 0 0 0 transparent;
    transition: box-shadow 0.3s;
}

[data-testid="stChatInput"]:focus-within {
    box-shadow: 0 0 0 3px rgba(22,163,74,0.25) !important;
    border-color: rgba(22,163,74,0.7) !important;
}

[data-testid="stChatInput"] textarea {
    color: var(--text-main) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ---- SPINNER ---- */
.stSpinner > div {
    border-top-color: var(--accent-1) !important;
}

/* ---- SCROLLBAR ---- */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(22,163,74,0.4); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-1); }

/* ---- DIVIDER inside chat ---- */
hr {
    border-color: var(--border) !important;
    margin: 0.75rem 0 !important;
}

/* ---- BUTTONS ---- */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    padding: 0.4rem 1rem !important;
    transition: opacity 0.2s, transform 0.1s !important;
    width: 100%;
}

.stButton > button:hover {
    opacity: 0.85 !important;
    transform: translateY(-1px) !important;
}

/* Stats summary banner */
.stats-banner {
    display: flex;
    gap: 1rem;
    padding: 0.65rem 1rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
}

.stat-chip {
    font-size: 0.72rem;
    color: var(--text-muted);
}

.stat-chip span {
    font-weight: 700;
    color: var(--text-main);
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--text-muted);
}

.empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

.empty-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    color: var(--text-main);
    margin-bottom: 0.4rem;
}

.section-label {
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin: 1rem 0 0.5rem 0.25rem;
}
</style>
""", unsafe_allow_html=True)


# ======================================
# SESSION STATE
# ======================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "search_history" not in st.session_state:
    st.session_state.search_history = []

if "total_cost_all" not in st.session_state:
    st.session_state.total_cost_all = 0.0

if "total_tokens_all" not in st.session_state:
    st.session_state.total_tokens_all = 0

if "selected_history" not in st.session_state:
    st.session_state.selected_history = None


# ======================================
# SIDEBAR — SEARCH HISTORY
# ======================================
with st.sidebar:
    st.markdown('<div class="sidebar-brand">⚡ SBC QA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Health Insurance Assistant</div>', unsafe_allow_html=True)

    # Clear history button
    if st.session_state.search_history:
        if st.button("🗑️ Clear History"):
            st.session_state.messages = []
            st.session_state.search_history = []
            st.session_state.total_cost_all = 0.0
            st.session_state.total_tokens_all = 0
            st.rerun()

    st.markdown('<div class="section-label">📋 Search History</div>', unsafe_allow_html=True)

    if not st.session_state.search_history:
        st.markdown("""
        <div style="text-align:center; padding: 1.5rem 0; color: #475569; font-size: 0.8rem;">
            No searches yet.<br>Ask your first question!
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, item in enumerate(reversed(st.session_state.search_history)):
            idx = len(st.session_state.search_history) - 1 - i
            q_short = item["question"][:45] + "…" if len(item["question"]) > 45 else item["question"]
            st.markdown(f"""
            <div class="history-item">
                <div class="history-question">💬 {q_short}</div>
                <div class="history-time">🕒 {item['timestamp']}</div>
                <div class="history-badge">⚡ {item.get('total_tokens', '—')} tokens</div>
            </div>
            """, unsafe_allow_html=True)

    # Session summary at bottom of sidebar
    if st.session_state.search_history:
        st.markdown("---")
        st.markdown('<div class="section-label">📊 Session Stats</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:0.78rem; color:#94a3b8; line-height:1.8;">
            🔢 <b style="color:#e2e8f0;">{len(st.session_state.search_history)}</b> questions asked<br>
            🪙 <b style="color:#a78bfa;">{st.session_state.total_tokens_all:,}</b> total tokens<br>
            💵 <b style="color:#34d399;">${st.session_state.total_cost_all:.4f}</b> total cost
        </div>
        """, unsafe_allow_html=True)


# ======================================
# MAIN CONTENT
# ======================================
st.markdown("""
<div class="main-header">
    <div class="main-title">Health Insurance SBC QA</div>
    <div class="main-tagline">Ask anything about your Summary of Benefits and Coverage document</div>
</div>
<div class="gradient-divider"></div>
""", unsafe_allow_html=True)


# ======================================
# DISPLAY CHAT HISTORY
# ======================================
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🏥</div>
        <div class="empty-title">Ready to Answer Your Questions</div>
        <p style="font-size:0.85rem;">Type a question below about deductibles, copays, network coverage, and more.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant" and "metrics" in message:
                metrics = message["metrics"]
                st.divider()
                col1, col2, col3 = st.columns(3)
                col1.metric("📥 Input Tokens",  metrics["prompt_tokens"])
                col2.metric("📤 Output Tokens", metrics["completion_tokens"])
                col3.metric("🔢 Total Tokens",  metrics["total_tokens"])
                col4, col5 = st.columns(2)
                col4.metric("⏱️ Response Time (s)", metrics["total_time"])
                col5.metric("💵 Cost ($)",          metrics["total_cost"])


# ======================================
# CHAT INPUT
# ======================================
question = st.chat_input("Ask about deductibles, copays, network coverage…")

# ======================================
# PROCESS QUESTION
# ======================================
if question:
    # USER MESSAGE
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # ASSISTANT MESSAGE
    with st.chat_message("assistant"):
        with st.spinner("✨ Searching through your SBC document…"):
            try:
                from query_pipeline import ask_question
                result = ask_question(question)

                answer = result["answer"].replace("`", "")
                st.markdown(answer)

                st.divider()
                col1, col2, col3 = st.columns(3)
                col1.metric("📥 Input Tokens",  result["prompt_tokens"])
                col2.metric("📤 Output Tokens", result["completion_tokens"])
                col3.metric("🔢 Total Tokens",  result["total_tokens"])
                col4, col5 = st.columns(2)
                col4.metric("⏱️ Response Time (s)", result["total_time"])
                col5.metric("💵 Cost ($)",          result["total_cost"])

                # SAVE TO CHAT HISTORY
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "metrics": {
                        "prompt_tokens":    result["prompt_tokens"],
                        "completion_tokens": result["completion_tokens"],
                        "total_tokens":     result["total_tokens"],
                        "total_time":       result["total_time"],
                        "total_cost":       result["total_cost"]
                    }
                })

                # SAVE TO SEARCH HISTORY
                st.session_state.search_history.append({
                    "question":    question,
                    "answer":      answer,
                    "timestamp":   datetime.now().strftime("%b %d, %H:%M"),
                    "total_tokens": result["total_tokens"],
                    "total_cost":  result["total_cost"]
                })

                # UPDATE SESSION TOTALS
                try:
                    st.session_state.total_tokens_all += int(result["total_tokens"])
                    st.session_state.total_cost_all   += float(result["total_cost"])
                except Exception:
                    pass

                st.rerun()

            except ImportError:
                # Demo mode when query_pipeline is not available
                demo_answer = f"*(Demo mode — `query_pipeline` not found)*\n\nYou asked: **{question}**"
                st.markdown(demo_answer)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": demo_answer
                })
                st.session_state.search_history.append({
                    "question":    question,
                    "answer":      demo_answer,
                    "timestamp":   datetime.now().strftime("%b %d, %H:%M"),
                    "total_tokens": 0,
                    "total_cost":  0.0
                })
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error: {e}")
