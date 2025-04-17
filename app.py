import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Secret key for session management 
GEMINI_API_KEY = 'AIzaSyCsXTGxnJrfyOB-tTFtOmzR4XL6VaVSZ2k'

import requests

# Replace with your actual API key from OpenWeather
WEATHER_API_KEY = '151e737556cf2b3114c276208bb7cacc'

@app.route('/weather', methods=['GET', 'POST'])
def weather_suggestions():
    if request.method == 'POST':
        city = request.form['city']

        # Call OpenWeather API
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or 'main' not in data:
            return render_template('weather.html', city=city, weather="Unavailable", suggested_items=[])

        temp = data['main']['temp']
        weather_desc = data['weather'][0]['main'].lower()

        # Match weather to tags
        tags = []
        if temp > 30:
            tags.append('light')
        elif temp < 15:
            tags.append('warm')
        elif 'rain' in weather_desc:
            tags.append('rainy')
        else:
            tags.append('normal')

        # Fetch matching clothes
        suggested_items = [item for item in closet_items if any(tag in item.get('tags', []) for tag in tags)]

        return render_template('weather.html', city=city, weather=f"{temp}°C, {weather_desc}", suggested_items=suggested_items)

    return render_template('weather.html')









# Define the route for the chatbot
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot_interface():
    if request.method == 'POST':
        user_mood = request.json.get('mood')  # Get the mood from the request body
        mood_tags = user_mood.split(",")  # Example user input: "happy, excited"

        # Fetch relevant items based on the mood tags
        relevant_items = fetch_closet_items_by_mood(mood_tags)

        # If no relevant items in wardrobe, suggest items from the closet
        if relevant_items:
            suggestions = relevant_items
        else:
            suggestions = closet_items  # If no matching wardrobe items, suggest all closet items

        # Return the filtered closet items as response to the frontend
        return jsonify({
            "message": f"Here are some clothing suggestions based on your mood: "
               f"{', '.join([f'{item['name']} <img src=\"{item['image_url']}\" alt=\"{item['name']}\" style=\"max-width: 100px; height: auto;\" />' for item in suggestions])}",
            "items": suggestions  # Send items as well
        })

    return render_template('chatbot.html')





# Function to fetch items based on mood tag
def fetch_closet_items_by_mood(mood_tags):
    filtered_items = []
    for item in closet_items:
        if any(tag in item['tags'] for tag in mood_tags):
            filtered_items.append(item)
    return filtered_items


# Function to get AI (Gemini) response based on the user's mood input
def get_ai_response(user_mood):
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    # Send the user mood as input to the AI model
    data = {
        "prompt": f"Suggest clothing based on the mood: {user_mood}",
        "max_tokens": 150
    }
    response = requests.post("https://api.gemini.com/v1/completions", headers=headers, json=data)
    return response.json().get('choices')[0].get('text')
# OpenWeatherMap API details
## OpenWeatherMap API details

                

# Function to get clothing suggestion based on weather condition


import json
import os

USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE): 
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)
WARDROBE_FILE = 'wardrobe.json'

