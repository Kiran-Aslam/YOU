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

def init_day5_session_state():
    """Initialize session state variables for Day 5"""
    if 'day5_task1_completed' not in st.session_state:
        st.session_state.day5_task1_completed = False
    if 'day5_task2_completed' not in st.session_state:
        st.session_state.day5_task2_completed = False
    if 'day5_timer_running' not in st.session_state:
        st.session_state.day5_timer_running = False
    if 'day5_timer_start' not in st.session_state:
        st.session_state.day5_timer_start = None
    if 'day5_reflection_text' not in st.session_state:
        st.session_state.day5_reflection_text = ""

def save_reflection(reflection_text):
    """Save user reflection to a local file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save reflection with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = data_dir / f"day5_reflection_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Day 5 Reflection - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write("Task 2: My Mental Safe Space\n\n")
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
        music_path = Path("music/relax.mp3")  # Changed to relaxing ambient music for Day 5

        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            return True
        else:
            st.warning("🎵 Music file not found. Create a 'music' folder and add 'fireplace_rain.mp3' for ambient sounds.")
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

def show_day5_screen():
    """Main function to display Day 5 screen"""
    
    # Initialize session state
    init_day5_session_state()
    
    # Custom CSS for Day 5
    st.markdown("""
    <style>
        /* Day 5 specific styling */
        .day5-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .day5-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .day5-title {
            font-size: 3rem;
            font-weight: bold;
            color: #f59e0b;
            text-shadow: 0 0 20px #f59e0b;
            margin-bottom: 1rem;
        }
        
        .day5-subtitle {
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
        
        .safe-space-info {
            background: rgba(245, 158, 11, 0.2);
            border: 2px solid #f59e0b;
            border-radius: 10px;
            padding: 1.5rem;
            color: #fed7aa;
            margin: 1rem 0;
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
        
        .safe-space-elements {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .element-card {
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid #f59e0b;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            color: #fbbf24;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="day5-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="day5-header">
        <h1 class="day5-title">Day 5 🏠</h1>
        <p class="day5-subtitle">The Safe Space Within</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="task-card">
        <div style="text-align: center; color: #f59e0b; font-size: 1.2rem;">
            <strong>Welcome to Day 5 🏠</strong>
        </div>
        <p style="color: #ffffff; margin-top: 1rem; text-align: center; font-size: 1.1rem;">
            Today, let’s build a safe space in your mind—a peaceful place you can return to whenever the world feels heavy. It’s your own little escape,
             created by you, just for you. A space where you can breathe, rest, and simply be. 🕊️
        </p>
    </div>
    """, unsafe_allow_html=True)
    

    

    
    # Task 1: 5-Minute Guided Imagination
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🧘‍♀️ Task 1: Guided Imagination 
        </div>
        <div class="task-instruction">
            Close your eyes and imagine a room where you feel <strong>absolutely safe, warm, and calm</strong>. 
            This is YOUR space—no one can enter without permission. Decorate it however you like. 
            What colors surround you? What lighting creates the perfect mood? What scents fill the air? 
            What sounds bring you peace? Make it as detailed as possible.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer logic
    if not st.session_state.day5_timer_running and not st.session_state.day5_task1_completed:
        if st.button("🏠 Start Task 1 (5-Minute Safe Space Meditation)", key="start_task1_day5"):
            st.session_state.day5_timer_running = True
            st.session_state.day5_timer_start = time.time()
            if play_ambient_music():
                st.success("🎵 Fireplace and rain sounds started. Begin building your sanctuary.")
            st.rerun()

    # Show timer if running
    if st.session_state.day5_timer_running:
        if st.session_state.day5_timer_start:
            elapsed_time = time.time() - st.session_state.day5_timer_start
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
                st.session_state.day5_timer_running = False
                st.session_state.day5_timer_start = None
                stop_ambient_music()
                st.success("⏹️ Timer stopped.")
                st.rerun()

            # Auto-refresh every second
            time.sleep(1)
            st.rerun()
        else:
            # Timer completed
            st.session_state.day5_timer_running = False
            st.session_state.day5_task1_completed = True
            stop_ambient_music()
            st.rerun()
    
    # Show completion message for Task 1
    if st.session_state.day5_task1_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 1 Completed!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="motivational-quote">
            "Within you lies a sanctuary that no storm can touch, no chaos can disturb. You have built your refuge—now you can return to it anytime." 🏡
        </div>
        """, unsafe_allow_html=True)
    
    # Task 2: Journal Prompt – Describe Your Mental Safe Space
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            ✍️ Task 2: Describe Your Mental Safe Space
        </div>
        <div class="task-instruction">
            Write a detailed description of your <strong>mental safe space</strong>. What does it look like? 
            What makes it feel safe and comfortable? What would you do there when life gets overwhelming? 
            Include all the sensory details—colors, textures, sounds, scents, lighting.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text area for reflection
    reflection_text = st.text_area(
        "My Mental Safe Space:",
        value=st.session_state.day5_reflection_text,
        height=200,
        placeholder="My safe space looks like...\n\nThe colors and lighting are...\n\nThe sounds I hear are...\n\nThe scents that fill the air are...\n\nWhat makes this space feel safe is...\n\nWhen life gets overwhelming, I would...\n\nThe most comforting feature of my space is...\n\nI feel safe here because...",
        key="reflection_input"
    )
    
    # Update session state
    st.session_state.day5_reflection_text = reflection_text
    
    # Submit button for Task 2
    if st.button("🏡 Submit My Safe Space Description", key="submit_task2_day5"):
        if reflection_text.strip():
            # Save reflection
            if save_reflection(reflection_text):
                st.session_state.day5_task2_completed = True
                st.success("✅ Your safe space description has been saved.")
                with st.spinner("AI is blessing your sanctuary..."):
                    ai_feedback = get_groq_feedback(reflection_text)
                st.markdown(f"""
                         <div class="motivational-quote">
                         {ai_feedback}
                         </div>
                         """, unsafe_allow_html=True)
            else:
                st.error("❌ Error saving reflection. Please try again.")
        else:
            st.warning("⚠️ Please describe your safe space before submitting.")
    
    # Show completion status
    if st.session_state.day5_task2_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 2 Completed! Your sanctuary is now complete and ready for you.
        </div>
        """, unsafe_allow_html=True)
    
    # Day completion check
    if st.session_state.day5_task1_completed and st.session_state.day5_task2_completed:
        st.markdown("""
        <div class="task-card" style="border-color: #00ff00;">
            <div style="text-align: center; color: #00ff00; font-size: 1.5rem;">
                🎉 Congratulations! You've completed Day 5! 🎉
            </div>
            <p style="color: #ffffff; margin-top: 1rem; text-align: center;">
                You've created a mental refuge that will always be available to you. This safe space is now part of your 
                inner toolkit—whenever you feel stressed, anxious, or overwhelmed, you can close your eyes and return to 
                this sanctuary you've built. Remember every detail, and visit it often.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Instructions for using the safe space
        st.markdown("""
        <div class="safe-space-info">
            <h4 style="color: #f59e0b; margin-bottom: 1rem;">🔑 How to Use Your Safe Space</h4>
            <p style="margin-bottom: 0.5rem;">• Close your eyes and take 3 deep breaths</p>
            <p style="margin-bottom: 0.5rem;">• Visualize walking into your safe space</p>
            <p style="margin-bottom: 0.5rem;">• Engage all your senses—see, hear, smell, feel everything</p>
            <p style="margin-bottom: 0.5rem;">• Stay for 2-5 minutes or as long as needed</p>
            <p style="margin-bottom: 0;">• Use this technique whenever you need instant calm</p>
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
        if st.button("🔄 Reset Day 5", key="reset_day5"):
            # Reset all Day 5 session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('day5_')]
            for key in keys_to_remove:
                del st.session_state[key]
            stop_ambient_music()
            st.rerun()
    
    with col3:
        if st.button("➡️ Next Day", key="next_day"):
            st.session_state.selected_day = 6
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

# If running this file directly (for testing)
if __name__ == "__main__":
    st.set_page_config(
        page_title="SoulScanner - Day 5",
        page_icon="🏠",
        layout="centered"
    )
    show_day5_screen()