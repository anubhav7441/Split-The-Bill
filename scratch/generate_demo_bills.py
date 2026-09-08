import json
import os
import sys

demo_bills = [
    {
        "id": "royal_biryani",
        "title": "Royal Biryani House",
        "category": "Indian & Mughlai",
        "icon": "🍛",
        "description": "Authentic Dum Biryani with Mutton Korma and Garlic Naan",
        "image_file": "01_royal_biryani.jpg",
        "currency": "₹",
        "bill": {
            "items": [
                {"name": "Chicken Biryani", "quantity": 2, "unit_price": 380.0, "line_total": 760.0, "confidence": 0.98},
                {"name": "Mutton Korma", "quantity": 1, "unit_price": 450.0, "line_total": 450.0, "confidence": 0.95},
                {"name": "Garlic Naan", "quantity": 4, "unit_price": 70.0, "line_total": 280.0, "confidence": 0.99},
                {"name": "Coke (250ml)", "quantity": 3, "unit_price": 45.0, "line_total": 135.0, "confidence": 0.96}
            ],
            "subtotal": 1625.0,
            "subtotal_confidence": 0.98,
            "discount": 0.0,
            "discount_confidence": 1.0,
            "tax": 81.26,
            "tax_confidence": 0.95,
            "service_charge": 162.50,
            "service_charge_confidence": 0.92,
            "printed_total": 1869.0,
            "printed_total_confidence": 0.99
        }
    },
    {
        "id": "bella_italia",
        "title": "Bella Italia Pizzeria",
        "category": "Italian & Pizza",
        "icon": "🍕",
        "description": "Woodfired Margherita, Truffle Pasta, and Tiramisu",
        "image_file": "02_bella_italia.jpg",
        "currency": "£",
        "bill": {
            "items": [
                {"name": "Margherita Pizza", "quantity": 1, "unit_price": 14.95, "line_total": 14.95, "confidence": 0.97},
                {"name": "Truffle Pasta", "quantity": 1, "unit_price": 18.50, "line_total": 18.50, "confidence": 0.95},
                {"name": "Garlic Bread w/ Cheese", "quantity": 1, "unit_price": 6.20, "line_total": 6.20, "confidence": 0.98},
                {"name": "Tiramisu", "quantity": 1, "unit_price": 7.80, "line_total": 7.80, "confidence": 0.94},
                {"name": "Sparkling Water (S.Pel)", "quantity": 2, "unit_price": 3.30, "line_total": 6.60, "confidence": 0.96}
            ],
            "subtotal": 54.05,
            "subtotal_confidence": 0.98,
            "discount": 0.0,
            "discount_confidence": 1.0,
            "tax": 10.81,
            "tax_confidence": 0.94,
            "service_charge": 6.76,
            "service_charge_confidence": 0.92,
            "printed_total": 71.62,
            "printed_total_confidence": 0.99
        }
    },
    {
        "id": "blue_tokai",
        "title": "Blue Tokai Artisan Cafe",
        "category": "Cafe & Bakery",
        "icon": "☕",
        "description": "Artisan Flat White, Avocado Toast, and Almond Croissants",
        "image_file": "03_blue_tokai.jpg",
        "currency": "₹",
        "bill": {
            "items": [
                {"name": "Flat White", "quantity": 1, "unit_price": 280.0, "line_total": 280.0, "confidence": 0.99},
                {"name": "Iced Caramel Latte", "quantity": 1, "unit_price": 310.0, "line_total": 310.0, "confidence": 0.98},
                {"name": "Almond Croissant", "quantity": 1, "unit_price": 220.0, "line_total": 220.0, "confidence": 0.97},
                {"name": "Avocado Sourdough Toast", "quantity": 1, "unit_price": 480.0, "line_total": 480.0, "confidence": 0.96},
                {"name": "Blueberry Muffin", "quantity": 1, "unit_price": 190.0, "line_total": 190.0, "confidence": 0.97}
            ],
            "subtotal": 1480.0,
            "subtotal_confidence": 0.99,
            "discount": 0.0,
            "discount_confidence": 1.0,
            "tax": 74.0,
            "tax_confidence": 0.96,
            "service_charge": 0.0,
            "service_charge_confidence": 1.0,
            "printed_total": 1554.0,
            "printed_total_confidence": 0.99
        }
    },
    {
        "id": "smash_burger",
        "title": "Smash Burger Shack",
        "category": "Burgers & Fast Casual",
        "icon": "🍔",
        "description": "Double Cheeseburger with Truffle Parm Fries & Shake",
        "image_file": "04_smash_burger.jpg",
        "currency": "$",
        "bill": {
            "items": [
                {"name": "Double Cheeseburger", "quantity": 1, "unit_price": 14.99, "line_total": 14.99, "confidence": 0.98},
                {"name": "Crispy Chicken Burger", "quantity": 1, "unit_price": 13.50, "line_total": 13.50, "confidence": 0.97},
                {"name": "Truffle Parm Fries", "quantity": 1, "unit_price": 6.75, "line_total": 6.75, "confidence": 0.96},
                {"name": "Onion Rings", "quantity": 1, "unit_price": 5.50, "line_total": 5.50, "confidence": 0.98},
                {"name": "Chocolate Shake", "quantity": 1, "unit_price": 6.95, "line_total": 6.95, "confidence": 0.97}
            ],
            "subtotal": 47.69,
            "subtotal_confidence": 0.99,
            "discount": 0.0,
            "discount_confidence": 1.0,
            "tax": 4.23,
            "tax_confidence": 0.95,
            "service_charge": 0.0,
            "service_charge_confidence": 1.0,
            "printed_total": 51.92,
            "printed_total_confidence": 0.99
        }
    },
    {
        "id": "tokyo_sushi",
        "title": "Tokyo Sushi Bar",
        "category": "Japanese & Sushi",
        "icon": "🍣",
        "description": "Fresh Salmon Sashimi, Dragon Roll, Edamame, and Miso",
        "image_file": "05_tokyo_sushi.jpg",
        "currency": "¥",
        "bill": {
            "items": [
                {"name": "Salmon Sashimi (5 pcs)", "quantity": 1, "unit_price": 1800.0, "line_total": 1800.0, "confidence": 0.98},
                {"name": "Spicy Tuna Roll (8 pcs)", "quantity": 1, "unit_price": 1400.0, "line_total": 1400.0, "confidence": 0.97},
                {"name": "Dragon Roll (8 pcs)", "quantity": 1, "unit_price": 2200.0, "line_total": 2200.0, "confidence": 0.98},
                {"name": "Edamame (Salted)", "quantity": 1, "unit_price": 600.0, "line_total": 600.0, "confidence": 0.99},
                {"name": "Miso Soup", "quantity": 2, "unit_price": 400.0, "line_total": 800.0, "confidence": 0.96},
                {"name": "Japanese Green Tea (Hot)", "quantity": 2, "unit_price": 500.0, "line_total": 1000.0, "confidence": 0.97}
            ],
            "subtotal": 7800.0,
            "subtotal_confidence": 0.99,
            "discount": 0.0,
            "discount_confidence": 1.0,
            "tax": 780.0,
            "tax_confidence": 0.95,
            "service_charge": 780.0,
            "service_charge_confidence": 0.94,
            "printed_total": 9360.0,
            "printed_total_confidence": 0.99
        }
    },
    {
        "id": "taqueria_fiesta",
        "title": "Taqueria La Fiesta",
        "category": "Mexican Street Food",
        "icon": "🌮",
        "description": "Beef Birria Tacos, Pollo Asado, Chips & Guacamole",
        "image_file": "06_taqueria_fiesta.jpg",
        "currency": "$",
        "bill": {
            "items": [
                {"name": "Chips & Guacamole", "quantity": 1, "unit_price": 7.95, "line_total": 7.95, "confidence": 0.99},
                {"name": "Beef Birria Tacos (3x)", "quantity": 2, "unit_price": 15.95, "line_total": 31.90, "confidence": 0.96},
                {"name": "Pollo Asado Taco (3x)", "quantity": 1, "unit_price": 13.95, "line_total": 13.95, "confidence": 0.98},
                {"name": "Horchata", "quantity": 1, "unit_price": 4.50, "line_total": 4.50, "confidence": 0.97},
                {"name": "Churros", "quantity": 1, "unit_price": 6.00, "line_total": 6.00, "confidence": 0.96}
            ],
            "subtotal": 64.30,
            "subtotal_confidence": 0.99,
            "discount": 0.0,
            "discount_confidence": 1.0,
            "tax": 5.43,
            "tax_confidence": 0.95,
            "service_charge": 0.0,
            "service_charge_confidence": 1.0,
            "printed_total": 69.73,
            "printed_total_confidence": 0.99
        }
    },
    {
        "id": "punjabi_dhaba",
        "title": "Grand Punjabi Dhaba",
        "category": "North Indian Feast",
        "icon": "🥘",
        "description": "Paneer Butter Masala, Dal Makhani, Garlic Naans & Sweet Lassi",
        "image_file": "07_punjabi_dhaba.svg",
        "currency": "₹",
        "bill": {
            "items": [
                {"name": "Paneer Butter Masala", "quantity": 1, "unit_price": 380.0, "line_total": 380.0, "confidence": 0.97},
                {"name": "Dal Makhani", "quantity": 1, "unit_price": 340.0, "line_total": 340.0, "confidence": 0.98},
                {"name": "Butter Garlic Naan", "quantity": 4, "unit_price": 75.0, "line_total": 300.0, "confidence": 0.99},
                {"name": "Jeera Rice", "quantity": 1, "unit_price": 220.0, "line_total": 220.0, "confidence": 0.96},
                {"name": "Special Sweet Lassi", "quantity": 3, "unit_price": 110.0, "line_total": 330.0, "confidence": 0.95},
                {"name": "Gulab Jamun (2 pcs)", "quantity": 2, "unit_price": 90.0, "line_total": 180.0, "confidence": 0.97}
            ],
            "subtotal": 1750.0,
            "subtotal_confidence": 0.98,
            "discount": 0.0,
            "discount_confidence": 1.0,
            "tax": 87.50,
            "tax_confidence": 0.95,
            "service_charge": 87.50,
            "service_charge_confidence": 0.93,
            "printed_total": 1925.0,
            "printed_total_confidence": 0.99
        }
    },
    {
        "id": "rooftop_lounge",
        "title": "Skyline Rooftop Lounge",
        "category": "Bar & Lounge",
        "icon": "🍸",
        "description": "Craft Cocktails, Loaded Nachos, BBQ Wings & Craft Beer",
        "image_file": "08_rooftop_lounge.svg",
        "currency": "₹",
        "bill": {
            "items": [
                {"name": "Classic Mint Mojito", "quantity": 2, "unit_price": 450.0, "line_total": 900.0, "confidence": 0.98},
                {"name": "Craft Wheat Beer Pitcher", "quantity": 1, "unit_price": 1200.0, "line_total": 1200.0, "confidence": 0.97},
                {"name": "Loaded Nachos Supreme", "quantity": 1, "unit_price": 520.0, "line_total": 520.0, "confidence": 0.96},
                {"name": "Peri Peri Chicken Wings", "quantity": 1, "unit_price": 480.0, "line_total": 480.0, "confidence": 0.98},
                {"name": "Truffle Fries Basket", "quantity": 1, "unit_price": 350.0, "line_total": 350.0, "confidence": 0.95}
            ],
            "subtotal": 3450.0,
            "subtotal_confidence": 0.99,
            "discount": 200.0,
            "discount_confidence": 0.98,
            "tax": 325.0,
            "tax_confidence": 0.95,
            "service_charge": 345.0,
            "service_charge_confidence": 0.92,
            "printed_total": 3920.0,
            "printed_total_confidence": 0.99
        }
    },
    {
        "id": "green_garden",
        "title": "Green Garden Organic Cafe",
        "category": "Healthy & Brunch",
        "icon": "🥗",
        "description": "Acai Bowl, Eggs Benedict, Cold Pressed Juices & Sourdough",
        "image_file": "09_green_garden.svg",
        "currency": "₹",
        "bill": {
            "items": [
                {"name": "Truffle Eggs Benedict", "quantity": 1, "unit_price": 490.0, "line_total": 490.0, "confidence": 0.98},
                {"name": "Tropical Acai Superbowl", "quantity": 1, "unit_price": 420.0, "line_total": 420.0, "confidence": 0.97},
                {"name": "Cold-Pressed Green Glow Juice", "quantity": 2, "unit_price": 240.0, "line_total": 480.0, "confidence": 0.96},
                {"name": "Warm Banana Walnut Bread", "quantity": 1, "unit_price": 210.0, "line_total": 210.0, "confidence": 0.99}
            ],
            "subtotal": 1600.0,
            "subtotal_confidence": 0.99,
            "discount": 80.0,
            "discount_confidence": 0.99,
            "tax": 76.0,
            "tax_confidence": 0.95,
            "service_charge": 0.0,
            "service_charge_confidence": 1.0,
            "printed_total": 1596.0,
            "printed_total_confidence": 0.99
        }
    },
    {
        "id": "smokehouse_bbq",
        "title": "Texas Smokehouse BBQ",
        "category": "BBQ & Steaks",
        "icon": "🥩",
        "description": "Slow-smoked Beef Brisket, Pulled Pork & Creamy Mac & Cheese",
        "image_file": "10_smokehouse_bbq.svg",
        "currency": "$",
        "bill": {
            "items": [
                {"name": "Smoked Beef Brisket (1/2 lb)", "quantity": 2, "unit_price": 21.50, "line_total": 43.00, "confidence": 0.98},
                {"name": "Pulled Pork Sandwich", "quantity": 1, "unit_price": 14.50, "line_total": 14.50, "confidence": 0.97},
                {"name": "Four-Cheese Mac & Cheese", "quantity": 1, "unit_price": 8.00, "line_total": 8.00, "confidence": 0.99},
                {"name": "Buttermilk Cornbread (2x)", "quantity": 1, "unit_price": 5.50, "line_total": 5.50, "confidence": 0.96},
                {"name": "Southern Sweet Iced Tea", "quantity": 2, "unit_price": 3.50, "line_total": 7.00, "confidence": 0.97}
            ],
            "subtotal": 78.00,
            "subtotal_confidence": 0.99,
            "discount": 0.0,
            "discount_confidence": 1.0,
            "tax": 6.83,
            "tax_confidence": 0.95,
            "service_charge": 14.04,
            "service_charge_confidence": 0.92,
            "printed_total": 98.87,
            "printed_total_confidence": 0.99
        }
    },
    {
        "id": "coastal_catch",
        "title": "Ocean Breeze Coastal Seafood",
        "category": "Seafood Grill",
        "icon": "🦞",
        "description": "Butter Garlic Prawns, Grilled Sea Bass & Coconut Rice",
        "image_file": "11_coastal_catch.svg",
        "currency": "₹",
        "bill": {
            "items": [
                {"name": "Butter Garlic Jumbo Prawns", "quantity": 1, "unit_price": 750.0, "line_total": 750.0, "confidence": 0.98},
                {"name": "Grilled Lemon Butter Sea Bass", "quantity": 1, "unit_price": 850.0, "line_total": 850.0, "confidence": 0.97},
                {"name": "Crispy Calamari Rings", "quantity": 1, "unit_price": 420.0, "line_total": 420.0, "confidence": 0.96},
                {"name": "Steamed Fragrant Rice", "quantity": 2, "unit_price": 160.0, "line_total": 320.0, "confidence": 0.98},
                {"name": "Fresh Lime Mint Cooler", "quantity": 2, "unit_price": 140.0, "line_total": 280.0, "confidence": 0.97}
            ],
            "subtotal": 2620.0,
            "subtotal_confidence": 0.99,
            "discount": 0.0,
            "discount_confidence": 1.0,
            "tax": 131.0,
            "tax_confidence": 0.96,
            "service_charge": 180.0,
            "service_charge_confidence": 0.93,
            "printed_total": 2931.0,
            "printed_total_confidence": 0.99
        }
    },
    {
        "id": "sweet_tooth",
        "title": "Sweet Tooth Waffle & Gelato",
        "category": "Desserts & Bakery",
        "icon": "🍰",
        "description": "Nutella Belgian Waffle, Molten Lava Cake & Gelato Scoops",
        "image_file": "12_sweet_tooth.svg",
        "currency": "₹",
        "bill": {
            "items": [
                {"name": "Nutella Strawberries Belgian Waffle", "quantity": 1, "unit_price": 360.0, "line_total": 360.0, "confidence": 0.99},
                {"name": "Dark Chocolate Molten Lava Cake", "quantity": 1, "unit_price": 290.0, "line_total": 290.0, "confidence": 0.98},
                {"name": "Pistachio & Mango Gelato Duo", "quantity": 2, "unit_price": 180.0, "line_total": 360.0, "confidence": 0.97},
                {"name": "Gourmet Hot Chocolate w/ Marshmallows", "quantity": 1, "unit_price": 240.0, "line_total": 240.0, "confidence": 0.98}
            ],
            "subtotal": 1250.0,
            "subtotal_confidence": 0.99,
            "discount": 100.0,
            "discount_confidence": 0.98,
            "tax": 57.50,
            "tax_confidence": 0.95,
            "service_charge": 0.0,
            "service_charge_confidence": 1.0,
            "printed_total": 1207.50,
            "printed_total_confidence": 0.99
        }
    },
    {
        "id": "dim_sum_house",
        "title": "Golden Lotus Dim Sum House",
        "category": "Asian & Dim Sum",
        "icon": "🥟",
        "description": "Crystal Prawn Dumplings, Siu Mai, BBQ Pork Buns & Jasmine Tea",
        "image_file": "13_dim_sum_house.svg",
        "currency": "$",
        "bill": {
            "items": [
                {"name": "Har Gow (Crystal Shrimp Dumpling)", "quantity": 2, "unit_price": 8.50, "line_total": 17.00, "confidence": 0.98},
                {"name": "Chicken Siu Mai (4 pcs)", "quantity": 1, "unit_price": 7.50, "line_total": 7.50, "confidence": 0.97},
                {"name": "Steamed BBQ Pork Buns (3 pcs)", "quantity": 1, "unit_price": 7.00, "line_total": 7.00, "confidence": 0.98},
                {"name": "Wok Crispy Veg Spring Rolls", "quantity": 1, "unit_price": 6.50, "line_total": 6.50, "confidence": 0.96},
                {"name": "Imperial Jasmine Hot Tea Pot", "quantity": 1, "unit_price": 5.00, "line_total": 5.00, "confidence": 0.99}
            ],
            "subtotal": 43.00,
            "subtotal_confidence": 0.99,
            "discount": 0.0,
            "discount_confidence": 1.0,
            "tax": 3.76,
            "tax_confidence": 0.96,
            "service_charge": 4.30,
            "service_charge_confidence": 0.93,
            "printed_total": 51.06,
            "printed_total_confidence": 0.99
        }
    },
    {
        "id": "sports_bar",
        "title": "The Dugout Sports Lounge",
        "category": "Pub & Finger Food",
        "icon": "🍻",
        "description": "Beer Pitcher, Loaded Buffalo Wings & Cheesy Fries",
        "image_file": "14_sports_bar.svg",
        "currency": "₹",
        "bill": {
            "items": [
                {"name": "Premium Lager Beer Pitcher (1.5L)", "quantity": 1, "unit_price": 1150.0, "line_total": 1150.0, "confidence": 0.98},
                {"name": "Buffalo Glazed Wings (12 pcs)", "quantity": 1, "unit_price": 540.0, "line_total": 540.0, "confidence": 0.97},
                {"name": "Cheesy Bacon Loaded Fries", "quantity": 1, "unit_price": 380.0, "line_total": 380.0, "confidence": 0.98},
                {"name": "Crispy Mozzarella Sticks", "quantity": 1, "unit_price": 320.0, "line_total": 320.0, "confidence": 0.96},
                {"name": "Red Bull Energy Drink", "quantity": 2, "unit_price": 180.0, "line_total": 360.0, "confidence": 0.97}
            ],
            "subtotal": 2750.0,
            "subtotal_confidence": 0.99,
            "discount": 0.0,
            "discount_confidence": 1.0,
            "tax": 275.0,
            "tax_confidence": 0.95,
            "service_charge": 200.0,
            "service_charge_confidence": 0.92,
            "printed_total": 3225.0,
            "printed_total_confidence": 0.99
        }
    },
    {
        "id": "south_indian_tiffin",
        "title": "Sri Krishna Bhavan Tiffin",
        "category": "South Indian Veg",
        "icon": "🥞",
        "description": "Ghee Roast Masala Dosa, Idli Vada Combo & Filter Coffee",
        "image_file": "15_south_indian_tiffin.svg",
        "currency": "₹",
        "bill": {
            "items": [
                {"name": "Special Ghee Masala Dosa", "quantity": 2, "unit_price": 140.0, "line_total": 280.0, "confidence": 0.99},
                {"name": "Steamed Idli (2) & Medu Vada (1) Combo", "quantity": 2, "unit_price": 110.0, "line_total": 220.0, "confidence": 0.98},
                {"name": "Crispy Onion Rava Dosa", "quantity": 1, "unit_price": 160.0, "line_total": 160.0, "confidence": 0.97},
                {"name": "Degree Kumbakonam Filter Coffee", "quantity": 4, "unit_price": 45.0, "line_total": 180.0, "confidence": 0.99}
            ],
            "subtotal": 840.0,
            "subtotal_confidence": 0.99,
            "discount": 0.0,
            "discount_confidence": 1.0,
            "tax": 42.0,
            "tax_confidence": 0.96,
            "service_charge": 0.0,
            "service_charge_confidence": 1.0,
            "printed_total": 882.0,
            "printed_total_confidence": 0.99
        }
    }
]