def load_wardrobe():
    if os.path.exists(WARDROBE_FILE):
        with open(WARDROBE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_wardrobe(wardrobe_data):
    with open(WARDROBE_FILE, 'w') as f:
        json.dump(wardrobe_data, f, indent=4)


# Sample data for closet items
closet_items = [
    {
        'name': 'Beige and Red Saree',
        'category': 'Saree',
        'color': 'Beige/Red',
        'price': 12900.00,
        'image_url': '/static/images/saree7.jpg',
        'size': 'medium',
        'tags': ['happy', "warm"]
    },
    {
        'name': 'Red Female Sweater',
        'category': 'Sweater',
        'color': 'Red',
        'price': 4000.00,
        'image_url': '/static/images/red_sweater.jpg',
        'size': 'medium',
        'tags': ['happy',"warm"]
    },
    {
        'name': 'Casual Ladies Sweater',
        'category': 'Sweater',
        'color': 'White/Black',
        'price': 2000.00,
        'image_url': '/static/images/casual_ladies_sweater.jpg',
        'size': 'medium',
        'tags': ['casual','normal']
    },
    {
        'name': 'Classic Black Ladies Sweater',
        'category': 'Sweater',
        'color': 'White/Black',
        'price': 3000.00,
        'image_url': '/static/images/classic_black_sweater.jpg',
        'size': 'medium',
        'tags': ['sad',"warm"]
    },
    {
        'name': 'Classic Navy Blue Ladies Sweater',
        'category': 'Sweater',
        'color': 'Navy',
        'price': 3000.00,
        'image_url': '/static/images/navy_blue.png',
        'size': 'medium',
        'tags': ['sad']
    },
    {
        'name': 'Grey Sweater',
        'category': 'Sweater',
        'color': 'Grey',
        'price': 3000.00,
        'image_url': '/static/images/grey.jpg',
        'size': 'medium',
        'tags': ['sad']
    },
    {
        'name': 'Pink Sweater',
        'category': 'Sweater',
        'color': 'Pink',
        'price': 9500.00,
        'image_url': '/static/images/pink_sweater.webp',
        'size': 'medium',
        'tags': ['happy']
    },
    {
        'name': 'Light Pink Sweater',
        'category': 'Sweater',
        'color': 'Pink',
        'price': 8000.00,
        'image_url': '/static/images/light_pink_sweater.avif',
        'size': 'medium',
        'tags': ['happy']
    },
    {
        'name': 'Lava Red Sweater',
        'category': 'Sweater',
        'color': 'Red',
        'price': 8900.00,
        'image_url': '/static/images/lava_red.webp',
        'size': 'medium',
        'tags': ['happy']
    },
    {
        'name': 'Royal Blue Saree',
        'category': 'Saree',
        'color': 'Blue',
        'price': 18000.00,
        'image_url': '/static/images/blue saree.png',
        'size': 'medium',
        'tags': ['elegant']
    },
    {
        'name': 'Royal Blue Lehenga',
        'category': 'Lehenga',
        'color': 'Blue',
        'price': 118000.00,
        'image_url': '/static/images/royal_blue_lehenga.webp',
        'size': 'medium',
        'tags': ['elegant']
    },
    {
        'name': 'Elegant Blue Lehenga',
        'category': 'Lehenga',
        'color': 'Blue',
        'price': 128000.00,
        'image_url': '/static/images/lehenga2.webp',
        'size': 'medium',
        'tags': ['elegant']
    },
    {
        'name': 'Golden Lehenga',
        'category': 'Lehenga',
        'color': 'Golden',
        'price': 338000.00,
        'image_url': '/static/images/lehenga3.jpg',
        'size': 'medium',
        'tags': ['elegant']
    },
    {
        'name': 'Red Cotton Panjabi',
        'category': 'Panjabi',
        'color': 'Red',
        'price': 3800.00,
        'image_url': '/static/images/panjabi1_red.webp',
        'size': 'medium',
        'tags': ['happy',"normal"]
    },
    {
        'name': 'White Cotton Panjabi',
        'category': 'Panjabi',
        'color': 'White',
        'price': 3800.00,
        'image_url': '/static/images/panjabi2_white.webp',
        'size': 'medium',
        'tags': ['formal',"normal"]
    },
    {
        'name': 'Golden Silk Panjabi',
        'category': 'Panjabi',
        'color': 'Golden',
        'price': 5000.00,
        'image_url': '/static/images/panjabi3_golden.webp',
        'size': 'medium',
        'tags': ['elegant',"warm"]
    },
    {
        'name': 'Blue Cotton Panjabi',
        'category': 'Panjabi',
        'color': 'Blue',
        'price': 3000.00,
        'image_url': '/static/images/panjabi4_blue.webp',
        'size': 'medium',
        'tags': ['casual']
    },
    {
        'name': 'Golden Embroidered Saree',
        'category': 'Saree',
        'color': 'Golden',
        'price': 9500.00,
        'image_url': '/static/images/saree5.jpg',
        'size': 'medium',
        'tags': ['elegant']
    },
    {
        'name': 'Green Dyed Saree',
        'category': 'Saree',
        'color': 'Green',
        'price': 11727.27,
        'image_url': '/static/images/saree3.webp',
        'size': 'medium',
        'tags': ['casual']
    },
    {
        'name': 'Pastel Color Saree',
        'category': 'Saree',
        'color': 'Pastel',
        'price': 2586.36,
        'image_url': '/static/images/saree2.webp',
        'size': 'medium',
        'tags': ['happy']
    },
    {
        'name': 'Pink Floral Saree',
        'category': 'Saree',
        'color': 'Pink',
        'price': 8500.00,
        'image_url': '/static/images/saree4.webp',
        'size': 'medium',
        'tags': ['happy']
    },
    {
        'name': 'Red Printed Saree',
        'category': 'Saree',
        'color': 'Red',
        'price': 3045.45,
        'image_url': '/static/images/saree1.webp',
        'size': 'medium',
        'tags': ['happy']
    },
    {
        'name': 'Teal Saree',
        'category': 'Saree',
        'color': 'Teal',
        'price': 10600.00,
        'image_url': '/static/images/saree6.jpg',
        'size': 'medium',
        'tags': ['elegant']
    },
    {
        'name': 'Brown Jamdani Saree',
        'category': 'Saree',
        'color': 'Brown',
        'price': 7100.00,
        'image_url': '/static/images/saree8.webp',
        'size': 'medium',
        'tags': ['casual']
    },
    {
        'name': 'Marigold Appliqued and Embroidered Cotton Saree',
        'category': 'Saree',
        'color': 'Yellow/Red',
        'price': 2086.36,
        'image_url': '/static/images/orange_sharee.webp',
        'size': 'medium',
        'tags': ['happy']
    },
    {
        'name': 'Green/Blue Tie-Dyed and Printed Cotton Saree',
        'category': 'Saree',
        'color': 'Green/Blue',
        'price': 2586.36,
        'image_url': '/static/images/green_blue_saree.webp',
        'size': 'medium',
        'tags': ['casual']
    },
    {
        'name': 'Women Pure Wool Shawl',
        'category': 'Shawls',
        'color': 'Black and Blue',
        'price': 4200.00,
        'image_url': '/static/images/women_pure_wool_shawl.webp',
        'size': 'medium',
        'tags': ['elegant']
    },
    {
        'name': 'Women Kashmiri Shawl',
        'category': 'Shawls',
        'color': 'White',
        'price': 4300.00,
        'image_url': '/static/images/shawl2.webp',
        'size': 'medium',
        'tags': ['elegant']
    },
    {
        'name': 'Golden Shawl',
        'category': 'Shawls',
        'color': 'Golden',
        'price': 4700.00,
        'image_url': '/static/images/shawl3.webp',
        'size': 'medium',
        'tags': ['elegant']
    },
    {
        'name': 'Leather Formal Shoe',
        'category': 'Formal Shoe',
        'color': 'Brown',
        'price': 3500.00,
        'image_url': '/static/images/shoe1.jpeg',
        'size': 'medium',
        'tags': ['formal']
    },
    {
        'name': 'Black Formal Shoe',
        'category': 'Formal Shoe',
        'color': 'Black',
        'price': 2500.00,
        'image_url': '/static/images/shoe2.jpeg',
        'size': 'medium',
        'tags': ['formal']
    },
    {
        'name': 'Black Formal Shinning Shoe',
        'category': 'Formal Shoe',
        'color': 'Black',
        'price': 2200.00,
        'image_url': '/static/images/shoe4.jpg',
        'size': 'medium',
        'tags': ['formal']
    },
    {
        'name': 'Sports Shoe',
        'category': 'Casual Shoe',
        'color': 'White',
        'price': 3200.00,
        'image_url': '/static/images/shoe10.jpg',
        'size': 'medium',
        'tags': ['casual']
    },
    {
        'name': 'Sports Ajanta Shoe',
        'category': 'Casual Shoe',
        'color': 'Blue',
        'price': 4500.00,
        'image_url': '/static/images/shoe12.jpg',
        'size': 'medium',
        'tags': ['casual']
    },
    {
        'name': 'Summer Casual Shoe',
        'category': 'Casual Shoe',
        'color': 'Brown',
        'price': 3600.00,
        'image_url': '/static/images/shoe22.jpg',
        'size': 'medium',
        'tags': ['casual',"light"]
    },
    {
        'name': 'High Heels',
        'category': 'Heels',
        'color': 'Black',
        'price': 5199.00,
        'image_url': '/static/images/heels1.jpg',
        'size': 'medium',
        'tags': ['elegant']
    },
    {
        'name': 'High Golden Heels',
        'category': 'Heels',
        'color': 'Golden',
        'price': 5499.00,
        'image_url': '/static/images/heels2.jpg',
        'size': 'medium',
        'tags': ['elegant']
    },
    {
        'name': 'High Pink Heels',
        'category': 'Heels',
        'color': 'Pink',
        'price': 5199.00,
        'image_url': '/static/images/heel3.jpg',
        'size': 'medium',
        'tags': ['elegant']
    },
    {
        'name': 'Salowar Flower Kamiz',
        'category': 'Ethnic',
        'color': 'Blue',
        'price': 5299.00,
        'image_url': '/static/images/selowar2.webp',
        'size': 'medium',
        'tags': ['casual',"light"]
    },
    {
        'name': 'Salowar Green Kamiz',
        'category': 'Ethnic',
        'color': 'Green',
        'price': 4899.00,
        'image_url': '/static/images/selowar4.webp',
        'size': 'medium',
        'tags': ['casual']
    },
    {
        'name': 'Salowar White Green Kamiz',
        'category': 'Ethnic',
        'color': 'Green',
        'price': 5299.00,
        'image_url': '/static/images/kamiz4.webp',
        'size': 'medium',
        'tags': ['casual']
    },
    {
        'name': 'Katha Style Salowar Kamiz',
        'category': 'Ethnic',
        'color': 'Orange',
        'price': 5299.00,
        'image_url': '/static/images/brunt orange.webp',
        'size': 'medium',
        'tags': ['casual']
    },

    {
        'name': 'Shirt',
        'category': 'Shirt',
        'color': 'Orange',
        'price': 2399.00,
        'image_url': '/static/images/shirt2.jpg',
        'size': 'medium',
        'tags': ['casual']
    },


    {
        'name': 'Blue Formal Shirt',
        'category': 'Shirt',
        'color': 'Blue',
        'price': 3299.00,
        'image_url': '/static/images/shirt.jpg',
        'size': 'medium',
        'tags': ['formal', 'elegant']
    },

    {
        'name': 'Casual Shirt',
        'category': 'Shirt',
        'color': 'Brown',
        'price': 2399.00,
        'image_url': '/static/images/shirt4.jpg',
        'size': 'medium',
        'tags': ['casual', 'comfortable']
    },
    {
        'name': 'Casual Dark Pink Shirt',
        'category': 'Shirt',
        'color': 'Pink',
        'price': 1899.00,
        'image_url': '/static/images/shirt5.jpg',
        'size': 'medium',
        'tags': ['casual', 'comfortable']
    },
    {
        'name': 'Casual Maroon Shirt',
        'category': 'Shirt',
        'color': 'Maroon',
        'price': 2399.00,
        'image_url': '/static/images/shir6.jpg',
        'size': 'medium',
        'tags': ['casual', 'comfortable']
    },
    {
        'name': 'Jeans Pant',
        'category': 'Pant',
        'color': 'Blue',
        'price': 1699.00,
        'image_url': '/static/images/pant1.jpg',
        'size': 'medium',
        'tags': ['casual', 'comfortable']
    },
    {
        'name': 'Jeans White Indigo Pant',
        'category': 'Pant',
        'color': 'Blue',
        'price': 1799.00,
        'image_url': '/static/images/pant2.jpg',
        'size': 'medium',
        'tags': ['casual', 'comfortable']
    },
    {
        'name': 'Brown Fit Chino Pant',
        'category': 'Pant',
        'color': 'Brown',
        'price': 1699.00,
        'image_url': '/static/images/pant3.jpg',
        'size': 'medium',
        'tags': ['casual', 'comfortable']
    },
    {
        'name': 'Knit Fabric Formal Pant',
        'category': 'Pant',
        'color': 'Black',
        'price': 1699.00,
        'image_url': '/static/images/pant4.jpeg',
        'size': 'medium',
        'tags': ['formal', 'elegant']
    },
    {
        'name': 'Fit Chino Formal Pant',
        'category': 'Pant',
        'color': 'Black',
        'price': 1699.00,
        'image_url': '/static/images/pant5.jpeg',
        'size': 'medium',
        'tags': ['formal', 'elegant']
    },
    {
        'name': 'Women Ready Blouse',
        'category': 'Blouse',
        'color': 'White',
        'price': 1340.00,
        'image_url': '/static/images/blouse1.webp',
        'size': 'medium',
        'tags': ['casual', 'comfortable']
    },
    {
        'name': 'Women Ready Black Blouse',
        'category': 'Blouse',
        'color': 'Black',
        'price': 1799.00,
        'image_url': '/static/images/blouse2.webp',
        'size': 'medium',
        'tags': ['formal', 'elegant']
    },
    {
        'name': 'Women Ready Orange Blouse',
        'category': 'Blouse',
        'color': 'Orange',
        'price': 1659.00,
        'image_url': '/static/images/blouse4.webp',
        'size': 'medium',
        'tags': ['casual', 'comfortable']
    },
    {
        'name': 'White Tops',
        'category': 'Tops',
        'color': 'White',
        'price': 1380.00,
        'image_url': '/static/images/tops.jpg',
        'size': 'medium',
        'tags': ['casual', 'comfortable']
    },
    {
        'name': 'White Sky Blue Tops',
        'category': 'Tops',
        'color': 'Blue',
        'price': 1280.00,
        'image_url': '/static/images/tops2.webp',
        'size': 'medium',
        'tags': ['casual', 'comfortable']
    },
    {
        'name': 'Maroon Tops',
        'category': 'Tops',
        'color': 'Maroon',
        'price': 1570.00,
        'image_url': '/static/images/tops3.jpg',
        'size': 'medium',
        'tags': ['casual', 'comfortable']
    },
    {
        'name': 'Black Tops',
        'category': 'Tops',
        'color': 'Black',
        'price': 1240.00,
        'image_url': '/static/images/tops5.avif',
        'size': 'medium',
        'tags': ['casual', 'comfortable']
    },
    {
        'name': 'Printed Tops',
        'category': 'Tops',
        'color': 'Black',
        'price': 1545.00,
        'image_url': '/static/images/tops6.jpg',
        'size': 'medium',
        'tags': ['casual', 'comfortable']
    }
]


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if email ends with @gmail.com
        if not email.endswith('@gmail.com'):
            error = "Email must be a Gmail address (e.g., yourname@gmail.com)."
            return render_template('register.html', error=error)

        users = load_users()

        # Check if email already registered
        if any(user['email'] == email for user in users):
            error = "This email is already registered. Please log in."
            return render_template('register.html', error=error)

        # Register the user
        users.append({'username': username, 'email': email, 'password': password})
        save_users(users)

        return redirect(url_for('login'))

    return render_template('register.html')




@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        users = load_users()

        # Find user in file
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)

        if user:
            # Store the first name in the session
            first_name = user['username'].split()[0]  # Assuming the username is in the format "First Last"
            session['first_name'] = first_name  # Save the first name in the session
            session['username'] = user['username']
            session['email'] = user['email']

            return redirect(url_for('dashboard'))
        else:
            error = "Invalid email or password"
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    email = session['email']

    wardrobe_data = load_wardrobe()
    wardrobe_items = wardrobe_data.get(email, [])

    return render_template('dashboard.html', username=username, wardrobe_items=wardrobe_items)









