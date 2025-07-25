"""
Logging configuration for competitive analysis system
"""
import logging
import os
from datetime import datetime
from typing import Optional

class CompetitiveAnalysisLogger:
    """Centralized logging for the competitive analysis system"""
    
    def __init__(self, name: str = "competitive_analysis", log_level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        
        if not self.logger.handlers:
            self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        self.logger.setLevel(self.log_level)
        
        # Create logs directory if it doesn't exist
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # File handler with rotation
        log_file = os.path.join(log_dir, f"competitive_analysis_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(self.log_level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, extra: Optional[dict] = None):
        """Log info message"""
        self.logger.info(message, extra=extra)
    
    def warning(self, message: str, extra: Optional[dict] = None):
        """Log warning message"""
        self.logger.warning(message, extra=extra)
    
    def error(self, message: str, extra: Optional[dict] = None):
        """Log error message"""
        self.logger.error(message, extra=extra)
    
    def debug(self, message: str, extra: Optional[dict] = None):
        """Log debug message"""
        self.logger.debug(message, extra=extra)
    
    def critical(self, message: str, extra: Optional[dict] = None):
        """Log critical message"""
        self.logger.critical(message, extra=extra)
    
    def log_analysis_start(self, analysis_type: str):
        """Log analysis start"""
        self.info(f"🚀 Starting {analysis_type} analysis", extra={"analysis_type": analysis_type})
    
    def log_analysis_complete(self, analysis_type: str, duration: float, results: dict):
        """Log analysis completion"""
        self.info(
            f"✅ {analysis_type} analysis completed in {duration:.2f}s", 
            extra={
                "analysis_type": analysis_type,
                "duration": duration,
                "results_summary": {
                    "findings": results.get("findings_count", 0),
                    "opportunities": results.get("opportunities_count", 0),
                    "trends": results.get("trends_identified", 0)
                }
            }
        )
    
    def log_analysis_error(self, analysis_type: str, error: str):
        """Log analysis error"""
        self.error(
            f"❌ {analysis_type} analysis failed: {error}",
            extra={"analysis_type": analysis_type, "error": error}
        )
    
    def log_database_operation(self, operation: str, table: str, success: bool, error: Optional[str] = None):
        """Log database operations"""
        if success:
            self.debug(f"Database {operation} on {table} successful")
        else:
            self.error(f"Database {operation} on {table} failed: {error}")
    
    def log_api_call(self, api_name: str, endpoint: str, success: bool, duration: float):
        """Log API calls"""
        if success:
            self.debug(f"API call to {api_name}:{endpoint} successful ({duration:.2f}s)")
        else:
            self.warning(f"API call to {api_name}:{endpoint} failed ({duration:.2f}s)")
    
    def log_email_notification(self, email_type: str, recipients: int, success: bool):
        """Log email notifications"""
        if success:
            self.info(f"📧 {email_type} email sent to {recipients} recipients")
        else:
            self.warning(f"📧 Failed to send {email_type} email to {recipients} recipients")

# Global logger instance
logger = CompetitiveAnalysisLogger(
    log_level=os.getenv("LOG_LEVEL", "INFO")
)

# Convenience functions
def log_info(message: str, extra: Optional[dict] = None):
    logger.info(message, extra)

def log_warning(message: str, extra: Optional[dict] = None):
    logger.warning(message, extra)

def log_error(message: str, extra: Optional[dict] = None):
    logger.error(message, extra)

def log_debug(message: str, extra: Optional[dict] = None):
    logger.debug(message, extra)

def log_critical(message: str, extra: Optional[dict] = None):
    logger.critical(message, extra)