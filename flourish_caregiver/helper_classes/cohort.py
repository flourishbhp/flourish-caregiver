

class CohortError(Exception):
    pass


class Cohort:

    """Class that determines the cohort that a child belong too
    """

    def __init__(self, delivery_date=None):
        self.delivery_date = delivery_date


    def age(self):
        pass
        # delivdt
        
    def cohort_a(self):
        pass
    
    def cohort_b(self):
        pass
    
    def cohort_c(self):
        pass