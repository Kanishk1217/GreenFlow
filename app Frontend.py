"""
GreenFlow Hydroponics - Flask Web Application
Converts the HTML application to Python backend with Flask
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
from datetime import datetime, timedelta
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'greenflow_secret_key_2024'
CORS(app)

# ===== DATA STORAGE (In-memory) =====
# In production, use a proper database like PostgreSQL or MongoDB
users_db = {}
chat_history = {}
subscriptions = {}
consultations = []

# Sample packages data
PACKAGES = {
    'starter': {
        'name': 'Starter Kit',
        'price': 9999,
        'plants': 4,
        'area': '2x2 ft'
    },
    'professional': {
        'name': 'Professional Setup',
        'price': 24999,
        'plants': 12,
        'area': '4x4 ft'
    },
    'commercial': {
        'name': 'Commercial System',
        'price': 59999,
        'plants': 30,
        'area': '8x8 ft'
    }
}

# Sample plants for dashboard
SAMPLE_PLANTS = [
    {'name': 'Cherry Tomatoes', 'icon': '🍅', 'progress': 75},
    {'name': 'Spinach', 'icon': '🥬', 'progress': 95},
    {'name': 'Lettuce', 'icon': '🥗', 'progress': 85},
    {'name': 'Basil', 'icon': '🌿', 'progress': 90},
    {'name': 'Mint', 'icon': '🍃', 'progress': 88},
    {'name': 'Strawberry', 'icon': '🍓', 'progress': 60}
]

# Bot responses for chat
BOT_RESPONSES = {
    'hello': 'Hello! Welcome to GreenFlow. How can I help you with your hydroponic garden today?',
    'help': 'I can help you with: setup, troubleshooting, plant care, and package information. What would you like to know?',
    'water': 'For hydroponic systems, check water levels daily and maintain pH between 5.5-6.5. Change water every 3-4 weeks.',
    'light': 'Most plants need 12-16 hours of LED light daily. Ensure lights are 12-24 inches from plants.',
    'plants': 'Popular choices: tomatoes, lettuce, spinach, basil, herbs, and strawberries. Choose based on space and climate.',
    'cost': 'Our starter kit is ₹9,999, professional is ₹24,999, and commercial is ₹59,999.',
    'default': 'That\'s a great question! For specific advice, please book a consultation with our experts.'
}


# ===== HELPER FUNCTIONS =====
def get_bot_response(user_message):
    """Generate bot response based on user message"""
    message_lower = user_message.lower()
    
    for keyword, response in BOT_RESPONSES.items():
        if keyword in message_lower:
            return response
    
    return BOT_RESPONSES['default']


def check_authentication(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not authenticated'}), 401
        return f(*args, **kwargs)
    return decorated_function


# ===== ROUTES =====
@app.route('/')
def index():
    """Main page route"""
    return render_template('index.html')


# ===== AUTHENTICATION ROUTES =====
@app.route('/api/login', methods=['POST'])
def login():
    """Login endpoint"""
    data = request.json
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    # Validate input
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password required'}), 400
    
    # Check if user exists
    if email in users_db:
        user = users_db[email]
        if user['password'] == password:  # In production, use hashed passwords
            session['user_id'] = email
            session['user_name'] = user['name']
            
            return jsonify({
                'success': True,
                'user': {
                    'id': email,
                    'name': user['name'],
                    'email': email
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid password'}), 401
    else:
        return jsonify({'success': False, 'message': 'User not found'}), 404


@app.route('/api/register', methods=['POST'])
def register():
    """Register endpoint"""
    data = request.json
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    # Validate input
    if not name or not email or not password:
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    
    if len(password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
    
    # Check if user already exists
    if email in users_db:
        return jsonify({'success': False, 'message': 'Email already registered'}), 409
    
    # Create new user
    users_db[email] = {
        'name': name,
        'email': email,
        'password': password,  # In production, hash this
        'created_at': datetime.now().isoformat(),
        'subscription': False
    }
    
    session['user_id'] = email
    session['user_name'] = name
    chat_history[email] = []
    
    return jsonify({
        'success': True,
        'user': {
            'id': email,
            'name': name,
            'email': email
        }
    })


@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout endpoint"""
    if 'user_id' in session:
        session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@app.route('/api/current-user')
def get_current_user():
    """Get current user information"""
    if 'user_id' in session:
        user_id = session['user_id']
        user = users_db.get(user_id)
        if user:
            return jsonify({
                'success': True,
                'user': {
                    'id': user_id,
                    'name': user['name'],
                    'email': user['email']
                }
            })
    
    return jsonify({'success': False, 'user': None})


# ===== PACKAGES ROUTES =====
@app.route('/api/packages', methods=['GET'])
def get_packages():
    """Get all available packages"""
    return jsonify({
        'success': True,
        'packages': PACKAGES
    })


@app.route('/api/packages/<package_id>', methods=['GET'])
def get_package_details(package_id):
    """Get details of a specific package"""
    if package_id in PACKAGES:
        return jsonify({
            'success': True,
            'package': PACKAGES[package_id]
        })
    else:
        return jsonify({'success': False, 'message': 'Package not found'}), 404


