from quiz_module import clean_json_block


def test_clean_json_block():

    raw = """
```json
[
    {
        "question": "What is 2 + 2?",
        "options": [
            "3",
            "4",
            "5",
            "6"
        ],
        "answer": "4"
    }
]