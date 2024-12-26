import logging
from common.middleware_logs_custom import get_current_user


class UserIDFilter(logging.Filter):
  def filter(self, record):
    user = get_current_user()
    record.user_id = getattr(user, 'id', 'anonymous') if user and user.is_authenticated else 'anonymous'
    return True
