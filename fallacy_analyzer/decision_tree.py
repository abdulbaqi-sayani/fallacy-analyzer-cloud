# المسار: fallacy_analyzer_cloud/fallacy_analyzer/decision_tree.py

from typing import Dict, Any, Optional
from .categorical_syllogism import CategoricalSyllogismEngine

class LogicalFallacyClassifier:
    """
    مُصنف مشجر القرارات المزدوج المطور والمنضبط بالسحابة.
    """
    def __init__(self, argument_data: Dict[str, Any]):
        self.premises = argument_data.get("premises", [])
        self.conclusion = argument_data.get("conclusion", "")
        self.logical_form = argument_data.get("logical_form", None)
        self.semantic_features = argument_data.get("semantic_features", {})
        self.categorical_engine = CategoricalSyllogismEngine()

    def classify(self) -> str:
        # 1. فحص القياس الحملي الأرسطي أولاً
        if len(self.premises) >= 1 and self.conclusion:
            cat_res = self.categorical_engine.analyze_syllogism(self.premises, self.conclusion)
            if cat_res.get("is_categorical"):
                if not cat_res.get("is_valid"):
                    return f"مغالطة حملية أرسطية: {cat_res.get('fallacy_name')} - {cat_res.get('details')}"
                else:
                    return f"برهان أرسطي صحيح: {cat_res.get('syllogism_type')} ({cat_res.get('details')})"

        # 2. فحص البراهين الصورية الشرطية المباشرة
        valid_proof = self._check_valid_proof_forms()
        if valid_proof:
            return f"برهان منطقي صحيح: {valid_proof}"

        # 3. فحص المغالطات الصورية الشرطية
        formal_fallacy = self._check_formal_fallacies()
        if formal_fallacy:
            return f"مغالطة صورية: {formal_fallacy}"

        # 4. فحص مغالطات الصلة والارتباط
        relevance_fallacy = self._check_relevance_fallacies()
        if relevance_fallacy:
            return f"مغالطة غير صورية (صلة): {relevance_fallacy}"

        # 5. فحص مغالطات الافتراض الدائري المعضلة الزائفة
        presumption_fallacy = self._check_presumption_fallacies()
        if presumption_fallacy:
            return f"مغالطة غير صورية (افتراض): {presumption_fallacy}"

        # 6. فحص مغالطات السببية والاستقراء
        inductive_fallacy = self._check_inductive_fallacies()
        if inductive_fallacy:
            return f"مغالطة غير صورية (استقراء/سببية): {inductive_fallacy}"

        # 7. فحص مغالطات اللبس والغموض اللغوي
        ambiguity_fallacy = self._check_ambiguity_fallacies()
        if ambiguity_fallacy:
            return f"مغالطة غير صورية (غموض): {ambiguity_fallacy}"

        return "حجة استنباطية سليمة منطقياً (استدلال صحيح خالٍ من المغالطات)"

    def _check_valid_proof_forms(self) -> Optional[str]:
        form = self.logical_form
        if form == "(not P -> Contradiction) -> P":
            return "البرهان بالخلف وإثبات المحال (Reductio ad Absurdum)"
        elif form == "((P -> Q) and not Q) -> not P":
            return "قياس نفي التالي - البرهان بالإلزام (Modus Tollens)"
        elif form == "((P -> Q) and P) -> Q":
            return "قياس إثبات المقدم (Modus Ponens)"
        elif form == "((P or Q) and not P) -> Q":
            return "القياس الشرطي المنفصل - السبر والتقسيم (Disjunctive Syllogism)"
        return None

    def _check_formal_fallacies(self) -> Optional[str]:
        form = self.logical_form
        if form == "((P -> Q) and Q) -> P":
            return "إثبات التالي (Affirming the Consequent)"
        elif form == "((P -> Q) and not P) -> not Q":
            return "إنكار المقدم (Denying the Antecedent)"
        return None

    def _check_relevance_fallacies(self) -> Optional[str]:
        features = self.semantic_features
        if features.get("shifts_burden_of_proof"):
            return "تحويل عبء الإثبات الزائف (Shifting the Burden of Proof)"
        if features.get("targets_person_character"):
            return "شخصنة الحجة (Ad Hominem)"
        if features.get("distorts_opponent_argument"):
            return "رجل القش (Straw Man)"
        if features.get("shifts_topic_divergence"):
            return "الرنجة الحمراء (Red Herring)"
        if features.get("appeals_to_unqualified_authority"):
            return "التوسل بالسلطة الزائفة (Ad Verecundiam)"
        return None

    def _check_presumption_fallacies(self) -> Optional[str]:
        is_single_fallback = "جملة استدلالية" in self.conclusion
        if not is_single_fallback and len(self.premises) > 1:
            if any(premise == self.conclusion for premise in self.premises):
                return "المصادرة على المطلوب (Begging the Question)"

        if self.semantic_features.get("forces_binary_options") and not self.semantic_features.get("is_truly_binary"):
            return "المعضلة الزائفة (False Dilemma)"
        return None

    def _check_inductive_fallacies(self) -> Optional[str]:
        features = self.semantic_features
        if features.get("sample_size_insufficient"):
            return "التعميم المتسرع (Hasty Generalization)"
        if features.get("temporal_sequence_as_causation"):
            return "السبب الزائف / التعاقب الزمني (Post Hoc Ergo Propter Hoc)"
        if features.get("unproven_chain_reaction"):
            return "المنحدر الزلق (Slippery Slope)"
        return None

    def _check_ambiguity_fallacies(self) -> Optional[str]:
        if self.semantic_features.get("word_meaning_shifted"):
            return "الاشتراك اللفظي (Equivocation)"
        if self.semantic_features.get("assumes_part_equals_whole"):
            return "مغالطة التركيب/التقسيم (Composition/Division)"
        return None