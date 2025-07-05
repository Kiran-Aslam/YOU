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

def init_day8_session_state():
    """Initialize session state variables for Day 8"""
    if 'day8_task1_completed' not in st.session_state:
        st.session_state.day8_task1_completed = False
    if 'day8_task2_completed' not in st.session_state:
        st.session_state.day8_task2_completed = False
    if 'day8_timer_running' not in st.session_state:
        st.session_state.day8_timer_running = False
    if 'day8_timer_start' not in st.session_state:
        st.session_state.day8_timer_start = None
    if 'day8_reflection_text' not in st.session_state:
        st.session_state.day8_reflection_text = ""

def save_reflection(reflection_text):
    """Save user reflection to a local file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save reflection with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = data_dir / f"day8_reflection_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Day 8 Reflection - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write("Task 2: Me as a Child\n\n")
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
        music_path = Path("music/relax.mp3")  # Changed to relaxing ambient music for Day 8

        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            return True
        else:
            st.warning("🎵 Music file not found. Create a 'music' folder and add 'music_box_lullaby.mp3' for ambient sounds.")
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

def show_day8_screen():
    """Main function to display Day 8 screen"""
    
    # Initialize session state
    init_day8_session_state()
    
    # Custom CSS for Day 8
    st.markdown("""
    <style>
        /* Day 8 specific styling */
        .day8-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .day8-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .day8-title {
            font-size: 3rem;
            font-weight: bold;
            color: #ec4899;
            text-shadow: 0 0 20px #ec4899;
            margin-bottom: 1rem;
        }
        
        .day8-subtitle {
            font-size: 1.3rem;
            color: #f472b6;
            font-style: italic;
        }
        
        .task-card {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid #ec4899;
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .task-card:hover {
            border-color: #f472b6;
            box-shadow: 0 8px 25px rgba(236, 72, 153, 0.3);
        }
        
        .task-header {
            color: #ec4899;
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
            color: #ec4899;
            text-align: center;
            margin: 2rem 0;
            text-shadow: 0 0 20px #ec4899;
        }
        
        .motivational-quote {
            background: linear-gradient(135deg, #ec4899, #f472b6);
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
            border: 2px solid #ec4899;
            border-radius: 10px;
            color: #000000;
            font-size: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .stTextArea textarea:focus {
            border-color: #f472b6;
            box-shadow: 0 0 15px rgba(244, 114, 182, 0.5);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="day8-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="day8-header">
        <h1 class="day8-title">Day 8 🌟</h1>
        <p class="day8-subtitle">A Walk Through Childhood</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="task-card">
        <div style="text-align: center; color: #ec4899; font-size: 1.2rem;">
            <strong>Welcome to Day 8 🌟</strong>
        </div>
        <p style="color: #ffffff; margin-top: 1rem; text-align: center; font-size: 1.1rem;">
            Today, we’re taking a soft step back in time — to the little you. Before rules, pressure, or “shoulds,” there was a version of you full of wonder, curiosity, and real joy.
             That inner child still lives in you, holding clues to what truly lights you up. Let’s reconnect with that magic today.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task 1: 4-Minute Inner Child Visualization
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🧘‍♀️ Task 1: Inner Child Visualization 
        </div>
        <div class="task-instruction">
            Sit back, close your eyes. Picture yourself at age 7. Where are you? What are you doing? 
            What do you love? Can you feel that freedom again — even for a moment? 
            <strong>Let that child show you what pure joy feels like.</strong> Don't judge, just observe and feel.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer logic
    if not st.session_state.day8_timer_running and not st.session_state.day8_task1_completed:
        if st.button("🌟 Start Task 1 (4-Minute Inner Child Journey)", key="start_task1_day8"):
            st.session_state.day8_timer_running = True
            st.session_state.day8_timer_start = time.time()
            if play_ambient_music():
                st.success("🎵 Relaxing ambient music started. Begin your journey back to childhood.")
            st.rerun()

    # Show timer if running
    if st.session_state.day8_timer_running:
        if st.session_state.day8_timer_start:
            elapsed_time = time.time() - st.session_state.day8_timer_start
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
                st.session_state.day8_timer_running = False
                st.session_state.day8_timer_start = None
                stop_ambient_music()
                st.success("⏹️ Timer stopped.")
                st.rerun()

            # Auto-refresh every second
            time.sleep(1)
            st.rerun()
        else:
            # Timer completed
            st.session_state.day8_timer_running = False
            st.session_state.day8_task1_completed = True
            stop_ambient_music()
            st.rerun()
    
    # Show completion message for Task 1
    if st.session_state.day8_task1_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 1 Completed!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="motivational-quote">
            "You've just reconnected with the purest version of yourself. That child's dreams are still valid, still waiting to be honored." 🌟
        </div>
        """, unsafe_allow_html=True)
    
    # Task 2: Journal Prompt – Me as a Child
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            ✍️ Task 2: Me as a Child
        </div>
        <div class="task-instruction">
            What was something you loved doing as a child but haven’t done in ages? What did you crave most back then — love, safety, freedom? Take a moment and write a few kind, gentle words to that little version of you.
            They’re still with you, still hoping to be seen and loved. Let them know you haven’t forgotten them.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text area for reflection
    reflection_text = st.text_area(
        "Letter to My Inner Child:",
        value=st.session_state.day8_reflection_text,
        height=280,
        placeholder="What I loved doing as a child that I've forgotten:\n\nWhat I needed most back then:\n\nWhat made me feel most alive and free:\n\nThe dreams I had that felt impossible:\n\nDear Little Me,\nI want you to know that...\n\nI'm sorry for...\n\nI promise to...\n\nYou were perfect just as you were because...\n\nWith love,\nYour Grown-Up Self",
        key="reflection_input"
    )
    
    # Update session state
    st.session_state.day8_reflection_text = reflection_text
    
    # Submit button for Task 2
    if st.button("🌟 Submit My Letter to My Inner Child", key="submit_task2_day8"):
        if reflection_text.strip():
            # Save reflection
            if save_reflection(reflection_text):
                st.session_state.day8_task2_completed = True
                st.success("✅ Your letter to your inner child has been saved.")
                with st.spinner("AI is reflecting on your childhood connection..."):
                    ai_feedback = get_groq_feedback(reflection_text)
                st.markdown(f"""
                         <div class="motivational-quote">
                         {ai_feedback}
                         </div>
                         """, unsafe_allow_html=True)
            else:
                st.error("❌ Error saving reflection. Please try again.")
        else:
            st.warning("⚠️ Please write your letter to your inner child before submitting.")
    
    # Show completion status
    if st.session_state.day8_task2_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 2 Completed! Your inner child has been heard and honored.
        </div>
        """, unsafe_allow_html=True)
    
    # Day completion check
    if st.session_state.day8_task1_completed and st.session_state.day8_task2_completed:
        st.markdown("""
        <div class="task-card" style="border-color: #00ff00;">
            <div style="text-align: center; color: #00ff00; font-size: 1.5rem;">
                🎉 Congratulations! You've completed Day 8! 🎉
            </div>
            <p style="color: #ffffff; margin-top: 1rem; text-align: center;">
                You've just completed one of the most profound journeys — reconnecting with your inner child. 
                That little person inside you holds the blueprint of your authentic self, your purest dreams, 
                and your natural capacity for joy. The loves and needs you discovered today are not childish — 
                they are the foundation of who you truly are. Honor them, nurture them, and let them guide you 
                back to the life that feels most genuinely yours.
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
        if st.button("🌟 Reset Day 8", key="reset_day8"):
            # Reset all Day 8 session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('day8_')]
            for key in keys_to_remove:
                del st.session_state[key]
            stop_ambient_music()
            st.rerun()
    
    with col3:
        if st.button("➡️ Next Day", key="next_day"):
            st.session_state.selected_day = 9
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

# If running this file directly (for testing)
if __name__ == "__main__":
    st.set_page_config(
        page_title="SoulScanner - Day 8",
        page_icon="🌟",
        layout="centered"
    )
    show_day8_screen()