import streamlit as st

def render_categories_tab():
    """Render the categories browsing tab"""
    st.markdown('<h2 class="sub-header">Available Categories</h2>', unsafe_allow_html=True)
    st.markdown('<p>Choose from these categories when documenting cultural heritage sites:</p>', unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        st.warning("Please login to view categories")
        return
    
    # Ensure categories are loaded
    if 'categories' not in st.session_state or not st.session_state.categories:
        from utils.helpers import load_categories
        success = load_categories()
        if not success:
            st.error("Failed to load categories. Please try again.")
            return
    
    if st.session_state.categories:
        display_categories(st.session_state.categories)
    else:
        st.info("No categories available. Please try again later.")

def display_categories(categories_data):
    """Display categories in a nice formatted way"""
    if not categories_data:
        st.warning("No categories available")
        return
    
    st.success(f"Found {len(categories_data)} categories available for use!")
    
    # Display categories in a grid
    cols = st.columns(2)
    
    for idx, category in enumerate(categories_data):
        with cols[idx % 2]:
            render_category_card(category)

def render_category_card(category):
    """Render a single category as a card"""
    st.markdown(f"""
    <div class="category-card">
        <h3>{category.get('title', category.get('name', 'Unnamed Category'))}</h3>
        <p class="category-description">{category.get('description', 'No description available')}</p>
        <div class="category-meta">
            <span class="category-id">ID: {category.get('id', 'N/A')}</span>
            <span class="category-rank">Rank: {category.get('rank', 'N/A')}</span>
            <span class="category-status">{'Published' if category.get('published') else 'Draft'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)