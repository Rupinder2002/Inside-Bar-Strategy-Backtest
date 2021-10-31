# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.types import DomainDict
from database import UpdateUserDetails
from readdatadb import fetch_about_program, fetch_deadline, fetch_how_to_apply, fetch_link, fetch_who_can_apply
class ValidateUserDetailsForm(Action):
    def name(self) -> Text:
        return "user_details_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["username", "email", "userLanguage", "password"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not yet filled, request user to fill this slot next
                return [SlotSet("requested_slot", slot_name)]

        # All slots filled 
        return [SlotSet("requested_slot", None)]
    

#class UserDetailsSubmit(Action):
 #   def name(self) -> Text:
  #      return "action_userdetails_submit"

   # def run(
    #    self,
     #   dispatcher: CollectingDispatcher,
      #  tracker: Tracker,
       # domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #dispatcher.utter_message(template="utter_confirm_details")
    
class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker:Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_thankyou_details", username = tracker.get_slot("username"), email = tracker.get_slot("email"), userLanguage = tracker.get_slot("userLanguage"), password = tracker.get_slot("password"))
        UpdateUserDetails(tracker.get_slot("username"),tracker.get_slot("email"), tracker.get_slot("userLanguage"), tracker.get_slot("password"))
        dispatcher.utter_message("Thank You for your valuable time and information. Info has been saved in our records.")
        dispatcher.utter_message(template = "utter_ask_type_program_info")
        return []

class ProgramNameForm(Action):
    def name(self) -> Text:
        return "program_name_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["program_name"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not yet filled, request user to fill this slot next
                print("result00",slot_name)
                return [SlotSet("requested_slot", slot_name)]

        # All slots filled 
        return [SlotSet("requested_slot", None)]


class AboutProgram(Action):
    def name(self) -> Text:
        return "action_about_program"

    def run(
        self,
        dispatcher,
        tracker:Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text,Any]]:
        
        result = fetch_about_program(tracker.get_slot("program_name"))
        result = str(result)
       
        dispatcher.utter_message(result)
        dispatcher.utter_message(response="utter_know_more_education_part")
        return []

class WhoCanApply(Action):
    def name(self) -> Text:
        return "action_who_can_apply"

    def run(
        self,
        dispatcher,
        tracker:Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text,Any]]:
        
        result = fetch_who_can_apply (tracker.get_slot("program_name"))
        result = str(result)
       
        dispatcher.utter_message(result)
        dispatcher.utter_message(template="utter_know_more_education_part")
        return []

class Deadline(Action):
    def name(self) -> Text:
        return "action_deadline"

    def run(
        self,
        dispatcher,
        tracker:Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text,Any]]:
        
        result = fetch_deadline(tracker.get_slot("program_name"))
        result = str(result)
       
        dispatcher.utter_message(result)
        dispatcher.utter_message(template="utter_know_more_education_part")
        return []

class HowToApply(Action):
    def name(self) -> Text:
        return "action_how_to_apply"

    def run(
        self,
        dispatcher,
        tracker:Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text,Any]]:
        
        result = fetch_how_to_apply(tracker.get_slot("program_name"))
        result = str(result)
       
        dispatcher.utter_message(result)
        dispatcher.utter_message(template="utter_know_more_education_part")
        return []
class Link(Action):
    def name(self) -> Text:
        return "action_link"

    def run(
        self,
        dispatcher,
        tracker:Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text,Any]]:
        
        result = fetch_link(tracker.get_slot("program_name"))
        result = str(result)
       
        dispatcher.utter_message(result)
        #dispatcher.utter_message(response="utter_know_more_education_part")
        return []

class getUserId(Action):
    def name(self) -> Text:
        return "getUserId"

    def run(
        self,
        dispatcher,
        tracker:Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text,Any]]:
        
        userId = tracker.get_slot("userId")
        print("userId",userId)
        # dispatcher.utter_message(result)
        #dispatcher.utter_message(response="utter_know_more_education_part")
        return [SlotSet("userId",userId)]


 