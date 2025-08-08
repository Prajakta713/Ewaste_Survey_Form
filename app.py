from flask import Flask, render_template, request

app = Flask(__name__)

# Revised device weights (more realistic averages in kg)
device_weights = {
    "smartphone": 0.15,  # Reduced from 0.2 (modern phones are lighter)
    "laptop": 1.8,       # Reduced from 2.0
    "tv": 10.0,          # Reduced from 15.0 (average LED TV)
    "charger": 0.05
}

# Device lifetimes (years)
device_lifetimes = {
    "smartphone": 3,
    "laptop": 5,
    "tv": 8,
    "charger": 2
}

# India's e-waste data (Global E-Waste Monitor 2023)
average_indian_waste = 2.5  # kg/year (benchmark)
india_total_ewaste = 3.2e6 * 1000  # 3.2 million tonnes → kg
population = 1.4e9  # 1.4 billion

@app.route("/")
def index():
    return render_template("creative_survey.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    # Get user inputs
    phones_drawer = int(request.form.get("phones_drawer", 0))
    laptops_5yrs = int(request.form.get("laptops_5yrs", 0))
    tvs_use = int(request.form.get("tvs_use", 0))
    chargers = int(request.form.get("chargers", 0))
    upgrade_freq = request.form.get("upgrade_freq", "three_plus")
    old_device_action = request.form.get("old_device_action", "keep")

    # --- CALCULATION LOGIC ---
    # 1. UNUSED DEVICES (immediate waste)
    unused_waste = (
        phones_drawer * device_weights["smartphone"] +  # Old phones in drawer
        chargers * device_weights["charger"]             # Unused chargers
    )

    # 2. DEVICES IN USE (annual share based on lifetime)
    active_waste = (
        (laptops_5yrs * device_weights["laptop"] / device_lifetimes["laptop"]) +
        (tvs_use * device_weights["tv"] / device_lifetimes["tv"])
    )

    # 3. UPGRADE FREQUENCY (additional phone waste)
    upgrade_waste = 0
    if upgrade_freq == "yearly":
        upgrade_waste = device_weights["smartphone"]
    elif upgrade_freq == "two_years":
        upgrade_waste = device_weights["smartphone"] / 2

    # 4. RECYCLING ADJUSTMENT
    recycling_factor = 1.0  # Default: no reduction
    if old_device_action == "sell":
        recycling_factor = 0.7  # 30% reduction
    elif old_device_action == "give":
        recycling_factor = 0.5  # 50% reduction
    elif old_device_action == "recycle":
        recycling_factor = 0.9  # 10% reduction

    # TOTAL ANNUAL WASTE
    total_ewaste_kg = (unused_waste + active_waste + upgrade_waste) * recycling_factor

    # India per capita (official data)
    india_per_capita = india_total_ewaste / population

    # User's contribution (% of India's per capita)
    contribution_percent = (total_ewaste_kg / india_per_capita) * 100

    return render_template(
        "result.html",
        personal=round(total_ewaste_kg, 2),
        india_per_capita=round(india_per_capita, 2),
        average_indian=average_indian_waste,
        contribution_percent=round(contribution_percent, 2)
    )

if __name__ == "__main__":
    app.run(debug=True)