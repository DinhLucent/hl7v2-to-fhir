from datetime import datetime


class HL7ToFHIRMapper:
    """Contains mapping rules to translate HL7 v2 fields to FHIR R4."""

    GENDER_MAP = {
        "M": "male",
        "F": "female",
        "O": "other",
        "U": "unknown",
        "A": "other",
        "N": "other"
    }

    @staticmethod
    def map_administrative_sex(hl7_sex: str) -> str:
        """Map HL7 Administrative Sex (PID-8) to FHIR AdministrativeGender."""
        return HL7ToFHIRMapper.GENDER_MAP.get(hl7_sex.upper(), "unknown")

    @staticmethod
    def map_date(hl7_date: str) -> str | None:
        """Convert HL7 date/time (YYYYMMDD[HHMMSS]) to FHIR iso8601 string."""
        if not hl7_date:
            return None
        
        # Simplified parsing for minimum YYYYMMDD
        cleaned = hl7_date.strip()
        try:
            if len(cleaned) == 8:
                dt = datetime.strptime(cleaned, "%Y%m%d")
                return dt.strftime("%Y-%m-%d")
            elif len(cleaned) >= 14:
                dt = datetime.strptime(cleaned[:14], "%Y%m%d%H%M%S")
                return dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        except ValueError:
            pass
        return None
