# HL7 v2 to FHIR R4 Translation Engine

Lightweight Python translation engine mapping legacy HL7 v2.x ER7 pipe-and-hat messages into structured FHIR R4 Transaction Bundles.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FHIR](https://img.shields.io/badge/FHIR-R4-0079D6?style=flat-square)
![HL7](https://img.shields.io/badge/HL7-v2.x-DC143C?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-0D9488?style=flat-square)

---

## Architecture & Mapping Pipeline

Translates raw clinical messages (ADT, ORU) into standard FHIR R4 resources (`Patient`, `Observation`) bundled in a transaction envelope with deterministic UUID references.

```mermaid
graph LR
    A[📄 Raw HL7 v2.x ER7] -->|Line & Delimiter Parsing| B(⚙️ HL7 Parser)
    B -->|Domain Models| C(🔄 Resource Mapper)
    C -->|Cross-walk Vocabularies| D(📦 FHIR Bundle Generator)
    D -->|Transaction Envelope| E[🏥 FHIR R4 JSON Bundle]
```

---

## Features

- **Zero-Dependency Core**: Implemented with Python standard library modules (`uuid`, `datetime`, `json`) for high-throughput pipeline embedding.
- **Resilient ER7 Splitting**: Handles carriage return (`\r`), newline (`\n`), and mixed delimiters from various hospital analyzer feeds.
- **Standards Cross-Walk**: Maps clinical concepts such as HL7 administrative sex codes (`F`, `M`, `O`, `U`) to FHIR code systems, parses HL7 timestamp formats into ISO 8601 strings.
- **Dual Interface**: Supports both a direct Python API and a CLI utility with stdin piping support for shell scripts and middleware channels.

---

## Quick Start

### Installation

```bash
git clone https://github.com/DinhLucent/hl7v2-to-fhir.git
cd hl7v2-to-fhir
pip install -r requirements.txt
```

### CLI Usage

Process a raw HL7 file directly to formatted FHIR JSON:

```bash
python -m hl7v2_to_fhir.cli -f sample.hl7 --pretty
```

Or pipe clinical messages via stdin:

```bash
cat sample.hl7 | python -m hl7v2_to_fhir.cli --pretty
```

### Python API

```python
from hl7v2_to_fhir.parser import HL7Parser
from hl7v2_to_fhir.generator import FHIRBundleGenerator

raw_oru = "MSH|^~\\&|LAB|HOSPITAL|||20240101120000||ORU^R01|MSG001|P|2.5\rPID|1||PAT001||DOE^JOHN||19800101|M"

parser = HL7Parser()
generator = FHIRBundleGenerator()

# Parse message into domain models
message = parser.parse(raw_oru)

# Generate FHIR R4 transaction bundle dictionary
fhir_bundle = generator.generate(message)

print(fhir_bundle["resourceType"])  # "Bundle"
print(fhir_bundle["type"])          # "transaction"
```

---

## Project Structure

```
hl7v2-to-fhir/
├── hl7v2_to_fhir/
│   ├── cli.py             # CLI runner with stdin and file flags
│   ├── generator.py       # FHIR R4 Bundle assembly logic
│   ├── mapper.py          # Clinical vocabulary cross-walk logic
│   ├── models.py          # Internal HL7 segment dataclasses
│   └── parser.py          # ER7 message and segment parser
├── tests/
│   ├── test_generator.py  # Bundle generation tests
│   └── test_parser.py     # Delimiter and segment parsing tests
├── pyproject.toml         # Packaging configuration
├── requirements.txt       # Dependencies
├── LICENSE                # MIT License
└── README.md
```

---

## Running Tests

Run the test suite using pytest:

```bash
python -m pytest tests/ -v
```

---

## License

MIT License. Copyright (c) 2022-present Đinh Hoàng Sáng.

---
Built by [DinhLucent](https://github.com/DinhLucent)