@app.route('/closet', methods=['GET'])
def view_closet():
    if 'username' not in session:
        return redirect(url_for('login'))

    sort_by = request.args.get('sort_by', 'color')  # Default sorting is by color
    color_filter = request.args.get('color_filter', '')
    view_by = request.args.get('view_by', '')

    # Clear the success message if not related to cart operation
    success_message = session.pop('success_message', None)

    # Filter items by color
    if color_filter:
        filtered_items = [item for item in closet_items if color_filter.lower() in item['color'].lower()]
    else:
        filtered_items = closet_items[:]

    # Filter by category or fabric
    if view_by == 'category':
        filtered_items = [item for item in filtered_items if item['category']]
    elif view_by == 'fabric':
        filtered_items = [item for item in filtered_items if 'fabric' in item]  # Optional

    # Sort items
    if sort_by == 'price':
        filtered_items.sort(key=lambda x: x['price'])
    else:
        filtered_items.sort(key=lambda x: x['color'])

    username = session.get('username')  # ✅ Grab the username from the session

    return render_template(
        'view_closet.html',
        closet_items=filtered_items,
        success_message=success_message,
        username=username ) # ✅ Send to template 
    


from urllib.parse import unquote  # Make sure to import unquote if not already imported

@app.route('/add_to_cart/<string:item_name>', methods=['POST'])
def add_to_cart(item_name):
    item_name = unquote(item_name)  # Decode URL-encoded name like Red%20Sweater → Red Sweater
    quantity = int(request.form.get('quantity', 1))
    size = request.form.get('size', 'medium')  # Get size from form (default to 'medium')

    # Find the item in the closet_items list
    item = next((i for i in closet_items if i['name'] == item_name), None)
    if not item:
        session['success_message'] = "Item not found."
        return redirect(url_for('view_closet'))

    if 'cart' not in session:
        session['cart'] = []

    # Add size to the item before adding to cart
    for cart_item in session['cart']:
        if cart_item['name'] == item['name'] and cart_item['size'] == size:  # Check both name and size
            cart_item['quantity'] += quantity  # If item already in cart, just update quantity
            break
    else:
        item_copy = item.copy()
        item_copy['quantity'] = quantity
        item_copy['size'] = size  # Add size to the item copy
        session['cart'].append(item_copy)

    # Update the total price in the session
    session['total_price'] = sum(i['price'] * i['quantity'] for i in session['cart'])

    session['success_message'] = f"'{item['name']}' (Size: {size}) has been added to the cart!"
    return redirect(url_for('view_closet'))