def generate_svg_receipt(demo):
    title = demo["title"]
    curr = demo["currency"]
    b = demo["bill"]
    items = b["items"]

    # Calculate height dynamically based on items
    h = 420 + len(items) * 26

    item_rows = ""
    y = 200
    for it in items:
        qty = int(it["quantity"]) if it["quantity"].is_integer() else it["quantity"]
        name = it["name"]
        if len(name) > 24:
            name = name[:22] + ".."
        total_str = f"{curr}{it['line_total']:,.2f}"
        rate_str = f"@{it['unit_price']:,.2f}"
        item_rows += f"""
        <text x="32" y="{y}" font-family="'Courier New', monospace" font-size="12" fill="#2d3748">{qty}x {name}</text>
        <text x="320" y="{y}" font-family="'Courier New', monospace" font-size="12" fill="#2d3748" text-anchor="end">{total_str}</text>
        """
        y += 24

    y += 10
    tax_rows = f"""
    <line x1="28" y1="{y}" x2="322" y2="{y}" stroke="#cbd5e1" stroke-dasharray="4,4" stroke-width="1.2"/>
    <text x="32" y="{y+22}" font-family="'Courier New', monospace" font-size="12" fill="#4a5568">Subtotal</text>
    <text x="320" y="{y+22}" font-family="'Courier New', monospace" font-size="12" fill="#4a5568" text-anchor="end">{curr}{b['subtotal']:,.2f}</text>
    """
    y += 38

    if b.get("discount", 0) > 0:
        tax_rows += f"""
        <text x="32" y="{y}" font-family="'Courier New', monospace" font-size="12" fill="#10b981">Discount</text>
        <text x="320" y="{y}" font-family="'Courier New', monospace" font-size="12" fill="#10b981" text-anchor="end">-{curr}{b['discount']:,.2f}</text>
        """
        y += 20

    if b.get("tax", 0) > 0:
        tax_rows += f"""
        <text x="32" y="{y}" font-family="'Courier New', monospace" font-size="12" fill="#4a5568">Tax / GST</text>
        <text x="320" y="{y}" font-family="'Courier New', monospace" font-size="12" fill="#4a5568" text-anchor="end">{curr}{b['tax']:,.2f}</text>
        """
        y += 20

    if b.get("service_charge", 0) > 0:
        tax_rows += f"""
        <text x="32" y="{y}" font-family="'Courier New', monospace" font-size="12" fill="#4a5568">Service Charge</text>
        <text x="320" y="{y}" font-family="'Courier New', monospace" font-size="12" fill="#4a5568" text-anchor="end">{curr}{b['service_charge']:,.2f}</text>
        """
        y += 20

    y += 6
    total_section = f"""
    <line x1="28" y1="{y}" x2="322" y2="{y}" stroke="#1a202c" stroke-width="1.5"/>
    <text x="32" y="{y+24}" font-family="'Courier New', monospace" font-size="15" font-weight="bold" fill="#111827">TOTAL AMOUNT</text>
    <text x="320" y="{y+24}" font-family="'Courier New', monospace" font-size="16" font-weight="bold" fill="#111827" text-anchor="end">{curr}{b['printed_total']:,.2f}</text>
    <line x1="28" y1="{y+34}" x2="322" y2="{y+34}" stroke="#1a202c" stroke-width="1.5"/>
    """

    y += 58

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="350" height="{h}" viewBox="0 0 350 {h}">
    <defs>
        <filter id="paper-shadow" x="-5%" y="-2%" width="110%" height="106%">
            <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity="0.25"/>
        </filter>
        <pattern id="sawtooth" width="16" height="8" patternUnits="userSpaceOnUse">
            <polygon points="0,0 8,8 16,0" fill="#1e1b4b"/>
        </pattern>
    </defs>
    
    <!-- Background Card Frame -->
    <rect x="15" y="10" width="320" height="{h-20}" rx="6" fill="#fffdf9" filter="url(#paper-shadow)"/>
    
    <!-- Top jagged tear -->
    <path d="M 15 14 Q 25 10 35 14 T 55 14 T 75 14 T 95 14 T 115 14 T 135 14 T 155 14 T 175 14 T 195 14 T 215 14 T 235 14 T 255 14 T 275 14 T 295 14 T 315 14 T 335 14" stroke="#e2e8f0" fill="none" stroke-width="1"/>
    
    <!-- Receipt Header -->
    <text x="175" y="48" font-family="'Courier New', monospace" font-size="16" font-weight="bold" fill="#111827" text-anchor="middle">{title.upper()}</text>
    <text x="175" y="68" font-family="'Courier New', monospace" font-size="11" fill="#64748b" text-anchor="middle">Official Restaurant Bill Receipt</text>
    <text x="175" y="84" font-family="'Courier New', monospace" font-size="10" fill="#94a3b8" text-anchor="middle">Table #12 · Guests: 3 · Cashier: System</text>
    <text x="175" y="98" font-family="'Courier New', monospace" font-size="10" fill="#94a3b8" text-anchor="middle">Date: 26-Oct-2023 20:45</text>
    
    <line x1="28" y1="112" x2="322" y2="112" stroke="#111827" stroke-width="1.2"/>
    <text x="32" y="128" font-family="'Courier New', monospace" font-size="11" font-weight="bold" fill="#1e293b">QTY  ITEM</text>
    <text x="320" y="128" font-family="'Courier New', monospace" font-size="11" font-weight="bold" fill="#1e293b" text-anchor="end">PRICE</text>
    <line x1="28" y1="136" x2="322" y2="136" stroke="#cbd5e1" stroke-dasharray="4,4" stroke-width="1"/>
    
    <!-- Items -->
    {item_rows}
    
    <!-- Totals -->
    {tax_rows}
    
    {total_section}
    
    <!-- Footer Note -->
    <text x="175" y="{y+16}" font-family="'Courier New', monospace" font-size="11" font-weight="bold" fill="#475569" text-anchor="middle">THANK YOU! VISIT AGAIN</text>
    <text x="175" y="{y+32}" font-family="'Courier New', monospace" font-size="9" fill="#94a3b8" text-anchor="middle">*** Paid in Full · Card Auth: #94821 ***</text>
    
    <!-- Barcode mockup -->
    <g transform="translate(60, {y+44})">
        <rect x="0" y="0" width="3" height="24" fill="#334155"/>
        <rect x="6" y="0" width="1" height="24" fill="#334155"/>
        <rect x="10" y="0" width="4" height="24" fill="#334155"/>
        <rect x="18" y="0" width="2" height="24" fill="#334155"/>
        <rect x="23" y="0" width="5" height="24" fill="#334155"/>
        <rect x="32" y="0" width="2" height="24" fill="#334155"/>
        <rect x="37" y="0" width="1" height="24" fill="#334155"/>
        <rect x="42" y="0" width="6" height="24" fill="#334155"/>
        <rect x="52" y="0" width="2" height="24" fill="#334155"/>
        <rect x="58" y="0" width="4" height="24" fill="#334155"/>
        <rect x="66" y="0" width="1" height="24" fill="#334155"/>
        <rect x="70" y="0" width="3" height="24" fill="#334155"/>
        <rect x="77" y="0" width="5" height="24" fill="#334155"/>
        <rect x="86" y="0" width="2" height="24" fill="#334155"/>
        <rect x="92" y="0" width="4" height="24" fill="#334155"/>
        <rect x="100" y="0" width="1" height="24" fill="#334155"/>
        <rect x="105" y="0" width="3" height="24" fill="#334155"/>
        <rect x="112" y="0" width="6" height="24" fill="#334155"/>
        <rect x="122" y="0" width="2" height="24" fill="#334155"/>
        <rect x="128" y="0" width="3" height="24" fill="#334155"/>
        <rect x="135" y="0" width="1" height="24" fill="#334155"/>
        <rect x="140" y="0" width="5" height="24" fill="#334155"/>
        <rect x="150" y="0" width="2" height="24" fill="#334155"/>
        <rect x="156" y="0" width="4" height="24" fill="#334155"/>
        <rect x="164" y="0" width="1" height="24" fill="#334155"/>
        <rect x="170" y="0" width="3" height="24" fill="#334155"/>
        <rect x="176" y="0" width="6" height="24" fill="#334155"/>
        <rect x="186" y="0" width="2" height="24" fill="#334155"/>
        <rect x="192" y="0" width="4" height="24" fill="#334155"/>
        <rect x="200" y="0" width="2" height="24" fill="#334155"/>
        <rect x="206" y="0" width="5" height="24" fill="#334155"/>
        <rect x="215" y="0" width="2" height="24" fill="#334155"/>
        <rect x="220" y="0" width="4" height="24" fill="#334155"/>
    </g>
</svg>
"""
    return svg


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_data_dir = os.path.join(root, "sample_data")
    static_bills_dir = os.path.join(root, "static", "sample_bills")
    os.makedirs(sample_data_dir, exist_ok=True)
    os.makedirs(static_bills_dir, exist_ok=True)

    # Save demo_bills.json
    json_path = os.path.join(sample_data_dir, "demo_bills.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(demo_bills, f, indent=2)
    print(f"Saved {len(demo_bills)} demo bills to {json_path}")

    # Generate SVGs for bills (all bills get an SVG receipt representation)
    for b in demo_bills:
        svg_filename = b["image_file"]
        if svg_filename.endswith(".svg"):
            out_path = os.path.join(static_bills_dir, svg_filename)
            svg_content = generate_svg_receipt(b)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(svg_content)
            print(f"Generated SVG: {svg_filename}")

    # Also keep the single demo_bill.json backward compatible with bill 1
    with open(os.path.join(sample_data_dir, "demo_bill.json"), "w", encoding="utf-8") as f:
        json.dump(demo_bills[0]["bill"], f, indent=2)
    print("Updated demo_bill.json for backward compatibility.")

if __name__ == "__main__":
    main()
