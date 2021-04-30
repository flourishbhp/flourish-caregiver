from edc_action_item.models import ActionItem


class DataSetActionItem(ActionItem):

    subject_identifier_model = 'flourish_caregiver.maternaldataset'

    def save(self, *args, **kwargs):
        pass
