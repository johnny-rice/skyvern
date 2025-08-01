from typing import Awaitable, Callable

from anthropic import AsyncAnthropic, AsyncAnthropicBedrock
from fastapi import FastAPI
from openai import AsyncAzureOpenAI, AsyncOpenAI

from skyvern.forge.agent import ForgeAgent
from skyvern.forge.agent_functions import AgentFunction
from skyvern.forge.sdk.api.llm.api_handler_factory import LLMAPIHandlerFactory
from skyvern.forge.sdk.artifact.manager import ArtifactManager
from skyvern.forge.sdk.artifact.storage.factory import StorageFactory
from skyvern.forge.sdk.artifact.storage.s3 import S3Storage
from skyvern.forge.sdk.cache.factory import CacheFactory
from skyvern.forge.sdk.db.client import AgentDB
from skyvern.forge.sdk.experimentation.providers import BaseExperimentationProvider, NoOpExperimentationProvider
from skyvern.forge.sdk.schemas.organizations import Organization
from skyvern.forge.sdk.settings_manager import SettingsManager
from skyvern.forge.sdk.trace import TraceManager
from skyvern.forge.sdk.trace.lmnr import LaminarTrace
from skyvern.forge.sdk.workflow.context_manager import WorkflowContextManager
from skyvern.forge.sdk.workflow.service import WorkflowService
from skyvern.webeye.browser_manager import BrowserManager
from skyvern.webeye.persistent_sessions_manager import PersistentSessionsManager
from skyvern.webeye.scraper.scraper import ScrapeExcludeFunc

SETTINGS_MANAGER = SettingsManager.get_settings()
DATABASE = AgentDB(
    SettingsManager.get_settings().DATABASE_STRING,
    debug_enabled=SettingsManager.get_settings().DEBUG_MODE,
)
if SettingsManager.get_settings().SKYVERN_STORAGE_TYPE == "s3":
    StorageFactory.set_storage(S3Storage())
STORAGE = StorageFactory.get_storage()
CACHE = CacheFactory.get_cache()
ARTIFACT_MANAGER = ArtifactManager()
BROWSER_MANAGER = BrowserManager()
EXPERIMENTATION_PROVIDER: BaseExperimentationProvider = NoOpExperimentationProvider()
LLM_API_HANDLER = LLMAPIHandlerFactory.get_llm_api_handler(SettingsManager.get_settings().LLM_KEY)
OPENAI_CLIENT = AsyncOpenAI(api_key=SettingsManager.get_settings().OPENAI_API_KEY or "")
if SettingsManager.get_settings().ENABLE_AZURE_CUA:
    OPENAI_CLIENT = AsyncAzureOpenAI(
        api_key=SettingsManager.get_settings().AZURE_CUA_API_KEY,
        api_version=SettingsManager.get_settings().AZURE_CUA_API_VERSION,
        azure_endpoint=SettingsManager.get_settings().AZURE_CUA_ENDPOINT,
        azure_deployment=SettingsManager.get_settings().AZURE_CUA_DEPLOYMENT,
    )
ANTHROPIC_CLIENT = AsyncAnthropic(api_key=SettingsManager.get_settings().ANTHROPIC_API_KEY)
if SettingsManager.get_settings().ENABLE_BEDROCK_ANTHROPIC:
    ANTHROPIC_CLIENT = AsyncAnthropicBedrock()

# Add UI-TARS client setup
UI_TARS_CLIENT = None
if SettingsManager.get_settings().ENABLE_VOLCENGINE:
    UI_TARS_CLIENT = AsyncOpenAI(
        api_key=SettingsManager.get_settings().VOLCENGINE_API_KEY,
        base_url=SettingsManager.get_settings().VOLCENGINE_API_BASE,
    )

SECONDARY_LLM_API_HANDLER = LLMAPIHandlerFactory.get_llm_api_handler(
    SETTINGS_MANAGER.SECONDARY_LLM_KEY if SETTINGS_MANAGER.SECONDARY_LLM_KEY else SETTINGS_MANAGER.LLM_KEY
)
SELECT_AGENT_LLM_API_HANDLER = (
    LLMAPIHandlerFactory.get_llm_api_handler(SETTINGS_MANAGER.SELECT_AGENT_LLM_KEY)
    if SETTINGS_MANAGER.SELECT_AGENT_LLM_KEY
    else SECONDARY_LLM_API_HANDLER
)
SINGLE_CLICK_AGENT_LLM_API_HANDLER = (
    LLMAPIHandlerFactory.get_llm_api_handler(SETTINGS_MANAGER.SINGLE_CLICK_AGENT_LLM_KEY)
    if SETTINGS_MANAGER.SINGLE_CLICK_AGENT_LLM_KEY
    else SECONDARY_LLM_API_HANDLER
)
WORKFLOW_CONTEXT_MANAGER = WorkflowContextManager()
WORKFLOW_SERVICE = WorkflowService()
AGENT_FUNCTION = AgentFunction()
PERSISTENT_SESSIONS_MANAGER = PersistentSessionsManager(database=DATABASE)
scrape_exclude: ScrapeExcludeFunc | None = None
authentication_function: Callable[[str], Awaitable[Organization]] | None = None
authenticate_user_function: Callable[[str], Awaitable[str | None]] | None = None
setup_api_app: Callable[[FastAPI], None] | None = None

agent = ForgeAgent()

if SettingsManager.get_settings().TRACE_ENABLED:
    if SettingsManager.get_settings().TRACE_PROVIDER == "lmnr":
        TraceManager.set_trace_provider(LaminarTrace(api_key=SettingsManager.get_settings().TRACE_PROVIDER_API_KEY))
