import streamlit as st

def show_why_i_made_you_screen():
    """Show the beautiful title, floating emojis, navigation buttons, and a gradient message."""

    st.markdown("""
    <style>
        .heart-float {
            position: absolute;
            color: #06b6d4;
            font-size: 1.5rem;
            animation: float 6s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        .heart-1 { top: 10%; left: 10%; animation-delay: 0s; }
        .heart-2 { top: 20%; right: 15%; animation-delay: 2s; }
        .heart-3 { bottom: 30%; left: 20%; animation-delay: 4s; }
        .heart-4 { bottom: 20%; right: 10%; animation-delay: 1s; }

        .why-title {
            text-align: center;
            font-size: 3.2rem;
            font-weight: bold;
            margin-top: 2.5rem;
            margin-bottom: 1.2rem;
            background: linear-gradient(90deg, #06b6d4 10%, #8b5cf6 60%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 2px;
            text-shadow: 0 2px 12px rgba(139,92,246,0.15);
        }
        .why-desc {
            text-align: left; /* <-- changed from center to left */
            font-size: 1.15rem;
            font-weight: 500;
            margin: 0 auto 2.5rem auto;
            max-width: 600px;
            background: linear-gradient(90deg, #06b6d4 10%, #8b5cf6 60%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 1px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Beautiful Title
    st.markdown('<div class="why-title">WHY I MADE YOU</div>', unsafe_allow_html=True)

    # Gradient Description (now left aligned)
    st.markdown("""
    <div class="why-desc" style="line-height: 1.8; font-size: 1.05rem; color: #e0e0e0;">
        In a world constantly shouting, comparing, rushing...<br>
        we rarely stop and whisper to ourselves:<br>
        <strong>"Who am I, really?"</strong><br><br>While reading <em>The Art of Being Alone</em>, something clicked.<br>
        <strong>I highly recommend you read it.</strong><br>The way the author wrote — so raw, so real — it felt like someone finally understood the parts of me I didn’t even know needed understanding.<br><br>There was one line I couldn’t shake:<br>
        <em>“The scariest thing is to look in the mirror and not recognize the person staring right at you.”</em><br><br>That hit hard — because it was true.<br>We spend so much time trying to be accepted by others,<br>changing ourselves to fit their standards,<br>watering down our truth so we’re easier to love.<br><br>And in doing that, we forget what we truly love about ourselves.<br>What makes us smile.<br>What we deeply believe in.<br>What hurts us.<br>What heals us.<br><br>I realized…<br>I had become a collection of tabs — 
        one open for each person in my life:<br>A different me for my friends.<br>A different me for my professors.<br>A different me for the world.<br>And somewhere along the way…<br>
        <strong>I crashed.</strong><br><br>So no — I didn’t create <strong>YOU</strong> to impress anyone.<br>I created it as a quiet space.<br>A mirror.<br>A place where you can meet yourself — without filters.<br>Where you're not trying to "be better", just trying to <em>be</em>.<br><br>Because here’s the truth:<br>
        <strong>You don’t need fixing.<br>You need listening.</strong><br><br>
        <strong>YOU</strong> is here for that.<br>To help you slow down.<br>To help you explore your shadows and your light.<br>To help you reconnect with the beautiful, messy, forgotten parts of you.<br><br>Not to become someone new —<br>but to finally <em>remember</em> the real YOU that was always there.<br><br>With all my heart,<br>
        <strong>Kiran Aslam</strong>
    </div>
""", unsafe_allow_html=True)


    # Floating emojis
    st.markdown("""
    <div class="heart-float heart-1">💙</div>
    <div class="heart-float heart-2">✨</div>
    <div class="heart-float heart-3">🌟</div>
    <div class="heart-float heart-4">💜</div>
    """, unsafe_allow_html=True)

    # Navigation buttons at the bottom
    st.markdown('<div style="position: relative; z-index: 1; margin-top: 6rem;">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("🏠 Go to Home", key="blog_home"):
            st.session_state.selected_day = None
            st.rerun()

    with col2:
        if st.button("🔄 Restart Journey", key="blog_restart"):
            st.session_state.selected_day = 1
            st.rerun()

    with col3:
        if st.button("← Back", key="blog_back"):
            st.session_state.selected_day = 14
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)