import json
import logging
import os
import sys

import openai

# OpenAI APIキーの設定
openai.api_key = os.environ.get("OPEN_AI_API_KEY")

BASIC_LOG_FILE_NAME = "chat_utf8.log"
JSON_LOG_FILE_NAME1 = "log.json"
JSON_LOG_FILE_NAME2 = "logs.json"
TEXT_LOG_FILE_NAME = "logs.txt"
EXTRA_LOG_FILE_NAME = "example.log"


# JSONフォーマットのログを出力するロガー
# json_logger = logging.getLogger('json_logger')
# json_handler = logging.FileHandler(JSON_LOG_FILE_NAME2)
# json_formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
# json_handler.setFormatter(json_formatter)
# json_logger.setLevel(logging.INFO)
# json_logger.addHandler(json_handler)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
            "logger": record.name,
        }
        # extra_data = log_data
        return json.dumps(log_data)
        # return log_data


class JsonArrayFormatter(logging.Formatter):
    def format(self, record):
        log = {}
        log["level"] = record.levelname
        log["time"] = self.formatTime(record, self.datefmt)
        log["message"] = record.getMessage()
        return json.dumps(log)


class JsonArrayLogger:
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        # self.handler = logging.StreamHandler()
        self.handler = logging.FileHandler(JSON_LOG_FILE_NAME2, encoding="utf-8")
        self.formatter = JsonFormatter()
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.logs = []

    def log(self, level, message):
        record = logging.LogRecord(
            "",
            level,
            "",
            0,
            message,
            None,
            None,
        )
        log = json.loads(self.formatter.format(record))
        self.logs.append(log)


def get_logs(log_file):
    # check if log file exists
    if os.path.isfile(log_file):
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
    return logs


# ログファイルの設定
logging.basicConfig(
    filename=BASIC_LOG_FILE_NAME,
    encoding="utf-8",
    level=logging.INFO,  # format="%(asctime)s - %(message)s"
)
# テキストフォーマットのログを出力するロガー
text_logger = logging.getLogger("text_logger")
text_handler = logging.FileHandler(TEXT_LOG_FILE_NAME, encoding="utf-8")
text_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
text_handler.setFormatter(text_formatter)
text_logger.setLevel(logging.INFO)
text_logger.addHandler(text_handler)

basic_logger = logging.getLogger("basic_logger")
json_logger = JsonArrayLogger("json_logger")
logs = get_logs(JSON_LOG_FILE_NAME1)


# 対話の入力と出力を記録する関数
def log_chat(input_message, output_message):
    # logger.info(f"Input: {input_message}")
    text_logger.info(f"Input: {input_message}")
    text_logger.info(f"Output: {output_message}")
    json_logger.log(logging.INFO, f"Input: {input_message}")
    json_logger.log(logging.INFO, f"Output: {output_message}")
    json_logger.logger.info(json_logger.logs)
    # ログをファイルに書き込む
    with open(JSON_LOG_FILE_NAME1, "w") as f:
        json.dump(logs + json_logger.logs, f)


# ChatGPTにリクエストを送信する関数
def call_chatgpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


# ユーザー入力とChatGPTの応答
def get_response(input_message):
    # ChatGPTにリクエストを送信して応答を取得する処理を実装
    response = call_chatgpt(input_message)

    # 対話の入力と出力をログファイルに記録
    log_chat(input_message, response)
    return response

def init_log(log_file_name):

    if len(basic_logger.handlers):
        handler = basic_logger.handlers[0]
    else:
        handler = logging.FileHandler(log_file_name, encoding="utf-8")
    # # handler = logging.StreamHandler()
    # formatter = JsonFormatter()
    # handler.setFormatter(formatter)
    basic_logger.addHandler(handler)

if __name__ == "__main__":
    # 対話の例
    init_log(EXTRA_LOG_FILE_NAME)

    # user_input = input("ユーザー: ")
    print(f"sys.argc: {len(sys.argv)}")
    print(f"sys.argv[1]: {sys.argv[1]}")
    user_input = sys.argv[1]
    response = get_response(user_input)
    print("ChatGPT:", response)
