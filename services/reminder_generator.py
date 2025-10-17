import asyncio
from enum import Enum
import httpx

from utils.time import TimeEnum

# token = "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"
models = [
    "google/gemma-3-27b-it:free",
    "google/gemma-3-12b-it:free",
    "google/gemma-3-4b-it:free",
    "meta-llama/llama-4-maverick:free",
]
tokens = [
    "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",
    "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",
]


async def generate_reminder(time_left: TimeEnum, student_name: str | None = None):
    i = 0
    model_index = 0
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        if time_left.value == TimeEnum.two_hour.value:
            style_hint = (
                "Можеш почати з привітання (наприклад, 'Привіт' чи 'Хей' чи щось), "
                "щоб створити дружню атмосферу."
            )
        elif time_left.value == TimeEnum.fifteen_minutes.value:
            style_hint = (
                "НЕ(!) привітайся та не використовуй код <code> взагалі. Зроби повідомлення більш динамічним і коротким, "
                "ніби нагадування від друга перед стартом."
            )
        while True:
            try:
                response = await client.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {tokens[i]}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": f"{models[model_index]}",
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "Ти креативний асистент, який створює веселі нагадування для дітей 🧒. "
                                    "Повертаєш лише текст у HTML стилі Telegram "
                                    "(<b>, <i>, <code>), без markdown і без пояснень. "
                                    "Пиши без орфографічних помилок, дружнім тоном і з емодзі."
                                ),
                            },
                            {
                                "role": "user",
                                "content": (
                                    f"{style_hint}"
                                    f"Створи коротке, веселе нагадування для дитини до 12 років "
                                    f"{f'на ім’я {student_name} ' if student_name else ''}"
                                    f"про те, що урок програмування на Python 🐍 почнеться через {time_left}. "
                                    "Текст має бути доброзичливим, з емодзі і одним жартівливим рядком Python-коду "
                                    "всередині тегу <code>. Не пиши про HTML або пояснення."
                                ),
                            },
                        ],
                    },
                )
                data = response.json()
                if response.status_code == 200:
                    text = data["choices"][0]["message"]["content"]
                    print(
                        f"✅ Нагадування ({time_left.value}):\n{text}\n",
                        "**",
                        i,
                        models[model_index],
                    )
                    return text
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    if i == len(tokens) - 1:
                        i = 0
                        model_index += 1
                    else:
                        i += 1
                elif e.response.status_code >= 400:
                    model_index += 1
                await asyncio.sleep(1)
            except (httpx.ReadTimeout, httpx.ConnectTimeout):
                await asyncio.sleep(5)
            if model_index == len(models) - 1 and i == len(tokens) - 1:
                break
        print("❌ Не вдалося отримати відповідь від OpenRouter.")
        return


async def main():
    # Нагадування за 2 години
    await generate_reminder(TimeEnum.fifteen_minutes, "Давид")


asyncio.run(main())
