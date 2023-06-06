# Copyright 2023 kazuh
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import json

JSON_LOG_FILE_NAME = 'logs.json'
TEXT_LOG_FILE_NAME = 'logs.txt'

# JSONフォーマットのログを出力するロガー
json_logger = logging.getLogger('json_logger')
json_handler = logging.FileHandler(JSON_LOG_FILE_NAME)
json_formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
json_handler.setFormatter(json_formatter)
json_logger.setLevel(logging.INFO)
json_logger.addHandler(json_handler)


# テキストフォーマットのログを出力するロガー
text_logger = logging.getLogger('text_logger')
text_handler = logging.FileHandler(TEXT_LOG_FILE_NAME)
text_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
text_handler.setFormatter(text_formatter)
text_logger.setLevel(logging.INFO)
text_logger.addHandler(text_handler)


# ログの内容を定義
log_message = 'Hello, world!'
log_data = {'app_name': 'MyAppName', 'version': '1.0'}

# ログを出力
def info(message):
    text_logger.info(log_message)

    # json_logger.info(json.dumps())

    # check if log file exists
    if os.path.isfile(JSON_LOG_FILE_NAME):
        with open(log_file, "r") as f:
            # read first character to check if log is JSON array
            first_char = f.read(1)
            if first_char == "[":
                # JSON array, read all content and parse
                f.seek(0)
                logs = json.load(f)
            else:
                # not a JSON array, create new array
                logs = []
    else:
        # log file doesn't exist, create new array
        logs = []


# 既存のログがある場合は、JSON配列として出力する
with open('logs.json', 'r+') as f:
    contents = f.read().strip()
    if contents.startswith('['):
        contents = contents[1:-1]
        f.seek(0)
        f.write(f'[{contents}, {json.dumps(log_data)}]')
    else:
        f.seek(0)
        f.write(f'[{json.dumps(log_data)}]')