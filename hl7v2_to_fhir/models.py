from dataclasses import dataclass, field


@dataclass
class HL7Segment:
    """Represents a single HL7 segment (e.g., MSH, PID)."""
    segment_id: str
    fields: list[str] = field(default_factory=list)

    def get_field(self, index: int) -> str:
        """Get field by index (1-based typical in HL7 specs)."""
        if index < 1 or index > len(self.fields):
            return ""
        return self.fields[index - 1]

@dataclass
class HL7Message:
    """Represents a parsed HL7 ER7 message."""
    segments: list[HL7Segment] = field(default_factory=list)

    def get_segments(self, segment_id: str) -> list[HL7Segment]:
        """Get all segments matching a given ID."""
        return [s for s in self.segments if s.segment_id == segment_id]

    def get_first_segment(self, segment_id: str) -> HL7Segment | None:
        """Get the first segment matching a given ID."""
        for s in self.segments:
            if s.segment_id == segment_id:
                return s
        return None
