from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define the pricing table
pricing_table = [
    {"tier": "S20", "ram_gb": 4, "price_per_hr": 0.11},
    {"tier": "S30", "ram_gb": 8, "price_per_hr": 0.11},
    {"tier": "S40", "ram_gb": 16, "price_per_hr": 0.21},
    {"tier": "S50", "ram_gb": 32, "price_per_hr": 0.42},
    {"tier": "S60", "ram_gb": 64, "price_per_hr": 0.87},
    {"tier": "S80", "ram_gb": 128, "price_per_hr": 1.66},
    {"tier": "S90", "ram_gb": 256, "price_per_hr": 3.08},
    {"tier": "S100", "ram_gb": 384, "price_per_hr": 4.34},
    {"tier": "S110", "ram_gb": 512, "price_per_hr": 5.79},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        vector_dimensionality = int(request.form['vector_dimensionality'])
        num_embeddings = int(request.form['num_embeddings'])
        product = vector_dimensionality * num_embeddings
        
        # Calculate space required
        space_per_vector_kb = 3 / 768  # KB per dimension
        total_space_kb = product * space_per_vector_kb
        total_space_gb = total_space_kb / (1024 * 1024)

        # Calculate required RAM (90% of available memory)
        required_ram_gb = total_space_gb / 0.9

        # Find the appropriate cluster tier
        recommended_tier = None
        for tier in pricing_table:
            if tier["ram_gb"] >= required_ram_gb:
                recommended_tier = tier
                break

        return render_template('result.html', required_ram_gb=required_ram_gb, recommended_tier=recommended_tier)

if __name__ == '__main__':
    app.run(debug=True)