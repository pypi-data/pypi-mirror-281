import redis
import datetime
import traceback
import requests


class LogsWeasel:

    def __init__(self, settings):
        self.SETTINGS = settings

    def redis_init(self):
        if self.SETTINGS['redis_connection'] is None:
            return None
        try:
            r = redis.Redis(host=self.SETTINGS['redis_connection']['host'], port=self.SETTINGS['redis_connection']['port'],
                            username=self.SETTINGS['redis_connection']['username'],
                            password=self.SETTINGS['redis_connection']['password'], ssl=False,
                            ssl_cert_reqs=None, db=self.SETTINGS['redis_connection']['db'],
                            decode_responses=True, socket_connect_timeout=2)
        except Exception:
            traceback.print_exc()
            return False
        return r

    def generate_week(self):
        weekday = datetime.date.today().weekday()
        end_timedelta = 6 - weekday
        start_weekday = datetime.date.today() - datetime.timedelta(days=weekday)
        end_weekday = datetime.date.today() + datetime.timedelta(days=end_timedelta)
        week_str = f'{start_weekday.strftime("%Y-%m-%d")}_{end_weekday.strftime("%Y-%m-%d")}'
        return week_str

    def add_log_to_redis(self, message, postfix):
        if self.SETTINGS['redis_connection'] is None:
            return
        else:
            try:
                r = self.redis_init()
                if r is False or r is None:
                    return
                else:
                    if self.SETTINGS['redis_files']['frequency'] == 'day':
                        r.append(self.SETTINGS['redis_files']['prefix_file'] + str(datetime.date.today()) + postfix, f'\n{message}')
                    elif self.SETTINGS['redis_files']['frequency'] == 'month':
                        r.append(self.SETTINGS['redis_files']['prefix_file'] + datetime.date.today().strftime('%Y-%m') + postfix, f'\n{message}')
                    elif self.SETTINGS['redis_files']['frequency'] == 'week':
                        r.append(self.SETTINGS['redis_files']['prefix_file'] + self.generate_week() + postfix, f'\n{message}')
                    else:
                        raise Exception('Bad SETTINGS["redis_files"]["frequency"]')
            except Exception:
                traceback.print_exc()

    def send_message(self, message):
        if self.SETTINGS['telegram_token'] is None:
            return
        else:
            url = f"https://api.telegram.org/bot{self.SETTINGS['telegram_token']}/sendMessage"
            for user_id in self.SETTINGS['users_list']:
                try:
                    payload = {
                        'chat_id': user_id,
                        'text': message
                    }
                    response = requests.post(url, data=payload)
                    if response.status_code != 200:
                        print(f"Failed to send message to {user_id}: {response.text}")
                except Exception:
                    traceback.print_exc()

    def info(self, message, postfix='', send=False):
        message_full = f'INFO || {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || {message}'
        print('\033[92m' + message_full + '\033[0m')
        self.add_log_to_redis(message_full, postfix)
        if send:
            message_full = f'✅ INFO\n_ _ _ _ _\n{message}'
            self.send_message(message_full)

    def info_start(self, message, postfix='', send=False):
        message_full = f'INFO || START || {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || {message}'
        print('\033[92m' + message_full + '\033[0m')
        self.add_log_to_redis(message_full, postfix)
        if send:
            message_full = f'✅ INFO\nSTART\n_ _ _ _ _\n{message}'
            self.send_message(message_full)

    def info_done(self, message, postfix='', send=False):
        message_full = f'INFO || DONE || {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || {message}'
        print('\033[92m' + message_full + '\033[0m')
        self.add_log_to_redis(message_full, postfix)
        if send:
            message_full = f'✅ INFO\nDONE\n_ _ _ _ _\n{message}'
            self.send_message(message_full)

    def info_not_done(self, message, postfix='', send=False):
        message_full = f'INFO || NOT DONE || {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || {message}'
        print('\033[92m' + message_full + '\033[0m')
        self.add_log_to_redis(message_full, postfix)
        if send:
            message_full = f'✅ INFO\nNOT DONE\n_ _ _ _ _\n{message}'
            self.send_message(message_full)

    def warning(self, message, postfix='', send=False, exc=False):
        if exc:
            traceback_row = f'\n{traceback.format_exc()}'
        else:
            traceback_row = ''
        message_full = f'WARNING || {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || {message}{traceback_row}'
        print('\033[93m' + message_full + '\033[0m')
        self.add_log_to_redis(message_full, postfix)
        if send:
            message_full = f'⚠️ WARNING\n_ _ _ _ _\n{message}'
            self.send_message(message_full)

    def warning_not_done(self, message, postfix='', send=False, exc=False):
        if exc:
            traceback_row = f'\n{traceback.format_exc()}'
        else:
            traceback_row = ''
        message_full = f'WARNING || NOT DONE || {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || {message}{traceback_row}'
        print('\033[93m' + message_full + '\033[0m')
        self.add_log_to_redis(message_full, postfix)
        if send:
            message_full = f'⚠️ WARNING\nNOT DONE\n_ _ _ _ _\n{message}'
            self.send_message(message_full)

    def warning_error(self, message, postfix='', send=False, exc=False):
        if exc:
            traceback_row = f'\n{traceback.format_exc()}'
        else:
            traceback_row = ''
        message_full = f'WARNING || DONE WITH ERROR || {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || {message}{traceback_row}'
        print('\033[93m' + message_full + '\033[0m')
        self.add_log_to_redis(message_full, postfix)
        if send:
            message_full = f'⚠️ WARNING\nDONE WITH ERROR\n_ _ _ _ _\n{message}'
            self.send_message(message_full)

    def critical(self, message, postfix='', send=False, exc=True):
        if exc:
            traceback_row = f'\n{traceback.format_exc()}'
        else:
            traceback_row = ''
        message_full = f'CRITICAL ERROR! || {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || {message}{traceback_row}'
        print('\033[91m' + message_full + '\033[0m')
        self.add_log_to_redis(message_full, postfix)
        if send:
            message_full = f'‼️ CRITICAL ERROR!\n_ _ _ _ _\n{message}'
            self.send_message(message_full)

    def critical_fatal(self, message, postfix='', send=False, exc=True):
        if exc:
            traceback_row = f'\n{traceback.format_exc()}'
        else:
            traceback_row = ''
        message_full = f'FATAL ERROR!!! || {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || {message}{traceback_row}'
        print('\033[91m' + message_full + '\033[0m')
        self.add_log_to_redis(message_full, postfix)
        if send:
            message_full = f'‼️ FATAL ERROR!!!\n_ _ _ _ _\n{message}'
            self.send_message(message_full)
