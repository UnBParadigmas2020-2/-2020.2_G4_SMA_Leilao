from datetime import datetime, timezone
from pade.misc.utility import display_message
import os
import re 

class Logger:
    def __init__(self):
        now_str = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H:%M:%S')
        actual_path = os.path.dirname(os.path.abspath(__file__))

        self.log_file_name = f'{actual_path}/../logs/leilao_{now_str}.txt'
        self.log_file = open(self.log_file_name, 'w')

    def log(self,sender, text, line_break=True, log_time=True):
        time_str = ''
        if log_time is True:
            time_str = '[' + datetime.now(timezone.utc).strftime('%H:%M:%S.%f')[0:-4] + ']'

        if re.search(' ̂\n', text) is not None:
            formatted_text = re.sub(' ̂\n', '', text)
            time_str = '\n' + time_str
        else:
            formatted_text = text

        self.log_file.write(f'{time_str} {sender}: {formatted_text}')
        display_message(sender, text)
        if line_break is True:
            self.log_file.write('\n')

    def close_file(self):
        self.log_file.close()