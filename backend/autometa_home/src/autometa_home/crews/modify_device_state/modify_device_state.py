from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task 
import os
from src.autometa_home.types import validate_result_format_new_state


# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ModifyDeviceState():
	"""ModifyDeviceState crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	deepseek_reasoner_r1 = LLM(
		model=os.getenv("MODEL"),
		base_url=os.getenv("BASE_URL"),
		api_key=os.getenv("OPENAI_API_KEY"),
	)

	@agent
	def device_action_modifier(self) -> Agent:
		print(self.agents_config)
		return Agent(
			config=self.agents_config['device_action_modifier'],
			verbose=True,
			llm=self.deepseek_reasoner_r1,
		)

	# @agent
	# def reporting_analyst(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['reporting_analyst'],
	# 		verbose=True
	# 	)

	@task
	def device_action_modifying(self) -> Task:
		return Task(
			config=self.tasks_config['device_action_modifying'],
			guardrail=validate_result_format_new_state,
		)

	# @task
	# def reporting_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['reporting_task'],
	# 		output_file='report.md'
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the ModifyDeviceState crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
