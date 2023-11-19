#! /bin/bash
pip install -r /opt/requirements.txt

# ls -l /app
streamlit run /app/transcripcion.py --server.port=8080
