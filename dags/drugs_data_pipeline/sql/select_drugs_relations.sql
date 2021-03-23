SELECT drugs.drug AS drug, pubmed.title AS title, pubmed.date AS date, 
        pubmed.journal as journal, 'pubmed' AS publication
FROM drugs, pubmed
WHERE pubmed.title ILIKE '%' || drugs.drug || '%'

UNION

SELECT drugs.drug AS drug, clinical_trials.scientific_title AS title, clinical_trials.date AS date, 
        clinical_trials.journal as journal, 'clinical_trial' AS publication
FROM drugs, clinical_trials
WHERE clinical_trials.scientific_title ILIKE '%' || drugs.drug || '%';