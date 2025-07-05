import streamlit as st
import time
import datetime
import os
from pathlib import Path
from utils import get_groq_feedback

# Import for audio (you'll need to install: pip install pygame)
try:
    import pygame
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    st.warning("⚠️ Install pygame for audio support: pip install pygame")

def init_day1_session_state():
    """Initialize session state variables for Day 1"""
    if 'day1_task1_completed' not in st.session_state:
        st.session_state.day1_task1_completed = False
    if 'day1_task2_completed' not in st.session_state:
        st.session_state.day1_task2_completed = False
    if 'day1_timer_running' not in st.session_state:
        st.session_state.day1_timer_running = False
    if 'day1_timer_start' not in st.session_state:
        st.session_state.day1_timer_start = None
    if 'day1_reflection_text' not in st.session_state:
        st.session_state.day1_reflection_text = ""

def save_reflection(reflection_text):
    """Save user reflection to a local file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save reflection with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = data_dir / f"day1_reflection_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Day 1 Reflection - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write("Task 2: Things I Dislike and Why\n\n")
            f.write(reflection_text)
        
        return True
    except Exception as e:
        st.error(f"Error saving reflection: {str(e)}")
        return False

def play_ambient_music():
    """Play ambient music if available"""
    if not AUDIO_AVAILABLE:
        return False
    
    try:
        pygame.mixer.init()
        music_path = Path("music/relax.mp3")
        
        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            return True
        else:
            st.warning("🎵 Music file not found. Create a 'music' folder and add 'relax.mp3' for ambient sounds.")
            return False
    except Exception as e:
        st.error(f"Error playing music: {str(e)}")
        return False

def stop_ambient_music():
    """Stop ambient music"""
    if AUDIO_AVAILABLE:
        try:
            pygame.mixer.music.stop()
        except:
            pass

def show_day1_screen():
    """Main function to display Day 1 screen"""
    
    # Initialize session state
    init_day1_session_state()
    
    # Custom CSS for Day 1
    st.markdown("""
    <style>
        /* Day 1 specific styling */
        .day1-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .day1-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .day1-title {
            font-size: 3rem;
            font-weight: bold;
            color: #f472b6;
            text-shadow: 0 0 20px #f472b6;
            margin-bottom: 1rem;
        }
        
        .day1-subtitle {
            font-size: 1.3rem;
            color: #b19cd9;
            font-style: italic;
        }
        
        .task-card {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid #00ffff;
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .task-card:hover {
            border-color: #ff00ff;
            box-shadow: 0 8px 25px rgba(255, 0, 255, 0.3);
        }
        
        .task-header {
            color: #00ffff;
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .task-instruction {
            color: #ffffff;
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }
        
        .timer-display {
            font-size: 4rem;
            font-weight: bold;
            color: #00ffff;
            text-align: center;
            margin: 2rem 0;
            text-shadow: 0 0 20px #00ffff;
        }
        
        .motivational-quote {
            background: linear-gradient(135deg, #ff00ff, #00ffff);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 2rem 0;
            text-align: center;
            color: white;
            font-size: 1.2rem;
            font-style: italic;
            font-weight: bold;
        }
        
        .completion-message {
            background: rgba(0, 255, 0, 0.2);
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 1rem;
            color: #00ff00;
            font-weight: bold;
            margin: 1rem 0;
            text-align: center;
        }
        
        .stTextArea textarea {
            background-color: rgba(255, 255, 255, 0.1);
            border: 2px solid #00ffff;
            border-radius: 10px;
            color: #000000;
            font-size: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .stTextArea textarea:focus {
            border-color: #ff00ff;
            box-shadow: 0 0 15px rgba(255, 0, 255, 0.5);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="day1-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="day1-header">
        <h1 class="day1-title">Day 1 🌟</h1>
        <p class="day1-subtitle">Self-Discovery Begins</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="task-card">
        <div style="text-align: center; color: #00ffff; font-size: 1.2rem;">
            <strong>Welcome to Day 1  🧘‍♀️</strong>
        </div>
        <p style="color: #ffffff; margin-top: 1rem; text-align: center; font-size: 1.1rem;">
            Today we'll explore the power of stillness and honest self-reflection. 
            Take your time with each task and be gentle with yourself.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task 1: 5-Minute Stillness Practice
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🧘 Task 1: 5-Minute Stillness Practice
        </div>
        <div class="task-instruction">
            Find a quiet place, sit comfortably, close your eyes, and do nothing for the next 5 minutes. 
            Let your mind reveal what it wants. Don't force anything – just be present.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer logic
    if not st.session_state.day1_timer_running and not st.session_state.day1_task1_completed:
        if st.button("🎯 Start Task 1 (5-Minute Timer)", key="start_task1_Day1"):
            st.session_state.day1_timer_running = True
            st.session_state.day1_timer_start = time.time()
            if play_ambient_music():
                st.success("🎵 Ambient music started. Relax and enjoy the silence.")
            st.rerun()

    # Show timer if running (THIS MUST BE INSIDE THE FUNCTION)
    if st.session_state.day1_timer_running:
        if st.session_state.day1_timer_start:
            elapsed_time = time.time() - st.session_state.day1_timer_start
            remaining_time = max(0, 300 - elapsed_time)
        if remaining_time > 0:
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            st.markdown(f"""
            <div class="timer-display">
                {minutes:02d}:{seconds:02d}
            </div>
            """, unsafe_allow_html=True)

            # Progress bar
            progress = (300 - remaining_time) / 300
            st.progress(progress)

            # Stop Timer Button
            if st.button("⏹️ Stop Timer", key="stop_task1"):
                st.session_state.day1_timer_running = False
                st.session_state.day1_timer_start = None
                stop_ambient_music()
                st.success("⏹️ Timer stopped.")
                st.rerun()

            # Auto-refresh every second
            time.sleep(1)
            st.rerun()
        else:
            # Timer completed
            st.session_state.day1_timer_running = False
            st.session_state.day1_task1_completed = True
            stop_ambient_music()
            st.rerun()
    
    # Show completion message for Task 1
    if st.session_state.day1_task1_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 1 Completed!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="motivational-quote">
            "Sometimes the answers come in silence." 🌙
        </div>
        """, unsafe_allow_html=True)
    
    # Task 2: Write What You Dislike – And Why
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            ✍️ Task 2: Write What You Dislike – And Why
        </div>
        <div class="task-instruction">
            List 3 things you genuinely dislike and explain why. Don't worry about judgment — 
            be honest with yourself. This exercise helps you understand your values and boundaries.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text area for reflection
    reflection_text = st.text_area(
        "Your Honest Reflection:",
        value=st.session_state.day1_reflection_text,
        height=200,
        placeholder="1. I dislike... because...\n2. I dislike... because...\n3. I dislike... because...",
        key="reflection_input_day1"
    )
    
    # Update session state
    st.session_state.day1_reflection_text = reflection_text
    
    # Submit button for Task 2
    if st.button("💫 Submit My Reflection", key="submit_task2"):
        if reflection_text.strip():
            # Save reflection
            if save_reflection(reflection_text):
                st.session_state.day1_task2_completed = True
                st.success("✅ Reflection saved successfully!")
                with st.spinner("AI is thinking..."):
                    ai_feedback = get_groq_feedback(reflection_text)
                st.markdown(f"""
                         <div class="motivational-quote">
                         {ai_feedback}
                         </div>
                         """, unsafe_allow_html=True)
            else:
                st.error("❌ Error saving reflection. Please try again.")
        else:
            st.warning("⚠️ Please write your reflection before submitting.")
    
    # Show completion status
    if st.session_state.day1_task2_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 2 Completed! Your reflection has been saved.
        </div>
        """, unsafe_allow_html=True)
    
    # Day completion check
    if st.session_state.day1_task1_completed and st.session_state.day1_task2_completed:
        st.markdown("""
        <div class="task-card" style="border-color: #00ff00;">
            <div style="text-align: center; color: #00ff00; font-size: 1.5rem;">
                🎉 Congratulations! You've completed Day 1! 🎉
            </div>
            <p style="color: #ffffff; margin-top: 1rem; text-align: center;">
                You've taken the first step on your journey of self-discovery. 
                Tomorrow, we'll explore gratitude and its power to transform your perspective.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🏠 Back to Home", key="back_home"):
            st.session_state.selected_day = None
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Day 1", key="reset_day1"):
            # Reset all Day 1 session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('day1_')]
            for key in keys_to_remove:
                del st.session_state[key]
            stop_ambient_music()
            st.rerun()
    
    with col3:
        if st.button("➡️ Next Day", key="next_day"):
            st.session_state.selected_day = 2
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

# If running this file directly (for testing)
if __name__ == "__main__":
    st.set_page_config(
        page_title="SoulScanner - Day 1",
        page_icon="🌙",
        layout="centered"
    )
    show_day1_screen()