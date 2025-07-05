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

def init_day12_session_state():
    """Initialize session state variables for Day 12"""
    if 'day12_task1_completed' not in st.session_state:
        st.session_state.day12_task1_completed = False
    if 'day12_task2_completed' not in st.session_state:
        st.session_state.day12_task2_completed = False
    if 'day12_timer_running' not in st.session_state:
        st.session_state.day12_timer_running = False
    if 'day12_timer_start' not in st.session_state:
        st.session_state.day12_timer_start = None
    if 'day12_reflection_text' not in st.session_state:
        st.session_state.day12_reflection_text = ""

def save_reflection(reflection_text):
    """Save user reflection to a local file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save reflection with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = data_dir / f"day12_reflection_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Day 12 Reflection - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write("Task 2: My Guiding Values\n\n")
            f.write(reflection_text)
        
        return True
    except Exception as e:
        st.error(f"Error saving reflection: {str(e)}")
        return False

def play_ambient_music():
    """Play contemplative ambient music if available"""
    if not AUDIO_AVAILABLE:
        return False
    
    try:
        pygame.mixer.init()
        music_path = Path("music/relax.mp3")  # Changed to relax for Day 12

        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            return True
        else:
            st.warning("🎵 Music file not found. Create a 'music' folder and add 'soft_echo_flute.mp3' for ambient sounds.")
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

def show_day12_screen():
    """Main function to display Day 12 screen"""
    
    # Initialize session state
    init_day12_session_state()
    
    # Custom CSS for Day 12
    st.markdown("""
    <style>
        /* Day 12 specific styling */
        .day12-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .day12-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .day12-title {
            font-size: 3rem;
            font-weight: bold;
            color: #06b6d4;
            text-shadow: 0 0 20px #06b6d4;
            margin-bottom: 1rem;
        }
        
        .day12-subtitle {
            font-size: 1.3rem;
            color: #67e8f9;
            font-style: italic;
        }
        
        .task-card {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid #06b6d4;
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .task-card:hover {
            border-color: #67e8f9;
            box-shadow: 0 8px 25px rgba(6, 182, 212, 0.3);
        }
        
        .task-header {
            color: #06b6d4;
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
            color: #06b6d4;
            text-align: center;
            margin: 2rem 0;
            text-shadow: 0 0 20px #06b6d4;
        }
        
        .motivational-quote {
            background: linear-gradient(135deg, #06b6d4, #67e8f9);
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
            border: 2px solid #06b6d4;
            border-radius: 10px;
            color: #000000;
            font-size: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .stTextArea textarea:focus {
            border-color: #67e8f9;
            box-shadow: 0 0 15px rgba(103, 232, 249, 0.5);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="day12-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="day12-header">
        <h1 class="day12-title">Day 12 🧭</h1>
        <p class="day12-subtitle">The Compass Within</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="task-card">
        <div style="text-align: center; color: #06b6d4; font-size: 1.2rem;">
            <strong>Welcome to Day 12 🧭</strong>
        </div>
        <p style="color: #ffffff; margin-top: 1rem; text-align: center; font-size: 1.1rem;">
            Today is about tuning into what really matters to you. In a world full of noise and opinions,
            your values are like your inner compass — they help you make choices that feel right and real. Let’s take a moment to get clear on what you truly stand for.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task 1: 4-Minute Value Reflection
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🧘‍♀️ Task 1: Value Reflection
        </div>
        <div class="task-instruction">
            Sit quietly. Ask yourself: <strong>"If I could only live by 3 values, what would they be?"</strong> 
             Don’t force it — just breathe and listen. Let the answers rise from within, 
            not from what you think you should value, but from what truly feels right in your heart.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer logic
    if not st.session_state.day12_timer_running and not st.session_state.day12_task1_completed:
        if st.button("🧭 Start Task 1 (4-Minute Value Reflection)", key="start_task1_day12"):
            st.session_state.day12_timer_running = True
            st.session_state.day12_timer_start = time.time()
            if play_ambient_music():
                st.success("🎵 Soft echo and flute sounds started. Begin exploring your core values.")
            st.rerun()

    # Show timer if running
    if st.session_state.day12_timer_running:
        if st.session_state.day12_timer_start:
            elapsed_time = time.time() - st.session_state.day12_timer_start
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
                st.session_state.day12_timer_running = False
                st.session_state.day12_timer_start = None
                stop_ambient_music()
                st.success("⏹️ Timer stopped.")
                st.rerun()

            # Auto-refresh every second
            time.sleep(1)
            st.rerun()
        else:
            # Timer completed
            st.session_state.day12_timer_running = False
            st.session_state.day12_task1_completed = True
            stop_ambient_music()
            st.rerun()
    
    # Show completion message for Task 1
    if st.session_state.day12_task1_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 1 Completed!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="motivational-quote">
            "Your values are your compass. They don't change with the weather or the crowd. What you discovered just now? That's your true north." 🧭
        </div>
        """, unsafe_allow_html=True)
    
    # Task 2: Journal Prompt – My Guiding Values
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            ✍️ Task 2: My Guiding Values
        </div>
        <div class="task-instruction">
            What are <strong>3 values you wish to live by</strong>? How aligned is your current life with them? 
            What small shifts could bring you closer to living these values daily? Your compass is only useful 
            if you follow its direction.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text area for reflection
    reflection_text = st.text_area(
        "My Guiding Values Analysis:",
        value=st.session_state.day12_reflection_text,
        height=200,
        placeholder="My 3 core values are:\n1. \n2. \n3. \n\nHow aligned my current life is with these values:\n\nAreas where I'm living my values well:\n\nAreas where I'm not aligned with my values:\n\nSmall shifts I can make to live more aligned:\n\nOne action I'll take this week to honor my values:",
        key="reflection_input"
    )
    
    # Update session state
    st.session_state.day12_reflection_text = reflection_text
    
    # Submit button for Task 2
    if st.button("🧭 Submit My Guiding Values Analysis", key="submit_task2_day12"):
        if reflection_text.strip():
            # Save reflection
            if save_reflection(reflection_text):
                st.session_state.day12_task2_completed = True
                st.success("✅ Your guiding values analysis has been saved.")
                with st.spinner("AI is analyzing your inner compass..."):
                    ai_feedback = get_groq_feedback(reflection_text)
                st.markdown(f"""
                         <div class="motivational-quote">
                         {ai_feedback}
                         </div>
                         """, unsafe_allow_html=True)
            else:
                st.error("❌ Error saving reflection. Please try again.")
        else:
            st.warning("⚠️ Please analyze your guiding values before submitting.")
    
    # Show completion status
    if st.session_state.day12_task2_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 2 Completed! Your inner compass is now calibrated and clear.
        </div>
        """, unsafe_allow_html=True)
    
    # Day completion check
    if st.session_state.day12_task1_completed and st.session_state.day12_task2_completed:
        st.markdown("""
        <div class="task-card" style="border-color: #00ff00;">
            <div style="text-align: center; color: #00ff00; font-size: 1.5rem;">
                🎉 Congratulations! You've completed Day 12! 🎉
            </div>
            <p style="color: #ffffff; margin-top: 1rem; text-align: center;">
                You've discovered your inner compass — your core values that guide your path through life. 
                These aren't just abstract concepts; they're the foundation of authentic living. When you align 
                your actions with your values, you create a life of meaning and fulfillment. Your compass is now 
                clear. Trust it. Follow it. Let it guide you toward the life you truly want to live.
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
        if st.button("🧭 Reset Day 12", key="reset_day12"):
            # Reset all Day 12 session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('day12_')]
            for key in keys_to_remove:
                del st.session_state[key]
            stop_ambient_music()
            st.rerun()
    
    with col3:
        if st.button("➡️ Next Day", key="next_day"):
            st.session_state.selected_day = 13
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

# If running this file directly (for testing)
if __name__ == "__main__":
    st.set_page_config(
        page_title="SoulScanner - Day 12",
        page_icon="🧭",
        layout="centered"
    )
    show_day12_screen()