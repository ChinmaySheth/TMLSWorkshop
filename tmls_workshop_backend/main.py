from fastapi import FastAPI, HTTPException
import json
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAITextCompletion
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from pydantic import BaseModel
import ast
import pandas as pd

app = FastAPI()

kernel = None
data = None

# This is a horrible practice. Please remove before moving to production.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"status": "SUCCESS"}

@app.get("/invocations")
def invocations():
    return {"status": "SUCCESS"}

@app.get("/user-list")
def user_list():
    with open('data/sample_data.json') as f:
        data = json.load(f)

    return {"data": data}

class TextInputForLLM(BaseModel):
    textInputForGPT: str


def validate_search_steps(steps_list):
    "TODO: Validating the data type of a parameter, etc."
    valid_params_dict = {"filterLocation": {"search_postal": True, "search_city": True, "search_province": True},
                         "filterNetWorth": {"lower_limit": True, "upper_limit": True},
                         "filterName": {"search_name": True},
                         "filterCompany": {"search_company": True}
                        }
    for step in steps_list:
        if "step" not in step or step["step"] not in valid_params_dict or "params" not in step:
            return False
        
        for param in step["params"]:
            if param not in valid_params_dict[step["step"]]:
                return False

    return True


def validate_profiles(profiles):
    column_list = ["ID", "name", "gender", "age", "company_name", "years_at_current_company", "n_previous_jobs", "net_worth", "postal_code", "city", "province", "street", "person_2", "relationship"]
    for profile in profiles:
        for key in profile.keys():
            if key not in column_list:
                return False
            
    return True

@app.post("/chat")
def generate_llm_response(textInputForGPT: TextInputForLLM):
    global kernel
    if kernel == None:
        start_kernel()

    #Validation skills
    skills = kernel.import_semantic_skill_from_directory("skills", "ParseIntentSkill")
    check_valid_search = skills["CheckValidSearch"]
 
    is_search_valid = check_valid_search(str(textInputForGPT.textInputForGPT))

    if not is_search_valid:
        response = create_response(str(textInputForGPT.textInputForGPT), False, False, [])
        return {"data": [], "msg": response} 
        #raise HTTPException(status_code=404, detail="Search query is not valid.")

    parse_user_search_steps = skills["ParseUserSearchSteps"]
    search_steps_list = parse_user_search_steps(str(textInputForGPT.textInputForGPT)).result

    #Syntax check
    try:
        result = ast.literal_eval(search_steps_list)
    except:
        response = create_response(str(textInputForGPT.textInputForGPT), True, False, [])
        return {"data": [], "msg": response} 
        #raise HTTPException(status_code=404, detail="Search steps not valid.")

    #Semantic check
    are_search_steps_valid = validate_search_steps(result)

    if not are_search_steps_valid:
        response = create_response(str(textInputForGPT.textInputForGPT), True, False, [])
        return {"data": [], "msg": response} 
        #raise HTTPException(status_code=404, detail="Search steps not valid.")
    

    #Native skill
    native_skill = kernel.import_native_skill_from_directory("skills", "FilterSkill")
    filter_location = native_skill["filterLocation"]
    filter_networth = native_skill["filterNetWorth"]
    filter_name = native_skill["filterName"]
    filter_company = native_skill["filterCompany"]
    input="data/sample_data.json"
    output_profiles_list = []

    #print(result) This is correct
    #Execute the skills on the data
    for step_count, step in enumerate(result):
        
        if step_count == 0:
            profiles_list = pd.read_json(input)
        else:
            profiles_list = pd.DataFrame(output_profiles_list)
        if step["step"] == "filterLocation":
            context_variables = sk.ContextVariables(variables={
                "search_postal": step["params"]["search_postal"],
                "search_city": step["params"]["search_city"],
                "search_province": step["params"]["search_province"]
            })

            result = filter_location(profiles_list, context_variables).result #Deterministic step
            try:
                result_json = json.loads(result)
                if validate_profiles(result_json): #Validate columns in dict
                    output_profiles_list = (result_json)
            except:
                #TODO: Add appropriate error handling
                pass

        if step["step"] == "filterNetWorth":
            context_variables = sk.ContextVariables(variables={
                "lower_limit": step["params"]["lower_limit"],
                "upper_limit": step["params"]["upper_limit"]
            })
            result = filter_networth(profiles_list, context_variables).result
            try:
                result_json = json.loads(result)
                if validate_profiles(result_json):
                    output_profiles_list = (result_json)
            except:
                pass
        if step["step"] == "filterName":
            context_variables = sk.ContextVariables(variables={
                "search_name": step["params"]["search_name"]
            })
            result = filter_name(profiles_list, context_variables).result
            try:
                result_json = json.loads(result)
                if validate_profiles(result_json):
                    output_profiles_list = (result_json)
            except:
                pass
        if step["step"] == "filterCompany":
            context_variables = sk.ContextVariables(variables={
                "search_company": step["params"]["search_company"]
            })
            result = filter_company(profiles_list, context_variables).result
            try:
                result_json = json.loads(result)
                if validate_profiles(result_json):
                    output_profiles_list = (result_json)
            except:
                pass

    ##Create response 
    response = create_response(str(textInputForGPT.textInputForGPT), True, True, output_profiles_list)
    #print(response)

    return {"data": output_profiles_list, "msg": response}


def create_response(original_query: str, valid_search: str, valid_response: str, data):
    global kernel
    context = kernel.create_new_context()
    context["ask"] = original_query
    skills = kernel.import_semantic_skill_from_directory("skills", "ResultSkill")
    generate_response = skills["ResultResponse"]
    input_str = """Original request: {}
Valid request: {}
Valid search: {}
Rows returned: {}""".format(original_query, valid_response, valid_search, len(data))
    context["response_context"] = input_str
    response = generate_response(context=context)
    return response.result


def load_data():
    global data
    with open("data/sample_data.json") as f:
        data = json.load(f)


@app.get("/parse-user-search/")
def parse_user_search(textInput: TextInputForLLM):
    global kernel
    if kernel == None:
        start_kernel()

    skill = kernel.import_semantic_skill_from_directory("skills", "ParseIntentSkill")

    summary = asyncio.run(
        kernel.run_on_str_async(textInput, skill["ParseUserSearchSteps"])
    )
    output = str(summary.variables).strip()
    return output

def start_kernel():
    global kernel
    kernel = sk.Kernel()
    model = "text-davinci-003"

    # Configure AI backend used by the kernel
    api_key, org_id = sk.openai_settings_from_dot_env()
    kernel.add_text_completion_service("dv", OpenAITextCompletion(model, api_key, org_id))