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

def init_day14_session_state():
    """Initialize session state variables for Day 14"""
    if 'day14_task1_completed' not in st.session_state:
        st.session_state.day14_task1_completed = False
    if 'day14_task2_completed' not in st.session_state:
        st.session_state.day14_task2_completed = False
    if 'day14_timer_running' not in st.session_state:
        st.session_state.day14_timer_running = False
    if 'day14_timer_start' not in st.session_state:
        st.session_state.day14_timer_start = None
    if 'day14_reflection_text' not in st.session_state:
        st.session_state.day14_reflection_text = ""
    if 'day14_final_reflection' not in st.session_state:
        st.session_state.day14_final_reflection = ""

def save_reflection(reflection_text, final_reflection):
    """Save user reflection to a local file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save reflection with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = data_dir / f"day14_reflection_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Day 14 Reflection - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write("Task 2: What Have I Learned About Myself?\n\n")
            f.write(reflection_text)
            f.write("\n\n" + "="*50 + "\n\n")
            f.write("Final Reflection: From this journey, I carry forward...\n\n")
            f.write(final_reflection)
        
        return True
    except Exception as e:
        st.error(f"Error saving reflection: {str(e)}")
        return False

def play_ambient_music():
    """Play soft ambient glow + heartbeat + wind for Day 14"""
    if not AUDIO_AVAILABLE:
        return False
    
    try:
        pygame.mixer.init()
        music_path = Path("music/relax.mp3")  # Changed to integration sounds for Day 14
        
        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            return True
        else:
            st.warning("🎵 Music file not found. Create a 'music' folder and add 'ambient_glow_heartbeat_wind.mp3' for ambient sounds.")
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

def show_day14_screen():
    """Main function to display Day 14 screen"""
    
    # Initialize session state
    init_day14_session_state()
    
    # Custom CSS for Day 14
    st.markdown("""
    <style>
        /* Day 14 specific styling */
        .day14-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .day14-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .day14-title {
            font-size: 3rem;
            font-weight: bold;
            color: #8b5cf6;
            text-shadow: 0 0 20px #8b5cf6;
            margin-bottom: 1rem;
        }
        
        .day14-subtitle {
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
        
        .final-completion {
            background: linear-gradient(135deg, #8b5cf6, #a78bfa, #8b5cf6);
            border: 3px solid #8b5cf6;
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            text-align: center;
            color: white;
            font-size: 1.3rem;
            font-weight: bold;
            box-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
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
        
        .integration-glow {
            animation: integrationGlow 3s ease-in-out infinite alternate;
        }
        
        @keyframes integrationGlow {
            from { text-shadow: 0 0 20px #8b5cf6; }
            to { text-shadow: 0 0 30px #a78bfa, 0 0 40px #8b5cf6; }
        }
        
        .journey-summary {
            background: rgba(139, 92, 246, 0.1);
            border: 2px solid #8b5cf6;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 2rem 0;
            color: #ffffff;
            font-size: 1.1rem;
            line-height: 1.6;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="day14-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="day14-header">
        <h1 class="day14-title integration-glow">Day 14 💡</h1>
        <p class="day14-subtitle">Becoming Whole Again</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="task-card">
        <div style="text-align: center; color: #8b5cf6; font-size: 1.2rem;">
            <strong>Welcome to Day 14💡</strong>
        </div>
        <p style="color: #ffffff; margin-top: 1rem; text-align: center; font-size: 1.1rem;">
            Today is about bringing it all together — every insight, every feeling from the past 13 days.
             It’s a gentle reminder that you don’t have to be perfect to be whole. Your joy, fear, strength, messiness, and softness all belong. Today, you simply accept all of you, with love.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Journey Summary
    st.markdown("""
    <div class="journey-summary">
        <h3 style="color: #8b5cf6; text-align: center; margin-bottom: 1rem;">🌟 Your 14-Day Journey</h3>
        <p>You’ve explored every part of yourself — your thoughts, fears, dreams, and strengths. Each day peeled back another layer, revealing more of who you truly are.
         Today is about owning it all. Every piece, every experience, every part of you belongs. This is your full, powerful self — not perfect, but real and complete.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task 1: Whole Self Meditation
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🧘‍♀️ Task 1: Whole Self Meditation
        </div>
        <div class="task-instruction">
            Close your eyes. Imagine yourself walking through each day of this journey. You meet all your past selves — 
            the one who's afraid, the one who smiles, the one who hides, and the one who dreams. Stand in front of them 
            and say: <strong>"You are all me — and I accept you."</strong> Feel a gentle light wrap around you, 
            holding all your pieces together in peace.
        </div>
    </div>S
    """, unsafe_allow_html=True)
    
    # Timer logic
    if not st.session_state.day14_timer_running and not st.session_state.day14_task1_completed:
        if st.button("💡 Start Task 1 (6-Minute Whole Self Meditation)", key="start_task1_day14"):
            st.session_state.day14_timer_running = True
            st.session_state.day14_timer_start = time.time()
            if play_ambient_music():
                st.success("🎵 Soft ambient glow with heartbeat and wind started. Let integration begin.")
            st.rerun()

    # Show timer if running
    if st.session_state.day14_timer_running:
        if st.session_state.day14_timer_start:
            elapsed_time = time.time() - st.session_state.day14_timer_start
            remaining_time = max(0, 360 - elapsed_time)  # 6 minutes = 360 seconds
        if remaining_time > 0:
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            st.markdown(f"""
            <div class="timer-display integration-glow">
                {minutes:02d}:{seconds:02d}
            </div>
            """, unsafe_allow_html=True)

            # Progress bar
            progress = (360 - remaining_time) / 360
            st.progress(progress)

            # Stop Timer Button
            if st.button("⏹️ Stop Timer", key="stop_task1"):
                st.session_state.day14_timer_running = False
                st.session_state.day14_timer_start = None
                stop_ambient_music()
                st.success("⏹️ Timer stopped.")
                st.rerun()

            # Auto-refresh every second
            time.sleep(1)
            st.rerun()
        else:
            # Timer completed
            st.session_state.day14_timer_running = False
            st.session_state.day14_task1_completed = True
            stop_ambient_music()
            st.rerun()
    
    # Show completion message for Task 1
    if st.session_state.day14_task1_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 1 Completed!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="motivational-quote">
            "The curious paradox is that when I accept myself just as I am, then I can change." - Carl Rogers 💫
        </div>
        """, unsafe_allow_html=True)
    
    # Task 2: Journal Prompt – What Have I Learned About Myself?
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            ✍️ Task 2: What Have I Learned About Myself?
        </div>
        <div class="task-instruction">
            Look back. What surprised you most during this journey? What is one belief about yourself that changed? 
            What part of you did you reconnect with? Take time to honor the insights you've gained and the 
            growth you've experienced.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text area for reflection
    reflection_text = st.text_area(
        "What Have I Learned About Myself:",
        value=st.session_state.day14_reflection_text,
        height=200,
        placeholder="What surprised me most during this journey:\n\nOne belief about myself that changed:\n\nA part of me I reconnected with:\n\nThe biggest insight I gained:\n\nHow I see myself differently now:\n\nWhat I'm most grateful for from this journey:\n\nA strength I discovered in myself:",
        key="reflection_input"
    )
    
    # Update session state
    st.session_state.day14_reflection_text = reflection_text
    
    # Final Reflection Bonus
    st.markdown("""
    <div class="task-card">
        <div class="task-header">
            🌱 Final Reflection Bonus
        </div>
        <div class="task-instruction">
            Complete this sentence: <strong>"From this journey, I carry forward..."</strong><br>
            Write whatever flows from your heart. This is your commitment to yourself and your growth.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Final reflection text area
    final_reflection = st.text_area(
        "From this journey, I carry forward...",
        value=st.session_state.day14_final_reflection,
        height=150,
        placeholder="From this journey, I carry forward...\n\n(Write whatever flows from your heart - your intentions, commitments, hopes, or newfound wisdom)",
        key="final_reflection_input"
    )
    
    # Update session state
    st.session_state.day14_final_reflection = final_reflection
    
    # Submit button for Task 2
    if st.button("💡 Submit My Integration Reflection", key="submit_task2_day14"):
        if reflection_text.strip() and final_reflection.strip():
            # Save reflection
            if save_reflection(reflection_text, final_reflection):
                st.session_state.day14_task2_completed = True
                st.success("✅ Your integration reflection has been saved.")
                with st.spinner("AI is celebrating your journey..."):
                    combined_reflection = f"Journey Learning: {reflection_text}\n\nCarrying Forward: {final_reflection}"
                    ai_feedback = get_groq_feedback(combined_reflection)
                st.markdown(f"""
                         <div class="motivational-quote">
                         {ai_feedback}
                         </div>
                         """, unsafe_allow_html=True)
            else:
                st.error("❌ Error saving reflection. Please try again.")
        else:
            st.warning("⚠️ Please complete both reflections before submitting.")
    
    # Show completion status
    if st.session_state.day14_task2_completed:
        st.markdown("""
        <div class="completion-message">
            ✅ Task 2 Completed! You've integrated your journey beautifully.
        </div>
        """, unsafe_allow_html=True)
    
    # Day completion check
    if st.session_state.day14_task1_completed and st.session_state.day14_task2_completed:
        st.markdown("""
        <div class="final-completion">
            <h2>🎉 CONGRATULATIONS! 🎉</h2>
            <h3>You've completed your 14-Day SoulScanner Journey!</h3>
            <p style="margin-top: 1.5rem; font-size: 1.1rem;">
                You've traveled through the depths of yourself with courage and curiosity. You've met your fears, 
                embraced your strengths, uncovered your dreams, and integrated all parts of yourself with love. 
                This isn't the end — it's the beginning of living as your whole, authentic self.
            </p>
            <p style="margin-top: 1rem; font-size: 1rem;">
                <strong>You are whole. You are enough. You are ready.</strong>
            </p>
            <p style="margin-top: 1rem; font-size: 0.9rem; font-style: italic;">
                The journey continues in how you choose to live each day. Carry this wisdom forward. 💫
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Final wisdom message
        st.markdown("""
        <div class="journey-summary">
            <h4 style="color: #8b5cf6; text-align: center;">🌟 Your Journey's Wisdom</h4>
            <p style="text-align: center; font-style: italic;">
                "The privilege of a lifetime is being who you are." - Joseph Campbell
            </p>
            <p style="text-align: center; margin-top: 1rem;">
                You've claimed this privilege. You've become who you are, fully and beautifully. 
                Take this wholeness into the world — it's your gift to yourself and others.
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
        if st.button("💡 Reset Day 14", key="reset_day14"):
            # Reset all Day 14 session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('day14_')]
            for key in keys_to_remove:
                del st.session_state[key]
            stop_ambient_music()
            st.rerun()
    
    with col3:
        if st.button("🔄 Restart Journey", key="restart_journey"):
            st.session_state.selected_day = 1
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

# If running this file directly (for testing)
if __name__ == "__main__":
    st.set_page_config(
        page_title="SoulScanner - Day 14",
        page_icon="💡",
        layout="centered"
    )
    show_day14_screen()