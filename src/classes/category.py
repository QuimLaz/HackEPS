from typing import Dict


class Category:

    def __init__(self, type: int, description: str, stress_level: int):
        self.type: int = type
        self.description: str = description
        self.stress_level: int = stress_level

    @staticmethod
    def from_json(category_map: Dict):
        return Category(category_map['type'], category_map['description'], category_map['stressLevel'])

    def to_json(self) -> Dict:
        return {
            'type': self.type,
            'description': self.description,
            'stressLevel': self.stress_level
        }
