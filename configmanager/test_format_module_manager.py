from configmanager.format_module_manager import ModuleManager

def test_inizialization() -> None:
    moduleManager = ModuleManager()
    assert moduleManager is not None


def test_collect_modules() -> None:
    moduleManager = ModuleManager()
    modules_in_file:list = ModuleManager.get_modules()
    assert len(modules_in_file) > 0
