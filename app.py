from flask import Flask, render_template, request, flash
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Load the data from the Excel file
try:
    df = pd.read_excel('products.xlsx')
    print("Excel file loaded successfully.")
except Exception as e:
    print(f"Error loading Excel file: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.form.get('search_query', '').strip()
    if search_query:
        try:
            # Filter the DataFrame based on the search query
            results = df[df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().to_list(), axis=1)]
            flash(f"Search results for '{search_query}': {len(results)} found.")
        except Exception as e:
            flash(f"Error searching: {e}")
            results = pd.DataFrame()
    else:
        results = df
    
    return render_template('index.html', tables=[results.to_html(classes='data')], titles=results.columns.values, search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)
