"""
    App configuration schema
"""
APP_CONFIG_SCHEMA = {
    "api": {
        "type": dict,
        "required": True,
        "schema": {
            "host": {
                "type": str,
                "default": "127.0.0.1"
            },
            "port": {
                "type": int,
                "default": 8080
            }
        }
    },
    "template_source": {
        "type": str,
        "required": True,
        "allowed": ["git", "fs"],
        "dependency": ["template_fs_source", "template_git_source"]
    },
    "template_fs_source": {
        "type": dict,
        "required": False,
        "schema": {
            "root": {
                "type": str,
                "required": True
            }
        }
    },
    "template_git_source": {
        "type": dict,
        "required": False,
        "schema": {
            "url": {
                "type": str,
                "required": True,
            },
            "branch": {
                "type": str,
                "required": False,
                "default": "master"
            },
            "root": {
                "type": str,
                "required": False,
                "default": "./"
            }
        }
    },
    "template_local_cache_dir": {
        "type": str | None,
        "default": None
    },
    "template_engine": {
        "type": dict,
        "required": False,
        "default": {},
        "schema": {
            "strict_undefined": {
                "type": bool,
                "default": True
            },
            "trim_blocks": {
                "type": bool,
                "default": True
            },
            "lstrip_blocks": {
                "type": bool,
                "default": True,
            }
        }
    },
    "context_policy": {
        "type": dict,
        "required": False,
        "default": {},
        "schema": {
            "allow_unknown_fields": {
                "type": bool,
                "default": False
            }
        }
    },
    "logging": {
        "type": dict,
        "required": False,
        "default": {},
        "schema": {
            "level": {
                "type": str,
                "default": "INFO",
                "allowed": ("DEBUG", "INFO", "WARNING", "ERROR")
            },
            "format": {
                "type": str,
                "default": (
                    "%(asctime)s ",
                    "[%(levelname)s] ",
                    "%(name)s ",
                    "%(message)s "
                )
            }
        }
    }
}