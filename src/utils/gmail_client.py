"""
Gmail client for sending competitive analysis reports
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Any, Optional
from datetime import datetime, date
import json
from dotenv import load_dotenv

load_dotenv()

class GmailClient:
    """Handles email notifications and reports via Gmail SMTP"""
    
    def __init__(self):
        self.gmail_user = os.getenv("GMAIL_USER")
        self.gmail_password = os.getenv("GMAIL_PASSWORD")
        self.notification_recipients = os.getenv("NOTIFICATION_RECIPIENTS", "").split(",")
        
        if not all([self.gmail_user, self.gmail_password]):
            print("Warning: Gmail credentials not configured. Email notifications will be disabled.")
            self.enabled = False
        else:
            self.enabled = True
            
        if not self.notification_recipients or self.notification_recipients == [""]:
            print("Warning: No notification recipients configured.")
            self.notification_recipients = []
        
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_daily_report(self, report_data: Dict[str, Any]) -> bool:
        """Send daily competitive analysis report"""
        if not self.enabled or not self.notification_recipients:
            print("Email notifications disabled or no recipients configured")
            return False
            
        try:
            subject = f"Daily AI Market Intelligence Report - {date.today().strftime('%B %d, %Y')}"
            html_content = self._generate_daily_report_html(report_data)
            
            success_count = 0
            for recipient in self.notification_recipients:
                if recipient.strip():
                    if self._send_email(
                        to_email=recipient.strip(),
                        subject=subject,
                        html_content=html_content,
                        email_type="daily_report"
                    ):
                        success_count += 1
            
            return success_count > 0
        except Exception as e:
            print(f"Error sending daily report: {e}")
            return False
    
    def send_critical_alert(self, alert_data: Dict[str, Any]) -> bool:
        """Send critical alert for urgent competitive intelligence"""
        if not self.enabled or not self.notification_recipients:
            print("Email notifications disabled or no recipients configured")
            return False
            
        try:
            subject = f"🚨 CRITICAL ALERT: {alert_data.get('title', 'Competitive Intelligence Update')}"
            html_content = self._generate_alert_html(alert_data)
            
            success_count = 0
            for recipient in self.notification_recipients:
                if recipient.strip():
                    if self._send_email(
                        to_email=recipient.strip(),
                        subject=subject,
                        html_content=html_content,
                        email_type="critical_alert"
                    ):
                        success_count += 1
            
            return success_count > 0
        except Exception as e:
            print(f"Error sending critical alert: {e}")
            return False
    
    def send_weekly_summary(self, summary_data: Dict[str, Any]) -> bool:
        """Send weekly comprehensive summary"""
        if not self.enabled or not self.notification_recipients:
            print("Email notifications disabled or no recipients configured")
            return False
            
        try:
            subject = f"Weekly AI Market Intelligence Summary - Week of {date.today().strftime('%B %d, %Y')}"
            html_content = self._generate_weekly_summary_html(summary_data)
            
            success_count = 0
            for recipient in self.notification_recipients:
                if recipient.strip():
                    if self._send_email(
                        to_email=recipient.strip(),
                        subject=subject,
                        html_content=html_content,
                        email_type="weekly_summary"
                    ):
                        success_count += 1
            
            return success_count > 0
        except Exception as e:
            print(f"Error sending weekly summary: {e}")
            return False
    
    def _send_email(self, to_email: str, subject: str, html_content: str, email_type: str) -> bool:
        """Send email using Gmail SMTP"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.gmail_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Connect to Gmail SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable TLS encryption
            server.login(self.gmail_user, self.gmail_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.gmail_user, to_email, text)
            server.quit()
            
            print(f"Successfully sent {email_type} email to {to_email}")
            return True
            
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def _generate_daily_report_html(self, report_data: Dict[str, Any]) -> str:
        """Generate HTML content for daily report"""
        company_name = os.getenv("COMPANY_NAME", "Your Company")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Daily AI Market Intelligence Report</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 28px; font-weight: 300; }}
                .header p {{ margin: 10px 0 0; opacity: 0.9; font-size: 16px; }}
                .content {{ padding: 30px; }}
                .section {{ margin-bottom: 30px; }}
                .section-title {{ color: #667eea; font-size: 20px; font-weight: 600; margin-bottom: 15px; border-bottom: 2px solid #e1e5fe; padding-bottom: 8px; }}
                .summary-box {{ background: #f8f9ff; border-left: 4px solid #667eea; padding: 20px; border-radius: 0 8px 8px 0; margin-bottom: 20px; }}
                .insight-item {{ background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
                .insight-title {{ font-weight: 600; color: #333; margin-bottom: 8px; }}
                .insight-meta {{ font-size: 12px; color: #666; margin-bottom: 10px; }}
                .score-badge {{ display: inline-block; padding: 4px 12px; border-radius: 15px; font-size: 12px; font-weight: 600; }}
                .score-high {{ background: #e8f5e8; color: #2e7d32; }}
                .score-medium {{ background: #fff3e0; color: #f57c00; }}
                .score-low {{ background: #ffebee; color: #c62828; }}
                .metrics {{ display: flex; justify-content: space-around; background: #f8f9ff; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .metric {{ text-align: center; }}
                .metric-value {{ font-size: 24px; font-weight: 700; color: #667eea; }}
                .metric-label {{ font-size: 12px; color: #666; text-transform: uppercase; }}
                .footer {{ background: #f5f5f5; padding: 20px; text-align: center; color: #666; font-size: 14px; }}
                .cta-button {{ display: inline-block; background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 10px 0; }}
                .alert {{ background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 6px; padding: 15px; margin: 15px 0; }}
                .alert-critical {{ background: #f8d7da; border-color: #f5c6cb; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Daily AI Market Intelligence</h1>
                    <p>{company_name} • {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
                
                <div class="content">
                    <div class="summary-box">
                        <h3 style="margin-top: 0; color: #667eea;">Executive Summary</h3>
                        <p>{report_data.get('executive_summary', 'No executive summary available')}</p>
                    </div>
                    
                    <div class="metrics">
                        <div class="metric">
                            <div class="metric-value">{report_data.get('findings_count', 0)}</div>
                            <div class="metric-label">Market Findings</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{report_data.get('opportunities_count', 0)}</div>
                            <div class="metric-label">New Opportunities</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{report_data.get('competitor_updates', 0)}</div>
                            <div class="metric-label">Competitor Updates</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{report_data.get('trends_identified', 0)}</div>
                            <div class="metric-label">Trends Identified</div>
                        </div>
                    </div>
        """
        
        # Add critical alerts if any
        if report_data.get('critical_alerts'):
            html += """
                    <div class="section">
                        <div class="section-title">🚨 Critical Alerts</div>
            """
            for alert in report_data['critical_alerts']:
                html += f"""
                        <div class="alert alert-critical">
                            <strong>{alert.get('title', 'Critical Update')}</strong><br>
                            {alert.get('description', 'No description available')}
                        </div>
                """
            html += "</div>"
        
        # Add top opportunities
        if report_data.get('top_opportunities'):
            html += """
                    <div class="section">
                        <div class="section-title">🎯 Top Opportunities</div>
            """
            for opp in report_data['top_opportunities'][:3]:
                score_class = "score-high" if opp.get('score', 0) > 0.7 else "score-medium" if opp.get('score', 0) > 0.4 else "score-low"
                html += f"""
                        <div class="insight-item">
                            <div class="insight-title">{opp.get('title', 'Untitled Opportunity')}</div>
                            <div class="insight-meta">
                                <span class="score-badge {score_class}">Score: {opp.get('score', 0):.2f}</span>
                                Priority: {opp.get('priority', 'medium').title()}
                            </div>
                            <p>{opp.get('description', 'No description available')}</p>
                        </div>
                """
            html += "</div>"
        
        # Add key insights
        if report_data.get('key_insights'):
            html += """
                    <div class="section">
                        <div class="section-title">💡 Key Insights</div>
                        <ul>
            """
            for insight in report_data['key_insights']:
                html += f"<li>{insight}</li>"
            html += "</ul></div>"
        
        # Add strategic recommendations
        if report_data.get('recommendations'):
            html += """
                    <div class="section">
                        <div class="section-title">📋 Strategic Recommendations</div>
                        <ol>
            """
            for rec in report_data['recommendations']:
                html += f"<li>{rec}</li>"
            html += "</ol></div>"
        
        # Close HTML
        html += f"""
                    <div class="section">
                        <a href="http://localhost:8501" class="cta-button">View Full Dashboard</a>
                    </div>
                </div>
                
                <div class="footer">
                    <p>Generated by {company_name} Competitive Analysis AI Agent</p>
                    <p>This report contains confidential business intelligence. Please handle accordingly.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _generate_alert_html(self, alert_data: Dict[str, Any]) -> str:
        """Generate HTML content for critical alerts"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 20px; }}
                .alert-container {{ max-width: 600px; margin: 0 auto; background: #fff; border: 2px solid #dc3545; border-radius: 8px; }}
                .alert-header {{ background: #dc3545; color: white; padding: 20px; text-align: center; }}
                .alert-content {{ padding: 30px; }}
                .urgency-high {{ background: #f8d7da; border-left: 4px solid #dc3545; padding: 15px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="alert-container">
                <div class="alert-header">
                    <h1>🚨 CRITICAL ALERT</h1>
                    <p>{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
                <div class="alert-content">
                    <h2>{alert_data.get('title', 'Critical Update')}</h2>
                    <div class="urgency-high">
                        <strong>Impact Level:</strong> {alert_data.get('impact_level', 'High')}<br>
                        <strong>Source:</strong> {alert_data.get('source', 'Competitive Intelligence System')}
                    </div>
                    <p>{alert_data.get('description', 'No description provided')}</p>
                    
                    {f"<p><strong>Recommended Action:</strong> {alert_data['recommended_action']}</p>" if alert_data.get('recommended_action') else ""}
                    
                    <p style="margin-top: 30px; font-size: 14px; color: #666;">
                        This is an automated alert from your competitive analysis system. 
                        Please review and take appropriate action.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def _generate_weekly_summary_html(self, summary_data: Dict[str, Any]) -> str:
        """Generate HTML content for weekly summary"""
        # This would be a comprehensive weekly report
        # For now, using a similar structure to daily report but with weekly data
        return self._generate_daily_report_html(summary_data)

# Create global Gmail client instance
gmail_client = GmailClient()