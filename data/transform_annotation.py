import json
import re

# Define the input and output file names
input_file = "annotation_0531.jsonl"
output_file = "transformed_annotations.jsonl"
report_file = "report_no_NA.jsonl"
valid_records_file = "valid_records.jsonl"

def extract_title_and_abstract(displayed_text):
    title_match = re.search(r"^Title:\s*(.+)$", displayed_text, re.MULTILINE)
    abstract_match = re.search(r"^Abstract:\s*(.+)$", displayed_text, re.MULTILINE)
    title = title_match.group(1) if title_match else ""
    abstract = abstract_match.group(1) if abstract_match else ""
    return title, abstract

# Define the transformation function
def transform_record(record):
    title, abstract = extract_title_and_abstract(record["displayed_text"])
    return {
        "pid": record["id"],
        "context": record["label_annotations"]["Multi-aspect Summary"].get("Context", ""),
        "key_idea": record["label_annotations"]["Multi-aspect Summary"].get("Key idea", ""),
        "method": record["label_annotations"]["Multi-aspect Summary"].get("Method", ""),
        "outcome": record["label_annotations"]["Multi-aspect Summary"].get("Outcome", ""),
        "future_impact": record["label_annotations"]["Multi-aspect Summary"].get("Future Impact", ""),
        "venue": None,  # Placeholder for missing data in the input
        "year": None,   # Placeholder for missing data in the input
        "title": title
    }

# Check if specific fields in a record are not "N/A"
def has_no_NA(record):
    fields_to_check = ["context", "key_idea", "method", "outcome", "future_impact"]
    return all(record[field] not in [None, "N/A", ""] for field in fields_to_check)

# Count records where context, key_idea, method, outcome are not "N/A"
def count_valid_fields(record):
    fields_to_count = ["context", "key_idea", "method", "outcome"]
    return all(record[field] not in [None, "N/A", ""] for field in fields_to_count)

# Initialize counters
total_records = 0

# Read the input file and process each line
with open(input_file, "r") as infile, \
     open(output_file, "w") as outfile, \
     open(report_file, "w") as reportfile, \
     open(valid_records_file, "w") as validfile:
    for line in infile:
        total_records += 1
        record = json.loads(line)
        transformed_record = transform_record(record)
        outfile.write(json.dumps(transformed_record) + "\n")
        if has_no_NA(transformed_record):
            reportfile.write(json.dumps(transformed_record) + "\n")
        if count_valid_fields(transformed_record):
            validfile.write(json.dumps(transformed_record) + "\n")

print(f"Transformation complete. Output written to {output_file}.")
print(f"Report of lines without any N/A written to {report_file}.")
print(f"Records where 'context', 'key_idea', 'method', and 'outcome' are not N/A written to {valid_records_file}.")
print(f"Total number of records processed: {total_records}")
