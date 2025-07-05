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

def init_day7_session_state():
    """Initialize session state variables for Day 7"""
    if 'day7_task1_completed' not in st.session_state:
        st.session_state.day7_task1_completed = False
    if 'day7_task2_completed' not in st.session_state:
        st.session_state.day7_task2_completed = False
    if 'day7_timer_running' not in st.session_state:
        st.session_state.day7_timer_running = False
    if 'day7_timer_start' not in st.session_state:
        st.session_state.day7_timer_start = None
    if 'day7_reflection_text' not in st.session_state:
        st.session_state.day7_reflection_text = ""

def save_reflection(reflection_text):
    """Save user reflection to a local file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save reflection with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = data_dir / f"day7_reflection_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Day 7 Reflection - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write("Task 2: People Who Shape Me\n\n")
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
        music_path = Path("music/relax.mp3")  # Changed to wind chimes + ambient for Day 7
        
        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            return True
        else:
            st.warning("🎵 Music file not found. Create a 'music' folder and add 'wind_chimes_ambient.mp3' for ambient sounds.")
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

def show_day7_screen():
    """Main function to display Day 7 screen"""
    
    # Initialize session state
    init_day7_session_state()
    
    # Custom CSS for Day 7
    st.markdown("""
    <style>
        /* Day 7 specific styling */
        .day7-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .day7-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .day7-title {
            font-size: 3rem;
            font-weight: bold;
            color: #10b981;
            text-shadow: 0 0 20px #10b981;
            margin-bottom: 1rem;
        }
        
        .day7-subtitle {
            font-size: 1.3rem;
            color: #34d399;
            font-style: italic;
        }
        
        .task-card {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid #10b981;
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .task-card:hover {
            border-color: #34d399;
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
        }
        
        .task-header {
            color: #10b981;
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
            color: #10b981;
            text-align: center;
            margin: 2rem 0;
            text-shadow: 0 0 20px #10b981;
        }
        
        .motivational-quote {
            background: linear-gradient(135deg, #10b981, #34d399);
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
            border: 2px solid #10b981;
            border-radius: 10px;
            color: #000000;
            font-size: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .stTextArea textarea:focus {
            border-color: #34d399;
            box-shadow: 0 0 15px rgba(52, 211, 153, 0.5);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="day7-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="day7-header">
        <h1 class="day7-title">Day 7 💡</h1>
        <p class="day7-subtitle">The Relationship Mirror</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="task-card">
        <div style="text-align: center; color: #10b981; font-size: 1.2rem;">
            <strong>Welcome to Day 7 💡</strong>
        </div>
        <p style="color: #ffffff; margin-top: 1rem; text-align: center; font-size: 1.1rem;">
            The people around you say a lot about you. They reflect your thoughts, your energy, and even how you see yourself.
             Ever notice how some people lift you up and others drain you? Today, take a moment to think about what your relationships are showing you about you.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task 1: 5-Minute Relationship Reflection
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🧘‍♀️ Task 1: Relationship Reflection
        </div>
        <div class="task-instruction">
            Close your eyes. Think of one person you interact with often. Now observe: how does your body feel 
            when you think of them? Heavy? Light? Safe? Nervous? Let these emotions speak. 
            <strong>Notice the physical sensations</strong> — your body knows the truth about every relationship.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer logic
    if not st.session_state.day7_timer_running and not st.session_state.day7_task1_completed:
        if st.button("💡 Start Task 1 (5-Minute Relationship Reflection)", key="start_task1_day7"):
            st.session_state.day7_timer_running = True
            st.session_state.day7_timer_start = time.time()
            if play_ambient_music():
                st.success("🎵 Wind chimes and ambient tones started. Begin reflecting on your relationships.")
            st.rerun()

    # Show timer if running
    if st.session_state.day7_timer_running:
        if st.session_state.day7_timer_start:
            elapsed_time = time.time() - st.session_state.day7_timer_start
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
                st.session_state.day7_timer_running = False
                st.session_state.day7_timer_start = None
                stop_ambient_music()
                st.success("⏹️ Timer stopped.")
                st.rerun()

            # Auto-refresh every second
            time.sleep(1)
            st.rerun()
        else:
            # Timer completed
            st.session_state.day7_timer_running = False
            st.session_state.day7_task1_completed = True
            stop_ambient_music()
            st.rerun()
    
    # Show completion message for Task 1
    if st.session_state.day7_task1_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 1 Completed!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="motivational-quote">
            "Your body is the truth detector your mind often ignores. You've just listened to the wisdom of your relationships." 💡
        </div>
        """, unsafe_allow_html=True)
    
    # Task 2: Journal Prompt – People Who Shape Me
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            ✍️ Task 2: People Who Shape Me
        </div>
        <div class="task-instruction">
            Write about <strong>one person who lifts your energy</strong>, and <strong>one who drains it</strong>. 
            Why do you think that happens? How can you protect your energy while still being kind? 
            What do these relationships teach you about yourself?
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text area for reflection
    reflection_text = st.text_area(
        "People Who Shape Me Analysis:",
        value=st.session_state.day7_reflection_text,
        height=250,
        placeholder="Person who lifts my energy:\nName (or initials): \nHow they make me feel: \nWhy I think this happens: \nWhat this teaches me about myself: \n\nPerson who drains my energy:\nName (or initials): \nHow they make me feel: \nWhy I think this happens: \nWhat this teaches me about myself: \n\nHow I can protect my energy while still being kind:\n\nWhat these relationships reveal about my needs and boundaries:",
        key="reflection_input"
    )
    
    # Update session state
    st.session_state.day7_reflection_text = reflection_text
    
    # Submit button for Task 2
    if st.button("💡 Submit My Relationship Analysis", key="submit_task2_day7"):
        if reflection_text.strip():
            # Save reflection
            if save_reflection(reflection_text):
                st.session_state.day7_task2_completed = True
                st.success("✅ Your relationship analysis has been saved.")
                with st.spinner("AI is analyzing your relationship patterns..."):
                    ai_feedback = get_groq_feedback(reflection_text)
                st.markdown(f"""
                         <div class="motivational-quote">
                         {ai_feedback}
                         </div>
                         """, unsafe_allow_html=True)
            else:
                st.error("❌ Error saving reflection. Please try again.")
        else:
            st.warning("⚠️ Please analyze your relationships before submitting.")
    
    # Show completion status
    if st.session_state.day7_task2_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 2 Completed! Your relationship awareness is now crystal clear.
        </div>
        """, unsafe_allow_html=True)
    
    # Day completion check
    if st.session_state.day7_task1_completed and st.session_state.day7_task2_completed:
        st.markdown("""
        <div class="task-card" style="border-color: #00ff00;">
            <div style="text-align: center; color: #00ff00; font-size: 1.5rem;">
                🎉 Congratulations! You've completed Day 7! 🎉
            </div>
            <p style="color: #ffffff; margin-top: 1rem; text-align: center;">
                You've gained powerful insights into how relationships shape your energy and well-being. 
                The people in your life are mirrors, showing you aspects of yourself and your boundaries. 
                This awareness empowers you to cultivate relationships that nurture your growth while 
                protecting your energy. You now understand that healthy relationships are not just about 
                being kind — they're about honoring your own needs and creating space for mutual respect.
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
        if st.button("💡 Reset Day 7", key="reset_day7"):
            # Reset all Day 7 session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('day7_')]
            for key in keys_to_remove:
                del st.session_state[key]
            stop_ambient_music()
            st.rerun()
    
    with col3:
        if st.button("➡️ Next Day", key="next_day"):
            st.session_state.selected_day = 8
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

# If running this file directly (for testing)
if __name__ == "__main__":
    st.set_page_config(
        page_title="SoulScanner - Day 7",
        page_icon="💡",
        layout="centered"
    )
    show_day7_screen()