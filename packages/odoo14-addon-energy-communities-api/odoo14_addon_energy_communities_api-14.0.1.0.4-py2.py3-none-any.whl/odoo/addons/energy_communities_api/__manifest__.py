{
    "name": "Energy Communities API/REST addon",
    "summary": """
        API/REST endpoints for energy communities
    """,
    "description": """
        This addon enables an API/REST communication with energy communities platform based in Fastapi framework
    """,
    "author": "Coopdevs Treball SCCL & Som Energia SCCL & SomIT",
    "website": "https://coopdevs.org",
    "category": "Customizations",
    "version": "14.0.1.0.4",
    "depends": ["energy_communities"],
    "external_dependencies": {"python": ["httpx>=0.27.0"]},
    "data": [
        "data/fastapi_endpoint_data.xml",
        "security/res_users_role_data.xml",
        "security/ir_rule_data.xml",
    ],
}
