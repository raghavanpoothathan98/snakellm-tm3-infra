from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
from pydantic import BaseModel, Field, ConfigDict


class ContainerRef(BaseModel):
    model_config = ConfigDict(extra="allow")
    full_uri: Optional[str] = None


class ToolSpec(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str
    version: str
    container: Optional[ContainerRef] = None


class RuleSpec(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str
    shell_cmd: str
    resources: Optional[Dict[str, Any]] = None
    threads: Optional[int] = None


class PipelineSpec(BaseModel):
    model_config = ConfigDict(extra="allow")
    tools: List[ToolSpec]
    rules: List[RuleSpec]
    dag_edges: Optional[List[Tuple[str, str]]] = None