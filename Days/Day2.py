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

def init_day2_session_state():
    """Initialize session state variables for Day 2"""
    if 'day2_task1_completed' not in st.session_state:
        st.session_state.day2_task1_completed = False
    if 'day2_task2_completed' not in st.session_state:
        st.session_state.day2_task2_completed = False
    if 'day2_timer_running' not in st.session_state:
        st.session_state.day2_timer_running = False
    if 'day2_timer_start' not in st.session_state:
        st.session_state.day2_timer_start = None
    if 'day2_reflection_text' not in st.session_state:
        st.session_state.day2_reflection_text = ""

def save_reflection(reflection_text):
    """Save user reflection to a local file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save reflection with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = data_dir / f"day2_reflection_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Day 2 Reflection - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write("Task 2: What Makes You Genuinely Smile\n\n")
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
        music_path = Path("music/relax.mp3")  # Changed to relax for Day 2

        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            return True
        else:
            st.warning("🎵 Music file not found. Create a 'music' folder and add 'piano.mp3' for ambient sounds.")
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

def show_day2_screen():
    """Main function to display Day 2 screen"""
    
    # Initialize session state
    init_day2_session_state()
    
    # Custom CSS for Day 2
    st.markdown("""
    <style>
        /* Day 2 specific styling */
        .day2-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .day2-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .day2-title {
            font-size: 3rem;
            font-weight: bold;
            color: #ffdd00;
            text-shadow: 0 0 20px #ffdd00;
            margin-bottom: 1rem;
        }
        
        .day2-subtitle {
            font-size: 1.3rem;
            color: #ffa500;
            font-style: italic;
        }
        
        .task-card {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid #ffdd00;
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .task-card:hover {
            border-color: #ffa500;
            box-shadow: 0 8px 25px rgba(255, 165, 0, 0.3);
        }
        
        .task-header {
            color: #ffdd00;
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
            color: #ffdd00;
            text-align: center;
            margin: 2rem 0;
            text-shadow: 0 0 20px #ffdd00;
        }
        
        .motivational-quote {
            background: linear-gradient(135deg, #ffdd00, #ffa500);
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
            border: 2px solid #ffdd00;
            border-radius: 10px;
            color: #000000;
            font-size: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .stTextArea textarea:focus {
            border-color: #ffa500;
            box-shadow: 0 0 15px rgba(255, 165, 0, 0.5);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="day2-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="day2-header">
        <h1 class="day2-title">Day 2 😊</h1>
        <p class="day2-subtitle">What Makes You Smile?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="task-card">
        <div style="text-align: center; color: #ffdd00; font-size: 1.2rem;">
            <strong>Welcome to Day 2😊</strong>
        </div>
        <p style="color: #ffffff; margin-top: 1rem; text-align: center; font-size: 1.1rem;">
            Let’s pause for a moment and forget the stress. What truly makes you happy?
            Big or small, silly or serious—every little spark matters. ✨
            Ready to rediscover those tiny joys that light you up inside?
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task 1: 3-Minute Smile Meditation
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🧘‍♀️ Task 1: Smile Meditation
        </div>
        <div class="task-instruction">
            Sit in silence for 3 minutes. Gently close your eyes and bring to mind the <strong>last moment you genuinely smiled.</strong> 
            Who were you with? What were you doing? Just <strong>feel that moment</strong> again. Let that warmth fill your heart.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer logic
    if not st.session_state.day2_timer_running and not st.session_state.day2_task1_completed:
        if st.button("😊 Start Task 1 (3-Minute Smile Meditation)", key="start_task1_day2"):
            st.session_state.day2_timer_running = True
            st.session_state.day2_timer_start = time.time()
            if play_ambient_music():
                st.success("🎵 Gentle piano music started. Close your eyes and smile from within.")
            st.rerun()

    # Show timer if running
    if st.session_state.day2_timer_running:
        if st.session_state.day2_timer_start:
            elapsed_time = time.time() - st.session_state.day2_timer_start
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
                st.session_state.day2_timer_running = False
                st.session_state.day2_timer_start = None
                stop_ambient_music()
                st.success("⏹️ Timer stopped.")
                st.rerun()

            # Auto-refresh every second
            time.sleep(1)
            st.rerun()
        else:
            # Timer completed
            st.session_state.day2_timer_running = False
            st.session_state.day2_task1_completed = True
            stop_ambient_music()
            st.rerun()
    
    # Show completion message for Task 1
    if st.session_state.day2_task1_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 1 Completed!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="motivational-quote">
            "A smile is the universal language of kindness." 😊✨
        </div>
        """, unsafe_allow_html=True)
    
    # Task 2: Journal Prompt – "List What Makes You Genuinely Smile"
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            ✍️ Task 2: What Makes You Genuinely Smile?
        </div>
        <div class="task-instruction">
            Think of 3 things—big or small—that bring you genuine joy.
            It could be your favorite person, a cozy corner in your home, a song, or a memory that always warms you up inside. Write down why they bring you joy and what they mean to you. Sometimes the smallest things hold the most warmth. 💛
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text area for reflection
    reflection_text = st.text_area(
        "What Makes You Smile:",
        value=st.session_state.day2_reflection_text,
        height=200,
        placeholder="1. _____ makes me smile because...\n2. _____ brings me joy because...\n3. _____ lights up my heart because...",
        key="reflection_input_day2"
    )
    
    # Update session state
    st.session_state.day2_reflection_text = reflection_text
    
    # Submit button for Task 2
    if st.button("💛 Submit My Smile Reflection", key="submit_task2_day2"):
        if reflection_text.strip():
            # Save reflection
            if save_reflection(reflection_text):
                st.session_state.day2_task2_completed = True
                st.success("✅ Your smile reflection has been saved!")
                with st.spinner("AI is reflecting on your joy..."):
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
    if st.session_state.day2_task2_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 2 Completed! Your smile reflection has been saved.
        </div>
        """, unsafe_allow_html=True)
    
    # Day completion check
    if st.session_state.day2_task1_completed and st.session_state.day2_task2_completed:
        st.markdown("""
        <div class="task-card" style="border-color: #00ff00;">
            <div style="text-align: center; color: #00ff00; font-size: 1.5rem;">
                🎉 Congratulations! You've completed Day 2! 🎉
            </div>
            <p style="color: #ffffff; margin-top: 1rem; text-align: center;">
                You've connected with your inner joy and discovered what truly makes you smile. 
                Tomorrow, we'll explore another dimension of your beautiful self.
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
        if st.button("🔄 Reset Day 2", key="reset_day2"):
            # Reset all Day 2 session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('day2_')]
            for key in keys_to_remove:
                del st.session_state[key]
            stop_ambient_music()
            st.rerun()
    
    with col3:
        if st.button("➡️ Next Day", key="next_day"):
            st.session_state.selected_day = 3
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

# If running this file directly (for testing)
if __name__ == "__main__":
    st.set_page_config(
        page_title="SoulScanner - Day 2",
        page_icon="😊",
        layout="centered"
    )
    show_day2_screen()