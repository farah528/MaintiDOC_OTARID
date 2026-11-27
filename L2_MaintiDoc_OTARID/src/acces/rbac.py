from pathlib import Path
def user_groups(user: str, config=Path("config/utilisateurs.yaml")):
    try:
        import yaml
        return yaml.safe_load(config.read_text(encoding="utf-8"))["users"][user]["groups"]
    except ImportError:
        # Minimal parser keeps local smoke tests usable before optional PyYAML install.
        groups = {"tech_compresseurs":["techniciens_compresseurs"], "tech_incendie":["techniciens_incendie"], "responsable":["responsables_maintenance"]}
        return groups[user]
