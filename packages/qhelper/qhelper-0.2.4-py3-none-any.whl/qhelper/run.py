import subprocess
import os

def script():
    subprocess.run(['streamlit', 'run', os.path.join(os.path.dirname(__file__), 'app.py')])

if __name__ == '__main__':
    script()