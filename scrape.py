import requests
from plyer import notification
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz

scheduler = BlockingScheduler()
tz = pytz.timezone('Asia/Kolkata')

# API request setup
headers = {
    'Authorization': 'Bearer e21be8f2-b7d3-48f2-a905-ff6aa126d20b',
    'Content-type': 'application/json'
}

# Function to fetch data from the API
def fetch_data():
    response = requests.get('https://api.brightdata.com/dca/dataset?id=j_m1l9z4rw2pbtssk32t', headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            return data
        else:
            print("Unexpected data format.")
            return None
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")
        return None

# Function to check prices and notify if under ₹32,000
def check_prices_and_notify():
    data = fetch_data()
    if data:
        for item in data:
            # Extracting the product title and final price
            product_name = item.get('title', 'Unnamed product')
            final_price = item.get('finalPrice', {}).get('value', None)
            currency = item.get('finalPrice', {}).get('currency', 'USD')

            # Display product and price
            if final_price is not None:
                print(f"Product: {product_name}, Price: {final_price} {currency}")
                
                # If the price is below a threshold, send notification (in USD or equivalent)
                if final_price < 32000:  # Adjust this value as per your needs
                    # Ensure title and message are within the 64 characters limit
                    notification_title = (f"Price Drop: {product_name}")[:64]
                    notification_message = (f"Now only {final_price} USD!")[:64]
        
                    notification.notify(
                        title=notification_title,
                        message=notification_message,
                        timeout=10  # Notification duration
                    )
            else:
                print(f"No price found for product: {product_name}")

# Add the job to run daily at 2:18 AM
scheduler.add_job(check_prices_and_notify, 'cron', hour=2, minute=23, timezone=tz)

# Start the scheduler
scheduler.start()
