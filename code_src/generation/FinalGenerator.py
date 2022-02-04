from .seeder import random
from .StructGenerator import StructGenerator
from .generation_blocks import BLOCKS


class FinalGenerator(StructGenerator):
    def __init__(self):
        super().__init__()

    def generate(self):
        super().generate()
        nb_bedrock = random.randint(1, 3)
        self.resume_world[-1][:nb_bedrock] = [BLOCKS["BEDROCK"]]*nb_bedrock
