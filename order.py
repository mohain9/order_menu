
import streamlit as st
import pandas as pd
from pathlib import Path
import os
import time
from datetime import datetime

# --- Session State Initialization ---
if 'selections' not in st.session_state:
    st.session_state.selections = {}

if 'last_interaction_time' not in st.session_state:
    st.session_state.last_interaction_time = {}

if 'last_selected_item' not in st.session_state:
    st.session_state.last_selected_item = None

if 'show_spinner' not in st.session_state:
    st.session_state['show_spinner'] = False
if 'file_found' not in st.session_state:
    st.session_state['file_found'] = False
    
if 'timestamp' not in st.session_state:
    st.session_state['timestamp'] = None

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False  


# Get the user's home directory
home_dir = str(Path.home())
dateonly = datetime.now().strftime("%Y%m%d")

# Create the folder path in the user's home directory
folder_path = os.path.join(home_dir, f"{dateonly}_orders")

folder_path = f"{dateonly}_orders"

# Create folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

current_dir = Path(__file__).parent
image_paths = {
    "Hänchen Soup": current_dir / "assets" / "image" / "soup1.jpg",
    "Gemuse Soup": current_dir / "assets" / "image" / "soup2.jpg",
    "Nudeln Soup": current_dir / "assets" / "image" / "soup3.jpg",
    "Pasta": current_dir / "assets" / "image" / "pasta.jpg",
    "Reis": current_dir / "assets" / "image" / "rice.jpg",
    "Pizza": current_dir / "assets" / "image" / "pizza.jpg",
}

# --- Data Definitions (using item_details as the single source) ---
item_details = {
    "Hänchen Soup": {
        "price": 2,
        "description": "A delicious chicken soup, very hot.",
        "cooking_time": "5 min"
    },
    "Gemuse Soup": {
        "price": 3,
        "description": "This is a vegan vegetable soup.",
        "cooking_time": "2 min"
    },
    "Nudeln Soup": {
        "price": 2,
        "description": "A sweet noodle soup, very tasty.",
        "cooking_time": "6 min"
    }
}
item_names = list(item_details.keys()) # Get item names from the dictionary

main_item_details = {
    "Pasta": {
        "price": 12,
        "description": "Pasta mit tomaten, very hot.",
        "cooking_time": "15 min"
    },
    "Reis": {
        "price": 13,
        "description": "Reise mit gemuse.",
        "cooking_time": "20 min"
    },
    "Pizza": {
        "price": 10,
        "description": "Pizza und hänchen",
        "cooking_time": "10 min"
    }
}
main_item_names = list(main_item_details.keys()) # Get item names from the dictionary



# --- Callback Function to track interactions ---
def update_interaction_time(item_name):
    st.session_state.last_interaction_time[item_name] = datetime.now()

# --- Page Configuration ---
st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="mein_restaurant", page_icon=":pizza:")

# --- UI Layout ---
expandc1, expandc2 = st.columns(2)

with expandc1.expander("Soup", expanded=True):
    c1, c2 = st.columns((2, 2))
    
    for item in item_names:
        details = item_details.get(item)
        price = details["price"] if details else "N/A"
        
        is_checked = c1.checkbox(
            item,
            key=f"checkbox_{item}",
            on_change=update_interaction_time,
            label_visibility="visible",
            args=(item,),width="content"
        )
        #c2.caption(f"{price}€")
        
        if is_checked:
            quantity = c1.number_input(
                'Hinzufügen:',
                min_value=1,
                max_value=10,
                value=1,
                label_visibility="collapsed",#"visible",#"hidden",
                key=f"count_{item}"
            )
            st.session_state.selections[item] = {
                "count": quantity,
                "price": price,
                "total": quantity * price
            }
        elif item in st.session_state.selections:
            del st.session_state.selections[item]

with expandc2.expander("Main Course", expanded=True):
    c1, c2 = st.columns((2, 2))
    for item in main_item_names:
        details = main_item_details.get(item)
        price = details["price"] if details else "N/A"
        
        is_checked = c1.checkbox(
            item,
            key=f"checkbox_{item}",
            on_change=update_interaction_time,
            label_visibility="visible",
            args=(item,),width="content"
        )
        #c2.caption(f"{price}€")
        
        if is_checked:
            quantity = c1.number_input(
                'Hinzufügen:',
                min_value=1,
                max_value=10,
                value=1,
                label_visibility="collapsed",#"hidden",
                key=f"count_{item}"
            )
            st.session_state.selections[item] = {
                "count": quantity,
                "price": price,
                "total": quantity * price
            }
        elif item in st.session_state.selections:
            del st.session_state.selections[item]


