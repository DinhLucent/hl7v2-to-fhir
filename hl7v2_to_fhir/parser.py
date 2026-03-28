from .models import HL7Message, HL7Segment


class HL7Parser:
    """Parser for ER7 delimited HL7 v2 messages."""
    
    def __init__(self, segment_separator: str = "\r", field_separator: str = "|"):
        self.segment_separator = segment_separator
        self.field_separator = field_separator

    def parse(self, raw_message: str) -> HL7Message:
        """Parse a raw ER7 HL7 string into an HL7Message object."""
        # Use provided separator or fallback to common newlines if \r not strictly used
        if self.segment_separator not in raw_message and "\n" in raw_message:
            segments_raw = raw_message.split("\n")
        else:
            segments_raw = raw_message.split(self.segment_separator)

        parsed_segments = []
        for seg_str in segments_raw:
            seg_str = seg_str.strip()
            if not seg_str:
                continue
                
            fields = seg_str.split(self.field_separator)
            segment_id = fields[0]
            
            # For MSH, the first field is actually the field separator itself due to how split works.
            # HL7 spec: MSH|^~\\&|... -> fields[1] is ^~\\&
            if segment_id == "MSH":
                # Reconstruct MSH to align with standard (1-based) indexing expectation
                # MSH.1 = |, MSH.2 = ^~\\&
                adjusted_fields = [self.field_separator] + fields[1:]
                parsed_segments.append(HL7Segment(segment_id=segment_id, fields=adjusted_fields))
            else:
                # Other segments: PID|1|... -> Fields after PID
                parsed_segments.append(HL7Segment(segment_id=segment_id, fields=fields[1:]))
                
        return HL7Message(segments=parsed_segments)
