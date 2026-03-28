import unittest

from hl7v2_to_fhir.generator import FHIRBundleGenerator
from hl7v2_to_fhir.parser import HL7Parser


class TestFHIRGenerator(unittest.TestCase):
    
    def setUp(self):
        self.parser = HL7Parser()
        self.generator = FHIRBundleGenerator()
        self.sample_oru = (
            "MSH|^~\\&|SENDING_APP|SENDING_FAC|RECV_APP|RECV_FAC|20260328120000||ORU^R01|MSG12345|P|2.5\n"
            "PID|1||PID12345^^^AUTH^MR||DOE^JOHN^^^MR.||19800101|M\n"
            "OBR|1|OBR123|OBR456|80053^COMPREHENSIVE METABOLIC PANEL\n"
            "OBX|1|NM|GLU^GLUCOSE||105|mg/dL|70-99|H|||F|||20260328100000\n"
        )
        
    def test_bundle_generation(self):
        message = self.parser.parse(self.sample_oru)
        bundle = self.generator.generate(message)
        
        self.assertEqual(bundle["resourceType"], "Bundle")
        self.assertEqual(bundle["type"], "transaction")
        self.assertEqual(len(bundle["entry"]), 2) # 1 Patient, 1 Observation
        
        # Verify Patient properties
        patient_entry = bundle["entry"][0]["resource"]
        self.assertEqual(patient_entry["resourceType"], "Patient")
        self.assertEqual(patient_entry["gender"], "male")
        self.assertEqual(patient_entry["birthDate"], "1980-01-01")
        self.assertEqual(patient_entry["identifier"][0]["value"], "PID12345")
        self.assertEqual(patient_entry["name"][0]["family"], "DOE")
        self.assertEqual(patient_entry["name"][0]["given"][0], "JOHN")
        
        # Verify Observation properties
        obs_entry = bundle["entry"][1]["resource"]
        self.assertEqual(obs_entry["resourceType"], "Observation")
        self.assertEqual(obs_entry["status"], "final")
        self.assertEqual(obs_entry["valueString"], "105")
        self.assertEqual(obs_entry["effectiveDateTime"], "2026-03-28T10:00:00+00:00")
        self.assertEqual(obs_entry["code"]["coding"][0]["code"], "GLU")

if __name__ == "__main__":
    unittest.main()
