from flask import Flask, jsonify, request

app = Flask(__name__)

# Core Business Logic extracted from baseline Aceestver scripts
PROGRAMS = {
    "Fat Loss (FL)": {
        "workout": "Mon: Back Squat 5x5 | Tue: EMOM 20min Assault Bike | Wed: Bench Press | Thu: Deadlift | Fri: Zone 2 Cardio",
        "diet": "Breakfast: Egg Whites + Oats | Lunch: Grilled Chicken + Brown Rice | Dinner: Fish Curry + Millet Roti",
        "calorie_factor": 22
    },
    "Muscle Gain (MG)": {
        "workout": "Mon: Squat 5x5 | Tue: Bench 5x5 | Wed: Deadlift 4x6 | Thu: Front Squat 4x8 | Fri: Incline Press 4x10",
        "diet": "Breakfast: Eggs + PB Oats | Lunch: Chicken Biryani | Dinner: Mutton Curry + Rice",
        "calorie_factor": 35
    },
    "Beginner (BG)": {
        "workout": "Full Body Circuit: Air Squats, Ring Rows, Push-ups. Focus: Technique Mastery",
        "diet": "Balanced Tamil Meals: Idli-Sambar, Rice-Dal, Chapati. Protein Target: 120g/day",
        "calorie_factor": 26
    }
}

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "online",
        "service": "ACEest Fitness & Gym Management System API",
        "version": "1.0.0"
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/programs', methods=['GET'])
def get_programs():
    return jsonify({"programs": PROGRAMS}), 200

@app.route('/api/calculate-calories', methods=['POST'])
def calculate_calories():
    data = request.get_json()
    if not data or 'weight' not in data or 'program' not in data:
        return jsonify({"error": "Missing required fields: 'weight' and 'program'"}), 400
    
    prog_key = data['program']
    weight = data['weight']
    
    if prog_key not in PROGRAMS:
        return jsonify({"error": "Invalid program selected"}), 400
    
    try:
        weight = float(weight)
        if weight <= 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Weight must be a positive number"}), 400

    calories = int(weight * PROGRAMS[prog_key]["calorie_factor"])
    return jsonify({
        "program": prog_key,
        "weight_kg": weight,
        "estimated_calories": calories
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)