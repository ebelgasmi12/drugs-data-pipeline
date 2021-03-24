import pytest

class TestDagValidation:
    """
    DAG Validation tests.
    """
    # Import time threshold (in seconds)
    IMPORT_TIME_THRESHOLD = 2
    EXPECTED_NUMBER_OF_DAGS = 1
    MAX_RETRIES = 5
    
    def test_dags_import(self, dagbag):
        """
        Test if that Airflow is able to import 
        all DAGs without errors.
        """
        # Check if there's import errors
        assert len(dagbag.import_errors) == 0, \
            "Unable to import DAGs. Reasons:\n{}".format(dagbag.import_errors)

    def test_dags_import_time(self, dagbag):
        """
        Test if DAGs import time is below a threshold.
        """
        # Fiter slow DAGs
        slow_dags = filter(
            lambda d: d.duration.total_seconds() > self.IMPORT_TIME_THRESHOLD, 
            dagbag.dagbag_stats)
        # Get slow DAGs names
        slow_dags_names = ', '.join(map(lambda d: d.file[1:], slow_dags))        
        # Check if slow dags list is empty
        assert len(list(slow_dags)) == 0, \
            "The following DAGs take more than {}s to load: {}"\
                .format(self.IMPORT_TIME_THRESHOLD, slow_dags_names)
    
    def test_number_of_dags(self, dagbag):
        """
        Test if the DAG folder contains the right number of DAGs.
        """
        # Get number of DAGs
        dag_num = sum([d.dag_num for d in dagbag.dagbag_stats])
        # Test if number of DAGs matches the expected value
        assert dag_num == self.EXPECTED_NUMBER_OF_DAGS, \
            "Wrong number of dags. Expected {}, got {}."\
                .format(self.EXPECTED_NUMBER_OF_DAGS, dag_num)

    def test_max_retries(self, dagbag):
        """
        Test if DAGs don't exceed the retries threshold.
        """
        # For each DAG
        for dag_id, dag in dagbag.dags.items():
            # Get number of retries
            retries = dag.default_args.get("retries", 0)
            # Get number of retries is below threshold
            assert retries <= self.MAX_RETRIES, \
                "Number of retries too high in the DAG: {}.".format(dag_id)