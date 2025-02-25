import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import time
import os

CHANNEL_LINK = "https://t.me/REDX_64"

def print_credits():
    credit_banner = """
    ╔══════════════════════════════════════════════╗
    ║  🚀  𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐔𝐬𝐞𝐫 𝐈𝐧𝐟𝐨 𝐅𝐞𝐭𝐜𝐡𝐞𝐫  🚀  ║
    ╠══════════════════════════════════════════════╣
    ║  🔹  𝐂𝐫𝐞𝐚𝐭𝐞𝐝 𝐛𝐲:  @REDX_64                  ║
    ║  🔹  𝐒𝐮𝐩𝐩𝐨𝐫𝐭 𝐁𝐲:  @REDX_HACKIN             ║
    ║                                              ║
    ║  📢  𝐎𝐟𝐟𝐢𝐜𝐢𝐚𝐥 𝐂𝐡𝐚𝐧𝐧𝐞𝐥:                     ║
    ║  ➤  https://t.me/REDX_64                     ║
    ╚══════════════════════════════════════════════╝
    """
    print(credit_banner)

def format_user_data(data):
    """Format user data into a structured and readable format"""
    formatted_data = "\n📌 𝗨𝘀𝗲𝗿 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻:\n" + "═" * 40 + "\n"
    
    for key, value in data.items():
        key = key.replace("_", " ").title()  # Capitalize and replace underscores
        formatted_data += f"🔹 {key}: {value}\n"

    formatted_data += "═" * 40
    return formatted_data

def parse_html_response(html):
    """Extract user data from HTML response using BeautifulSoup"""
    soup = BeautifulSoup(html, 'html.parser')
    user_info = soup.find('div', class_='user-info')
    
    if not user_info:
        return {"⚠️ Error": "No user information found in HTML"}
    
    data = {}
    for p in user_info.find_all('p'):
        bold = p.find('span', class_='bold')
        if bold:
            key = bold.text.strip().rstrip(':').lower().replace(' ', '_')
            value = bold.next_sibling.strip()
            
            # Convert special values
            if key == 'active':
                value = "✅ Yes" if value.lower() == 'yes' else "❌ No"
            elif 'date' in key or 'message' in key:
                try:
                    value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S").isoformat()
                except ValueError:
                    pass
            
            # Convert numeric values to integers
            if key in ['total_messages', 'group_messages', 
                      'admin_in_groups', 'username_changes',
                      'name_changes', 'total_groups']:
                try:
                    value = int(value)
                except ValueError:
                    pass
            
            data[key] = value
    
    return data

def get_user_data(user_id):
    api_url = f"https://goabror.uz/api/v1.php?id={user_id}"
    
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        if 'text/html' in response.headers.get('Content-Type', ''):
            return parse_html_response(response.text)
        else:
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"⚠️ Error": "Non-JSON response", "📄 Raw Output": response.text}
    
    except requests.exceptions.RequestException as e:
        return {"⚠️ Error": str(e)}

if __name__ == "__main__":
    print_credits()
    
    user_id = input("🔹 Enter Telegram User ID: ").strip()
    
    if not user_id.isdigit():
        print("\n❌ Invalid User ID! Please enter numbers only.")
    else:
        result = get_user_data(user_id)
        print("\n" + "═" * 50)
        
        if '⚠️ Error' in result:
            print("❌ " + result["⚠️ Error"])
        else:
            print(format_user_data(result))

        print("═" * 50)
    
    
    time.sleep(2)
    choice = input("\n📢 Do you want to join our Telegram Channel? (Y/N): ").strip().lower()

    if choice == 'y':
        print(f"\n➡️ Opening {CHANNEL_LINK}...")
        os.system(f"am start -a android.intent.action.VIEW -d {CHANNEL_LINK}")
    else:
        print("\n❌ You chose not to join the channel. Have a great day! 🚀")