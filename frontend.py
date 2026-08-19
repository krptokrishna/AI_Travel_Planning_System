import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from main import app


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Voyara AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(99, 102, 241, 0.18),
            transparent 25%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(14, 165, 233, 0.15),
            transparent 25%
        ),
        radial-gradient(
            circle at 50% 90%,
            rgba(168, 85, 247, 0.10),
            transparent 30%
        ),
        #070b17;

    color: #f8fafc;
}


/* Main container */

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* Hide Streamlit elements */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    padding: 42px;
    border-radius: 30px;

    background:
        linear-gradient(
            135deg,
            rgba(30, 41, 59, 0.95),
            rgba(15, 23, 42, 0.80)
        );

    border: 1px solid rgba(255, 255, 255, 0.08);

    box-shadow:
        0 30px 90px rgba(0, 0, 0, 0.35);

    margin-bottom: 28px;
}


.logo {
    font-size: 17px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #a5b4fc;
}


.hero-title {
    font-size: 48px;
    line-height: 1.08;
    font-weight: 800;
    margin-top: 18px;
    margin-bottom: 15px;
}


.hero-gradient {
    background:
        linear-gradient(
            90deg,
            #818cf8,
            #38bdf8,
            #c084fc
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


.hero-subtitle {
    color: #94a3b8;
    font-size: 16px;
    line-height: 1.7;
    max-width: 750px;
}


/* =========================================================
   FEATURE CARDS
   ========================================================= */

.feature-card {
    padding: 24px;

    border-radius: 20px;

    background: rgba(15, 23, 42, 0.75);

    border: 1px solid rgba(255, 255, 255, 0.07);

    min-height: 145px;

    transition: 0.25s ease;
}


.feature-card:hover {
    transform: translateY(-4px);

    border-color: rgba(129, 140, 248, 0.35);

    box-shadow:
        0 15px 40px rgba(0, 0, 0, 0.25);
}


.feature-icon {
    font-size: 30px;
}


.feature-title {
    font-weight: 700;
    margin-top: 12px;
    font-size: 16px;
}


.feature-text {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 7px;
    line-height: 1.5;
}


/* =========================================================
   SECTION TITLE
   ========================================================= */

.section-title {
    font-size: 23px;
    font-weight: 750;
    margin-top: 34px;
    margin-bottom: 16px;
}


/* =========================================================
   TEXT AREA
   ========================================================= */

.stTextArea textarea {
    background: rgba(15, 23, 42, 0.90) !important;

    color: #f8fafc !important;

    border:
        1px solid rgba(129, 140, 248, 0.25) !important;

    border-radius: 18px !important;

    padding: 18px !important;

    font-size: 15px !important;

    min-height: 130px !important;
}


.stTextArea textarea:focus {
    border:
        1px solid rgba(129, 140, 248, 0.75) !important;

    box-shadow:
        0 0 25px rgba(99, 102, 241, 0.15) !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    border-radius: 14px !important;

    border:
        1px solid rgba(255, 255, 255, 0.10) !important;

    background:
        linear-gradient(
            135deg,
            #6366f1,
            #8b5cf6
        ) !important;

    color: white !important;

    font-weight: 700 !important;

    min-height: 48px;

    transition: all 0.2s ease;
}


.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 12px 30px rgba(99, 102, 241, 0.30);
}


/* =========================================================
   RESULT CARD
   ========================================================= */

.result-card {
    background:
        rgba(15, 23, 42, 0.78);

    border:
        1px solid rgba(255, 255, 255, 0.07);

    border-radius: 22px;

    padding: 25px;

    margin-bottom: 18px;
}


.result-header {
    display: flex;

    align-items: center;

    gap: 12px;

    font-size: 20px;

    font-weight: 750;
}


.result-icon {
    font-size: 27px;
}


/* =========================================================
   APPROVAL CARD
   ========================================================= */

.approval {
    padding: 30px;

    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            rgba(79, 70, 229, 0.18),
            rgba(14, 165, 233, 0.08)
        );

    border:
        1px solid rgba(129, 140, 248, 0.28);

    margin-top: 30px;

    margin-bottom: 25px;
}


.approval-title {
    font-size: 25px;

    font-weight: 800;
}


.approval-text {
    color: #94a3b8;

    margin-top: 8px;

    line-height: 1.6;
}


/* =========================================================
   STATUS
   ========================================================= */

.status {
    display: inline-block;

    padding: 7px 14px;

    border-radius: 999px;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 0.5px;
}


.status-green {
    background: rgba(34, 197, 94, 0.12);

    color: #4ade80;
}


.status-red {
    background: rgba(239, 68, 68, 0.12);

    color: #f87171;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;

    color: #64748b;

    margin-top: 55px;

    font-size: 12px;

    line-height: 1.8;
}

