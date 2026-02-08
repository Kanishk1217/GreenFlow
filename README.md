# GreenFlow Hydroponics Website

A beautiful, interactive single-page website for GreenFlow Hydroponics - a hydroponic garden installation service in Ahmedabad, India.

## Features

✨ **Beautiful UI/UX**
- Smooth animations and transitions
- Responsive design for all devices
- Green-themed color scheme inspired by nature
- Animated background elements

🌱 **Core Functionality**
- User registration and login
- User profiles with personalized dashboard
- Package selection (40, 60, 100 plant systems)
- Garden tracking dashboard
- Real-time plant progress monitoring
- Harvest countdown timer

💬 **AI Chatbot**
- Interactive chatbot assistant
- Answers questions about plant care, watering, nutrients, pH levels
- Provides pricing and subscription information
- Booking assistance

📊 **Dashboard Features**
- Track individual plant growth
- Progress bars for each plant
- Days until harvest countdown
- Maintenance scheduling
- Subscription management

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python app.py
```

3. **Open your browser and visit:**
```
http://localhost:5000
```

## Usage

### For Users:
1. Click "Get Started" to create an account
2. Browse available packages (₹3,000 - ₹6,000)
3. Book a ₹200 consultation
4. After installation, track your garden progress on the dashboard
5. Use the chatbot (💬 button) for instant help
6. Subscribe to Premium (₹499/month) for additional support

### For Development:
- The app uses Flask for the backend
- All data is stored in-memory (replace with a database for production)
- Templates are in `/templates/`
- Main application logic is in `app.py`

## Project Structure

```
greenflow/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/
    └── index.html        # Single-page website template
```

## API Endpoints

- `GET /` - Main website
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/user` - Get current user
- `POST /api/logout` - Logout
- `POST /api/garden/create` - Create garden
- `GET /api/garden/<id>` - Get garden details
- `POST /api/chat` - Chatbot interaction
- `GET /api/packages` - Get available packages
- `GET /api/plants` - Get plant catalog
- `POST /api/subscribe` - Subscribe to premium

## Features Overview

### Packages:
1. **Balcony Starter (40 plants)** - ₹3,000
2. **Balcony Premium (60 plants)** - ₹4,500
3. **Terrace Garden (100 plants)** - ₹6,000

### Plants Available:
- Cherry Tomatoes 🍅
- Spinach 🥬
- Lettuce 🥗
- Strawberry 🍓
- Basil 🌿
- Mint 🍃

### Subscription Benefits (₹499/month):
- App reminders and notifications
- Expert support via phone
- Plant replacement warranty
- Growth analytics

## Technologies Used

- **Backend:** Python Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Fonts:** Google Fonts (Poppins, Space Mono)
- **Design:** Custom CSS with animations
- **Authentication:** Flask sessions with password hashing

## Production Deployment Notes

For production deployment, consider:
1. Replace in-memory storage with PostgreSQL/MySQL
2. Add environment variables for secrets
3. Implement proper session management with Redis
4. Add HTTPS/SSL certificates
5. Set up proper error logging
6. Implement rate limiting for API endpoints
7. Add payment gateway integration
8. Enhance chatbot with actual AI/ML models

## Business Model

- **Consultation:** ₹200 (one-time)
- **Installation:** ₹3,000 - ₹6,000 (one-time)
- **Subscription:** ₹499/month (recurring)
- **Target Market:** Urban homes in Ahmedabad with balconies/terraces
- **USP:** Space-efficient, water-saving, organic hydroponics

## Chatbot Commands

The chatbot can answer questions about:
- **hello/hi** - Greetings
- **help** - Get help menu
- **water** - Watering guidelines
- **nutrient** - Nutrient management
- **ph** - pH level information
- **light** - Lighting requirements
- **harvest** - Harvest timelines
- **pest** - Pest control
- **price** - Pricing information
- **subscription** - Subscription details
- **book** - Booking consultation

## License

Proprietary - GreenFlow Hydroponics

## Contact

For support or inquiries, use the chatbot on the website or contact the GreenFlow team.
