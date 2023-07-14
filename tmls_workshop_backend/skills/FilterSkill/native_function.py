from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel import SKContext
import pandas as pd

class FilterSkill:
    """
    FilterSkill provides native functions to search 
    client profiles according to criteria on name,
    location, company, or net worth.
    """

    @sk_function(
        description="Return profiles with net worth within range.",
        name="filterNetWorth"
    )
    @sk_function_context_parameter(name="lower_limit", description="Minimum net worth", default_value=0)
    @sk_function_context_parameter(name="upper_limit", description="Maximum net worth", default_value=1e12)
    def filterNetWorth(self, data: str, context: SKContext) -> str:

        data = pd.read_json(data)
        # Find profiles where net worth is within range 
        data_filtered = data.loc[(data.net_worth >= context['lower_limit']) & (data.net_worth <= context['upper_limit'])]
        return data_filtered.to_json(orient='records')
 

    @sk_function(
        description="Return profiles with first and/or last name matching search",
        name="filterName"
    )
    @sk_function_context_parameter(name="search_name", description="Name to search for")
    def filterName(self, data: str, context: SKContext) -> str:
        
        data = pd.read_json(data)
        # Find profiles where first and/or last name match search query 
        data_filtered = data.loc[data.name.str.contains(r"(^|\s|\-){}($|\s|\-)".format(context['search_name']), regex=True, case=False)]
        return data_filtered.to_json(orient='records')

    
    @sk_function(
        description="Return profiles with company name matching search",
        name="filterCompany"
    )
    @sk_function_context_parameter(name="search_company", description="Company to search for")
    def filterCompany(self, data: str, context: SKContext) -> str:

        data = pd.read_json(data)
        # Find profiles where company name contains search term 
        data_filtered = data.loc[data.company_name.str.contains(context['search_company'], regex=True, case=False)]
        return data_filtered.to_json(orient='records')
    
    
    @sk_function(
        description="Return profiles with address matching search (postal code, city, and/or province)",
        name="filterLocation"
    )
    @sk_function_context_parameter(name="search_postal", description="Postal code to search for", default_value=None)
    @sk_function_context_parameter(name="search_city", description="City to search for", default_value=None)
    @sk_function_context_parameter(name="search_province", description="Province to search for", default_value=None)
    def filterLocation(self, data: str, context: SKContext) -> str:
        
        data_filtered = data = pd.read_json(data)

        # Applying whichever search filters apply
        # Up to the user to make sure search terms don't conflict if multiple are used
        if context["search_postal"]:
            data_filtered = data_filtered.loc[data_filtered.postal_code.str.contains(context["search_postal"])]

        if context["search_city"]:
            data_filtered = data_filtered.loc[data_filtered.city.str.contains(context["search_city"])]

        if context["search_province"]:
            data_filtered = data_filtered.loc[data_filtered.province.str.contains(context["search_province"])]

        return data_filtered.to_json(orient='records')
