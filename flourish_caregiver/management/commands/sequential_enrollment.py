from django.core.management.base import BaseCommand
from tqdm import tqdm

from ...helper_classes import SequentialCohortEnrollment
from ...models import CaregiverChildConsent


class Command(BaseCommand):
    help = "Sequentially enrol children into cohorts"

    def handle(self, *args, **options):
        # Get a list of all children in the study
        child_identifiers = CaregiverChildConsent.objects.values_list(
            'subject_identifier', flat=True)
        child_identifiers = list(set(child_identifiers))

        # Loop through all of them and sequentially enrol those who have aged up.
        for child_id in tqdm(child_identifiers):
            sequential_cohort_enrol = SequentialCohortEnrollment(
                child_subject_identifier=child_id)
            try:
                aged_up = sequential_cohort_enrol.age_up_enrollment()
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to enroll {child_id}. Error {e}'))
            else:
                if aged_up:
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully aged up {child_id}.'))
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f'Participant {child_id} hasn\'t aged up.'))