</style>
""",
unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "streamlit_user"


# ============================================================
# HERO SECTION
# IMPORTANT:
# HTML STARTS FROM COLUMN 1 - NO INDENTATION
# ============================================================

st.markdown(
"""
<div class="hero">
<div class="logo">✦ VOYARA AI</div>

<div class="hero-title">
Your journey,
<span class="hero-gradient">intelligently planned.</span>
</div>

<div class="hero-subtitle">
An autonomous multi-agent travel assistant that searches flights,
discovers hotels, builds your itinerary and waits for your approval
before booking.
</div>

</div>
""",
unsafe_allow_html=True
)


# ============================================================
# FEATURE CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(
"""
<div class="feature-card">
<div class="feature-icon">✈️</div>

<div class="feature-title">
Smart Flights
</div>

<div class="feature-text">
Search and compare flight options for your journey.
</div>

</div>
""",
    unsafe_allow_html=True
    )


with c2:

    st.markdown(
"""
<div class="feature-card">
<div class="feature-icon">🏨</div>

<div class="feature-title">
Hotel Discovery
</div>

<div class="feature-text">
Find suitable hotels based on your travel plan.
</div>

</div>
""",
    unsafe_allow_html=True
    )


with c3:

    st.markdown(
"""
<div class="feature-card">
<div class="feature-icon">🗺️</div>

<div class="feature-title">
AI Itinerary
</div>

<div class="feature-text">
Generate a personalized day-by-day travel plan.
</div>

</div>
""",
    unsafe_allow_html=True
    )


with c4:

    st.markdown(
"""
<div class="feature-card">
<div class="feature-icon">🛡️</div>

<div class="feature-title">
Human Control
</div>

<div class="feature-text">
Booking only continues after your approval.
</div>

</div>
""",
    unsafe_allow_html=True
    )


# ============================================================
# TRIP PLANNER
# ============================================================

st.markdown(
'<div class="section-title">🌍 Where do you want to go?</div>',
unsafe_allow_html=True
)


user_query = st.text_area(
    "Travel request",

    placeholder=(
        "Example: Plan a 5-day trip from Kanpur to Goa "
        "for 2 people starting 10 September. "
        "Find flights, good hotels and create a complete itinerary."
    ),

    height=130,

    label_visibility="collapsed"
)


# ============================================================
# THREAD ID
# ============================================================

thread_id = st.text_input(
    "Trip ID",

    value=st.session_state.thread_id,

    label_visibility="collapsed"
)

st.session_state.thread_id = thread_id


# ============================================================
# PLAN BUTTON
# ============================================================

if st.button(
    "✦  Build My Journey",
    use_container_width=True
):

    if not user_query.strip():

        st.warning(
            "Please tell me where you want to travel."
        )

    else:

        config = {
            "configurable": {
                "thread_id": st.session_state.thread_id
            }
        }


        initial_state = {

            "messages": [
                HumanMessage(
                    content=user_query
                )
            ],

            "user_query": user_query,

            "flight_results": "",

            "hotel_results": "",

            "itinerary": "",

            "llm_calls": 0,

            "human_approval": "",

            "booking_status": "",

            "booking_confirmation": ""
        }


        # ----------------------------------------------------
        # AI PROCESS
        # ----------------------------------------------------

        with st.status(
            "🤖 Voyara AI is planning your journey...",
            expanded=True
        ) as status:

            st.write(
                "✈️ Searching for flights..."
            )

            st.write(
                "🏨 Discovering hotels..."
            )

            st.write(
                "🗺️ Building your itinerary..."
            )

            st.write(
                "🧠 Optimizing your travel plan..."
            )


            result = app.invoke(
                initial_state,
                config=config
            )


            status.update(
                label="✨ Travel plan is ready!",
                state="complete"
            )


        st.session_state.result = result

        st.rerun()


# ============================================================
# GET RESULT
# ============================================================

result = st.session_state.result


if result:

    # ========================================================
    # JOURNEY HEADER
    # ========================================================

    st.markdown(
        '<div class="section-title">✨ Your Journey</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # FLIGHTS
    # ========================================================

    if result.get("flight_results"):

        st.markdown(
"""
<div class="result-card">
<div class="result-header">
<span class="result-icon">✈️</span>
Flight Intelligence
</div>
</div>
""",
        unsafe_allow_html=True
        )


        with st.expander(
            "View flight options",
            expanded=True
        ):

            st.write(
                result["flight_results"]
            )


    # ========================================================
    # HOTELS
    # ========================================================

    if result.get("hotel_results"):

        st.markdown(
"""
<div class="result-card">
<div class="result-header">
<span class="result-icon">🏨</span>
Hotel Discovery
</div>
</div>
""",
        unsafe_allow_html=True
        )


        with st.expander(
            "View hotel recommendations",
            expanded=True
        ):

            st.write(
                result["hotel_results"]
            )


    # ========================================================
    # ITINERARY
    # ========================================================

    if result.get("itinerary"):

        st.markdown(
"""
<div class="result-card">
<div class="result-header">
<span class="result-icon">🗺️</span>
Your AI Itinerary
</div>
</div>
""",
        unsafe_allow_html=True
        )


        st.markdown(
            result["itinerary"]
        )


    # ========================================================
    # HUMAN APPROVAL
    # ========================================================

    if "__interrupt__" in result:

        interrupt_data = (
            result["__interrupt__"][0].value
        )


        st.markdown(
"""
<div class="approval">

