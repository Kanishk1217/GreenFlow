from flask import Flask, render_template, request, jsonify, session
from datetime import datetime, timedelta
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# In-memory data storage (replace with database in production)
users_db = {}
gardens_db = {}
chat_history = {}

# Sample plant data
PLANTS_DATA = {
    "cherry_tomatoes": {
        "name": "Cherry Tomatoes",
        "days_to_harvest": 60,
        "icon": "🍅",
        "description": "Sweet and juicy cherry tomatoes perfect for salads",
        "water_ph": "5.8-6.5",
        "growth_tips": "Needs plenty of sunlight and regular nutrient monitoring"
    },
    "spinach": {
        "name": "Spinach",
        "days_to_harvest": 40,
        "icon": "🥬",
        "description": "Nutrient-rich leafy green vegetable",
        "water_ph": "6.0-7.0",
        "growth_tips": "Grows best in cooler temperatures"
    },
    "lettuce": {
        "name": "Lettuce",
        "days_to_harvest": 30,
        "icon": "🥗",
        "description": "Crisp and fresh lettuce varieties",
        "water_ph": "5.5-6.5",
        "growth_tips": "Quick growing, perfect for beginners"
    },
    "strawberry": {
        "name": "Strawberry",
        "days_to_harvest": 90,
        "icon": "🍓",
        "description": "Sweet hydroponic strawberries",
        "water_ph": "5.5-6.5",
        "growth_tips": "Requires good air circulation"
    },
    "basil": {
        "name": "Basil",
        "days_to_harvest": 25,
        "icon": "🌿",
        "description": "Aromatic herb for cooking",
        "water_ph": "5.5-6.5",
        "growth_tips": "Pinch flowers to encourage leaf growth"
    },
    "mint": {
        "name": "Mint",
        "days_to_harvest": 30,
        "icon": "🍃",
        "description": "Refreshing herb with multiple uses",
        "water_ph": "6.0-7.0",
        "growth_tips": "Fast growing, prune regularly"
    }
}

PACKAGES = {
    "balcony_40": {
        "name": "Balcony Starter (40 plants)",
        "price": 3000,
        "plants": 40,
        "area": "40-60 sq ft",
        "description": "Perfect for small balconies"
    },
    "balcony_60": {
        "name": "Balcony Premium (60 plants)",
        "price": 4500,
        "plants": 60,
        "area": "60-80 sq ft",
        "description": "Enhanced balcony setup"
    },
    "terrace_100": {
        "name": "Terrace Garden (100 plants)",
        "price": 6000,
        "plants": 100,
        "area": "100-150 sq ft",
        "description": "Full terrace hydroponics system"
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if email in users_db:
        return jsonify({'success': False, 'message': 'User already exists'})
    
    users_db[email] = {
        'name': name,
        'password': generate_password_hash(password),
        'created_at': datetime.now().isoformat(),
        'preferences': {},
        'subscription': None
    }
    
    session['user'] = email
    return jsonify({'success': True, 'user': {'name': name, 'email': email}})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if email not in users_db:
        return jsonify({'success': False, 'message': 'User not found'})
    
    if not check_password_hash(users_db[email]['password'], password):
        return jsonify({'success': False, 'message': 'Invalid password'})
    
    session['user'] = email
    user_data = {
        'name': users_db[email]['name'],
        'email': email,
        'subscription': users_db[email].get('subscription')
    }
    return jsonify({'success': True, 'user': user_data})

@app.route('/api/user', methods=['GET'])
def get_user():
    if 'user' not in session:
        return jsonify({'success': False})
    
    email = session['user']
    user_data = {
        'name': users_db[email]['name'],
        'email': email,
        'subscription': users_db[email].get('subscription'),
        'preferences': users_db[email].get('preferences', {})
    }
    return jsonify({'success': True, 'user': user_data})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'success': True})

