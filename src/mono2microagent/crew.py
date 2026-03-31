import os
from pathlib import Path
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.mcp import MCPServerHTTP, create_static_tool_filter

@CrewBase
class ArchaionCrew():
    """Archaion Modernization Crew for Mainframe and Monolith Transformation"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        api_key = openrouter_api_key or openai_api_key
        is_openrouter_key = bool(api_key and api_key.startswith("sk-or-"))
        base_url = os.getenv("OPENAI_BASE_URL") or ("https://openrouter.ai/api/v1" if (openrouter_api_key or is_openrouter_key) else None)
        model = os.getenv("MODEL") or "openai/gpt-4o-mini"

        if not api_key:
            raise ValueError("Missing API key. Set OPENAI_API_KEY or OPENROUTER_API_KEY.")

        if base_url and not os.getenv("OPENAI_BASE_URL"):
            os.environ["OPENAI_BASE_URL"] = base_url

        self.llm = LLM(model=model, base_url=base_url, api_key=api_key)

        cast_endpoint = os.getenv("CAST_ENDPOINT")
        cast_api_key = os.getenv("CAST_X_API_KEY")
        self.cast_server = (
            MCPServerHTTP(
                url=cast_endpoint,
                headers={
                    "x-api-key": cast_api_key,
                    "Content-Type": "application/json",
                },
                cache_tools_list=True,
                tool_filter=create_static_tool_filter(
                    allowed_tool_names=[
                        "application_database_explorer",
                        "transaction_graph",
                        "transaction_graphs",
                        "application_iso_5055_explorer",
                    ]
                ),
            )
            if cast_endpoint and cast_api_key
            else None
        )

    @agent
    def mono2microAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['mono2microAgent'],
            llm=self.llm,
            mcps=[self.cast_server] if self.cast_server else [],
            verbose=True,
            memory=False
        )

    @task
    def refactoring_blueprint_task(self) -> Task:
        return Task(
            config=self.tasks_config['refactoring_blueprint_task'],
            output_file=os.getenv("ARCHAION_OUTPUT_FILE") or "refactoring_blueprint.md",
        )

    @crew
    def crew(self) -> Crew:
        local_storage_root = str(Path.cwd() / ".crewai")
        os.environ.setdefault("USERPROFILE", str(Path.cwd()))
        os.environ.setdefault("HOME", str(Path.cwd()))
        os.environ.setdefault("LOCALAPPDATA", local_storage_root)
        os.environ.setdefault("APPDATA", local_storage_root)
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
