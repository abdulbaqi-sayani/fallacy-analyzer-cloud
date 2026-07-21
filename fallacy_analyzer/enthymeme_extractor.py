# المسار: fallacy_analyzer/fallacy_analyzer/enthymeme_extractor.py

from typing import List, Tuple, Optional

class EnthymemeExtractor:
    """
    محرك استكمال المقدمات المضمرة (Enthymeme Extractor).
    يعمل على تحليل الفجوات الاستدلالية بين المقدمات الصريحة والنتيجة،
    واستخراج الفرضيات الخفية لإكمال البناء المنطقي قبل تقييمه.
    """

    def __init__(self):
        # قواعد استخراج المقدمات المضمرة الشائعة في الخطاب العادي
        self.implicit_value_rules = [
            ("ينبغي", "المقدمة المضمرة: كل ما يحقق المنفعة العامة أو يمنع الضرر هو مطلب محمود."),
            ("ممنوع", "المقدمة المضمرة: كل سلوك يخالف الضوابط المعتمدة يُعد غير مشروع."),
            ("خطير", "المقدمة المضمرة: كل أمر يترتب عليه تهديد للحياة أو الاستقرار يجب تجنبه.")
        ]

    def reconstruct_argument(self, premises: List[str], conclusion: str) -> Tuple[List[str], List[str]]:
        """
        إعادة بناء الحجة واستخراج المقدمات المضمرة إن وجدت.

        :param premises: قائمة المقدمات الصريحة.
        :param conclusion: النتيجة المعلنة.
        :return: (قائمة المقدمات الكلية المكتملة، قائمة المقدمات المضمرة المكتشفة)
        """
        implicit_premises = []
        full_premises = list(premises)

        # 1. التحليل الدلالي للقيم والنتائج المضمرة
        for word, rule in self.implicit_value_rules:
            if word in conclusion and not any(word in p for p in premises):
                if rule not in implicit_premises:
                    implicit_premises.append(rule)

        # 2. فحص الفجوة بين موضوع النتيجة ومحمولها (Missing Term Analysis)
        missing_link = self._detect_unlinked_terms(premises, conclusion)
        if missing_link:
            implicit_premises.append(missing_link)

        # دمج المقدمات المضمرة مع المقدمات الأصلية
        full_premises.extend(implicit_premises)

        return full_premises, implicit_premises

    def _detect_unlinked_terms(self, premises: List[str], conclusion: str) -> Optional[str]:
        """
        فحص الحد الأوسط الغائب للربط بين المقدمات والنتيجة.
        """
        if not premises or not conclusion:
            return None

        combined_premises = " ".join(premises)
        conclusion_words = set(conclusion.split())
        premise_words = set(combined_premises.split())

        # الكلمات الواردة في النتيجة والغائبة تماماً عن المقدمات
        unlinked_words = conclusion_words - premise_words
        stop_words = {"إذن", "فإن", "هو", "هي", "على", "في", "من", "أن", "هذا", "هذه", "عن", "إلى"}
        core_unlinked = unlinked_words - stop_words

        if core_unlinked:
            missing_term = " ".join(core_unlinked)
            return f"افتراض مضمر: توجد علاقة علية أو لزوم منطقي تربط بين المقدمات و ({missing_term})."

        return None