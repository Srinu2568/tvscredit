mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"mnvsrinivas1@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\

[theme]
primaryColor = '#84a3a7'
backgroundColor = '#EFEDE8'
secondaryBackgroundColor = '#fafafa'
textColor= '#424242'
font = 'sans serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
