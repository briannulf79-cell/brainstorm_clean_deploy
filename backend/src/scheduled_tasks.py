#!/usr/bin/env python3
"""
Scheduled tasks for Brainstorm AI Kit
Run this script via cron job or scheduler to handle:
- Trial expiration notifications
- Data cleanup
- System maintenance

Usage:
python scheduled_tasks.py [task_name]

Available tasks:
- trial_notifications: Check and send trial expiration notifications
- cleanup: Clean up expired data
- all: Run all tasks

Example cron job (run daily at 9 AM):
0 9 * * * cd /path/to/backend && python src/scheduled_tasks.py trial_notifications
"""

import os
import sys
import logging
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from main import app
from services.notification_service import notification_service
from services.demo_service import demo_service
from models import db, User

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_trial_notifications():
    """Check and send trial expiration notifications"""
    logger.info("Starting trial notification check...")
    
    with app.app_context():
        try:
            notification_service.check_and_send_trial_notifications()
            logger.info("Trial notification check completed successfully")
            return True
        except Exception as e:
            logger.error(f"Error in trial notification check: {str(e)}")
            return False

def run_cleanup_tasks():
    """Run cleanup tasks"""
    logger.info("Starting cleanup tasks...")
    
    with app.app_context():
        try:
            # Clean up any orphaned data, expired sessions, etc.
            # Add your cleanup logic here
            
            logger.info("Cleanup tasks completed successfully")
            return True
        except Exception as e:
            logger.error(f"Error in cleanup tasks: {str(e)}")
            return False

def seed_demo_data():
    """Seed demo data if needed"""
    logger.info("Checking demo data...")
    
    with app.app_context():
        try:
            demo_service.seed_demo_data()
            logger.info("Demo data check completed")
            return True
        except Exception as e:
            logger.error(f"Error seeding demo data: {str(e)}")
            return False

def run_all_tasks():
    """Run all scheduled tasks"""
    logger.info("Running all scheduled tasks...")
    
    tasks = [
        ("Trial Notifications", run_trial_notifications),
        ("Demo Data Check", seed_demo_data),
        ("Cleanup Tasks", run_cleanup_tasks)
    ]
    
    results = []
    for task_name, task_func in tasks:
        logger.info(f"Running {task_name}...")
        try:
            result = task_func()
            results.append((task_name, result))
            logger.info(f"{task_name}: {'SUCCESS' if result else 'FAILED'}")
        except Exception as e:
            logger.error(f"{task_name}: ERROR - {str(e)}")
            results.append((task_name, False))
    
    # Log summary
    successful = sum(1 for _, success in results if success)
    total = len(results)
    logger.info(f"Task summary: {successful}/{total} tasks completed successfully")
    
    return successful == total

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        print("Usage: python scheduled_tasks.py [task_name]")
        print("Available tasks: trial_notifications, cleanup, demo_data, all")
        sys.exit(1)
    
    task = sys.argv[1].lower()
    
    # Set up logging to file for cron jobs
    log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'scheduled_tasks.log')
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    
    logger.info(f"Starting scheduled task: {task}")
    
    if task == 'trial_notifications':
        success = run_trial_notifications()
    elif task == 'cleanup':
        success = run_cleanup_tasks()
    elif task == 'demo_data':
        success = seed_demo_data()
    elif task == 'all':
        success = run_all_tasks()
    else:
        logger.error(f"Unknown task: {task}")
        print(f"Unknown task: {task}")
        sys.exit(1)
    
    if success:
        logger.info(f"Task '{task}' completed successfully")
        sys.exit(0)
    else:
        logger.error(f"Task '{task}' failed")
        sys.exit(1)

if __name__ == '__main__':
    main()