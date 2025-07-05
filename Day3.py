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

def init_day3_session_state():
    """Initialize session state variables for Day 3"""
    if 'day3_task1_completed' not in st.session_state:
        st.session_state.day3_task1_completed = False
    if 'day3_task2_completed' not in st.session_state:
        st.session_state.day3_task2_completed = False
    if 'day3_timer_running' not in st.session_state:
        st.session_state.day3_timer_running = False
    if 'day3_timer_start' not in st.session_state:
        st.session_state.day3_timer_start = None
    if 'day3_reflection_text' not in st.session_state:
        st.session_state.day3_reflection_text = ""

def save_reflection(reflection_text):
    """Save user reflection to a local file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save reflection with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = data_dir / f"day3_reflection_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Day 3 Reflection - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write("Task 2: What Are You Afraid Of?\n\n")
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
        music_path = Path("music/relax.mp3")  # Changed to relax for Day 3

        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            return True
        else:
            st.warning("🎵 Music file not found. Create a 'music' folder and add 'ambient.mp3' for ambient sounds.")
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

def show_day3_screen():
    """Main function to display Day 3 screen"""
    
    # Initialize session state
    init_day3_session_state()
    
    # Custom CSS for Day 3
    st.markdown("""
    <style>
        /* Day 3 specific styling */
        .day3-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .day3-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .day3-title {
            font-size: 3rem;
            font-weight: bold;
            color: #8b5cf6;
            text-shadow: 0 0 20px #8b5cf6;
            margin-bottom: 1rem;
        }
        
        .day3-subtitle {
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
        
        .fear-warning {
            background: rgba(139, 92, 246, 0.2);
            border: 2px solid #8b5cf6;
            border-radius: 10px;
            padding: 1rem;
            color: #a78bfa;
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
    st.markdown('<div class="day3-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="day3-header">
        <h1 class="day3-title">Day 3 🌑</h1>
        <p class="day3-subtitle">Facing Your Fears</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="task-card">
        <div style="text-align: center; color: #8b5cf6; font-size: 1.2rem;">
            <strong>Welcome to Day 3 🌑</strong>
        </div>
        <p style="color: #ffffff; margin-top: 1rem; text-align: center; font-size: 1.1rem;">
            Today we explore the shadows within us. Fear is not the enemy — it's a teacher. 
            By acknowledging what frightens us, we begin to understand ourselves more deeply.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gentle warning
    st.markdown("""
    <div class="fear-warning">
        💜 Gentle Reminder: This is a safe space. Go at your own pace and be compassionate with yourself.
    </div>
    """, unsafe_allow_html=True)
    
    # Task 1: 5-Minute Fear Visualization
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🧘‍♀️ Task 1: Visualize Your Fear 
        </div>
        <div class="task-instruction">
            Sit in a quiet place. Close your eyes for 5 minutes. Gently ask yourself: 
            <em>"What is the one fear that has been living in me lately?"</em> 
            Let the image come naturally — don't force it. Just observe it. Don't fight it.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer logic
    if not st.session_state.day3_timer_running and not st.session_state.day3_task1_completed:
        if st.button("🌑 Start Task 1 (5-Minute Fear Visualization)", key="start_task1_day3"):
            st.session_state.day3_timer_running = True
            st.session_state.day3_timer_start = time.time()
            if play_ambient_music():
                st.success("🎵 Ambient sounds started. Breathe deeply and let your awareness expand.")
            st.rerun()

    # Show timer if running
    if st.session_state.day3_timer_running:
        if st.session_state.day3_timer_start:
            elapsed_time = time.time() - st.session_state.day3_timer_start
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
                st.session_state.day3_timer_running = False
                st.session_state.day3_timer_start = None
                stop_ambient_music()
                st.success("⏹️ Timer stopped.")
                st.rerun()

            # Auto-refresh every second
            time.sleep(1)
            st.rerun()
        else:
            # Timer completed
            st.session_state.day3_timer_running = False
            st.session_state.day3_task1_completed = True
            stop_ambient_music()
            st.rerun()
    
    # Show completion message for Task 1
    if st.session_state.day3_task1_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 1 Completed!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="motivational-quote">
            "The cave you fear to enter holds the treasure you seek." 🌟
        </div>
        """, unsafe_allow_html=True)
    
    # Task 2: Journal Prompt – "What Are You Afraid Of?"
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            ✍️ Task 2: What Are You Afraid Of?
        </div>
        <div class="task-instruction">
            Write about <strong>one thing you fear deeply</strong> — and why. Where did this fear come from? 
            How has it affected your choices or thoughts? Be honest and gentle with yourself. 
            Remember: naming your fear is the first step to understanding it.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text area for reflection
    reflection_text = st.text_area(
        "Your Fear Reflection:",
        value=st.session_state.day3_reflection_text,
        height=200,
        placeholder="I am afraid of... because...\n\nThis fear might have started when...\n\nIt has affected my life by...\n\nWhat I've learned about this fear is...",
        key="reflection_input"
    )
    
    # Update session state
    st.session_state.day3_reflection_text = reflection_text
    
    # Submit button for Task 2
    if st.button("💜 Submit My Fear Reflection", key="submit_task2_day3"):
        if reflection_text.strip():
            # Save reflection
            if save_reflection(reflection_text):
                st.session_state.day3_task2_completed = True
                st.success("✅ Your fear reflection has been saved with care.")
                with st.spinner("AI is gently processing your courage..."):
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
    if st.session_state.day3_task2_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 2 Completed! Your fear reflection has been safely stored.
        </div>
        """, unsafe_allow_html=True)
    
    # Day completion check
    if st.session_state.day3_task1_completed and st.session_state.day3_task2_completed:
        st.markdown("""
        <div class="task-card" style="border-color: #00ff00;">
            <div style="text-align: center; color: #00ff00; font-size: 1.5rem;">
                🎉 Congratulations! You've completed Day 3! 🎉
            </div>
            <p style="color: #ffffff; margin-top: 1rem; text-align: center;">
                You've shown incredible courage by facing your fears. This act of acknowledgment 
                is a profound step toward inner freedom. Tomorrow, we'll explore another facet of your journey.
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
        if st.button("🔄 Reset Day 3", key="reset_day3"):
            # Reset all Day 3 session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('day3_')]
            for key in keys_to_remove:
                del st.session_state[key]
            stop_ambient_music()
            st.rerun()
    
    with col3:
        if st.button("➡️ Next Day", key="next_day"):
            st.session_state.selected_day = 4
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

# If running this file directly (for testing)
if __name__ == "__main__":
    st.set_page_config(
        page_title="SoulScanner - Day 3",
        page_icon="🌑",
        layout="centered"
    )
    show_day3_screen()