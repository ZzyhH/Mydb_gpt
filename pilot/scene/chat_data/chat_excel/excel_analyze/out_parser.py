import json
import logging
from typing import Dict, NamedTuple, List
from pilot.out_parser.base import BaseOutputParser, T
from pilot.configs.config import Config

CFG = Config()


class ExcelAnalyzeResponse(NamedTuple):
    sql: str
    thoughts: str
    display: str


logger = logging.getLogger(__name__)


class ChatExcelOutputParser(BaseOutputParser):
    def __init__(self, sep: str, is_stream_out: bool):
        super().__init__(sep=sep, is_stream_out=is_stream_out)

    def parse_prompt_response(self, model_out_text):
        clean_str = super().parse_prompt_response(model_out_text)
        print("clean prompt response:", clean_str)
        try:
            response = json.loads(clean_str)
            for key in sorted(response):
                if key.strip() == "sql":
                    sql = response[key].replace("\\", " ")
                if key.strip() == "thoughts":
                    thoughts = response[key]
                if key.strip() == "display":
                    display = response[key]
            return ExcelAnalyzeResponse(sql, thoughts, display)
        except Exception as e:
            raise ValueError(f"LLM Response Can't Parser! \n")

    def parse_view_response(self, speak, data, prompt_response) -> str:
        ### tool out data to table view
        return data
