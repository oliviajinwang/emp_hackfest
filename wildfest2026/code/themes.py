import streamlit as st

# custom theming function to apply user-selected color themes across the app
def set_theme():
    st.sidebar.title("Themes")
    
    themes = {
        "Ocean Blue": {"bg": "#001D3D", "text": "#E0E1DD", "sidebar": "#003566", "accent": "#FFC300"},
        "Light": {"bg": "#FFFFFF", "text": "#31333F", "sidebar": "#F0F2F6", "accent": "#FF4B4B"},
        "Dark": {"bg": "#121212", "text": "#E0E0E0", "sidebar": "#1E1E1E", "accent": "#BB86FC"},
        "Forest Green": {"bg": "#0D1F0D", "text": "#E8F5E9", "sidebar": "#162B16", "accent": "#4CAF50"},
        "Crimson Red": {"bg": "#2D0303", "text": "#F5E8E8", "sidebar": "#4A0606", "accent": "#FF4D4D"},
        "Solarized Yellow": {"bg": "#FDF6E3", "text": "#657B83", "sidebar": "#EEE8D5", "accent": "#B58900"}
    }

    # user selects a theme from the sidebar dropdown
    theme_choice = st.sidebar.selectbox(
        "Choose a color theme", 
        ["Ocean Blue", "Light", "Dark", "Forest Green", "Crimson Red", "Solarized Yellow"]
    )

    # apply the selected theme's colors to the app using custom CSS
    selected = themes[theme_choice]
    custom_css = f"""
        <style>
            /* Kill the white line at the top */
            header[data-testid="stHeader"] {{
                background: rgba(0,0,0,0);
                background-color: rgba(0,0,0,0);
                height: 0px;
            }}
            
            /* Remove the decoration bar specifically */
            div[data-testid="stDecoration"] {{
                display: none;
                width: 0;
                secondary-background-color: transparent;
            }}

            /* Main Background */
            .stApp {{
                background-color: {selected['bg']};
                color: {selected['text']};
            }}

            /* Sidebar Background */
            [data-testid="stSidebar"] {{
                background-color: {selected['sidebar']};
            }}

            /* Text color enforcement */
            h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {{
                color: {selected['text']} !important;
            }}

            /* Metric widget adjustments */
            [data-testid="stMetricValue"] {{
                color: {selected['accent']} !important;
            }}

            /* Button Styling to match theme */
            .stButton>button {{
                border-color: {selected['accent']};
                color: {selected['accent']};
                background-color: transparent;
            }}
            .stButton>button:hover {{
                background-color: {selected['accent']};
                color: {selected['bg']};
            }}
        </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)
