#!/usr/bin/env python3
"""
Generate sample product data for PartSelect case study.
This creates realistic product data when scraping is not possible.
"""

import csv
import random
import os


def generate_sample_data(num_products=50):
    """
    Generate sample product data for refrigerator and dishwasher parts.
    
    Args:
        num_products: Number of products to generate (default: 50)
    """
    
    # Sample product titles and descriptions
    refrigerator_parts = [
        ("Refrigerator Water Filter", "High-quality refrigerator water filter that removes contaminants and improves taste. Compatible with most major refrigerator brands."),
        ("Refrigerator Door Gasket", "Durable refrigerator door gasket seal that prevents cold air loss and maintains proper temperature. Easy to install."),
        ("Refrigerator Thermostat", "Precision refrigerator thermostat that controls temperature accurately. Replacement part for various refrigerator models."),
        ("Refrigerator Evaporator Fan Motor", "Quiet and efficient evaporator fan motor for refrigerator cooling system. OEM replacement part."),
        ("Refrigerator Defrost Timer", "Automatic defrost timer that cycles defrost mode. Compatible with multiple refrigerator brands."),
        ("Refrigerator Ice Maker Assembly", "Complete ice maker assembly with all necessary components. Easy installation with included instructions."),
        ("Refrigerator Door Handle", "Sturdy refrigerator door handle replacement. Available in various finishes to match your refrigerator."),
        ("Refrigerator Light Bulb", "LED refrigerator light bulb that provides bright illumination. Energy-efficient and long-lasting."),
        ("Refrigerator Door Shelf", "Spacious refrigerator door shelf for organizing food items. Adjustable and easy to clean."),
        ("Refrigerator Crisper Drawer", "Large capacity crisper drawer for storing fruits and vegetables. Helps maintain freshness."),
        ("Refrigerator Compressor Relay", "Reliable compressor relay that starts and protects the refrigerator compressor. OEM quality replacement."),
        ("Refrigerator Door Switch", "Magnetic door switch that controls interior lighting. Simple replacement procedure."),
        ("Refrigerator Temperature Sensor", "Accurate temperature sensor that monitors refrigerator temperature. Essential for proper cooling."),
        ("Refrigerator Drain Pan", "Heavy-duty drain pan that collects condensation. Prevents water damage to floor."),
        ("Refrigerator Door Hinge", "Durable door hinge that ensures smooth door operation. Reinforced design for long-lasting use."),
        ("Refrigerator Shelf Support", "Adjustable shelf support brackets for customizing refrigerator storage space. Easy to install."),
        ("Refrigerator Door Latch", "Secure door latch that keeps refrigerator door closed. Compatible with various models."),
        ("Refrigerator Condenser Fan Blade", "Efficient condenser fan blade that improves air circulation. Reduces energy consumption."),
        ("Refrigerator Water Inlet Valve", "Reliable water inlet valve for ice maker and water dispenser. Prevents leaks and ensures proper water flow."),
        ("Refrigerator Control Board", "Advanced control board that manages refrigerator functions. OEM replacement with full compatibility."),
        ("Refrigerator Door Bin", "Organized door bin for storing condiments and beverages. Easy to remove for cleaning."),
        ("Refrigerator Thermistor", "Precise thermistor that monitors temperature changes. Critical component for temperature control."),
        ("Refrigerator Door Seal", "Flexible door seal that creates airtight closure. Prevents energy waste and maintains temperature."),
        ("Refrigerator Light Socket", "Standard light socket for refrigerator interior lighting. Compatible with LED and incandescent bulbs."),
        ("Refrigerator Door Gasket Magnet", "Strong magnetic strip for door gasket attachment. Ensures secure seal."),
    ]
    
    dishwasher_parts = [
        ("Dishwasher Upper Rack", "Adjustable upper rack for dishwasher. Provides flexible loading options for dishes and utensils."),
        ("Dishwasher Lower Spray Arm", "Efficient lower spray arm that distributes water evenly. Ensures thorough cleaning of dishes."),
        ("Dishwasher Door Latch", "Secure door latch that keeps dishwasher door closed during cycle. Safety feature prevents leaks."),
        ("Dishwasher Door Gasket", "Watertight door gasket that prevents leaks. Essential for proper dishwasher operation."),
        ("Dishwasher Heating Element", "Powerful heating element that dries dishes effectively. Energy-efficient design reduces operating costs."),
        ("Dishwasher Water Inlet Valve", "Reliable water inlet valve that controls water flow. Prevents leaks and ensures proper filling."),
        ("Dishwasher Circulation Pump", "Quiet circulation pump that moves water throughout dishwasher. OEM quality replacement."),
        ("Dishwasher Door Handle", "Stylish door handle replacement for dishwasher. Available in various finishes."),
        ("Dishwasher Filter", "High-quality filter that traps food particles. Easy to clean and maintain."),
        ("Dishwasher Detergent Dispenser", "Automatic detergent dispenser that releases detergent at the right time. Reliable operation."),
        ("Dishwasher Door Switch", "Magnetic door switch that prevents operation when door is open. Safety feature."),
        ("Dishwasher Rack Roller", "Smooth rack roller that allows easy rack movement. Durable construction for long-lasting use."),
        ("Dishwasher Upper Spray Arm", "Upper spray arm that cleans upper rack dishes. Even water distribution for thorough cleaning."),
        ("Dishwasher Drain Pump", "Efficient drain pump that removes water after cycle. Prevents standing water and odors."),
        ("Dishwasher Control Board", "Advanced control board that manages dishwasher functions. Programmable settings for customized cleaning."),
        ("Dishwasher Door Spring", "Balanced door spring that assists with door operation. Prevents door from slamming."),
        ("Dishwasher Rinse Aid Dispenser", "Automatic rinse aid dispenser that improves drying. Reduces water spots on dishes."),
        ("Dishwasher Float Switch", "Float switch that monitors water level. Prevents overfilling and protects dishwasher."),
        ("Dishwasher Door Hinge", "Durable door hinge that ensures smooth door operation. Reinforced design."),
        ("Dishwasher Heater Relay", "Reliable heater relay that controls heating element. Protects against overheating."),
        ("Dishwasher Rack Guide", "Smooth rack guide that ensures proper rack alignment. Easy to install."),
        ("Dishwasher Water Level Switch", "Precise water level switch that monitors fill level. Essential for proper operation."),
        ("Dishwasher Door Latch Switch", "Safety latch switch that prevents operation when door is ajar. Protects users and prevents leaks."),
        ("Dishwasher Spray Nozzle", "Precision spray nozzle that directs water flow. Ensures thorough cleaning coverage."),
        ("Dishwasher Door Gasket Seal", "Flexible gasket seal that creates watertight closure. Prevents leaks and water damage."),
    ]
    
    products = []
    
    # Generate refrigerator products
    num_refrigerator = num_products // 2
    for i in range(num_refrigerator):
        title, description = random.choice(refrigerator_parts)
        part_number = f"PS{random.randint(10000000, 99999999)}"
        #product_url = f"https://www.partselect.com/{part_number}.htm"
        
        products.append({
            'category': 'refrigerator',
            'part_number': part_number,
            'title': title,
            'description': description
        })
    
    # Generate dishwasher products
    num_dishwasher = num_products - num_refrigerator
    for i in range(num_dishwasher):
        title, description = random.choice(dishwasher_parts)
        part_number = f"PS{random.randint(10000000, 99999999)}"
        
        products.append({
            'category': 'dishwasher',
            'part_number': part_number,
            'title': title,
            'description': description
        })
    
    # Shuffle products
    random.shuffle(products)
    
    return products


