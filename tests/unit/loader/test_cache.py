import pytest
from norn_templates_engine.loader.base import TemplateRepoCache
from norn_templates_engine.loader.base import TemplatePack
from norn_templates_engine.loader import errors

def test_cache_add_duplicate_raises():
    cache = TemplateRepoCache()
    pack = TemplatePack(
        name="test_pack",
        path="/templates/test_pack",
        content="<test content string>",
        includes={
            "include_part": "/templates/test_pack/include/include_part",
            "include_second_part": "/templates/test_pack/include/include_second_part"
        },
        service_type="nginx"
    )
    cache.add(pack)
    with pytest.raises(errors.TemplateCachheExists):
        cache.add(pack)

def test_cache_update_replaces():
    cache = TemplateRepoCache()
    pack = TemplatePack(
        name="test_pack",
        path="/templates/test_pack",
        content="<test content string>",
        includes={
            "include_part": "/templates/test_pack/include/include_part",
            "include_second_part": "/templates/test_pack/include/include_second_part"
        },
        service_type="nginx"
    )
    updated_pack = TemplatePack(
        name="test_pack",
        path="/templates/test_pack",
        content="<updated content string>",
        includes={
            "include_part": "/templates/test_pack/include/include_part",
            "include_second_part": "/templates/test_pack/include/include_second_part"
        },
        service_type="nginx"
    )
    cache.add(pack)
    cache.update(updated_pack)

    assert cache.template_packs[updated_pack.name].content == updated_pack.content


