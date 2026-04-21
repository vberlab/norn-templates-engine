Norn template engine

Базовая структура проекта
api/ 
render/ - пакет с модулями оркестрации. 
template_engine/ - базовый рендер
template_source/ - источник данных по шаблонам(работа с ФС)

Запрос
api
→ render
  → source (loader/read)
  → dependency_resolver
  → template_engine
→ response

Ключевые ограничения
template_engine не зависит от source
source не знает про render
render — единственное место, где всё соединяется

Pipeline данных
template_source слой:
  source -> manifest -> index -> loader

render слой:
  request -> context -> fragment check -> load -> engine -> result

# Render Pipeline

## Input

```json
{
  "template": "templates/nginx/common/template.j2",
  "context": {
    "server_name": "example.com"
  },
  "fragments": [
    "templates/nginx/common/include/debug_locations.j2"
  ]
}

## Context processing 
{
  "server_name": "example.com",
  "fragments": {
    "debug_locations": "templates/nginx/common/include/debug_locations.j2"
  }
}

## Repository index 
{
  "templates": {
    "templates/nginx/common/template.j2": {
      "path": "templates/nginx/common/template.j2"
    }
  },
  "fragments": {
    "templates/nginx/common/include/debug_locations.j2": {
      "path": "templates/nginx/common/include/debug_locations.j2",
      "owner": "templates/nginx/common/template.j2"
    }
  }
}

## Fragment validation
[
  "templates/nginx/common/include/debug_locations.j2"
]

## Loader output
{
  "entrypoint": "templates/nginx/common/template.j2",
  "templates_map": {
    "templates/nginx/common/template.j2": "server { ... }",
    "templates/nginx/common/include/debug_locations.j2": "location /debug/ { ... }"
  },
  "selected_fragments": {
    "debug_locations": "templates/nginx/common/include/debug_locations.j2"
  }
}

## Template engine input
{
  "entrypoint": "templates/nginx/common/template.j2",
  "templates_map": { "...": "..." },
  "context": {
    "server_name": "example.com",
    "fragments": {
      "debug_locations": "templates/nginx/common/include/debug_locations.j2"
    }
  }
}

## Output result
{
  "content": "server { listen 80; server_name example.com; ... }"
}

## Full pipeline 
TemplateSource
→ RepositoryIndexer (RepoManifest)
→ RepositoryIndex
→ TemplateLoader

RenderRequest
→ ContextProcessor
→ FragmentChecker
→ TemplateLoader
→ TemplateEngine
→ RenderResult

