from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *
from typing import List, Dict
import re


class LLMRequestStep(DataStep):
    def execute(self, context):
        """
        Execute the LLM request step
        :param context:
        :return:
        """
        try:
            if context.get('skip_prompt_generation'):
                return

            llm_instance = context.get('llm_instance')
            messages = context.get('llm_messages')

            if context.get('verbose'):
                logger.info(f"{self.name}: Sending the following messages to the LLM: {messages}")

            try:
                response = llm_instance.chat(messages)
            except Exception as e:
                if context.get('verbose'):
                    logger.error(f"{self.name}: An error occurred during LLM request: {e}")
                context['llm_response'] = None
                return

            if context.get('verbose'):
                logger.info(f"{self.name}: Received the following response from the LLM: {response}")

            if not response:
                if context.get('verbose'):
                    logger.error(f"{self.name}: LLM request returned no valid response")
                context['llm_response'] = None
            else:
                context['llm_response'] = self.extract_queries(response)
                if context.get('verbose'):
                    logger.info(f"{self.name}: LLM request completed")
        except Exception as e:
            if context.get('verbose'):
                logger.error(f"{self.name}: An error occurred during LLM request: {e}")
            context['llm_response'] = None
            return

    @staticmethod
    def extract_queries(response: str) -> Dict[str, List[str]]:
        blocks = re.findall(r"####\s*START\s*(.*?)####\s*END\s*", response, re.DOTALL)
        if not blocks:
            raise ValueError("The response does not contain valid blocks delimited by #### START and #### END.")

        queries = {'chart': [], 'table': []}
        for block in blocks:
            block_type_match = re.search(r"##\s*(Table|Chart)\s*:", block)
            if not block_type_match:
                continue
            block_type = block_type_match[1].strip().lower()
            query_match = re.search(r"```sql\s*(.*?)\s*```", block, re.DOTALL)
            if not query_match:
                continue
            query = query_match[1].strip()
            if not query.startswith("SELECT"):
                if "SELECT" not in query:
                    raise ValueError("The query does not start with 'SELECT' keyword.")
                else:
                    query = query[query.index("SELECT"):]
            queries[block_type].append(query)

        return queries
