mkdir -p ~/.streamlit/
wget https://media.githubusercontent.com/media/shahrukhx01/retrieval-annotator/main/generated_queries_anusha.csv -O generated_queries_anusha1.csv
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml