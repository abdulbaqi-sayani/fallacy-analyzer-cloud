# المسار: tests/test_fallacy_pipeline.py

import unittest
from fastapi.testclient import TestClient
from fallacy_analyzer.nlp_pipeline import ArgumentNLPPipeline
from fallacy_analyzer.decision_tree import LogicalFallacyClassifier
from api.main import app

class TestFallacyPipelineAndAPI(unittest.TestCase):
    """
    اختبارات وحدة وتكامل شمولية للتحقق من سلامة خط المعالجة،
    ومحرك المقدمات المضمرة، ومشجر القرارات، وواجهة البرمجة API.
    """

    def setUp(self):
        """تهيئة الكائنات واختبار العميل برمجياً قبل كل اختبار."""
        self.pipeline = ArgumentNLPPipeline()
        self.client = TestClient(app)

    def test_enthymeme_extraction_logic(self):
        """اختبار كفاءة محرك استخراج المقدمات المضمرة الخفية."""
        text = "ينبغي منع هذا السلوك لأنه خطير."
        processed = self.pipeline.process_text(text)
        
        self.assertIn("implicit_premises", processed)
        self.assertTrue(len(processed["implicit_premises"]) > 0)
        self.assertTrue(any("افتراض مضمر" in p or "المقدمة المضمرة" in p for p in processed["implicit_premises"]))

    def test_formal_fallacy_affirming_consequent(self):
        """اختبار كشف مغالطة إثبات التالي الصورية."""
        text = "إذا كان المطر ينزل فإن الأرض تبتل. الأرض مبتلة. إذن المطر ينزل. بما أن النتيجة تحققت"
        processed = self.pipeline.process_text(text)
        classifier = LogicalFallacyClassifier(processed)
        result = classifier.classify()
        self.assertIn("إثبات التالي", result)

    def test_informal_fallacy_ad_hominem(self):
        """اختبار كشف مغالطة شخصنة الحجة غير الصورية."""
        text = "هذا التحليل اقتصادي فاسد لأنه صدر من شخص كاذب وجاهل."
        processed = self.pipeline.process_text(text)
        classifier = LogicalFallacyClassifier(processed)
        result = classifier.classify()
        self.assertIn("شخصنة الحجة", result)

    def test_api_analyze_endpoint_success(self):
        """اختبار نقطة النهاية API للتحقق من اتساق عقد البيانات الجديد بالكامل."""
        response = self.client.post(
            "/analyze",
            json={"text": "الخيار الأول ممتاز لأنه ينبغي تحسين الجودة المعتمدة."}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # التحقق من وجود الحقول الجديدة في الاستجابة
        self.assertIn("original_text", data)
        self.assertIn("raw_premises", data)
        self.assertIn("implicit_premises", data)
        self.assertIn("full_premises", data)
        self.assertIn("extracted_conclusion", data)
        self.assertIn("classification_result", data)

    def test_api_analyze_endpoint_validation_error(self):
        """اختبار رفض API للنصوص القصيرة غير الصالحة للاستدلال."""
        response = self.client.post(
            "/analyze",
            json={"text": "قصير"}
        )
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
