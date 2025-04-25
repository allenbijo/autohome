#!/usr/bin/env python
from pydantic import BaseModel
import asyncio

from crewai.flow import Flow, listen, start

# from autometa_home.crews.nlp_crew.nlp_crew import PoemCrew
from crews.nlp_crew.intent_processing import Intent2Action
from crews.device_picker.device_picker import DeviceManager
from crews.modify_device_state.modify_device_state import ModifyDeviceState

import json

import winsound #remove later

class HomeState(BaseModel):
    input_text: str = ""
    home_desc_dict: dict = {}
    current_home_state: dict = {}
    identified_actions: list = []
    actions_to_perform: list = []
    new_states: list = []


class HomeFlow(Flow[HomeState]):

    @start()
    def get_home_state(self):
        with open("device_types.json", "r") as f:
            self.state.home_desc_dict = json.load(f)
        with open("state.json", "r") as f:
            self.state.current_home_state = json.load(f)

    @listen(get_home_state)
    def nlp_processing(self):
        result = (
            Intent2Action()
            .crew()
            .kickoff(inputs={"home_state": self.state.home_desc_dict,
                             "intent": self.state.input_text})
        )

        print("Identified actions: ", result.raw)
        self.state.identified_actions = eval(result.raw)

    @listen(nlp_processing)
    async def pick_devices(self):
        tasks = []

        async def run_for_type(devices, action):
            result = (
                DeviceManager()
                .crew()
                .kickoff(inputs={"current_states": devices,
                                 "action": action})
            )
            for device in eval(result.raw):
                self.state.actions_to_perform.append((devices[device], action, device))
            return result.raw

        for change in self.state.identified_actions:
            device_type, room = change[0], change[1]
            devices = self.state.current_home_state[device_type][room]
            tasks.append(asyncio.create_task(run_for_type(devices, change[2])))

        asyncio.gather(*tasks)

    @listen(pick_devices)
    async def update_state(self):
        tasks = []
        
        async def run_for_device(device):
            result = (
                ModifyDeviceState()
                .crew()
                .kickoff(inputs={"state": device[0],
                                "action": device[1]})
            )
            
            self.state.new_states.append({device[2]: eval(result.raw)})
            # for device_type in self.state.current_home_state:
            #     for room in self.state.current_home_state[device_type]:
            #         for device in self.state.current_home_state[device_type][room]:
            #             if device == device[2]:
            #                 for state in change:
            #                     self.state.current_home_state[device_type][room][device][state] = change[state]

            
        for device in self.state.actions_to_perform:
            tasks.append(asyncio.create_task(run_for_device(device)))
            
        asyncio.gather(*tasks)
        
    @listen(update_state)
    def save_state(self):
        print(self.state.new_states)



def kickoff(input = "Turn on the lights"):
    home_flow = HomeFlow()
    home_flow.state.input_text = input
    home_flow.kickoff()
    return home_flow.state.new_states


def plot():
    poem_flow = HomeFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
    winsound.Beep(2500, 500)
