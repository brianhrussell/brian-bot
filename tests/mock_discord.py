from unittest import mock
import sys
import types

module_name = 'discord'
bogus_module = types.ModuleType(module_name)
sys.modules[module_name] = bogus_module
bogus_module.User = mock.Mock(name=module_name+'.User')
bogus_module.Guild = mock.Mock(name=module_name+'.Guild')
bogus_module.HTTPException = mock.Mock(name=module_name+'.HTTPException')
bogus_module.Client = mock.Mock(name=module_name+'.Client')