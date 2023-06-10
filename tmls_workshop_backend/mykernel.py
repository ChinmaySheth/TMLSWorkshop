import semantic_kernel as sk
import semantic_kernel.ai.open_ai as sk_oai
from semantic_kernel.utils.settings import openai_settings_from_dot_env

import asyncio
import sys
sys.path.append("./python")  # nopep8

kernel = sk.KernelBuilder.create_kernel()

model = "text-davinci-003"

# Configure AI backend used by the kernel
api_key, org_id = openai_settings_from_dot_env()
kernel.config.add_text_backend(
    "davinci-003", sk_oai.OpenAITextCompletion(model, api_key, org_id)
)

#advisor_query = "Find people in the Robinson family"
advisor_query = "Profiles between $500k and $2 million"

from semantic_kernel.kernel_extensions.import_semantic_skill_from_directory import import_semantic_skill_from_directory

skills_directory = "./backend/skills"
parsing_skill = import_semantic_skill_from_directory(kernel, skills_directory, "ParseIntentSkill")

summary = asyncio.run(kernel.run_on_str_async(advisor_query, parsing_skill["ParseUserSearchSteps"]))
output = str(summary.variables).strip()
print("Output: " + output)
