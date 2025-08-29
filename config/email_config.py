"""
Email configuration for sending Allure test reports
"""

# Email Configuration
EMAIL_CONFIG = {
    # Gmail SMTP Configuration
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'use_tls': True,
    
    # Sender Configuration
    'sender_email': 'ndumiso@olarm.com',
    'sender_password': 'Thi$P@$$wordI$100%superunique3',
    
    # Recipient Configuration
    'recipient_email': 'ndumiso@olarm.com',
    
    # Email Settings
    'subject_prefix': 'Olarm Mobile App Upgrade Test Results',
    'send_on_success': True,
    'send_on_failure': True,
    'send_on_completion': True,
}

# Alternative SMTP configurations
SMTP_CONFIGS = {
    'gmail': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'use_tls': True,
    },
    'outlook': {
        'smtp_server': 'smtp-mail.outlook.com',
        'smtp_port': 587,
        'use_tls': True,
    },
    'yahoo': {
        'smtp_server': 'smtp.mail.yahoo.com',
        'smtp_port': 587,
        'use_tls': True,
    },
    'office365': {
        'smtp_server': 'smtp.office365.com',
        'smtp_port': 587,
        'use_tls': True,
    }
}

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
            return False, f"Missing required field: {field}"
    
    # Validate email format
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, config['sender_email']):
        return False, f"Invalid sender email format: {config['sender_email']}"
    
    if not re.match(email_pattern, config['recipient_email']):
        return False, f"Invalid recipient email format: {config['recipient_email']}"
    
    return True, "Configuration is valid"
