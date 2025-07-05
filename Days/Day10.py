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

def init_day10_session_state():
    """Initialize session state variables for Day 10"""
    if 'day10_task1_completed' not in st.session_state:
        st.session_state.day10_task1_completed = False
    if 'day10_task2_completed' not in st.session_state:
        st.session_state.day10_task2_completed = False
    if 'day10_timer_running' not in st.session_state:
        st.session_state.day10_timer_running = False
    if 'day10_timer_start' not in st.session_state:
        st.session_state.day10_timer_start = None
    if 'day10_reflection_text' not in st.session_state:
        st.session_state.day10_reflection_text = ""

def save_reflection(reflection_text):
    """Save user reflection to a local file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save reflection with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = data_dir / f"day10_reflection_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Day 10 Reflection - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write("Task 2: Facing It Gently\n\n")
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
        music_path = Path("music/relax.mp3")  # Changed to relaxing ambient music for Day 10

        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            return True
        else:
            st.warning("🎵 Music file not found. Create a 'music' folder and add 'heartbeat_wind.mp3' for ambient sounds.")
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

def show_day10_screen():
    """Main function to display Day 10 screen"""
    
    # Initialize session state
    init_day10_session_state()
    
    # Custom CSS for Day 10
    st.markdown("""
    <style>
        /* Day 10 specific styling */
        .day10-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .day10-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .day10-title {
            font-size: 3rem;
            font-weight: bold;
            color: #7c3aed;
            text-shadow: 0 0 20px #7c3aed;
            margin-bottom: 1rem;
        }
        
        .day10-subtitle {
            font-size: 1.3rem;
            color: #a855f7;
            font-style: italic;
        }
        
        .task-card {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid #7c3aed;
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .task-card:hover {
            border-color: #a855f7;
            box-shadow: 0 8px 25px rgba(124, 58, 237, 0.3);
        }
        
        .task-header {
            color: #7c3aed;
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
            color: #7c3aed;
            text-align: center;
            margin: 2rem 0;
            text-shadow: 0 0 20px #7c3aed;
        }
        
        .motivational-quote {
            background: linear-gradient(135deg, #7c3aed, #a855f7);
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
            border: 2px solid #7c3aed;
            border-radius: 10px;
            color: #000000;
            font-size: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .stTextArea textarea:focus {
            border-color: #a855f7;
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.5);
        }
        
        .fear-transformation {
            background: rgba(124, 58, 237, 0.1);
            border-left: 4px solid #7c3aed;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 10px 10px 0;
        }
        
        .courage-reminder {
            background: rgba(168, 85, 247, 0.2);
            border: 1px solid #a855f7;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            text-align: center;
            color: #ffffff;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="day10-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="day10-header">
        <h1 class="day10-title">Day 10 💡</h1>
        <p class="day10-subtitle">Name the Fear Again</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="task-card">
        <div style="text-align: center; color: #7c3aed; font-size: 1.2rem;">
            <strong>Welcome to Day 10 💡</strong>
        </div>
        <p style="color: #ffffff; margin-top: 1rem; text-align: center; font-size: 1.1rem;">
            Today we’re looking at fear again — but in a gentler way. Fear isn’t always bad. It shows up because it’s trying to protect you. Instead of fighting it, try to listen to it.
            What is it trying to tell you? When you understand your fear, it becomes easier to move past it and feel braver inside.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fear transformation insight
    st.markdown("""
    <div class="fear-transformation">
        <div style="color: #7c3aed; font-weight: bold; margin-bottom: 0.5rem;">
            💫 Fear Transformation Insight:
        </div>
        <p style="color: #ffffff; margin: 0; font-size: 1rem;">
            Fear often guards our deepest dreams. What you're most afraid of losing or failing at 
            might be exactly what you're meant to pursue. Today, we listen to fear's message 
            and gently question its authority over your life.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task 1: 4-Minute Fear Revisit Meditation
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🧘‍♀️ Task 1: Fear Revisit Meditation 
        </div>
        <div class="task-instruction">
            Sit in silence. Bring back one fear you named before. Now ask: "What is it protecting me from?" 
            Breathe into that question. <strong>Don't try to fix or change anything — just listen.</strong> 
            Let your fear speak. What does it want you to know? What is it trying to keep safe?
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer logic
    if not st.session_state.day10_timer_running and not st.session_state.day10_task1_completed:
        if st.button("💡 Start Task 1 (4-Minute Fear Meditation)", key="start_task1_day10"):
            st.session_state.day10_timer_running = True
            st.session_state.day10_timer_start = time.time()
            if play_ambient_music():
                st.success("🎵 Heartbeat and wind sounds started. Begin your fear meditation.")
            st.rerun()

    # Show timer if running
    if st.session_state.day10_timer_running:
        if st.session_state.day10_timer_start:
            elapsed_time = time.time() - st.session_state.day10_timer_start
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
                st.session_state.day10_timer_running = False
                st.session_state.day10_timer_start = None
                stop_ambient_music()
                st.success("⏹️ Timer stopped.")
                st.rerun()

            # Auto-refresh every second
            time.sleep(1)
            st.rerun()
        else:
            # Timer completed
            st.session_state.day10_timer_running = False
            st.session_state.day10_task1_completed = True
            stop_ambient_music()
            st.rerun()
    
    # Show completion message for Task 1
    if st.session_state.day10_task1_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 1 Completed!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="motivational-quote">
            "You've just had a conversation with your fear. In listening to its message, you've begun to transform your relationship with it from enemy to teacher." 🌟
        </div>
        """, unsafe_allow_html=True)
    
    # Task 2: Journal Prompt – Facing It Gently
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            ✍️ Task 2: Facing It Gently
        </div>
        <div class="task-instruction">
            What’s one small, simple step you could take to face that fear today? Just a tiny move forward.
            Now imagine — how would your life feel if that fear wasn’t holding you back anymore? <strong>Remember, courage doesn’t mean you’re not scared. It means you’re choosing to move forward anyway, even with the fear there.</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text area for reflection
    reflection_text = st.text_area(
        "My Gentle Approach to Fear:",
        value=st.session_state.day10_reflection_text,
        height=300,
        placeholder="The fear I revisited today:\n\nWhat I discovered this fear is protecting:\n\nThe message my fear wanted me to hear:\n\nOne small action I could take to face this fear:\n\nWhat would change in my life if this fear disappeared:\n\nHow I imagine I would feel without this fear:\n\nWhat I would pursue if I were truly fearless:\n\nMy gentle commitment to myself:\n\nWhat support I need to take this small step:",
        key="reflection_input"
    )
    
    # Update session state
    st.session_state.day10_reflection_text = reflection_text
    
    # Submit button for Task 2
    if st.button("💡 Submit My Fear Transformation Journey", key="submit_task2_day10"):
        if reflection_text.strip():
            # Save reflection
            if save_reflection(reflection_text):
                st.session_state.day10_task2_completed = True
                st.success("✅ Your fear transformation journey has been saved.")
                with st.spinner("AI is reflecting on your courage journey..."):
                    ai_feedback = get_groq_feedback(reflection_text)
                st.markdown(f"""
                         <div class="motivational-quote">
                         {ai_feedback}
                         </div>
                         """, unsafe_allow_html=True)
            else:
                st.error("❌ Error saving reflection. Please try again.")
        else:
            st.warning("⚠️ Please write your fear transformation reflection before submitting.")
    
    # Show completion status
    if st.session_state.day10_task2_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 2 Completed! You've transformed your relationship with fear.
        </div>
        """, unsafe_allow_html=True)
    
    # Courage reminder
    st.markdown("""
    <div class="courage-reminder">
        <strong>💪 Courage Reminder:</strong><br>
        “The cave you’re scared to enter might be exactly where your biggest treasure is hiding. Fear isn’t your enemy 
        — it’s just standing at the door of the growth you’re ready for.”

    </div>
    """, unsafe_allow_html=True)
    
    # Day completion check
    if st.session_state.day10_task1_completed and st.session_state.day10_task2_completed:
        st.markdown("""
        <div class="task-card" style="border-color: #00ff00;">
            <div style="text-align: center; color: #00ff00; font-size: 1.5rem;">
                🎉 Congratulations! You've completed Day 10! 🎉
            </div>
            <p style="color: #ffffff; margin-top: 1rem; text-align: center;">
                You've just accomplished something profound — you've transformed your relationship with fear. 
                Instead of running from it, you listened to its message. Instead of being paralyzed by it, 
                you've identified a small, gentle step forward. This is how courage is born: not in the absence 
                of fear, but in the presence of wisdom. The small action you've committed to is not just a step 
                toward overcoming fear — it's a step toward becoming who you're truly meant to be.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional transformation message
        st.markdown("""
        <div class="motivational-quote">
            "What if you were fearless? Today, you've begun to find out. The answer isn't that you'd have no fear — 
            it's that you'd have a different relationship with it. Welcome to your courage journey." 🦋
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
        if st.button("💡 Reset Day 10", key="reset_day10"):
            # Reset all Day 10 session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('day10_')]
            for key in keys_to_remove:
                del st.session_state[key]
            stop_ambient_music()
            st.rerun()
    
    with col3:
        if st.button("➡️ Next Day", key="next_day"):
            st.session_state.selected_day = 11
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

# If running this file directly (for testing)
if __name__ == "__main__":
    st.set_page_config(
        page_title="SoulScanner - Day 10",
        page_icon="💡",
        layout="centered"
    )
    show_day10_screen()