@app.route('/api/garden/create', methods=['POST'])
def create_garden():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    email = session['user']
    
    garden_id = f"garden_{len(gardens_db) + 1}"
    gardens_db[garden_id] = {
        'owner': email,
        'name': data.get('name', 'My Garden'),
        'package': data.get('package'),
        'plants': data.get('plants', []),
        'created_at': datetime.now().isoformat(),
        'status': 'active'
    }
    
    return jsonify({'success': True, 'garden_id': garden_id})

@app.route('/api/garden/<garden_id>', methods=['GET'])
def get_garden(garden_id):
    if garden_id not in gardens_db:
        return jsonify({'success': False, 'message': 'Garden not found'})
    
    garden = gardens_db[garden_id]
    plants_with_data = []
    
    for plant in garden['plants']:
        plant_info = PLANTS_DATA.get(plant['type'], {})
        planted_date = datetime.fromisoformat(garden['created_at'])
        days_elapsed = (datetime.now() - planted_date).days
        days_remaining = plant_info.get('days_to_harvest', 60) - days_elapsed
        
        plants_with_data.append({
            'type': plant['type'],
            'name': plant_info.get('name', plant['type']),
            'icon': plant_info.get('icon', '🌱'),
            'days_remaining': max(0, days_remaining),
            'growth_percentage': min(100, (days_elapsed / plant_info.get('days_to_harvest', 60)) * 100),
            'days_elapsed': days_elapsed
        })
    
    return jsonify({
        'success': True,
        'garden': {
            **garden,
            'plants': plants_with_data
        }
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '').lower()
    
    # Simple rule-based chatbot
    responses = {
        'hello': 'Hello! I\'m your GreenFlow assistant. How can I help you with your hydroponic garden today?',
        'hi': 'Hi there! Ready to grow something amazing?',
        'help': 'I can help you with plant care, watering schedules, nutrient management, and troubleshooting. What would you like to know?',
        'water': 'For hydroponics, maintain pH between 5.5-6.5. Check water levels daily and top up as needed. The system uses about 1-2 liters per plant per week.',
        'nutrient': 'Add nutrients every 2 weeks. Use a balanced NPK formula designed for hydroponics. Start with half strength and adjust based on plant response.',
        'ph': 'Ideal pH for most hydroponic plants is 5.8-6.5. Test daily using pH strips or a digital meter. Adjust with pH up or down solutions.',
        'light': 'Most vegetables need 12-16 hours of light daily. Use full-spectrum LED grow lights if natural sunlight is insufficient.',
        'harvest': 'Harvest times vary by plant. Lettuce: 30 days, Spinach: 40 days, Tomatoes: 60 days. Check your plant\'s specific timeline in the app!',
        'pest': 'Use organic neem oil spray for common pests. Maintain good air circulation. Inspect plants weekly for early signs of issues.',
        'price': 'Our packages start at ₹3,000 for 40 plants. Installation includes setup, plants, and 1 month support. Subscription is ₹499/month.',
        'subscription': 'Our ₹499/month subscription includes: weekly tips, priority support, plant replacement warranty, and expert consultations.',
        'book': 'You can book a consultation visit for ₹200. Our expert will visit your space, assess sunlight and feasibility, and recommend the best setup!'
    }
    
    # Find matching response
    response = 'I\'m not sure about that. Could you ask about watering, nutrients, pH, lighting, harvest times, pests, pricing, or booking a consultation?'
    
    for keyword, resp in responses.items():
        if keyword in message:
            response = resp
            break
    
    return jsonify({'success': True, 'response': response})

@app.route('/api/packages', methods=['GET'])
def get_packages():
    return jsonify({'success': True, 'packages': PACKAGES})

@app.route('/api/plants', methods=['GET'])
def get_plants():
    return jsonify({'success': True, 'plants': PLANTS_DATA})

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    email = session['user']
    users_db[email]['subscription'] = {
        'plan': 'premium',
        'price': 499,
        'started_at': datetime.now().isoformat()
    }
    
    return jsonify({'success': True, 'message': 'Subscription activated!'})

if __name__ == '__main__':
    # Create templates directory
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
