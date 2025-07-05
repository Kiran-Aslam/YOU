import groq
import os
import streamlit as st

def get_groq_client():
    """Initialize Groq client with API key from environment or secrets"""
    try:
        # Try to get API key from Streamlit secrets first (for Hugging Face)
        if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
            api_key = st.secrets['GROQ_API_KEY']
        else:
            # Fallback to environment variable
            api_key = os.getenv('GROQ_API_KEY')
        
        if not api_key:
            return None
            
        return groq.Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing Groq client: {e}")
        return None

def get_groq_feedback(user_text):
    """Get AI feedback from Groq API"""
    client = get_groq_client()
    
    if not client:
        return "💙 Your reflection is meaningful. Every step of self-discovery matters."
    
    prompt = (
        "The user wrote this reflection:\n"
        f"{user_text}\n\n"
        "Give a short, empathetic motivational quote or feedback (max 2 sentences) that fits their feelings or thoughts. "
        "Be positive and supportive."
    )
    
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a supportive mental wellness coach."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=80,
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Return a fallback message if API fails
        return "💙 Your reflection is meaningful. Every step of self-discovery matters."