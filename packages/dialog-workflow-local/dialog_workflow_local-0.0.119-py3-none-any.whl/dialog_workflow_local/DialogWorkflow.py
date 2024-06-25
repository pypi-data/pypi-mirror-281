import json
import random

from database_mysql_local.generic_crud import GenericCRUD
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger
from message_local.CompoundMessage import CompoundMessage
from message_local.Recipient import Recipient
from user_context_remote.user_context import UserContext
from variable_local.variables_local import VariablesLocal

from .Constants import DIALOG_WORKFLOW_CODE_LOGGER_OBJECT, WorkflowActionEnum
from .ProfileContext import DialogWorkflowRecord
from .action import Action
from .utils import get_curr_state, update_profile_curr_state_in_db

user = UserContext()


class DialogWorkflowLocal(GenericCRUD, metaclass=MetaLogger, object=DIALOG_WORKFLOW_CODE_LOGGER_OBJECT):
    def __init__(self, is_test_data: bool = False) -> None:
        GenericCRUD.__init__(self, default_schema_name='dialog_workflow',
                             default_table_name='dialog_workflow_state_table',
                             default_view_table_name='dialog_workflow_state_view',
                             is_test_data=is_test_data)

    # TODO Please use MessagesLocal to store the message(s) recieved and anwers
    # TODO Please use the function defined in avatar similar to get_dialog_workflow_avatar_profile_id( profile_id1, prompt, group_id, profile_id2...) using avatar_table and avtar_group_table
    # TODO profile_curr_state_id
    def get_dialog_workflow_record(self, *, profile_curr_state: int, lang_code: LangCode,
                                   incoming_message: str = None) -> DialogWorkflowRecord:
        """Get all potential records in a specific state and choose randomly one of them"""
        select_clause_value = ("state_id, parent_state_id, workflow_action_id, lang_code, parameter1, variable1_id, "
                               "result_logical, result_figure_min, result_figure_max, next_state_id, "
                               "no_feedback_milliseconds, next_state_id_if_there_is_no_feedback")
        where = "state_id = %s AND lang_code = %s"
        if incoming_message and not incoming_message.isdigit() and not all(
                x.isdigit() for x in incoming_message.split(',')):
            # can't be WorkflowActionEnum.MENU_ACTION, as it is expecting number(s)
            where += " AND workflow_action_id <> " + str(WorkflowActionEnum.MENU_ACTION.value)
        optional_records = self.select_multi_dict_by_where(
            where=where, params=(profile_curr_state, lang_code.value), select_clause_value=select_clause_value)
        if not optional_records:
            raise Exception(f"No records found for state_id: {profile_curr_state} and language: {lang_code}")
        dialog_workflow_record = DialogWorkflowRecord(random.choice(optional_records))

        return dialog_workflow_record

    # TODO: get channel form campaign
    def post_message_and_get_message_json(self, *, incoming_message: str, channel_id: int = None,
                                          campaign_id: int = None, profile_id: int = None,
                                          previous_message_id: int = None) -> json:
        """This function is supposed to serve as a POST request using REST API.
        It runs until needing input from the user, which it then sends a JSON to the user with the message and exits
        param: incoming_message: the message to send"""
        # TODO: If it is an answer / forum response, write the answer to profile_question, and retrieve if already answered
        # TODO: get default variable for form - probably we have function
        # skip question if we have answer and it's not a form - move to next state
        incoming_message = incoming_message or ""
        profile_id = profile_id or user.get_effective_profile_id()
        lang_code = user.get_effective_profile_preferred_lang_code()
        # TODO Save the message using MessagesLocal (from DIALOG_WORKFLOW_PROFILE_ID, to UserContext.getEffectiveProfileId, ...)
        variables = VariablesLocal()
        # if incoming_message.isdigit():
        #     # TODO: get profile_curr_state from db
        #     update_profile_curr_state_in_db(new_state=profile_curr_state, profile_id=profile_id,
        #                                     channel_id=channel_id, campaign_id=campaign_id, message_id=previous_message_id)
        # else:
        if 1:
            profile_curr_state = get_curr_state(profile_id=profile_id, channel_id=channel_id,
                                                campaign_id=campaign_id, message_id=previous_message_id)
        got_response = incoming_message.strip() != ""  # This variable indicates if we must act now as we got a response from the user or as if we should send one to him
        init_action = Action(incoming_message=incoming_message, profile_id=profile_id,
                             lang_code=lang_code, profile_curr_state=profile_curr_state,
                             variables=variables)
        message_id = previous_message_id
        while True:
            dialog_workflow_record: DialogWorkflowRecord = self.get_dialog_workflow_record(
                profile_curr_state=init_action.profile_curr_state, lang_code=lang_code,
                incoming_message=incoming_message)
            selected_act = init_action.act(dialog_workflow_record, got_response)
            outgoing_message = selected_act.get("outgoing_message")
            # TODO Save the message using MessagesLocal (from DIALOG_WORKFLOW_PROFILE_ID, to UserContext.getEffectiveProfileId, ...)
            outgoing_compound_message_json = None
            if outgoing_message is not None:
                if isinstance(outgoing_message, dict):  # is form
                    outgoing_compound_message_json = json.dumps(outgoing_message)
                elif not isinstance(outgoing_message, list):
                    recipient = Recipient(profile_id=profile_id, preferred_lang_code_str=lang_code.value,
                                          user_id=user.get_effective_user_id(),
                                          first_name=user.get_real_name())
                    compound_message = CompoundMessage(original_body=outgoing_message, recipients=[recipient])
                    outgoing_compound_message_json = compound_message.get_compound_message_str()
                    # TODO: compound_message.get_message_id()
                    message_id = compound_message.message_ids[0] if compound_message.message_ids else None
                else:
                    outgoing_compound_message_json = outgoing_message
                # TODO insert message_table while message_source_subsystem_id=2, message_channel_id=14, dialog_workflow_state_id (currently called state_id)

            init_action.profile_curr_state = dialog_workflow_record.next_state_id if not selected_act.get(
                "is_state_changed") else init_action.profile_curr_state
            update_profile_curr_state_in_db(new_state=init_action.profile_curr_state, profile_id=profile_id,
                                            channel_id=channel_id, campaign_id=campaign_id, message_id=message_id)
            if outgoing_compound_message_json:
                return outgoing_compound_message_json
            got_response = False
