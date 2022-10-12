import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ['Peter Parker', 'Srinu']
usernames = ['pparker', 'srinu']
passwords = ['abc123', '123456']

# hashing the passwords
hashed_passwords = stauth.Hasher(passwords).generate

file_path = Path(__file__).parent/'hashed_pw.pkl'
with file_path.open('wb') as file:
    pickle.dump(hashed_passwords, file)