def save_to_csv(products, filename='partselect_products.csv'):
    """Save products to CSV file."""
    if not products:
        print("No products to save")
        return
    
    fieldnames = ['category', 'part_number', 'title', 'description']
    csv_path = os.path.join(os.path.dirname(__file__), filename)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
    
    print(f"✓ Saved {len(products)} products to {csv_path}")
    return csv_path


def main():
    """Main entry point."""
    print("=" * 60)
    print("PartSelect Sample Data Generator")
    print("=" * 60)
    print("\nGenerating sample product data for case study...")
    print("This creates realistic product data when scraping is not possible.")
    print("\nNote: This is sample data for demonstration purposes.")
    print("=" * 60)
    
    # Generate 50 products (25 refrigerator + 25 dishwasher)
    num_products = 50
    print(f"\nGenerating {num_products} products...")
    
    products = generate_sample_data(num_products)
    
    print(f"✓ Generated {len(products)} products")
    print(f"  - Refrigerator: {sum(1 for p in products if p['category'] == 'refrigerator')}")
    print(f"  - Dishwasher: {sum(1 for p in products if p['category'] == 'dishwasher')}")
    
    # Save to CSV
    csv_path = save_to_csv(products)
    
    print("\n" + "=" * 60)
    print("Sample data generation complete!")
    print("=" * 60)
    print(f"\nData saved to: {csv_path}")
    print("\nYou can now use this data for your AI assistant case study.")
    print("\nNote: This is sample data. In a real scenario, you would:")
    print("  1. Contact PartSelect for official data access")
    print("  2. Use their API if available")
    print("  3. Obtain permission for scraping if needed")


if __name__ == '__main__':
    main()

