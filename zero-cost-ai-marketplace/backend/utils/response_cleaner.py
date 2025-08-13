import re

class ResponseCleaner:
    def __init__(self) -> None:
        self.sympathy_patterns = [
            r"I understand.*?[.!]",
            r"I'm sorry.*?[.!]",
            r"I hope.*?[.!]",
            r"Please let me know.*?[.!]",
            r"Thank you.*?[.!]",
            r"I appreciate.*?[.!]",
            r"I'm happy.*?[.!]",
            r"I'd be glad.*?[.!]",
            r"Feel free.*?[.!]",
            r"Don't hesitate.*?[.!]",
        ]

    def clean_response(self, response: str) -> str:
        cleaned = response or ""
        for pattern in self.sympathy_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        if not cleaned:
            cleaned = "Completed."
        return cleaned
