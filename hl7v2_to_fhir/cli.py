import argparse
import json
import sys

from .generator import FHIRBundleGenerator
from .parser import HL7Parser


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert HL7 v2 ER7 messages to FHIR R4 Bundles")
    parser.add_argument("input", nargs="?", help="Input HL7 ER7 string or file path")
    parser.add_argument("--file", "-f", action="store_true", help="Read input from file")
    parser.add_argument("--pretty", "-p", action="store_true", help="Pretty print JSON output")
    
    args = parser.parse_args()

    if not args.input and sys.stdin.isatty():
        parser.print_help()
        sys.exit(1)

    # Read input
    raw_data = ""
    if not sys.stdin.isatty():
        raw_data = sys.stdin.read()
    elif args.file:
        try:
            with open(args.input, encoding="utf-8") as f:
                raw_data = f.read()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        raw_data = args.input

    if not raw_data:
        print("Error: No input data provided.", file=sys.stderr)
        sys.exit(1)

    # Parse and Generate
    hl7_parser = HL7Parser()
    try:
        message = hl7_parser.parse(raw_data)
        generator = FHIRBundleGenerator()
        fhir_bundle = generator.generate(message)
        
        if args.pretty:
            print(json.dumps(fhir_bundle, indent=2))
        else:
            print(json.dumps(fhir_bundle))
    except Exception as e:
        print(f"Conversion error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
