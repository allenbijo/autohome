from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os

from src.autometa_home.types import validate_result_format_devices

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class DeviceManager():
	"""DeviceManager crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	deepseek_reasoner_r1 = LLM(
		model=os.getenv("MODEL"),
		base_url=os.getenv("BASE_URL"),
		api_key=os.getenv("OPENAI_API_KEY"),
	)

	@agent
	def device_picker(self) -> Agent:
		return Agent(
			config=self.agents_config['device_picker'],
			verbose=True
		)

	@task
	def device_picking(self) -> Task:
		return Task(
			config=self.tasks_config['device_picking'],
			guardrail=validate_result_format_devices,
		)


	@crew
	def crew(self) -> Crew:
		"""Creates the DeviceManager crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
