from datadashr.config import *


class DataStep:
    def __init__(self, name):
        """
        Constructor for DataStep
        :param name:
        """
        self.name = name

    def execute(self, context):
        """
        Execute the data step
        :param context:
        :return:
        """
        raise NotImplementedError("Each step must implement the execute method")

    def __or__(self, other):
        if isinstance(other, DataStep):
            return DataStepGroup([self, other])
        elif isinstance(other, DataStepGroup):
            return DataStepGroup([self] + other.steps)
        else:
            raise ValueError("Unsupported type for concatenation with DataStep")


class DataStepGroup(DataStep):
    def __init__(self, steps):
        self.steps = steps
        super().__init__("DataStepGroup")

    def execute(self, context):
        for step in self.steps:
            step.execute(context)
