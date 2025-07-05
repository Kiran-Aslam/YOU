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

def init_day13_session_state():
    """Initialize session state variables for Day 13"""
    if 'day13_task1_completed' not in st.session_state:
        st.session_state.day13_task1_completed = False
    if 'day13_task2_completed' not in st.session_state:
        st.session_state.day13_task2_completed = False
    if 'day13_timer_running' not in st.session_state:
        st.session_state.day13_timer_running = False
    if 'day13_timer_start' not in st.session_state:
        st.session_state.day13_timer_start = None
    if 'day13_reflection_text' not in st.session_state:
        st.session_state.day13_reflection_text = ""

def save_reflection(reflection_text):
    """Save user reflection to a local file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save reflection with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = data_dir / f"day13_reflection_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Day 13 Reflection - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write("Task 2: If Nothing Stopped Me...\n\n")
            f.write(reflection_text)
        
        return True
    except Exception as e:
        st.error(f"Error saving reflection: {str(e)}")
        return False

def play_ambient_music():
    """Play inspiring ambient music if available"""
    if not AUDIO_AVAILABLE:
        return False
    
    try:
        pygame.mixer.init()
        music_path = Path("music/relax.mp3")  # Changed to relax for Day 13

        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            return True
        else:
            st.warning("🎵 Music file not found. Create a 'music' folder and add 'sunrise_soft_synth.mp3' for ambient sounds.")
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

def show_day13_screen():
    """Main function to display Day 13 screen"""
    
    # Initialize session state
    init_day13_session_state()
    
    # Custom CSS for Day 13
    st.markdown("""
    <style>
        /* Day 13 specific styling */
        .day13-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .day13-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .day13-title {
            font-size: 3rem;
            font-weight: bold;
            color: #f472b6;
            text-shadow: 0 0 20px #f472b6;
            margin-bottom: 1rem;
        }
        
        .day13-subtitle {
            font-size: 1.3rem;
            color: #fb7185;
            font-style: italic;
        }
        
        .task-card {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid #f472b6;
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .task-card:hover {
            border-color: #fb7185;
            box-shadow: 0 8px 25px rgba(244, 114, 182, 0.3);
        }
        
        .task-header {
            color: #f472b6;
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
            color: #f472b6;
            text-align: center;
            margin: 2rem 0;
            text-shadow: 0 0 20px #f472b6;
        }
        
        .motivational-quote {
            background: linear-gradient(135deg, #f472b6, #fb7185);
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
            border: 2px solid #f472b6;
            border-radius: 10px;
            color: #000000;
            font-size: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .stTextArea textarea:focus {
            border-color: #fb7185;
            box-shadow: 0 0 15px rgba(251, 113, 133, 0.5);
        }
        
        .dream-glow {
            animation: dreamGlow 3s ease-in-out infinite alternate;
        }
        
        @keyframes dreamGlow {
            from { text-shadow: 0 0 20px #f472b6; }
            to { text-shadow: 0 0 30px #fb7185, 0 0 40px #f472b6; }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="day13-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="day13-header">
        <h1 class="day13-title dream-glow">Day 13 ✨</h1>
        <p class="day13-subtitle">Let the Dream Speak</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="task-card">
        <div style="text-align: center; color: #f472b6; font-size: 1.2rem;">
            <strong>Welcome to Day 13 ✨</strong>
        </div>
        <p style="color: #ffffff; margin-top: 1rem; text-align: center; font-size: 1.1rem;">
            Today is about letting your dreams breathe again — with clarity and childlike wonder. Your imagination isn’t just daydreaming;
             it’s your soul showing you what’s possible. The dreams you’ve tucked away under fear or doubt? They’re still there, still alive. And today, you gently give them space to come back to life.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task 1: 5-Minute Dream Visualization
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🧘‍♀️ Task 1: Dream Visualization 
        </div>
        <div class="task-instruction">
            Close your eyes. Imagine your life five years from now — if fear, doubt, or limits didn't exist. 
            <strong>Where are you? Who's with you?</strong> Let the vision unfold naturally. Don't edit or judge — 
            just let your heart show you what it truly wants. This is your soul speaking through imagination.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer logic
    if not st.session_state.day13_timer_running and not st.session_state.day13_task1_completed:
        if st.button("✨ Start Task 1 (5-Minute Dream Visualization)", key="start_task1_day13"):
            st.session_state.day13_timer_running = True
            st.session_state.day13_timer_start = time.time()
            if play_ambient_music():
                st.success("🎵 Relaxing music started. Let your dreams unfold.")
            st.rerun()

    # Show timer if running
    if st.session_state.day13_timer_running:
        if st.session_state.day13_timer_start:
            elapsed_time = time.time() - st.session_state.day13_timer_start
            remaining_time = max(0, 300 - elapsed_time)  # 5 minutes = 300 seconds
        if remaining_time > 0:
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            st.markdown(f"""
            <div class="timer-display dream-glow">
                {minutes:02d}:{seconds:02d}
            </div>
            """, unsafe_allow_html=True)

            # Progress bar
            progress = (300 - remaining_time) / 300
            st.progress(progress)

            # Stop Timer Button
            if st.button("⏹️ Stop Timer", key="stop_task1"):
                st.session_state.day13_timer_running = False
                st.session_state.day13_timer_start = None
                stop_ambient_music()
                st.success("⏹️ Timer stopped.")
                st.rerun()

            # Auto-refresh every second
            time.sleep(1)
            st.rerun()
        else:
            # Timer completed
            st.session_state.day13_timer_running = False
            st.session_state.day13_task1_completed = True
            stop_ambient_music()
            st.rerun()
    
    # Show completion message for Task 1
    if st.session_state.day13_task1_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 1 Completed!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="motivational-quote">
            "Every great dream begins with a dreamer. You have within you the strength, the patience, and the passion to reach for the stars." ✨
        </div>
        """, unsafe_allow_html=True)
    
    # Task 2: Journal Prompt – If Nothing Stopped Me...
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            ✍️ Task 2: If Nothing Stopped Me...
        </div>
        <div class="task-instruction">
            What is <strong>one dream you've buried or ignored</strong>? Why does it still call to you? 
            What would it take to give it a chance again? Sometimes the dreams we've abandoned are the ones 
            our souls need most. It's time to excavate them with love and curiosity.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text area for reflection
    reflection_text = st.text_area(
        "If Nothing Stopped Me Analysis:",
        value=st.session_state.day13_reflection_text,
        height=200,
        placeholder="The dream I've buried or ignored:\n\nWhy this dream still calls to me:\n\nWhat made me abandon this dream:\n\nWhat it would take to give it a chance again:\n\nOne small step I could take toward this dream:\n\nHow my life would feel different if I pursued this dream:\n\nWhat I want to tell my younger self about dreams:",
        key="reflection_input"
    )
    
    # Update session state
    st.session_state.day13_reflection_text = reflection_text
    
    # Submit button for Task 2
    if st.button("✨ Submit My Dream Analysis", key="submit_task2_day13"):
        if reflection_text.strip():
            # Save reflection
            if save_reflection(reflection_text):
                st.session_state.day13_task2_completed = True
                st.success("✅ Your dream analysis has been saved.")
                with st.spinner("AI is exploring your dreams..."):
                    ai_feedback = get_groq_feedback(reflection_text)
                st.markdown(f"""
                         <div class="motivational-quote">
                         {ai_feedback}
                         </div>
                         """, unsafe_allow_html=True)
            else:
                st.error("❌ Error saving reflection. Please try again.")
        else:
            st.warning("⚠️ Please explore your dreams before submitting.")
    
    # Show completion status
    if st.session_state.day13_task2_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 2 Completed! Your dreams are no longer buried — they're alive and ready to grow.
        </div>
        """, unsafe_allow_html=True)
    
    # Day completion check
    if st.session_state.day13_task1_completed and st.session_state.day13_task2_completed:
        st.markdown("""
        <div class="task-card" style="border-color: #00ff00;">
            <div style="text-align: center; color: #00ff00; font-size: 1.5rem;">
                🎉 Congratulations! You've completed Day 13! 🎉
            </div>
            <p style="color: #ffffff; margin-top: 1rem; text-align: center;">
                You've reconnected with your dreams and given them permission to speak again. Your imagination has shown you 
                what's possible when fear and doubt step aside. These aren't just fantasies — they're glimpses of your 
                potential future. The dream you explored today is a seed. With attention, courage, and small daily actions, 
                seeds become forests. Your dreams are valid. Your dreams are possible. Your dreams are calling.
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
        if st.button("✨ Reset Day 13", key="reset_day13"):
            # Reset all Day 13 session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('day13_')]
            for key in keys_to_remove:
                del st.session_state[key]
            stop_ambient_music()
            st.rerun()
    
    with col3:
        if st.button("➡️ Next Day", key="next_day"):
            st.session_state.selected_day = 14
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

# If running this file directly (for testing)
if __name__ == "__main__":
    st.set_page_config(
        page_title="SoulScanner - Day 13",
        page_icon="✨",
        layout="centered"
    )
    show_day13_screen()