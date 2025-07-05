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

def init_day9_session_state():
    """Initialize session state variables for Day 9"""
    if 'day9_task1_completed' not in st.session_state:
        st.session_state.day9_task1_completed = False
    if 'day9_task2_completed' not in st.session_state:
        st.session_state.day9_task2_completed = False
    if 'day9_timer_running' not in st.session_state:
        st.session_state.day9_timer_running = False
    if 'day9_timer_start' not in st.session_state:
        st.session_state.day9_timer_start = None
    if 'day9_reflection_text' not in st.session_state:
        st.session_state.day9_reflection_text = ""

def save_reflection(reflection_text):
    """Save user reflection to a local file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save reflection with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = data_dir / f"day9_reflection_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Day 9 Reflection - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write("Task 2: My Creative Self\n\n")
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
        music_path = Path("music/relax.mp3")  # Changed to relaxing ambient music for Day 9

        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            return True
        else:
            st.warning("🎵 Music file not found. Create a 'music' folder and add 'soulful_piano.mp3' for ambient sounds.")
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

def show_day9_screen():
    """Main function to display Day 9 screen"""
    
    # Initialize session state
    init_day9_session_state()
    
    # Custom CSS for Day 9
    st.markdown("""
    <style>
        /* Day 9 specific styling */
        .day9-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .day9-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .day9-title {
            font-size: 3rem;
            font-weight: bold;
            color: #f59e0b;
            text-shadow: 0 0 20px #f59e0b;
            margin-bottom: 1rem;
        }
        
        .day9-subtitle {
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
        
        .creativity-icon {
            font-size: 2rem;
            margin-right: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="day9-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="day9-header">
        <h1 class="day9-title">Day 9 💡</h1>
        <p class="day9-subtitle">Creativity is Expression</p>
    
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="task-card">
        <div style="text-align: center; color: #f59e0b; font-size: 1.2rem;">
            <strong>Welcome to Day 9💡</strong>
        </div>
        <p style="color: #ffffff; margin-top: 1rem; text-align: center; font-size: 1.1rem;">
            Creativity isn’t just about painting or writing — it’s about expressing what’s deep inside you in your own unique way. Everyone has a creative spark, including you. 
            Today, give yourself the space to explore it without overthinking. Your ideas, your voice, your way of creating — they matter.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task 1: 5-Minute Creative Visualization
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🧘‍♀️ Task 1: Creative Visualization 
        </div>
        <div class="task-instruction">
            Close your eyes and imagine yourself creating freely — maybe you’re painting, dancing, writing, or just letting your thoughts flow. No pressure, no judgment, just you being fully yourself.
             How does it feel? Light? Joyful? Free? Let that feeling sink in. This is your true creative self — confident, expressive, and alive.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer logic
    if not st.session_state.day9_timer_running and not st.session_state.day9_task1_completed:
        if st.button("💡 Start Task 1 (5-Minute Creative Journey)", key="start_task1_day9"):
            st.session_state.day9_timer_running = True
            st.session_state.day9_timer_start = time.time()
            if play_ambient_music():
                st.success("🎵 Soulful piano music started. Begin your creative visualization.")
            st.rerun()

    # Show timer if running
    if st.session_state.day9_timer_running:
        if st.session_state.day9_timer_start:
            elapsed_time = time.time() - st.session_state.day9_timer_start
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
                st.session_state.day9_timer_running = False
                st.session_state.day9_timer_start = None
                stop_ambient_music()
                st.success("⏹️ Timer stopped.")
                st.rerun()

            # Auto-refresh every second
            time.sleep(1)
            st.rerun()
        else:
            # Timer completed
            st.session_state.day9_timer_running = False
            st.session_state.day9_task1_completed = True
            stop_ambient_music()
            st.rerun()
    
    # Show completion message for Task 1
    if st.session_state.day9_task1_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 1 Completed!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="motivational-quote">
            "You've just connected with your creative essence. That vision of yourself expressing freely is not a dream — it's a possibility waiting to be born." 🎨
        </div>
        """, unsafe_allow_html=True)
    
    # Task 2: Journal Prompt – My Creative Self
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            ✍️ Task 2: My Creative Self
        </div>
        <div class="task-instruction">
            What’s one creative thing you’ve always wanted to try — maybe painting, singing, or writing — but never gave yourself the chance? What stopped you? Fear? Doubt? Time?
             Imagine how it would feel to finally go for it, just for you. Your creativity matters, and the world deserves to see the beauty only you can create.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text area for reflection
    reflection_text = st.text_area(
        "My Creative Expression Journey:",
        value=st.session_state.day9_reflection_text,
        height=280,
        placeholder="The form of expression I've always wanted to try:\n\nWhat has held me back from trying it:\n\nThe fears or doubts I have about creative expression:\n\nWhat it would mean to finally let myself try:\n\nHow I imagine I would feel when expressing myself freely:\n\nThe message or feeling I want to share through my creativity:\n\nWhat I would tell someone else who's afraid to be creative:\n\nMy commitment to honoring my creative self:",
        key="reflection_input"
    )
    
    # Update session state
    st.session_state.day9_reflection_text = reflection_text
    
    # Submit button for Task 2
    if st.button("💡 Submit My Creative Self Reflection", key="submit_task2_day9"):
        if reflection_text.strip():
            # Save reflection
            if save_reflection(reflection_text):
                st.session_state.day9_task2_completed = True
                st.success("✅ Your creative self reflection has been saved.")
                with st.spinner("AI is reflecting on your creative journey..."):
                    ai_feedback = get_groq_feedback(reflection_text)
                st.markdown(f"""
                         <div class="motivational-quote">
                         {ai_feedback}
                         </div>
                         """, unsafe_allow_html=True)
            else:
                st.error("❌ Error saving reflection. Please try again.")
        else:
            st.warning("⚠️ Please write your creative self reflection before submitting.")
    
    # Show completion status
    if st.session_state.day9_task2_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 2 Completed! Your creative voice has been acknowledged and honored.
        </div>
        """, unsafe_allow_html=True)
    
    # Day completion check
    if st.session_state.day9_task1_completed and st.session_state.day9_task2_completed:
        st.markdown("""
        <div class="task-card" style="border-color: #00ff00;">
            <div style="text-align: center; color: #00ff00; font-size: 1.5rem;">
                🎉 Congratulations! You've completed Day 9! 🎉
            </div>
            <p style="color: #ffffff; margin-top: 1rem; text-align: center;">
                You've just taken a profound step toward honoring your creative self. Creativity isn't a luxury — 
                it's a necessity for the soul. The form of expression you've always wanted to try isn't just a hobby; 
                it's a calling from your authentic self. Remember: you don't have to be perfect to be creative. 
                You just have to be brave enough to begin. Your unique creative voice is needed in this world, 
                and today you've taken the first step toward letting it be heard.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional creative encouragement
        st.markdown("""
        <div class="motivational-quote">
            <span class="creativity-icon">🎨</span>
            "Your creativity is not a talent you either have or don't have. It's a birthright waiting to be claimed." 
            <span class="creativity-icon">🌟</span>
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
        if st.button("💡 Reset Day 9", key="reset_day9"):
            # Reset all Day 9 session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('day9_')]
            for key in keys_to_remove:
                del st.session_state[key]
            stop_ambient_music()
            st.rerun()
    
    with col3:
        if st.button("➡️ Next Day", key="next_day"):
            st.session_state.selected_day = 10
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

# If running this file directly (for testing)
if __name__ == "__main__":
    st.set_page_config(
        page_title="SoulScanner - Day 9",
        page_icon="💡",
        layout="centered"
    )
    show_day9_screen()