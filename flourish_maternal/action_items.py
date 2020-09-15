# from td_prn.action_items import MaternalOffStudyAction
#
# from edc_locator.action_items import SubjectLocatorAction
#
# from edc_action_item import Action, site_action_items, HIGH_PRIORITY
#
# MATERNAL_LOCATOR_ACTION = 'submit-maternal-locator'
# ULTRASOUND_ACTION = 'submit-ultrasound'
# MATERNAL_DELIVERY_ACTION = 'submit-maternal-delivery'
# MATERNAL_COVID_SCREENING_ACTION = 'update-maternal-covid-results'
#
#
# class MaternalLocatorAction(SubjectLocatorAction):
#     name = MATERNAL_LOCATOR_ACTION
#     display_name = 'Submit Maternal Locator'
#     reference_model = 'td_maternal.maternallocator'
#     admin_site_name = 'td_maternal_admin'
#
#
# class MaternalUltrasoundAction(Action):
#     name = ULTRASOUND_ACTION
#     display_name = 'Submit Maternal Ultrasound'
#     reference_model = 'td_maternal.maternalultrasoundinitial'
#     admin_site_name = 'td_maternal_admin'
#     create_by_user = False
#
#     def get_next_actions(self):
#         actions = []
#
#         # resave visit to update metadata
#         self.reference_model_obj.maternal_visit.save()
#
#         if self.reference_model_obj.number_of_gestations != '1':
#             actions = [MaternalOffStudyAction]
#         else:
#             self.delete_if_new(MaternalOffStudyAction)
#         return actions
#
#
# class MaternalLabourDeliveryAction(Action):
#     name = MATERNAL_DELIVERY_ACTION
#     display_name = 'Submit Maternal Delivery'
#     reference_model = 'td_maternal.maternallabourdel'
#     admin_site_name = 'td_maternal_admin'
#     priority = HIGH_PRIORITY
#
#     def get_next_actions(self):
#         actions = []
#         if self.reference_model_obj.live_infants_to_register != 1:
#             actions = [MaternalOffStudyAction]
#         return actions
#
#
# class MaternalCovidScreeningAction(Action):
#     name = MATERNAL_COVID_SCREENING_ACTION
#     display_name = 'Update Maternal Covid Screening Test Results'
#     reference_model = 'td_maternal.maternalcovidscreening'
#     admin_site_name = 'td_maternal_admin'
#     priority = HIGH_PRIORITY
#
#     def close_action_item_on_save(self):
#         """Returns True if action item for \'action_identifier\'
#         is to be closed on post_save.
#         """
#         return self.reference_model_obj.covid_results != 'pending'
#
#
# site_action_items.register(MaternalCovidScreeningAction)
# site_action_items.register(MaternalLabourDeliveryAction)
# site_action_items.register(MaternalLocatorAction)
# site_action_items.register(MaternalUltrasoundAction)
