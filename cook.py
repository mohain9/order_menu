import pandas as pd
import glob
import os
import streamlit as st
from datetime import datetime
import time
from streamlit_autorefresh import st_autorefresh
import base64

st.set_page_config(    layout="wide",    initial_sidebar_state="collapsed",    page_title="KOT",    page_icon=":female-cook:")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 1rem;
                    padding-left: 0.5rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

#-------------to remove the burger buttong----------------------
st.markdown(""" <style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style> """, unsafe_allow_html=True)
#------------------------------------------------------
st_autorefresh(interval=1000) 

# -------------------------------Side bar

## Create a SVG image
water_mark_svg = """
<svg version="1.1"
     width="300" height="200"
     xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#ffffff" />
  <circle cx="287" cy="16" r="50" fill="#05B1FB">    
      <animate
      attributeName="r"
      values="1;0.3;1"
      dur="2s"
      repeatCount="indefinite" />
  </circle>
  <text x="284" y="16" font-size="2" text-anchor="right" fill="white" font-family="Roboto">
  
    </text>
</svg>
"""
          
            ## Encode the SVG
water_mark_bstr = (base64.b64encode(bytes(water_mark_svg,'utf-8'))).decode('utf-8')
            
#---- Insert the encoded SVG in the CSS style sheet
st.markdown(f"""
    <style>
        .stApp {{
            background-image: url(data:image/svg+xml;base64,{water_mark_bstr});
            background-position: top right; 
            background-repeat: repeat; 
            background-size: cover; 
        }}
    """, unsafe_allow_html=True
)

# Function to get the current timestamp
def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# --- Initialize session state for timers ---
# This ensures a fresh start if the app is re-executed
if 'checkbox_timers' not in st.session_state:
    st.session_state.checkbox_timers = {}


date=datetime.now().strftime("%Y%m%d")
# Define the folder where your CSV files are located
folder_path = f"{date}_orders"

# Use specific glob patterns to find only the desired files
open_files = glob.glob(os.path.join(folder_path, "open*.csv"))
close_files = glob.glob(os.path.join(folder_path, "close*.csv"))

# Create dictionaries to store the DataFrames
open_dfs = {}
close_dfs = {}

# Read files for the "open" group
for file_path in open_files:
    file_name = os.path.basename(file_path).replace('.csv', '')
    df = pd.read_csv(file_path)
    open_dfs[file_name] = df

# Read files for the "close" group
for file_path in close_files:
    file_name = os.path.basename(file_path).replace('.csv', '')
    df = pd.read_csv(file_path)
    close_dfs[file_name] = df


#--- tab creation------
tab1,tab2 = st.tabs(["**KOT**", "**REPORT**"])
        
with tab1:
# --- Streamlit App Section ---
    st.text("Warten auf neue Aufträge(order).....")

    for file_name, df in open_dfs.items():
        with st.expander(file_name):
            st.write(df)
            
            # Create a unique checkbox for each DataFrame
            is_checked = st.checkbox("Servierfertig!", key=f"checkbox_{file_name}") 

            if is_checked:
                if file_name not in st.session_state.checkbox_timers:
                    st.session_state.checkbox_timers[file_name] = time.time()
                    st.info(f"Timer started for '{file_name}'. Waiting 2 seconds...")
                
                elif time.time() - st.session_state.checkbox_timers[file_name] >= 1:
                    # Generate the new filename
                    old_file_path = os.path.join(folder_path, f"{file_name}.csv")
                    new_file_name = f"close_{get_timestamp()}_{file_name}"
                    new_file_path = os.path.join(folder_path, f"{new_file_name}.csv")
                    
                    # --- New File Renaming Logic ---
                    try:
                        os.rename(old_file_path, new_file_path)
                        st.success(f"Benachrichtigung an den Kunden gesendet. Bestellung (order) gespeichert: {new_file_name}")
                    except FileNotFoundError:
                        st.error(f"Error: File not found at {old_file_path}")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                    
                    # After the action, remove the timer and disable the checkbox
                    del st.session_state.checkbox_timers[file_name]
                    st.session_state[f"checkbox_{file_name}"] = False
                    st.rerun()
            
            elif file_name in st.session_state.checkbox_timers:
                # If unchecked, clear the timer
                del st.session_state.checkbox_timers[file_name]
                st.warning("Timer cancelled.")

with tab2:
    st.write("reports are getting ready")
    for file_name, df in close_dfs.items():
        with st.expander(file_name):
            st.write(df)