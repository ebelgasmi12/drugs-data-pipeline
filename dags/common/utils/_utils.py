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
            drug_dict = {
                publication: [{"title": title, "date": date}],
                "journals": [{"title": journal, "date": date}]
            }
            # Add drug to results
            results[drug] = drug_dict
        # Registred drug case
        elif drug in results.keys():
            # Add publication to drug relations
            publications = results[drug].get(publication) or []
            publications.append({"title": title, "date": date})
            results[drug][publication] = publications
            # Add journal to drug relations
            journals = results[drug].get("journals") or []
            journals.append({"title": journal, "date": date})
            results[drug]["journals"] = journals
    # Return drugs relations
    return results