@app.route('/api/select-package', methods=['POST'])
@check_authentication
def select_package():
    """Select a package for installation"""
    user_id = session['user_id']
    data = request.json
    package_id = data.get('package_id')
    
    if package_id not in PACKAGES:
        return jsonify({'success': False, 'message': 'Invalid package'}), 400
    
    # Record package selection
    user = users_db.get(user_id)
    if user:
        user['selected_package'] = package_id
        user['package_selected_at'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'message': 'Package selected. Our team will contact you soon.',
            'package': PACKAGES[package_id]
        })
    
    return jsonify({'success': False, 'message': 'User not found'}), 404


# ===== DASHBOARD ROUTES =====
@app.route('/api/dashboard')
@check_authentication
def get_dashboard():
    """Get dashboard data"""
    user_id = session['user_id']
    user = users_db.get(user_id)
    
    return jsonify({
        'success': True,
        'user': {
            'name': user['name'],
            'email': user['email'],
            'subscription': user.get('subscription', False)
        },
        'plants': SAMPLE_PLANTS,
        'stats': {
            'total_plants': len(SAMPLE_PLANTS),
            'growing': sum(1 for p in SAMPLE_PLANTS if p['progress'] > 50),
            'health_score': 85
        }
    })


# ===== CHAT ROUTES =====
@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat messages"""
    data = request.json
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'success': False, 'message': 'Empty message'}), 400
    
    # Get bot response
    response = get_bot_response(message)
    
    # Store in chat history if user is logged in
    if 'user_id' in session:
        user_id = session['user_id']
        if user_id not in chat_history:
            chat_history[user_id] = []
        
        chat_history[user_id].append({
            'timestamp': datetime.now().isoformat(),
            'user': message,
            'bot': response
        })
    
    return jsonify({
        'success': True,
        'response': response
    })


@app.route('/api/chat-history')
@check_authentication
def get_chat_history():
    """Get chat history for logged-in user"""
    user_id = session['user_id']
    history = chat_history.get(user_id, [])
    
    return jsonify({
        'success': True,
        'history': history
    })


# ===== SUBSCRIPTION ROUTES =====
@app.route('/api/subscribe', methods=['POST'])
@check_authentication
def subscribe():
    """Subscribe to premium plan"""
    user_id = session['user_id']
    user = users_db.get(user_id)
    
    if user:
        user['subscription'] = True
        user['subscription_start'] = datetime.now().isoformat()
        user['subscription_end'] = (datetime.now() + timedelta(days=30)).isoformat()
        
        subscriptions[user_id] = {
            'start': user['subscription_start'],
            'end': user['subscription_end'],
            'plan': 'premium'
        }
        
        return jsonify({
            'success': True,
            'message': 'Subscription activated!',
            'subscription': subscriptions[user_id]
        })
    
    return jsonify({'success': False, 'message': 'User not found'}), 404


@app.route('/api/subscription-status')
@check_authentication
def get_subscription_status():
    """Get subscription status"""
    user_id = session['user_id']
    user = users_db.get(user_id)
    
    if user:
        return jsonify({
            'success': True,
            'subscription': user.get('subscription', False),
            'subscription_end': user.get('subscription_end')
        })
    
    return jsonify({'success': False, 'message': 'User not found'}), 404


# ===== CONSULTATION ROUTES =====
@app.route('/api/consultation', methods=['POST'])
def book_consultation():
    """Book a consultation"""
    data = request.json
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    message = data.get('message', '').strip()
    
    # Validate input
    if not all([name, email, phone]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    
    # Save consultation request
    consultation = {
        'id': len(consultations) + 1,
        'name': name,
        'email': email,
        'phone': phone,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'status': 'pending'
    }
    
    consultations.append(consultation)
    
    return jsonify({
        'success': True,
        'message': 'Consultation booked! Our team will call you within 24 hours.',
        'consultation': consultation
    })


@app.route('/api/consultations')
@check_authentication
def get_consultations():
    """Get all consultations (admin only for now)"""
    return jsonify({
        'success': True,
        'consultations': consultations
    })


# ===== FEATURES ROUTES =====
@app.route('/api/features', methods=['GET'])
def get_features():
    """Get features information"""
    features = [
        {
            'title': 'Smart Monitoring',
            'description': 'Real-time tracking of pH, nutrient levels, and plant growth.',
            'icon': '📊'
        },
        {
            'title': 'Automated Systems',
            'description': 'Self-regulating irrigation and nutrient delivery systems.',
            'icon': '⚙️'
        },
        {
            'title': 'Expert Support',
            'description': 'Access to our hydroponics experts for guidance and troubleshooting.',
            'icon': '👥'
        }
    ]
    
    return jsonify({
        'success': True,
        'features': features
    })


# ===== ERROR HANDLERS =====
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'success': False, 'message': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'success': False, 'message': 'Server error'}), 500


@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 errors"""
    return jsonify({'success': False, 'message': 'Unauthorized'}), 401


# ===== ADMIN ROUTES =====
@app.route('/api/admin/stats')
@check_authentication
def get_admin_stats():
    """Get admin statistics"""
    # Check if user is admin (simplified)
    return jsonify({
        'success': True,
        'stats': {
            'total_users': len(users_db),
            'total_consultations': len(consultations),
            'active_subscriptions': sum(1 for u in users_db.values() if u.get('subscription')),
            'pending_consultations': sum(1 for c in consultations if c['status'] == 'pending')
        }
    })


# ===== UTILITY ROUTES =====
@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
