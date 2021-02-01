from inspect import iscoroutinefunction


class Events:
    def __init__(self):
        self._event_slots = dict()

    def register(self, event_name, callback):
        if event_name not in self._event_slots:
            self._event_slots[event_name] = list()
        self._event_slots[event_name].append(callback)

    async def fire(self, event_name, *a, **kw):
        if event_name not in self._event_slots:
            return
        for callback in self._event_slots[event_name]:
            if iscoroutinefunction(callback):
                await callback(*a, **kw)
            else:
                callback(*a, **kw)
