from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
from src.autometa_home.types import validate_result_format_tasks

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class Intent2Action:
    """NLP Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    deepseek_reasoner_r1 = LLM(
        model=os.getenv("MODEL"),
        base_url=os.getenv("BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    @agent
    def intent_identifier(self) -> Agent:
        return Agent(
            config=self.agents_config["intent_identifier"],
            llm=self.deepseek_reasoner_r1,
        )

    @agent
    def action_identifier(self) -> Agent:
        return Agent(
            config=self.agents_config["action_identifier"],
            llm=self.deepseek_reasoner_r1,
        )

    @task
    def intent_identifying(self) -> Task:
        return Task(
            config=self.tasks_config["intent_identifying"],
        )

    @task
    def action_identifying(self) -> Task:
        return Task(
            config=self.tasks_config["action_identifying"],
            guardrail=validate_result_format_tasks,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
