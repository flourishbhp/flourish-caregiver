

class CohortError(Exception):
    pass


class Cohort:

    """Class that determines the cohort that a child belong too
    """

    def __init__(self, child_dob=None, ):
        self.child_dob = child_dob

    def age(self):
        pass

    def cohort_a(self):
        pass

    def cohort_b(self):
        pass

    def cohort_c(self):
        pass
