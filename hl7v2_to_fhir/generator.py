import uuid
from typing import Any

from .mapper import HL7ToFHIRMapper
from .models import HL7Message


class FHIRBundleGenerator:
    """Generates a FHIR R4 Bundle from a parsed HL7 ER7 message."""

    def __init__(self):
        self.mapper = HL7ToFHIRMapper()

    def generate(self, message: HL7Message) -> dict[str, Any]:
        """Transform an HL7Message into a FHIR transaction Bundle."""
        entries = []
        
        # Patient (PID)
        pid = message.get_first_segment("PID")
        patient_id = str(uuid.uuid4())
        if pid:
            patient_resource = self._build_patient(pid, patient_id)
            entries.append(self._create_entry(patient_resource, "POST", "Patient"))

        # Observation (OBX)
        obx_segments = message.get_segments("OBX")
        for obx in obx_segments:
            obs_resource = self._build_observation(obx, patient_id)
            if obs_resource:
                entries.append(self._create_entry(obs_resource, "POST", "Observation"))

        return {
            "resourceType": "Bundle",
            "type": "transaction",
            "entry": entries
        }

    def _create_entry(self, resource: dict[str, Any], method: str, url: str) -> dict[str, Any]:
        return {
            "fullUrl": f"urn:uuid:{resource.get('id', uuid.uuid4())}",
            "resource": resource,
            "request": {
                "method": method,
                "url": url
            }
        }

    def _build_patient(self, pid, patient_id: str) -> dict[str, Any]:
        # PID-3: Patient Identifier List
        identifier = pid.get_field(3).split("^")[0] if pid.get_field(3) else "unknown"
        
        # PID-5: Patient Name
        name_parts = pid.get_field(5).split("^")
        family = name_parts[0] if len(name_parts) > 0 else ""
        given = name_parts[1] if len(name_parts) > 1 else ""

        # PID-7: Date/Time of Birth
        dob = self.mapper.map_date(pid.get_field(7))

        # PID-8: Administrative Sex
        gender = self.mapper.map_administrative_sex(pid.get_field(8))

        return {
            "resourceType": "Patient",
            "id": patient_id,
            "identifier": [{"value": identifier}],
            "name": [{"family": family, "given": [given] if given else []}],
            "gender": gender,
            "birthDate": dob
        }

    def _build_observation(self, obx, patient_id: str) -> dict[str, Any]:
        # Minimal OBX to FHIR Observation
        # OBX-3: Observation Identifier
        obs_id_parts = obx.get_field(3).split("^")
        code = obs_id_parts[0] if obs_id_parts else "unknown"
        display = obs_id_parts[1] if len(obs_id_parts) > 1 else ""

        # OBX-5: Observation Value
        value = obx.get_field(5)

        # OBX-14: Date/Time of the Observation
        effective_date = self.mapper.map_date(obx.get_field(14))

        obs = {
            "resourceType": "Observation",
            "id": str(uuid.uuid4()),
            "status": "final",
            "code": {
                "coding": [{"code": code, "display": display}]
            },
            "subject": {"reference": f"urn:uuid:{patient_id}"}
        }
        
        if value:
            obs["valueString"] = value
        if effective_date:
            obs["effectiveDateTime"] = effective_date
            
        return obs
