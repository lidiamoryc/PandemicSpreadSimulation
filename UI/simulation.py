import streamlit as st
import json
import base64
import subprocess
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(base_dir, '..', 'vis.gif')



def simulation():
    """Wyświetla plik .gif utworzony po uruchomieniu symulacji."""

    # st.title("Symulacja:")

    ## run the simulation - instead of python, type the dir to the python.exe in the venv
    # subprocess.run(["python", os.path.join(base_dir, '..', 'main.py')])

    file_ = open(FILE_PATH, "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,
    )

    st.title("Wykresy:")

    image_paths = [
        os.path.join(base_dir, '..', 'plot', 'distributions_plot.png'),
        os.path.join(base_dir, '..', 'plot', 'rates_plot.png'),
        os.path.join(base_dir, '..', 'plot', 'state_history_plot.png')
    ]

    for image_path in image_paths:
        if os.path.exists(image_path):
            st.image(image_path, caption=os.path.basename(image_path), use_container_width=True)
        else:
            st.error(f"Nie znaleziono pliku: {image_path}")
