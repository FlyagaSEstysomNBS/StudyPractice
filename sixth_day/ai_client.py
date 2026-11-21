import json
import os
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIError, RateLimitError, APITimeoutError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from logger import logger

load_dotenv()


class TranslatorClient:
    def __init__(self):
        api_key = os.getenv("OLLAMA_API_KEY")
        base_url = os.getenv("OLLAMA_BASE_URL", "https://ollama.com")
        self.model = os.getenv("OLLAMA_MODEL", "deepseek-v4.1-flash")

        if not api_key:
            raise ValueError("Не задан OLLAMA_API_KEY в файле .env")

        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=30.0
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((APIError, RateLimitError, APITimeoutError, json.JSONDecodeError)),
        reraise=True
    )
    def translate_card(self, title: str, description: str, target_lang: str = "English") -> tuple[str, str]:
        """
        Переводит название и описание товара, возвращая кортеж (title_translated, description_translated)
        """
        system_prompt = (
            f"Ты профессиональный переводчик e-commerce карточек товаров на {target_lang}. "
            "Сохраняй коммерческий стиль, характеристики и форматирование. "
            "Верни ответ СТРОГО в формате JSON с двумя ключами: "
            '{"title": "перевод названия", "description": "перевод описания"}. '
            "Никакого лишнего текста или markdown-разметки."
        )

        user_content = json.dumps({"title": title, "description": description}, ensure_ascii=False)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.3
            )
            raw_text = response.choices[0].message.content.strip()
            if raw_text.startswith("```"):
                raw_text = raw_text.strip("`").removeprefix("json").strip()

            parsed = json.loads(raw_text)
            return parsed.get("title", ""), parsed.get("description", "")

        except AuthenticationError:
            logger.error("ОШИБКА авторизации: проверьте правильность OLLAMA_API_KEY!")
            raise