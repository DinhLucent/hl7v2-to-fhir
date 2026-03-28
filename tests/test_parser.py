import unittest

from hl7v2_to_fhir.parser import HL7Parser


class TestHL7Parser(unittest.TestCase):
    
    def setUp(self):
        self.parser = HL7Parser()
        self.sample_oru = (
            "MSH|^~\\&|SENDING_APP|SENDING_FAC|RECV_APP|RECV_FAC|20260328120000||ORU^R01|MSG12345|P|2.5\r"
            "PID|1||PID12345^^^AUTH^MR||DOE^JOHN^^^MR.||19800101|M\r"
            "OBR|1|OBR123|OBR456|80053^COMPREHENSIVE METABOLIC PANEL\r"
            "OBX|1|NM|GLU^GLUCOSE||105|mg/dL|70-99|H|||F\r"
        )
        
    def test_parse_segments(self):
        message = self.parser.parse(self.sample_oru)
        
        self.assertEqual(len(message.segments), 4)
        
        msh = message.get_first_segment("MSH")
        self.assertIsNotNone(msh)
        self.assertEqual(msh.get_field(1), "|")
        self.assertEqual(msh.get_field(2), "^~\\&")
        self.assertEqual(msh.get_field(9), "ORU^R01")
        
        pid = message.get_first_segment("PID")
        self.assertIsNotNone(pid)
        self.assertEqual(pid.get_field(3), "PID12345^^^AUTH^MR")
        self.assertEqual(pid.get_field(5), "DOE^JOHN^^^MR.")
        
        obx = message.get_first_segment("OBX")
        self.assertIsNotNone(obx)
        self.assertEqual(obx.get_field(3), "GLU^GLUCOSE")
        self.assertEqual(obx.get_field(5), "105")

if __name__ == "__main__":
    unittest.main()
