from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from aiagent.tools.custom_tool import ExportMarkdownPDF
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

@CrewBase
class Aiagent():

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    llm_hug= LLM(
        model="huggingface/Qwen/Qwen3-32B"
    )

    llm_groq = LLM(
        model="groq/qwen-qwq-32b"
    )

    llm_llama = LLM(
        model="ollama/mistral-nemo:latest",
        base_url="http://localhost:11434"
    )

    @agent
    def agent_recherche(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_recherche'],
            verbose=True,
            tools=[search_tool],
            llm=self.llm_llama
        )

    @agent
    def agent_redaction(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_redaction'],
            verbose=True,
            llm=self.llm_groq
        )

    @agent
    def agent_reviseur(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_reviseur'],
            verbose=True,
            llm=self.llm_hug
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



