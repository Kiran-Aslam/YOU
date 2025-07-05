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

def init_day11_session_state():
    """Initialize session state variables for Day 11"""
    if 'day11_task1_completed' not in st.session_state:
        st.session_state.day11_task1_completed = False
    if 'day11_task2_completed' not in st.session_state:
        st.session_state.day11_task2_completed = False
    if 'day11_timer_running' not in st.session_state:
        st.session_state.day11_timer_running = False
    if 'day11_timer_start' not in st.session_state:
        st.session_state.day11_timer_start = None
    if 'day11_reflection_text' not in st.session_state:
        st.session_state.day11_reflection_text = ""

def save_reflection(reflection_text):
    """Save user reflection to a local file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save reflection with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = data_dir / f"day11_reflection_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Day 11 Reflection - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write("Task 2: My Quiet Power\n\n")
            f.write(reflection_text)
        
        return True
    except Exception as e:
        st.error(f"Error saving reflection: {str(e)}")
        return False

def play_ambient_music():
    """Play empowering ambient music if available"""
    if not AUDIO_AVAILABLE:
        return False
    
    try:
        pygame.mixer.init()
        music_path = Path("music/relax.mp3")  # Changed to relax for Day 11

        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            return True
        else:
            st.warning("🎵 Music file not found. Create a 'music' folder and add 'drums_rising_tone.mp3' for ambient sounds.")
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

def show_day11_screen():
    """Main function to display Day 11 screen"""
    
    # Initialize session state
    init_day11_session_state()
    
    # Custom CSS for Day 11
    st.markdown("""
    <style>
        /* Day 11 specific styling */
        .day11-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .day11-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .day11-title {
            font-size: 3rem;
            font-weight: bold;
            color: #f59e0b;
            text-shadow: 0 0 20px #f59e0b;
            margin-bottom: 1rem;
        }
        
        .day11-subtitle {
            font-size: 1.3rem;
            color: #fbbf24;
            font-style: italic;
        }
        
        .task-card {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid #f59e0b;
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .task-card:hover {
            border-color: #fbbf24;
            box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3);
        }
        
        .task-header {
            color: #f59e0b;
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
            color: #f59e0b;
            text-align: center;
            margin: 2rem 0;
            text-shadow: 0 0 20px #f59e0b;
        }
        
        .motivational-quote {
            background: linear-gradient(135deg, #f59e0b, #fbbf24);
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
            border: 2px solid #f59e0b;
            border-radius: 10px;
            color: #000000;
            font-size: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .stTextArea textarea:focus {
            border-color: #fbbf24;
            box-shadow: 0 0 15px rgba(251, 191, 36, 0.5);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="day11-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="day11-header">
        <h1 class="day11-title">Day 11 💪</h1>
        <p class="day11-subtitle">Know Your Strength</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="task-card">
        <div style="text-align: center; color: #f59e0b; font-size: 1.2rem;">
            <strong>Welcome to Day 11 💪</strong>
        </div>
        <p style="color: #ffffff; margin-top: 1rem; text-align: center; font-size: 1.1rem;">
            Today is all about remembering your strength. You’ve made it through tough times,
         faced challenges, and survived every hard day so far. That’s not small — that’s resilience. Now it’s time to see that power in yourself and own it.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task 1: 3-Minute Inner Power Recall
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🧘‍♀️ Task 1: Inner Power Recall 
        </div>
        <div class="task-instruction">
            Close your eyes. Recall one moment in your life where you showed strength. It can be small — 
            even getting out of bed on a hard day. Feel that strength again. Hold it. Own it. 
            Let that feeling of resilience fill your entire being.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer logic
    if not st.session_state.day11_timer_running and not st.session_state.day11_task1_completed:
        if st.button("💪 Start Task 1 (3-Minute Inner Power Recall)", key="start_task1_day11"):
            st.session_state.day11_timer_running = True
            st.session_state.day11_timer_start = time.time()
            if play_ambient_music():
                st.success("🎵 Subtle drums and rising tones started. Begin recalling your inner strength.")
            st.rerun()

    # Show timer if running
    if st.session_state.day11_timer_running:
        if st.session_state.day11_timer_start:
            elapsed_time = time.time() - st.session_state.day11_timer_start
            remaining_time = max(0, 180 - elapsed_time)  # 3 minutes = 180 seconds
        if remaining_time > 0:
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            st.markdown(f"""
            <div class="timer-display">
                {minutes:02d}:{seconds:02d}
            </div>
            """, unsafe_allow_html=True)

            # Progress bar
            progress = (180 - remaining_time) / 180
            st.progress(progress)

            # Stop Timer Button
            if st.button("⏹️ Stop Timer", key="stop_task1"):
                st.session_state.day11_timer_running = False
                st.session_state.day11_timer_start = None
                stop_ambient_music()
                st.success("⏹️ Timer stopped.")
                st.rerun()

            # Auto-refresh every second
            time.sleep(1)
            st.rerun()
        else:
            # Timer completed
            st.session_state.day11_timer_running = False
            st.session_state.day11_task1_completed = True
            stop_ambient_music()
            st.rerun()
    
    # Show completion message for Task 1
    if st.session_state.day11_task1_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 1 Completed!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="motivational-quote">
            "You are braver than you believe, stronger than you seem, and more capable than you imagine. That strength you just felt? It's always been there." 💪
        </div>
        """, unsafe_allow_html=True)
    
    # Task 2: Journal Prompt – My Quiet Power
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            ✍️ Task 2: My Quiet Power
        </div>
        <div class="task-instruction">
            List <strong>3 moments where you surprised yourself</strong> with your resilience or strength. 
            What do these moments say about you? What kind of strength do you want to build more of? 
            Your quiet power is often your greatest power.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text area for reflection
    reflection_text = st.text_area(
        "My Quiet Power Analysis:",
        value=st.session_state.day11_reflection_text,
        height=200,
        placeholder="3 moments where I surprised myself:\n1. \n2. \n3. \n\nWhat these moments say about me:\n\nThe strength I want to build more of:\n\nHow I can tap into this strength when I need it most:\n\nOne way I'll honor my strength moving forward:",
        key="reflection_input"
    )
    
    # Update session state
    st.session_state.day11_reflection_text = reflection_text
    
    # Submit button for Task 2
    if st.button("💪 Submit My Quiet Power Analysis", key="submit_task2_day11"):
        if reflection_text.strip():
            # Save reflection
            if save_reflection(reflection_text):
                st.session_state.day11_task2_completed = True
                st.success("✅ Your quiet power analysis has been saved.")
                with st.spinner("AI is analyzing your inner strength..."):
                    ai_feedback = get_groq_feedback(reflection_text)
                st.markdown(f"""
                         <div class="motivational-quote">
                         {ai_feedback}
                         </div>
                         """, unsafe_allow_html=True)
            else:
                st.error("❌ Error saving reflection. Please try again.")
        else:
            st.warning("⚠️ Please analyze your quiet power before submitting.")
    
    # Show completion status
    if st.session_state.day11_task2_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 2 Completed! Your inner strength is now recognized and honored.
        </div>
        """, unsafe_allow_html=True)
    
    # Day completion check
    if st.session_state.day11_task1_completed and st.session_state.day11_task2_completed:
        st.markdown("""
        <div class="task-card" style="border-color: #00ff00;">
            <div style="text-align: center; color: #00ff00; font-size: 1.5rem;">
                🎉 Congratulations! You've completed Day 11! 🎉
            </div>
            <p style="color: #ffffff; margin-top: 1rem; text-align: center;">
                You've reconnected with your inner strength and recognized your resilience. This awareness is your superpower — 
                knowing that you've overcome challenges before means you can overcome whatever comes next. Your strength isn't 
                just in the big moments; it's in every small act of courage, every time you choose to keep going. 
                You are stronger than you think, and now you know it.
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
        if st.button("💪 Reset Day 11", key="reset_day11"):
            # Reset all Day 11 session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('day11_')]
            for key in keys_to_remove:
                del st.session_state[key]
            stop_ambient_music()
            st.rerun()
    
    with col3:
        if st.button("➡️ Next Day", key="next_day"):
            st.session_state.selected_day = 12
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

# If running this file directly (for testing)
if __name__ == "__main__":
    st.set_page_config(
        page_title="SoulScanner - Day 11",
        page_icon="💪",
        layout="centered"
    )
    show_day11_screen()