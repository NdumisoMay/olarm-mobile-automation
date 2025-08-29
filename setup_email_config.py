#!/usr/bin/env python3
"""
Setup script for email configuration
"""

import os
import getpass
import re
from pathlib import Path

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def setup_email_config():
    """Interactive setup for email configuration"""
    print("=" * 60)
    print("📧 Email Configuration Setup")
    print("=" * 60)
    print("This will help you configure email settings for sending Allure reports.")
    print()
    
    # Get sender email
    while True:
        sender_email = input("Enter your Gmail address: ").strip()
        if validate_email(sender_email):
            break
        print("❌ Invalid email format. Please enter a valid Gmail address.")
    
    print("\n📝 Gmail App Password Setup:")
    print("1. Go to your Google Account settings")
    print("2. Navigate to Security > 2-Step Verification")
    print("3. Generate an App Password for 'Mail'")
    print("4. Use that 16-character password below")
    print()
    
    # Get app password
    while True:
        app_password = getpass.getpass("Enter your Gmail App Password: ").strip()
        if len(app_password) >= 16:
            break
        print("❌ App password should be at least 16 characters long.")
    
    # Get recipient email
    while True:
        recipient_email = input("Enter recipient email (default: ndumiso@olarm.com): ").strip()
        if not recipient_email:
            recipient_email = "ndumiso@olarm.com"
            break
        if validate_email(recipient_email):
            break
        print("❌ Invalid email format. Please enter a valid email address.")
    
    # Create configuration
    config_content = f'''"""
Email configuration for sending Allure test reports
"""

# Email Configuration
EMAIL_CONFIG = {{
    # Gmail SMTP Configuration
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'use_tls': True,
    
    # Sender Configuration
    'sender_email': '{sender_email}',
    'sender_password': '{app_password}',
    
    # Recipient Configuration
    'recipient_email': '{recipient_email}',
    
    # Email Settings
    'subject_prefix': 'Olarm Mobile App Upgrade Test Results',
    'send_on_success': True,
    'send_on_failure': True,
    'send_on_completion': True,
}}

# Alternative SMTP configurations
SMTP_CONFIGS = {{
    'gmail': {{
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'use_tls': True,
    }},
    'outlook': {{
        'smtp_server': 'smtp-mail.outlook.com',
        'smtp_port': 587,
        'use_tls': True,
    }},
    'yahoo': {{
        'smtp_server': 'smtp.mail.yahoo.com',
        'smtp_port': 587,
        'use_tls': True,
    }},
    'office365': {{
        'smtp_server': 'smtp.office365.com',
        'smtp_port': 587,
        'use_tls': True,
    }}
}}

def get_email_config():
    """
    Get email configuration with environment variable overrides
    
    Returns:
        dict: Email configuration
    """
    import os
    
    config = EMAIL_CONFIG.copy()
    
    # Override with environment variables if set
    if os.getenv('SENDER_EMAIL'):
        config['sender_email'] = os.getenv('SENDER_EMAIL')
    
    if os.getenv('SENDER_PASSWORD'):
        config['sender_password'] = os.getenv('SENDER_PASSWORD')
    
    if os.getenv('RECIPIENT_EMAIL'):
        config['recipient_email'] = os.getenv('RECIPIENT_EMAIL')
    
    return config

def validate_email_config(config):
    """
    Validate email configuration
    
    Args:
        config (dict): Email configuration
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ['smtp_server', 'smtp_port', 'sender_email', 'sender_password', 'recipient_email']
    
    for field in required_fields:
        if not config.get(field):
            return False, f"Missing required field: {{field}}"
    
    # Validate email format
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{{2,}}$'
    
    if not re.match(email_pattern, config['sender_email']):
        return False, f"Invalid sender email format: {{config['sender_email']}}"
    
    if not re.match(email_pattern, config['recipient_email']):
        return False, f"Invalid recipient email format: {{config['recipient_email']}}"
    
    return True, "Configuration is valid"
'''
    
    # Write configuration file
    config_file = Path("config/email_config.py")
    config_file.parent.mkdir(exist_ok=True)
    
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print("\n✅ Email configuration saved to config/email_config.py")
    print(f"📧 Sender: {sender_email}")
    print(f"📧 Recipient: {recipient_email}")
    
    # Test configuration
    print("\n🧪 Testing email configuration...")
    try:
        from config.email_config import get_email_config, validate_email_config
        from utils.email_sender import EmailSender
        
        config = get_email_config()
        is_valid, error_msg = validate_email_config(config)
        
        if is_valid:
            email_sender = EmailSender(config)
            if email_sender.test_connection():
                print("✅ Email configuration is valid and connection test successful!")
                print("📧 You can now run tests with automatic email reporting.")
            else:
                print("⚠️ Email connection test failed. Please check your credentials.")
        else:
            print(f"❌ Email configuration invalid: {error_msg}")
            
    except Exception as e:
        print(f"❌ Failed to test email configuration: {e}")
    
    print("\n📋 Next steps:")
    print("1. Run: python run_upgrade_tests_with_email.py")
    print("2. Tests will automatically send email reports to ndumiso@olarm.com")
    print("3. Check the logs for email status")

if __name__ == "__main__":
    setup_email_config()


