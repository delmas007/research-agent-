from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from aiagent.tools.custom_tool import ExportMarkdownPDF
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

@CrewBase
class Aiagent():

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def agent_recherche(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_recherche'],
            verbose=True,
            tools=[search_tool]
        )

    @agent
    def agent_redaction(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_redaction'],
            verbose=True
        )

    @agent
    def agent_reviseur(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_reviseur'],
            verbose=True
        )


    @task
    def task_recherche(self) -> Task:
        return Task(
            config=self.tasks_config['task_recherche'],
        )

    @task
    def task_redaction(self) -> Task:
        return Task(
            config=self.tasks_config['task_redaction'],
        )

    @task
    def task_revision(self) -> Task:
        return Task(
            config=self.tasks_config['task_revision'],
            # output_file='report.md'
        )


    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
# result = Aiagent().crew().kickoff(inputs={
#                 "topic": "Intelligence artificielle et éthique",
#             })



