mkdir -p ~/.streamlit/
wget https://docs.google.com/spreadsheets/d/1kGPY2inrIc05Ik7162TkmuHRrWOlSDy8aFjKkUw0M8w/export?format=csv -O generated_queries_praveena1.csv
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml