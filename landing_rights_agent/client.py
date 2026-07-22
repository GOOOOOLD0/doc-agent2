from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date
from typing import Any


class AgentAPIError(RuntimeError):
    """Raised when the model API cannot complete a request."""


def extract_output_text(response: dict[str, Any]) -> str:
    """Extract assistant text from a raw Responses API response."""
    direct = response.get("output_text")
    chunks: list[str] = []
    if isinstance(direct, str) and direct.strip():
        chunks.append(direct.strip())

    output_items = response.get("output", [])
    if not chunks:
        for item in output_items:
            if not isinstance(item, dict) or item.get("type") != "message":
                continue
            for content in item.get("content", []):
                if not isinstance(content, dict):
                    continue
                if content.get("type") in {"output_text", "text"}:
                    value = content.get("text")
                    if isinstance(value, str):
                        chunks.append(value)

    text = "\n".join(chunks).strip()
    if not text:
        raise AgentAPIError("模型响应中没有可读取的文本输出。")

    all_sources: list[tuple[str, str]] = []
    seen_urls: set[str] = set()
    for item in output_items:
        if not isinstance(item, dict):
            continue
        source_candidates: list[dict[str, Any]] = []
        action = item.get("action")
        if isinstance(action, dict):
            source_candidates.extend(
                source
                for source in action.get("sources", [])
                if isinstance(source, dict)
            )
        if item.get("type") == "message":
            for content in item.get("content", []):
                if not isinstance(content, dict):
                    continue
                source_candidates.extend(
                    annotation
                    for annotation in content.get("annotations", [])
                    if isinstance(annotation, dict)
                    and annotation.get("type") == "url_citation"
                )
        for source in source_candidates:
            url = source.get("url")
            if not isinstance(url, str) or not url.startswith(("http://", "https://")):
                continue
            if url in seen_urls:
                continue
            title = source.get("title")
            all_sources.append((str(title or url), url))
            seen_urls.add(url)

    cited_urls = {
        value.rstrip("/")
        for value in re.findall(r"\]\((https?://[^)\s]+)\)", text)
    }
    cited_search_sources = [
        (title, url)
        for title, url in all_sources
        if url.rstrip("/") in cited_urls
    ]
    if cited_search_sources:
        source_lines = ["## 正文实际引用的 API 搜索来源"]
        source_lines.extend(
            f"- [{title}]({url})" for title, url in cited_search_sources
        )
        text += "\n\n" + "\n".join(source_lines)

    web_search_count = 0
    for container_name in ("x_tools",):
        container = response.get(container_name)
        if not isinstance(container, dict):
            continue
        web_search = container.get("web_search")
        if isinstance(web_search, dict) and isinstance(web_search.get("count"), int):
            web_search_count = max(web_search_count, web_search["count"])

    usage = response.get("usage")
    if isinstance(usage, dict):
        plugins = usage.get("plugins")
        if isinstance(plugins, dict):
            web_search = plugins.get("web_search")
            if isinstance(web_search, dict) and isinstance(web_search.get("count"), int):
                web_search_count = max(web_search_count, web_search["count"])

    if all_sources and not web_search_count:
        web_search_count = 1
    if web_search_count:
        text += (
            f"\n\n> 联网核查日期：{date.today().isoformat()}；"
            f"API 搜索调用次数：{web_search_count}；"
            f"搜索返回 URL：{len(all_sources)} 个；"
            f"正文实际引用其中：{len(cited_search_sources)} 个。"
        )
    return text


@dataclass(frozen=True)
class ResponsesClient:
    api_key: str
    provider: str = "qwen"
    model: str = "qwen3.6-flash"
    reasoning_effort: str = "medium"
    timeout: int = 180
    base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    max_retries: int = 2

    @classmethod
    def from_env(
        cls,
        *,
        model: str | None = None,
        reasoning_effort: str | None = None,
        timeout: int = 180,
    ) -> "ResponsesClient":
        provider = os.environ.get("LANDING_RIGHTS_PROVIDER", "qwen").strip().lower()
        providers = {
            "qwen": {
                "api_key_env": "DASHSCOPE_API_KEY",
                "model": "qwen3.6-flash",
                "base_url_env": "DASHSCOPE_BASE_URL",
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            },
            "openai": {
                "api_key_env": "OPENAI_API_KEY",
                "model": "gpt-5.6-terra",
                "base_url_env": "OPENAI_BASE_URL",
                "base_url": "https://api.openai.com/v1",
            },
        }
        if provider not in providers:
            supported = ", ".join(sorted(providers))
            raise AgentAPIError(
                f"不支持的 LANDING_RIGHTS_PROVIDER={provider!r}；可选值：{supported}。"
            )

        settings = providers[provider]
        api_key_env = settings["api_key_env"]
        api_key = os.environ.get(api_key_env, "").strip()
        if not api_key:
            raise AgentAPIError(
                f"未设置 {api_key_env}。请复制 .env.example 为 .env，并填写 API Key。"
            )
        return cls(
            api_key=api_key,
            provider=provider,
            model=model
            or os.environ.get("LANDING_RIGHTS_MODEL", settings["model"]),
            reasoning_effort=reasoning_effort
            or os.environ.get("LANDING_RIGHTS_REASONING_EFFORT", "medium"),
            timeout=timeout,
            base_url=os.environ.get(settings["base_url_env"], settings["base_url"]).rstrip(
                "/"
            ),
        )

    def build_payload(
        self,
        *,
        instructions: str,
        input_text: str,
        web_search: bool = False,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "instructions": instructions,
            "input": input_text,
            "reasoning": {"effort": self.reasoning_effort},
            "store": False,
        }
        if self.provider == "openai":
            payload["text"] = {"verbosity": "medium"}
        if web_search:
            if self.provider == "qwen":
                # Qwen only permits required tool choice when exactly one tool is present.
                payload["tools"] = [{"type": "web_search"}]
                payload["tool_choice"] = "required"
                # Qwen rejects required tool choice while thinking mode is enabled.
                payload["reasoning"] = {"effort": "none"}
            else:
                payload["tools"] = [
                    {
                        "type": "web_search",
                        "search_context_size": "high",
                    }
                ]
                payload["tool_choice"] = "auto"
                payload["include"] = ["web_search_call.action.sources"]
        return payload

    def create(
        self,
        *,
        instructions: str,
        input_text: str,
        web_search: bool = False,
    ) -> str:
        payload = self.build_payload(
            instructions=instructions,
            input_text=input_text,
            web_search=web_search,
        )
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/responses",
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "satellite-landing-rights-agent/0.1",
            },
        )

        for attempt in range(self.max_retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    data = json.loads(response.read().decode("utf-8"))
                return extract_output_text(data)
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")
                retryable = exc.code == 429 or 500 <= exc.code < 600
                if retryable and attempt < self.max_retries:
                    time.sleep(2**attempt)
                    continue
                raise AgentAPIError(
                    f"{self.provider} API 返回 HTTP {exc.code}: {detail[:500]}"
                ) from exc
            except urllib.error.URLError as exc:
                if attempt < self.max_retries:
                    time.sleep(2**attempt)
                    continue
                raise AgentAPIError(
                    f"无法连接 {self.provider} API: {exc.reason}"
                ) from exc
            except json.JSONDecodeError as exc:
                raise AgentAPIError(
                    f"{self.provider} API 返回了无法解析的 JSON。"
                ) from exc

        raise AgentAPIError(f"{self.provider} API 请求失败。")


# 保留旧名称，避免已有调用方立刻失效。
OpenAIResponsesClient = ResponsesClient