@app.route('/view_cart', methods=['GET'])
def view_cart():
    cart_items = session.get('cart', [])
    total_price = session.get('total_price', 0.0)
    return render_template('view_cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    if 'cart' in session:
        session['cart'] = [item for idx, item in enumerate(session['cart']) if idx != item_id]
        session['total_price'] = sum(item['price'] * item['quantity'] for item in session['cart'])
        session['success_message'] = "Item removed successfully!"  # Success message for item removal
    return redirect(url_for('view_cart'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    session.pop('total_price', None)
    session['success_message'] = "Cart cleared successfully!"  # Success message for clearing the cart
    return redirect(url_for('view_closet')) 


@app.route('/confirm_payment', methods=['POST'])
def confirm_payment():
    if 'username' not in session:
        return redirect(url_for('login'))

    email = session.get('email')  # Use the same email from login
    cart_items = session.get('cart', [])

    # Load current wardrobe data from file
    wardrobe_data = load_wardrobe()

    # If user already has wardrobe items, extend them
    if email in wardrobe_data:
        wardrobe_data[email].extend(cart_items)
    else:
        wardrobe_data[email] = cart_items

    # Save updated data
    save_wardrobe(wardrobe_data)

    # Clear cart
    session.pop('cart', None)
    session.pop('total_price', None)

    session['success_message'] = "Payment confirmed! Items moved to your wardrobe."

    return redirect(url_for('dashboard'))



# ================= VIEW CATEGORIES =================

@app.route('/view_categories', methods=['GET'])
def view_categories():
    return render_template('view_categories.html')

# ================= VIEW FABRICS =================

@app.route('/view_fabrics', methods=['GET'])
def view_fabrics():
    return render_template('view_fabrics.html')
@app.route('/fabric_instructions/<fabric>')
def fabric_instructions(fabric):
    # Fabric care instructions
    care_instructions = {
        'silk': 'Dry clean only. Do not bleach. Iron on low heat.',
        'cotton-silk': 'Hand wash in cold water. Do not wring. Iron on low heat.',
        'chiffon': 'Dry clean only. Do not tumble dry.',
        'georgette': 'Hand wash cold. Do not bleach.',
        # Add more fabric types here
    }

    # Get the specific instructions for the clicked fabric
    instructions = care_instructions.get(fabric, 'No instructions available for this fabric.')

    # Render a blank page to display the instructions
    return render_template('fabric_instructions.html', fabric=fabric, instructions=instructions)


@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('login'))

@app.route('/quick_view/<item_name>')
def quick_view(item_name):
    # Find the item in closet_items
    item = next((i for i in closet_items if i['name'] == item_name), None)
    if item:
        return render_template('quick_view.html', item=item)
    else:
        return redirect(url_for('view_closet'))  # If item is not found

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')  # Make sure you have a chatbot.html template


if __name__ == '__main__':
    app.run(port=1344, debug=True)
