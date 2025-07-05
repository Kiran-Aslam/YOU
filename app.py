import streamlit as st
import time
import os
from Days.Day1 import show_day1_screen
from Days.Day2 import show_day2_screen
from Days.Day3 import show_day3_screen
from Days.Day4 import show_day4_screen
from Days.Day5 import show_day5_screen
from Days.Day6 import show_day6_screen
from Days.Day7 import show_day7_screen
from Days.Day8 import show_day8_screen
from Days.Day9 import show_day9_screen
from Days.Day10 import show_day10_screen
from Days.Day11 import show_day11_screen
from Days.Day12 import show_day12_screen
from Days.Day13 import show_day13_screen
from Days.Day14 import show_day14_screen
from Days.WHY_I_MADE_YOU import show_why_i_made_you_screen

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="YOU - Mental Wellness Journey",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark neon gradient theme
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main app background with neon gradient */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a0033 25%, #000428 50%, #004e92 75%, #0c0c0c 100%);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main container styling - improved centering */
    .main-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 2rem;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        animation: fadeIn 2s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Title styling with neon glow effect - ensure center alignment */
    .neon-title {
        font-size: 5rem;
        font-weight: bold;
        color: #00ffff;
        text-shadow: 
            0 0 5px #00ffff,
            0 0 10px #00ffff,
            0 0 20px #00ffff,
            0 0 40px #00ffff;
        margin-bottom: 1rem;
        font-family: 'Arial Black', sans-serif;
        letter-spacing: 3px;
        animation: pulse 2s infinite;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        text-align: center;
        margin-left: auto;
        margin-right: auto;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Subtitle styling */
    .subtitle {
        font-size: 1.5rem;
        color: #b19cd9;
        margin-bottom: 3rem;
        font-style: italic;
        font-weight: 300;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        text-align: center;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        border: 2px solid #00ffff;
        border-radius: 10px;
        color: #000000 !important;
        font-size: 1.1rem;
        padding: 0.8rem;
        backdrop-filter: blur(10px);
        caret-color: #ffffff !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff00ff;
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.5);
        color: #000000 !important;
        caret-color: #ffffff !important;
    }
    
    .stNumberInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        border: 2px solid #00ffff;
        border-radius: 10px;
        color: #ffffff;
        font-size: 1.1rem;
        padding: 0.8rem;
        backdrop-filter: blur(10px);
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #ff00ff;
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.5);
    }
    
    /* Input labels */
    .stTextInput > label, .stNumberInput > label {
        color: #ffffff;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff00ff, #00ffff);
        border: none;
        border-radius: 25px;
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.8rem 2rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 0, 255, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 0, 255, 0.5);
        background: linear-gradient(45deg, #00ffff, #ff00ff);
    }
    
    /* Welcome message styling */
    .welcome-message {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid #00ffff;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .welcome-text {
        color: #00ffff;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    /* Warning message styling */
    .warning-message {
        background: rgba(255, 0, 0, 0.2);
        border: 2px solid #ff4444;
        border-radius: 10px;
        padding: 1rem;
        color: #ff4444;
        font-weight: bold;
        margin: 1rem 0;
        animation: shake 0.5s ease-in-out;
    }
    
    @keyframes shake {
        0%, 20%, 40%, 60%, 80% { transform: translateX(0); }
        10%, 30%, 50%, 70% { transform: translateX(-5px); }
        15%, 35%, 55%, 75% { transform: translateX(5px); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .neon-title {
            font-size: 2.5rem;
        }
        .subtitle {
            font-size: 1.1rem;
        }
        .main-container {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for user data
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_age' not in st.session_state:
    st.session_state.user_age = 0
if 'journey_started' not in st.session_state:
    st.session_state.journey_started = False

# Main app container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown("""
<style>
    .you-title {
        text-align: center;
        font-size: 5rem;
        font-weight: bold;
        margin-top: 2.5rem;
        margin-bottom: 1.2rem;
        letter-spacing: 4px;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 0 2px 24px #8b5cf6, 0 4px 32px #06b6d4;
        animation: title-glow 2.5s infinite alternate;
        position: relative;
        z-index: 2;
    }
    @keyframes title-glow {
        0% { text-shadow: 0 2px 24px #8b5cf6, 0 4px 32px #06b6d4; }
        100% { text-shadow: 0 4px 32px #f472b6, 0 8px 48px #06b6d4; }
    }
    .you-y { color: #f472b6; }
    .you-o { color: #06b6d4; }
    .you-u { color: #8b5cf6; }

    /* Floating emoji animation */
    .emoji-float {
        position: absolute;
        font-size: 2.2rem;
        z-index: 3;
        animation: float-emoji 4s ease-in-out infinite;
        pointer-events: none;
        user-select: none;
    }
    .emoji-1 { left: 12%; top: 0.5rem; animation-delay: 0s;}
    .emoji-2 { right: 12%; top: 0.5rem; animation-delay: 1.2s;}
    .emoji-3 { left: 22%; bottom: 0.5rem; animation-delay: 2.2s;}
    .emoji-4 { right: 22%; bottom: 0.5rem; animation-delay: 3s;}
    @keyframes float-emoji {
        0%, 100% { transform: translateY(0);}
        50% { transform: translateY(-18px);}
    }
    .title-container {
        position: relative;
        width: 100%;
        height: 6.5rem;
        margin-bottom: 1.5rem;
    }
</style>
<div class="title-container">
    <span class="emoji-float emoji-1">💙</span>
    <span class="emoji-float emoji-2">✨</span>
    <span class="emoji-float emoji-3">🌟</span>
    <span class="emoji-float emoji-4">💜</span>
    <div class="you-title">
        <span class="you-y">Y</span><span class="you-o">O</span><span class="you-u">U</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Stylish subtitle with colored, bold first letters
st.markdown("""
<style>
    .custom-subtitle {
        display: flex;
        justify-content: center;
        gap: 1.2rem;
        margin-bottom: 2.2rem;
        font-size: 1.2rem;
        font-family: 'Arial Black', Arial, sans-serif;
        font-weight: 300;
        letter-spacing: 2px;
    }
    .subtitle-word {
        display: inline-block;
    }
    .subtitle-y { color: #f472b6; }
    .subtitle-o { color: #06b6d4; }
    .subtitle-u { color: #8b5cf6; }
    .subtitle-word span {
        font-weight: bold;
        font-size: 1.6rem;
        letter-spacing: 1px;
        font-family: 'Arial Black', Arial, sans-serif;
        margin-right: 2px;
        vertical-align: middle;
        text-shadow: 0 2px 12px rgba(139,92,246,0.15);
    }
</style>
<div class="custom-subtitle">
    <span class="subtitle-word subtitle-y"><span>Y</span>ourself</span>
    <span style="color: #b19cd9; font-size: 1rem; margin: 0 0.5rem;">•</span>
    <span class="subtitle-word subtitle-o"><span>O</span>wn</span>
    <span style="color: #b19cd9; font-size: 1rem; margin: 0 0.5rem;">•</span>
    <span class="subtitle-word subtitle-u"><span>U</span>niqueness</span>
</div>
""", unsafe_allow_html=True)

# Check if journey has already started
if not st.session_state.journey_started:
    # Input section
    st.markdown("---")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Name input
        name = st.text_input(
            "✨ Your Name",
            placeholder="Enter your name...",
            key="name_input"
        )
    
    with col2:
        # Age input
        age = st.number_input(
            "🎂 Your Age",
            min_value=13,
            max_value=100,
            value=18,
            key="age_input"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Start journey button
    if st.button("🚀 Start My Journey", key="start_button"):
        # Validation
        if name.strip() == "" or age < 13:
            # Show warning message
            st.markdown(
                '<div class="warning-message">⚠️ Please enter your name and age (minimum 13 years) to begin your journey!</div>',
                unsafe_allow_html=True
            )
        else:
            # Store user data in session state
            st.session_state.user_name = name.strip()
            st.session_state.user_age = age
            st.session_state.journey_started = True
            
            # Force rerun to show welcome message
            st.rerun()

else:
    st.markdown(
        f'''
        <div class="welcome-message">
            <div class="welcome-text">Welcome to YOU 🌟</div>
            <p style="color: #b19cd9; font-size: 1.1rem; margin-top: 1rem;">
                A space created just for you. <br><br>
                This isn't about becoming someone new. It's about remembering the real you. <br>
                Noticing what makes you smile. What weighs you down. What gives you peace. <br>
                And in the end, maybe you'll remember who you were before the world told you who to be.
            </p>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Day topics/themes
    day_themes = [
        "Reflect", "Joy", "Face", "Essence", "Sanctuary",
        "Loop", "Mirror", "Innocence", "Express", "Courage", 
        "Power", "Compass", "Dream", "Wholeness", "WHY YOU"
    ]

    # Create grid layout with day blocks
    st.markdown('<div class="days-container">', unsafe_allow_html=True)

    selected_day = st.session_state.get("selected_day", None)
    for day in range(1, 16):
        theme = day_themes[day-1]
        btn = st.button(f"Day {day}: {theme}", key=f"day_{day}")
        if btn:
            st.session_state.selected_day = day
            selected_day = day

        # Show selected day content just below its button
        if selected_day == day:
            try:
                if day == 1:
                    show_day1_screen()
                elif day == 2:
                    show_day2_screen()
                elif day == 3:
                    show_day3_screen()
                elif day == 4:
                    show_day4_screen()
                elif day == 5:
                    show_day5_screen()
                elif day == 6:
                    show_day6_screen()
                elif day == 7:
                    show_day7_screen()
                elif day == 8:
                    show_day8_screen()
                elif day == 9:
                    show_day9_screen()
                elif day == 10:
                    show_day10_screen()
                elif day == 11:
                    show_day11_screen()
                elif day == 12:
                    show_day12_screen()
                elif day == 13:
                    show_day13_screen()
                elif day == 14:
                    show_day14_screen()
                elif day == 15:
                    show_why_i_made_you_screen()
                else:
                    st.info(f"🚧 Day {day} content will be added here!")
            except Exception as e:
                st.error(f"Error loading Day {day}: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Reset journey button
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🔄 Start Over", key="reset_button"):
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Close main container
st.markdown('</div>', unsafe_allow_html=True)

# Footer with additional info
st.markdown(
    """
    <div style="text-align: center; margin-top: 3rem; color: #666; font-size: 0.9rem;">
        <p>✨ Your journey to self-awareness begins here ✨</p>
    </div>
    """,
    unsafe_allow_html=True
)