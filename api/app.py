from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# ✅ Correct path
df = pd.read_csv("data/processed/cleaned_data.csv")

@app.route("/")
def home():
    return "API is running 🚀"

@app.route("/top-customers")
def top_customers():
    result = df.groupby('CustomerID')['Revenue'].sum().nlargest(5)
    return jsonify(result.to_dict())

@app.route("/top-countries")
def top_countries():
    result = df.groupby('Country')['Revenue'].sum().nlargest(5)
    return jsonify(result.to_dict())

@app.route("/dashboard")
def dashboard():
    return """
    <h1>Revenue Dashboard</h1>
    <p>Go to:</p>
    <ul>
        <li><a href='/top-customers'>Top Customers</a></li>
        <li><a href='/top-countries'>Top Countries</a></li>
    </ul>
    """

if __name__ == "__main__":
    app.run(debug=True)
    