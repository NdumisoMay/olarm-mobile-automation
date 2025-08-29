import smtplib
import os
import zipfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import logging

class EmailSender:
    """Email utility for sending Allure test reports"""
    
    def __init__(self, config=None):
        """
        Initialize email sender with configuration
        
        Args:
            config (dict): Email configuration dictionary
        """
        self.config = config or self._get_default_config()
        self.logger = logging.getLogger(__name__)
    
    def _get_default_config(self):
        """Get default email configuration"""
        return {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': os.getenv('SENDER_EMAIL', 'your-email@gmail.com'),
            'sender_password': os.getenv('SENDER_PASSWORD', 'your-app-password'),
            'recipient_email': 'ndumiso@olarm.com',
            'use_tls': True
        }
    
    def send_allure_report(self, allure_results_dir, allure_report_dir, test_summary=None):
        """
        Send Allure report via email
        
        Args:
            allure_results_dir (str): Path to allure-results directory
            allure_report_dir (str): Path to allure-report directory
            test_summary (dict): Test execution summary
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create ZIP file of the report
            zip_path = self._create_report_zip(allure_report_dir)
            
            # Prepare email content
            subject = self._generate_subject(test_summary)
            body = self._generate_email_body(test_summary)
            
            # Send email
            success = self._send_email(subject, body, zip_path)
            
            # Clean up ZIP file
            if os.path.exists(zip_path):
                os.remove(zip_path)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to send Allure report: {e}")
            return False
    
    def _create_report_zip(self, report_dir):
        """Create ZIP file of the Allure report"""
        zip_path = f"{report_dir}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(report_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, report_dir)
                    zipf.write(file_path, arcname)
        
        self.logger.info(f"Created ZIP file: {zip_path}")
        return zip_path
    
    def _generate_subject(self, test_summary):
        """Generate email subject"""
        date_str = datetime.now().strftime("%B %d, %Y")
        if test_summary:
            passed = test_summary.get('passed', 0)
            failed = test_summary.get('failed', 0)
            skipped = test_summary.get('skipped', 0)
            return f"Olarm Mobile App Upgrade Test Results - {date_str} ({passed} passed, {failed} failed, {skipped} skipped)"
        return f"Olarm Mobile App Upgrade Test Results - {date_str}"
    
    def _generate_email_body(self, test_summary):
        """Generate email body content"""
        date_str = datetime.now().strftime("%B %d, %Y at %H:%M")
        
        body = f"""
Hi Ndumiso,

Please find attached the comprehensive upgrade test results for the Olarm mobile app.

📊 Test Summary ({date_str}):
"""
        
        if test_summary:
            body += f"""
✅ {test_summary.get('passed', 0)} tests PASSED
❌ {test_summary.get('failed', 0)} tests FAILED
⏭️ {test_summary.get('skipped', 0)} tests SKIPPED
⏱️ Total Execution Time: {test_summary.get('duration', 'N/A')}
"""
        else:
            body += """
✅ Tests completed successfully
⏱️ Execution completed
"""
        
        body += """
🔄 Test Coverage:
• In-place upgrades: 2.0.5, 2.0.6, 2.0.7, 2.0.8 → 2.0.9 (app-release.apk)
• Clean installations: All versions tested
• Performance metrics: Installation, launch, and upgrade timing
• Error handling: Invalid APK paths and non-existent packages

📋 To view the report:
1. Extract the ZIP file
2. Open index.html in any web browser
3. Navigate through the detailed test results, screenshots, and performance metrics

📈 Report includes:
- Step-by-step test execution logs
- Before/after upgrade screenshots
- Performance timing data
- Error handling validation
- Test execution trends

Best regards,
Olarm Mobile Automation Team
"""
        
        return body
    
    def _send_email(self, subject, body, attachment_path):
        """Send email with attachment"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.config['sender_email']
            msg['To'] = self.config['recipient_email']
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachment
            if os.path.exists(attachment_path):
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'zip')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            
            if self.config.get('use_tls', True):
                server.starttls()
            
            server.login(self.config['sender_email'], self.config['sender_password'])
            text = msg.as_string()
            server.sendmail(self.config['sender_email'], self.config['recipient_email'], text)
            server.quit()
            
            self.logger.info(f"Email sent successfully to {self.config['recipient_email']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False
    
    def update_config(self, **kwargs):
        """Update email configuration"""
        self.config.update(kwargs)
    
    def test_connection(self):
        """Test email connection"""
        try:
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            
            if self.config.get('use_tls', True):
                server.starttls()
            
            server.login(self.config['sender_email'], self.config['sender_password'])
            server.quit()
            
            self.logger.info("Email connection test successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Email connection test failed: {e}")
            return False