<div class="approval-title">
🛡️ Final approval required
</div>

<div class="approval-text">
Your complete travel plan is ready.
Review the flights, hotels and itinerary before
allowing the booking agent to continue.
</div>

</div>
""",
        unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # USER REQUEST
        # ----------------------------------------------------

        st.markdown(
            "### 📝 Your Travel Request"
        )

        st.info(
            interrupt_data["user_query"]
        )


        # ----------------------------------------------------
        # FLIGHT REVIEW
        # ----------------------------------------------------

        with st.expander(
            "✈️ Review Flights",
            expanded=True
        ):

            st.write(
                interrupt_data["flight_results"]
            )


        # ----------------------------------------------------
        # HOTEL REVIEW
        # ----------------------------------------------------

        with st.expander(
            "🏨 Review Hotels",
            expanded=True
        ):

            st.write(
                interrupt_data["hotel_results"]
            )


        # ----------------------------------------------------
        # ITINERARY REVIEW
        # ----------------------------------------------------

        with st.expander(
            "🗺️ Review Itinerary",
            expanded=True
        ):

            st.markdown(
                interrupt_data["itinerary"]
            )


        st.markdown("###")


        # ----------------------------------------------------
        # APPROVAL BUTTONS
        # ----------------------------------------------------

        col1, col2 = st.columns(2)


        # ====================================================
        # APPROVE
        # ====================================================

        with col1:

            if st.button(
                "✅ Approve & Continue",
                use_container_width=True
            ):

                config = {
                    "configurable": {
                        "thread_id":
                        st.session_state.thread_id
                    }
                }


                with st.spinner(
                    "🔐 Processing booking..."
                ):

                    resumed_result = app.invoke(
                        Command(
                            resume="yes"
                        ),
                        config=config
                    )


                st.session_state.result = (
                    resumed_result
                )


                st.success(
                    "Booking process completed!"
                )


                st.rerun()


        # ====================================================
        # CANCEL
        # ====================================================

        with col2:

            if st.button(
                "❌ Cancel Booking",
                use_container_width=True
            ):

                config = {
                    "configurable": {
                        "thread_id":
                        st.session_state.thread_id
                    }
                }


                with st.spinner(
                    "Cancelling booking..."
                ):

                    resumed_result = app.invoke(
                        Command(
                            resume="no"
                        ),
                        config=config
                    )


                st.session_state.result = (
                    resumed_result
                )


                st.warning(
                    "Booking cancelled."
                )


                st.rerun()


    # ========================================================
    # BOOKING STATUS
    # ========================================================

    if result.get("booking_status"):

        st.markdown(
            '<div class="section-title">🎫 Booking Status</div>',
            unsafe_allow_html=True
        )


        if result["booking_status"] == "approved":

            st.markdown(
"""
<div class="result-card">

<span class="status status-green">
✓ APPROVED
</span>

<h3>
Booking request approved
</h3>

<p style="color:#94a3b8;">
Your booking workflow has been approved.
</p>

</div>
""",
            unsafe_allow_html=True
            )


        elif result["booking_status"] == "cancelled":

            st.markdown(
"""
<div class="result-card">

<span class="status status-red">
✕ CANCELLED
</span>

<h3>
Booking cancelled
</h3>

<p style="color:#94a3b8;">
The booking request was cancelled by you.
</p>

</div>
""",
            unsafe_allow_html=True
            )


    # ========================================================
    # BOOKING CONFIRMATION
    # ========================================================

    if result.get("booking_confirmation"):

        st.markdown(
"""
<div class="result-card">

<div class="result-header">
🎟️ Booking Confirmation
</div>

</div>
""",
        unsafe_allow_html=True
        )


        st.success(
            result["booking_confirmation"]
        )


    # ========================================================
    # SYSTEM STATS
    # ========================================================

    st.divider()

    s1, s2, s3 = st.columns(3)


    with s1:

        st.metric(
            "🤖 AI Calls",
            result.get(
                "llm_calls",
                0
            )
        )


    with s2:

        st.metric(
            "🧩 Agents",
            "5"
        )


    with s3:

        st.metric(
            "💾 Memory",
            "PostgreSQL"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
"""
<div class="footer">

VOYARA AI · Multi-Agent Travel Intelligence

<br>

Powered by LangGraph · Groq · Tavily · PostgreSQL

</div>
""",
unsafe_allow_html=True
)
