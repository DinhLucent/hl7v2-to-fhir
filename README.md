# HL7 v2 to FHIR Converter 🏥🔄

An autonomous, lightweight mapping engine designed to effortlessly translate legacy HL7 ER7 pipe-and-hat messages (v2.x) into modern FHIR R4 Bundles.

## 🚀 Overview
Legacy healthcare systems still rely heavily on HL7 v2 messages (ADT, ORU, ORM). This engine acts as the bridge to modern interoperability, parsing raw ER7 segments and orchestrating their translation into a `transaction` Bundle populated with `Patient`, `Observation`, and future FHIR resources.

## 🏗️ Architecture
- `hl7v2_to_fhir/parser.py`: Fast ER7 text splitting with resilient `\r` and `\n` segment handling.
- `hl7v2_to_fhir/mapper.py`: Cross-walk logic converting discrete standards (e.g. Administrative Sex mapping, DateTime parsing).
- `hl7v2_to_fhir/generator.py`: Assembles the parsed representations into structured FHIR dicts containing UUID-anchored entries.
- `hl7v2_to_fhir/cli.py`: A native command-line interface supporting standard input and direct file reading for pipeline integration.

## 🛠️ Usage

### CLI
Process a raw HL7 file directly:
```bash
python -m hl7v2_to_fhir.cli -f sample.hl7 --pretty
```

Or pipe a message through stdin:
```bash
cat sample.hl7 | python -m hl7v2_to_fhir.cli --pretty
```

### Python API
```python
from hl7v2_to_fhir.parser import HL7Parser
from hl7v2_to_fhir.generator import FHIRBundleGenerator

raw_oru = "MSH|^~\\&|...\\rPID|..."

parser = HL7Parser()
generator = FHIRBundleGenerator()

# Parse into Domain Models
message = parser.parse(raw_oru)

# Generate FHIR Bundle dictionary
fhir_bundle = generator.generate(message)
```

## 🛡️ Standards
- **Linter**: Ruff
- **Type Hints**: Python 3.10+
- **Testing**: Unittest

## 🤝 Contributing
Contributions are welcome as we scale out mapping logic for additional FHIR resources and HL7 segment structures.
