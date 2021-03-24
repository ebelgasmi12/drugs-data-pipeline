import json
import operator
import os
import sys

def get_max_drugs_journal(json_path):
    """
    Get journal with max unique drugs mentions.
    :param json_path: path to JSON file.
    :return: Name of the journal.
    :rtype: str
    """
    # Init journal mentions
    journal_mentions = {}
    # Read JSON file
    with open(json_path, "r") as json_file: 
        content = json.load(json_file)
    # For each drug
    for drug in content.keys():
        # For each journal that mentioned the drug
        for journal in content[drug]["journals"]:
            # New journal case
            if journal["title"] not in journal_mentions.keys():
                # Add it to journal list (with mentioned drug)
                journal_mentions[journal["title"]] = [drug]
            # Existing journal case
            else:
                # Check the unicity of drug mention
                if drug not in journal_mentions[journal["title"]]:
                    # Add drug if not mentioned before
                    journal_mentions[journal["title"]].append(drug)
    # Return journal with max drug mentions
    return max(journal_mentions.items(),  key=lambda x: len(x[1]))[0]


if __name__ == "__main__":
    # JSON file path
    json_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "../dags/drugs_data_pipeline/data/output/drugs_output.json")
    # Get journal
    max_drugs_journal = get_max_drugs_journal(json_path)
    # print it
    print("Le journal avec le plus de mentions de médicament: {}" \
          .format(max_drugs_journal))