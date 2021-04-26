from apscheduler.schedulers.background import BackgroundScheduler

from config.settings import SCHEDULER_HOUR, SCHEDULER_MINUTE
from menu.utils import send_update_email


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_update_email, 'cron', minute=SCHEDULER_MINUTE, hour=SCHEDULER_HOUR, replace_existing=True)
    scheduler.start()
