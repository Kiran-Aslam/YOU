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

def init_day6_session_state():
    """Initialize session state variables for Day 6"""
    if 'day6_task1_completed' not in st.session_state:
        st.session_state.day6_task1_completed = False
    if 'day6_task2_completed' not in st.session_state:
        st.session_state.day6_task2_completed = False
    if 'day6_timer_running' not in st.session_state:
        st.session_state.day6_timer_running = False
    if 'day6_timer_start' not in st.session_state:
        st.session_state.day6_timer_start = None
    if 'day6_reflection_text' not in st.session_state:
        st.session_state.day6_reflection_text = ""

def save_reflection(reflection_text):
    """Save user reflection to a local file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save reflection with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = data_dir / f"day6_reflection_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Day 6 Reflection - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write("Task 2: My Daily Loop\n\n")
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
        music_path = Path("music/relax.mp3")  # Changed to relaxing ambient music for Day 6

        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            return True
        else:
            st.warning("🎵 Music file not found. Create a 'music' folder and add 'ticking_clock_ambient.mp3' for ambient sounds.")
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

def show_day6_screen():
    """Main function to display Day 6 screen"""
    
    # Initialize session state
    init_day6_session_state()
    
    # Custom CSS for Day 6
    st.markdown("""
    <style>
        /* Day 6 specific styling */
        .day6-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .day6-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .day6-title {
            font-size: 3rem;
            font-weight: bold;
            color: #8b5cf6;
            text-shadow: 0 0 20px #8b5cf6;
            margin-bottom: 1rem;
        }
        
        .day6-subtitle {
            font-size: 1.3rem;
            color: #a78bfa;
            font-style: italic;
        }
        
        .task-card {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid #8b5cf6;
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .task-card:hover {
            border-color: #a78bfa;
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
        }
        
        .task-header {
            color: #8b5cf6;
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
            color: #8b5cf6;
            text-align: center;
            margin: 2rem 0;
            text-shadow: 0 0 20px #8b5cf6;
        }
        
        .motivational-quote {
            background: linear-gradient(135deg, #8b5cf6, #a78bfa);
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
            border: 2px solid #8b5cf6;
            border-radius: 10px;
            color: #000000;
            font-size: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .stTextArea textarea:focus {
            border-color: #a78bfa;
            box-shadow: 0 0 15px rgba(167, 139, 250, 0.5);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="day6-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="day6-header">
        <h1 class="day6-title">Day 6 🔄</h1>
        <p class="day6-subtitle">Patterns That Define You</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="task-card">
        <div style="text-align: center; color: #8b5cf6; font-size: 1.2rem;">
            <strong>Welcome to Day 6 🔄</strong>
        </div>
        <p style="color: #ffffff; margin-top: 1rem; text-align: center; font-size: 1.1rem;">
            Today, let’s take a closer look at the routines and patterns that guide your life.
Each habit—big or small—is shaping the person you’re becoming.
Are these habits helping you grow into your best self, or holding you back?
It’s time to notice the loops you’re stuck in… and gently choose better ones. 🌱
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task 1: 5-Minute Observe Your Daily Patterns
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🧘‍♀️ Task 1: Observe Your Daily Patterns 
        </div>
        <div class="task-instruction">
            Sit quietly and mentally walk through your average day — from the moment you wake up to sleep. 
            Notice what you do <strong>out of routine, without questioning</strong>. What parts feel automatic? 
            Which moments do you actually feel present in? Observe without judgment, just awareness.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer logic
    if not st.session_state.day6_timer_running and not st.session_state.day6_task1_completed:
        if st.button("🔄 Start Task 1 (5-Minute Pattern Observation)", key="start_task1_day6"):
            st.session_state.day6_timer_running = True
            st.session_state.day6_timer_start = time.time()
            if play_ambient_music():
                st.success("🎵 Ticking clock and ambient tones started. Begin observing your patterns.")
            st.rerun()

    # Show timer if running
    if st.session_state.day6_timer_running:
        if st.session_state.day6_timer_start:
            elapsed_time = time.time() - st.session_state.day6_timer_start
            remaining_time = max(0, 300 - elapsed_time)  # 5 minutes = 300 seconds
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
                st.session_state.day6_timer_running = False
                st.session_state.day6_timer_start = None
                stop_ambient_music()
                st.success("⏹️ Timer stopped.")
                st.rerun()

            # Auto-refresh every second
            time.sleep(1)
            st.rerun()
        else:
            # Timer completed
            st.session_state.day6_timer_running = False
            st.session_state.day6_task1_completed = True
            stop_ambient_music()
            st.rerun()
    
    # Show completion message for Task 1
    if st.session_state.day6_task1_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 1 Completed!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="motivational-quote">
            "We are what we repeatedly do. Excellence, then, is not an act, but a habit. You've just observed the blueprint of your life." 🔄
        </div>
        """, unsafe_allow_html=True)
    
    # Task 2: Journal Prompt – My Daily Loop
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            ✍️ Task 2: My Daily Loop
        </div>
        <div class="task-instruction">
            What are <strong>3 habits you follow every day — without fail</strong>? Why do you think you've formed them? 
            Do they serve you... or hold you back? Which one would you change if you could?
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text area for reflection
    reflection_text = st.text_area(
        "My Daily Loop Analysis:",
        value=st.session_state.day6_reflection_text,
        height=200,
        placeholder="My 3 daily habits without fail:\n1. \n2. \n3. \n\nWhy I think I formed these habits:\n\nWhich habits serve me:\n\nWhich habits hold me back:\n\nThe one habit I would change if I could:\n\nHow this habit change would improve my life:",
        key="reflection_input"
    )
    
    # Update session state
    st.session_state.day6_reflection_text = reflection_text
    
    # Submit button for Task 2
    if st.button("🔄 Submit My Daily Loop Analysis", key="submit_task2_day6"):
        if reflection_text.strip():
            # Save reflection
            if save_reflection(reflection_text):
                st.session_state.day6_task2_completed = True
                st.success("✅ Your daily loop analysis has been saved.")
                with st.spinner("AI is analyzing your patterns..."):
                    ai_feedback = get_groq_feedback(reflection_text)
                st.markdown(f"""
                         <div class="motivational-quote">
                         {ai_feedback}
                         </div>
                         """, unsafe_allow_html=True)
            else:
                st.error("❌ Error saving reflection. Please try again.")
        else:
            st.warning("⚠️ Please analyze your daily patterns before submitting.")
    
    # Show completion status
    if st.session_state.day6_task2_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 2 Completed! Your pattern awareness is now crystal clear.
        </div>
        """, unsafe_allow_html=True)
    
    # Day completion check
    if st.session_state.day6_task1_completed and st.session_state.day6_task2_completed:
        st.markdown("""
        <div class="task-card" style="border-color: #00ff00;">
            <div style="text-align: center; color: #00ff00; font-size: 1.5rem;">
                🎉 Congratulations! You've completed Day 6! 🎉
            </div>
            <p style="color: #ffffff; margin-top: 1rem; text-align: center;">
                You've gained profound awareness of the patterns that shape your daily life. This consciousness is the first step 
                toward intentional change. Your habits are the compound interest of self-improvement — small changes today 
                create extraordinary results tomorrow. You now have the power to choose your patterns consciously.
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
        if st.button("🔄 Reset Day 6", key="reset_day6"):
            # Reset all Day 6 session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('day6_')]
            for key in keys_to_remove:
                del st.session_state[key]
            stop_ambient_music()
            st.rerun()
    
    with col3:
        if st.button("➡️ Next Day", key="next_day"):
            st.session_state.selected_day = 7
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

# If running this file directly (for testing)
if __name__ == "__main__":
    st.set_page_config(
        page_title="SoulScanner - Day 6",
        page_icon="🔄",
        layout="centered"
    )
    show_day6_screen()