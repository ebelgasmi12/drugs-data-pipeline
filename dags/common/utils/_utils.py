def transform_records(records):
    """
    Transform drugs records fetched from database
    and return drugs relations dict.
    :param records: Database records (iterable).
    :return: Drugs relations dict.
    :rtype: dict
    """
    # Init results dict
    results = {}
    # Init journals hashes
    # for each drug
    drugs_journals_hashes = {}
    # For each record
    for record in records:
        # Get values
        drug, title, date, journal, publication = record
        # Date to string
        date = date.strftime("%m/%d/%Y")
        # Init drug dict
        drug_dict = {}
        # New drug case
        if drug not in results.keys():
            # Construct new drugs relations dict
            publication_dict = {"title": title, "date": date}
            journal_dict = {"title": journal, "date": date}
            drug_dict = {
                publication: [publication_dict],
                "journals": [journal_dict]
            }
            # Add drug to results
            results[drug] = drug_dict
            # register journal hash
            journal_hash = hash(frozenset(journal_dict.items()))
            drugs_journals_hashes[drug] = [journal_hash]
        # Registred drug case
        elif drug in results.keys():
            # Add publication to drug relations
            publications = results[drug].get(publication) or []
            publication_dict = {"title": title, "date": date}
            publications.append(publication_dict)
            results[drug][publication] = publications
            # Add journal to drug relations (if new)
            journal_dict = {"title": journal, "date": date}
            journal_hash = hash(frozenset(journal_dict.items()))
            if journal_hash not in drugs_journals_hashes[drug]:
                journals = results[drug]["journals"]
                journals.append(journal_dict)
                results[drug]["journals"] = journals
                drugs_journals_hashes[drug].append(journal_hash)
    # Return drugs relations
    return results