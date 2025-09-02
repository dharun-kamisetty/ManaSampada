import streamlit as st
from utils.ai_helper import get_groq_client
from utils.ai_helper import get_ai_chat_response


def render_ai_chat_tab():
    """Render clean AI chat interface for cultural heritage questions"""
    st.markdown('<h2 class="sub-header">Cultural Heritage AI Assistant</h2>', unsafe_allow_html=True)
    
    st.info("💡 Ask me anything about Indian cultural heritage, historical sites, or preservation techniques!")
    
    # Initialize chat history
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = [
            {"role": "assistant", "content": "Namaste! I'm here to help you learn about India's rich cultural heritage. What would you like to know?"}
        ]
    
    # Display chat messages
    for message in st.session_state.ai_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about Indian cultural heritage..."):
        # Add user message to chat history
        st.session_state.ai_messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = get_ai_chat_response(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.ai_messages.append({"role": "assistant", "content": response})
        
        # Limit chat history to last 10 messages
        if len(st.session_state.ai_messages) > 10:
            st.session_state.ai_messages = st.session_state.ai_messages[-10:]
            
def get_ai_response(prompt: str) -> str:
    """Get AI response for cultural heritage questions"""
    try:
        client = get_groq_client()
        if not client:
            return "I'm currently unavailable. Please try again later."
        
        system_prompt = """
        You are a knowledgeable AI assistant specializing in Indian cultural heritage, 
        history, archaeology, and preservation techniques. You provide accurate, 
        respectful, and insightful information about:
        
        - Indian temples, mosques, churches, and religious sites
        - Cultural traditions and practices across India
        - Historical context and significance
        - Preservation methods and best practices
        - Regional variations in cultural heritage
        
        Always be respectful of all cultures and religions. Provide factual information
        and cite historical context when appropriate.
        """
        
        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"I encountered an error: {str(e)}. Please try again."