all_item_details = item_details | main_item_details
all_item_names = list(all_item_details.keys())
# --- Logic to find the last selected item ---
checked_items = [item for item in all_item_names if st.session_state.get(f"checkbox_{item}")]

#checked_items = [item for item in item_names if st.session_state.get(f"checkbox_{item}")]
last_selected_item_name = None

if checked_items:
    last_selected_item_name = max(checked_items, key=lambda i: st.session_state.last_interaction_time.get(i, datetime.min))
st.session_state.last_selected_item = last_selected_item_name

# --- Sidebar Content ---
with st.sidebar:
    if st.session_state.last_selected_item:
        item = st.session_state.last_selected_item
        #details = item_details.get(item)
        details = all_item_details.get(item) # Look up details in the combined dictionary
        
        if item in image_paths:
            st.image(str(image_paths[item]))
        else:
            st.info("No picture.")
            
        if details:
            st.markdown(f"**Preis:** {details['price']}€")
            st.markdown(f"**Kochzeit:** {details['cooking_time']}")
            st.markdown(f"**Beschreibung:** {details['description']}")
        else:
            st.info("No description of the item.")

# --- Display Final Order (optional) ---
if st.session_state.selections:
    total_bill = sum(item['total'] for item in st.session_state.selections.values())
    st.write(f"Gesamt: {total_bill}€")
    # You can also display a dataframe of the order if you wish.
        
    data = [{"item": item, "count": details["count"], "price": details["price"]} for item, details in st.session_state.selections.items()]
    df = pd.DataFrame(data)
    df["total"] = df["count"] * df["price"]
    st.caption('Bitte überprüfen Sie unten Ihre Bestellung und klicken Sie auf "Jetzt bestellen"')
    st.dataframe(df)

    agree = st.checkbox(f"Ich bin einverstanden, zu bestellen und insgesamt zu bezahlen {total_bill}€.", disabled=st.session_state.button_clicked,key="agree_checkbox" )

# If the user clicks the button, generate and save the timestamp

    if agree and not st.session_state.button_clicked:
        ordernow_button = st.button("Jetzt bestellen!")
        if ordernow_button:
            # Generate timestamp and filenames and save them to session state
            st.session_state['timestamp'] = datetime.now().strftime("%Y%m%d%H%M%S")
            st.session_state['filename_open'] = f"open_{st.session_state['timestamp']}.csv"
            st.session_state['filename_close'] = f"close_{st.session_state['timestamp']}.csv"
            
            # Disable or hide the button by setting the flag
            st.session_state.button_clicked = True
           

            # Build the full path using the filename stored in session state
            filename = st.session_state['filename_open']
            full_path = os.path.join(folder_path, filename)

            # Save the DataFrame
            df.to_csv(full_path, index=False)
            #df.to_csv(st.session_state['filename_open'], index=False)    

            # 2. Update session state to show the spinner and rerun
            st.session_state['show_spinner'] = True
            st.session_state['file_found'] = False            
            st.rerun()

    if st.session_state['show_spinner']:
        #st.write("Coming soon...")
        # Use a spinner to show that the app is waiting
        with st.spinner('Überprufung...'):
            if 'timestamp' in st.session_state and st.session_state['timestamp']:
                # The timestamp from the original 'open' file
                timestamp_to_find = st.session_state['timestamp']
                
                # Check all files in the directory for a match
                for filename in os.listdir(folder_path):
                    # The condition to find the correct file
                    if filename.startswith("close_") and timestamp_to_find in filename:
                        st.session_state['file_found'] = True
                        # Store the actual filename that was found
                        st.session_state['filename_close'] = filename
                        break  # Stop searching once the file is found

                if not st.session_state['file_found']:
                    st.spinner('Überprufung...')
                    st.info("Kochen...")
                    time.sleep(5) # Wait if the file isn't found yet

        if st.session_state['file_found']:
            st.success("Ihre Bestellung ist zur Abholung bereit. Kommen Sie vorbei.")
            # Use the full path with the dynamically found filename
            full_path_close = os.path.join(folder_path, st.session_state['filename_close'])
            df = pd.read_csv(full_path_close)
            
        else:
            # If the file isn't found yet, rerun to keep the spinner active
            st.rerun()

else:
    st.write("No items selected.")