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

def init_day4_session_state():
    """Initialize session state variables for Day 4"""
    if 'day4_task1_completed' not in st.session_state:
        st.session_state.day4_task1_completed = False
    if 'day4_task2_completed' not in st.session_state:
        st.session_state.day4_task2_completed = False
    if 'day4_timer_running' not in st.session_state:
        st.session_state.day4_timer_running = False
    if 'day4_timer_start' not in st.session_state:
        st.session_state.day4_timer_start = None
    if 'day4_reflection_text' not in st.session_state:
        st.session_state.day4_reflection_text = ""

def save_reflection(reflection_text):
    """Save user reflection to a local file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save reflection with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = data_dir / f"day4_reflection_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Day 4 Reflection - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write("Task 2: Who Am I Without Labels?\n\n")
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
        music_path = Path("music/relax.mp3")  # Changed to relax for Day 4

        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            return True
        else:
            st.warning("🎵 Music file not found. Create a 'music' folder and add 'deepspace.mp3' for ambient sounds.")
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

def show_day4_screen():
    """Main function to display Day 4 screen"""
    
    # Initialize session state
    init_day4_session_state()
    
    # Custom CSS for Day 4
    st.markdown("""
    <style>
        /* Day 4 specific styling */
        .day4-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .day4-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .day4-title {
            font-size: 3rem;
            font-weight: bold;
            color: #6366f1;
            text-shadow: 0 0 20px #6366f1;
            margin-bottom: 1rem;
        }
        
        .day4-subtitle {
            font-size: 1.3rem;
            color: #818cf8;
            font-style: italic;
        }
        
        .task-card {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid #6366f1;
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .task-card:hover {
            border-color: #818cf8;
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
        }
        
        .task-header {
            color: #6366f1;
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
            color: #6366f1;
            text-align: center;
            margin: 2rem 0;
            text-shadow: 0 0 20px #6366f1;
        }
        
        .motivational-quote {
            background: linear-gradient(135deg, #6366f1, #818cf8);
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
        
        .labels-info {
            background: rgba(99, 102, 241, 0.2);
            border: 2px solid #6366f1;
            border-radius: 10px;
            padding: 1.5rem;
            color: #c7d2fe;
            margin: 1rem 0;
        }
        
        .stTextArea textarea {
            background-color: rgba(255, 255, 255, 0.1);
            border: 2px solid #6366f1;
            border-radius: 10px;
            color: #000000;
            font-size: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .stTextArea textarea:focus {
            border-color: #818cf8;
            box-shadow: 0 0 15px rgba(129, 140, 248, 0.5);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="day4-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="day4-header">
        <h1 class="day4-title">Day 4 🌌</h1>
        <p class="day4-subtitle">Who Am I Without the World?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="task-card">
        <div style="text-align: center; color: #6366f1; font-size: 1.2rem;">
            <strong>Welcome to Day 4 🌌</strong>
        </div>
        <p style="color: #ffffff; margin-top: 1rem; text-align: center; font-size: 1.1rem;">
            Today, let’s think about who you are without any roles, labels, or what others expect from you.
             Who are you when you let go of everything the world says you should be?
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Labels explanation
    st.markdown("""
    <div class="labels-info">
        <h4 style="color: #6366f1; margin-bottom: 1rem;">💭 What Are "Labels"?</h4>
        <p style="margin-bottom: 0.5rem;">
            Sometimes, we wear so many labels that we forget who we are without them.
        <p style="margin-bottom: 0.5rem;">
            "I'm a teacher," "I'm someone's partner," "I'm the responsible one," "I'm shy," "I'm successful."
        </p>
        <p style="margin-bottom: 0;">
            But are these truly you, or just roles you've learned to play?

In The Art of Being Alone, we’re reminded that real self-connection begins when we stop defining ourselves by the outside world.
When you're not someone’s friend, daughter, partner, or student—who are you, really?
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task 1: 4-Minute Silence the Noise
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🧘‍♀️ Task 1: Silence the Noise
        </div>
        <div class="task-instruction">
            Sit quietly and imagine a world where <strong>no one knows your name, age, status, or role</strong>. 
            You're just... you. Who are you when you're not trying to be someone? 
            Just sit with this feeling. Let the silence reveal your true self.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer logic
    if not st.session_state.day4_timer_running and not st.session_state.day4_task1_completed:
        if st.button("🌌 Start Task 1 (4-Minute Identity Meditation)", key="start_task1_day4"):
            st.session_state.day4_timer_running = True
            st.session_state.day4_timer_start = time.time()
            if play_ambient_music():
                st.success("🎵 Deep space ambient sounds started. Float beyond all definitions.")
            st.rerun()

    # Show timer if running
    if st.session_state.day4_timer_running:
        if st.session_state.day4_timer_start:
            elapsed_time = time.time() - st.session_state.day4_timer_start
            remaining_time = max(0, 240 - elapsed_time)  # 4 minutes = 240 seconds
        if remaining_time > 0:
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            st.markdown(f"""
            <div class="timer-display">
                {minutes:02d}:{seconds:02d}
            </div>
            """, unsafe_allow_html=True)

            # Progress bar
            progress = (240 - remaining_time) / 240
            st.progress(progress)

            # Stop Timer Button
            if st.button("⏹️ Stop Timer", key="stop_task1"):
                st.session_state.day4_timer_running = False
                st.session_state.day4_timer_start = None
                stop_ambient_music()
                st.success("⏹️ Timer stopped.")
                st.rerun()

            # Auto-refresh every second
            time.sleep(1)
            st.rerun()
        else:
            # Timer completed
            st.session_state.day4_timer_running = False
            st.session_state.day4_task1_completed = True
            stop_ambient_music()
            st.rerun()
    
    # Show completion message for Task 1
    if st.session_state.day4_task1_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 1 Completed!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="motivational-quote">
            "You are not who you think you are. You are not who others think you are. You are who you think others think you are. But who are you really?" 🌟
        </div>
        """, unsafe_allow_html=True)
    
    # Task 2: Journal Prompt – Who Am I Without Labels?
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            ✍️ Task 2: Who Am I Without Labels?
        </div>
        <div class="task-instruction">
            <strong>Without using your name, job, gender, age, or any social role...</strong> describe yourself. 
            What remains when you remove every label the world gave you? Write about your essence, 
            your core being, the "you" that exists beyond all definitions.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text area for reflection
    reflection_text = st.text_area(
        "Who Am I Beyond Labels:",
        value=st.session_state.day4_reflection_text,
        height=200,
        placeholder="I am... (without using name, job, age, gender, or social roles)\n\nAt my core, I feel like...\n\nWhen no one is watching, I am...\n\nThe essence of who I am is...\n\nWhat remains when all labels are stripped away is...",
        key="reflection_input"
    )
    
    # Update session state
    st.session_state.day4_reflection_text = reflection_text
    
    # Submit button for Task 2
    if st.button("🌟 Submit My Essence Reflection", key="submit_task2_day4"):
        if reflection_text.strip():
            # Save reflection
            if save_reflection(reflection_text):
                st.session_state.day4_task2_completed = True
                st.success("✅ Your essence reflection has been captured.")
                with st.spinner("AI is contemplating your true self..."):
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
    if st.session_state.day4_task2_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 2 Completed! Your essence has been honored and preserved.
        </div>
        """, unsafe_allow_html=True)
    
    # Day completion check
    if st.session_state.day4_task1_completed and st.session_state.day4_task2_completed:
        st.markdown("""
        <div class="task-card" style="border-color: #00ff00;">
            <div style="text-align: center; color: #00ff00; font-size: 1.5rem;">
                🎉 Congratulations! You've completed Day 4! 🎉
            </div>
            <p style="color: #ffffff; margin-top: 1rem; text-align: center;">
                You've glimpsed your true self beyond all worldly definitions. This is profound work — 
                you've connected with your essence, the part of you that exists independent of external validation. 
                Tomorrow, we'll continue this journey of self-discovery.
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
        if st.button("🔄 Reset Day 4", key="reset_day4"):
            # Reset all Day 4 session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('day4_')]
            for key in keys_to_remove:
                del st.session_state[key]
            stop_ambient_music()
            st.rerun()
    
    with col3:
        if st.button("➡️ Next Day", key="next_day"):
            st.session_state.selected_day = 5
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

# If running this file directly (for testing)
if __name__ == "__main__":
    st.set_page_config(
        page_title="SoulScanner - Day 4",
        page_icon="🌌",
        layout="centered"
    )
    show_day4_screen()