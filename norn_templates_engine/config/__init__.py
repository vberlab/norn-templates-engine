"""
    App config collections class
"""
from dataclasses import dataclass

class ConfigModel:
    @dataclass(frozen=True, slots=True)
    class Api:
        host: str
        port: int

    @dataclass(frozen=True, slots=True)
    class TemplateSource:
        type: str

    @dataclass(frozen=True, slots=True)
    class TemplateFsSource:
        root: str

    @dataclass(frozen=True, slots=True)
    class TemplateGitSource:
        url: str
        branch: str
        root: str

    @dataclass(frozen=True, slots=True)
    class TemplateLocalCacheDir:
        path: str

    @dataclass(frozen=True, slots=True)
    class TemplateEngine:
        strict_undefined: bool
        trim_blocks: bool
        lstrip_blocks: bool

    @dataclass(frozen=True, slots=True)
    class ContextPolicy:
        allow_unknown_fields: bool

    @dataclass(frozen=True, slots=True)
    class Logging:
        level: str

@dataclass(frozen=True, slots=True)
class AppConfig:
    api: ConfigModel.Api
    template_source: ConfigModel.TemplateSource
    template_fs_source: ConfigModel.TemplateFsSource | None
    template_git_source: ConfigModel.TemplateGitSource | None
    template_local_cache_dir: ConfigModel.TemplateLocalCacheDir | None
    template_engine: ConfigModel.TemplateEngine
    context_policy: ConfigModel.ContextPolicy
    logging: ConfigModel.Logging