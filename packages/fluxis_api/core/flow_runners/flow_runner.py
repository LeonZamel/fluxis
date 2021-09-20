from fluxis_engine.core.flow import Flow


class FlowRunner:
    def __init__(self, flow: Flow):
        self.flow = flow

    def run(self):
        """
        Override this
        """
        pass
