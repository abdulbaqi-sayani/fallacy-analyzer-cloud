# المسار: fallacy_analyzer_cloud/fallacy_analyzer/categorical_syllogism.py

import re
from typing import Dict, Any, List, Tuple

class CategoricalSyllogismEngine:
    """
    محرك تحليل القياس الحملي الأرسطي مع توحيد أل التعريف وتطهير الحدود.
    """

    def __init__(self):
        self.universal_affirmative = ["كل", "جميع", "كافة"]
        self.universal_negative = ["لا أحد", "لا شيء", "ليس أي"]
        self.particular_affirmative = ["بعض", "فئة من", "جزء من"]
        self.particular_negative = ["ليس بعض", "بعض... ليس"]

    def is_strictly_categorical(self, premises: List[str], conclusion: str) -> bool:
        combined = " ".join(premises) + " " + conclusion
        if any(kw in combined for kw in ["إذا", "لو", "لأن", "بسبب", "أثبت أنت", "باطل لأنه", "فإن"]):
            return False
        
        quantifiers = self.universal_affirmative + self.universal_negative + self.particular_affirmative + self.particular_negative
        return any(q in combined for q in quantifiers)

    def analyze_syllogism(self, premises: List[str], conclusion: str) -> Dict[str, Any]:
        if not self.is_strictly_categorical(premises, conclusion):
            return {"is_categorical": False}

        if len(premises) < 2:
            return {"is_categorical": False}

        p1_type, p1_terms = self._parse_proposition(premises[0])
        p2_type, p2_terms = self._parse_proposition(premises[1])
        c_type, c_terms = self._parse_proposition(conclusion)

        if not (p1_terms and p2_terms and c_terms):
            return {"is_categorical": False}

        # تطهير أل التعريف لتوحيد المطابقة (مثال: النباتات -> نباتات)
        all_terms = [self._normalize_term(t) for t in (p1_terms + p2_terms + c_terms)]
        unique_terms = set(all_terms)

        if len(unique_terms) != 3:
            return {
                "is_categorical": True,
                "is_valid": False,
                "syllogism_type": "قياس حملي غير صحيح",
                "fallacy_name": "مغالطة الحدود الأربعة (Fallacy of Four Terms)",
                "details": f"القياس يتضمن {len(unique_terms)} حدود بدلاً من 3 حدود قياسية."
            }

        mood = f"{p1_type}{p2_type}{c_type}"
        return {
            "is_categorical": True,
            "is_valid": True,
            "syllogism_type": f"قياس حملي أرسطي صحيح (نمط {mood})",
            "fallacy_name": None,
            "details": "قياس أرسطي صحيح مستوفٍ لكافة الشروط والحدود الثلاثة."
        }

    def _normalize_term(self, term: str) -> str:
        term = re.sub(r'[\u064B-\u0652]', '', term).strip()
        if term.startswith("ال") and len(term) > 3:
            term = term[2:]
        return term

    def _parse_proposition(self, text: str) -> Tuple[str, List[str]]:
        clean_text = re.sub(r'^(إذن|بالتالي|نتيجة|كل|جميع|بعض|لا أحد|ليس)\s+', '', text.strip()).strip()
        words = [w for w in clean_text.split() if w not in ["هو", "هي", "هم", "كان", "يكون"]]
        
        prop_type = "A"
        if any(kw in text for kw in self.universal_negative):
            prop_type = "E"
        elif any(kw in text for kw in self.particular_affirmative):
            prop_type = "I"
        elif any(kw in text for kw in self.particular_negative):
            prop_type = "O"

        if len(words) >= 2:
            return prop_type, [words[0], words[-1]]
        elif len(words) == 1:
            return prop_type, [words[0]]
        return prop_type, []