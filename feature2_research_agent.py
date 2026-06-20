from llm_client import generate_search_queries, synthesize_research
from search_tool import search_web
from notion_client_wrapper import create_research_page

def process_research_goal(goal: str) -> str:
    print(f"Generating search queries for: {goal}")
    queries = generate_search_queries(goal)
    if not queries:
        return "Failed to generate search queries."
        
    all_results = []
    for q in queries:
        print(f"Searching for: {q}")
        results = search_web(q)
        all_results.extend(results)
        
    print(f"Synthesizing {len(all_results)} total results...")
    synthesized = synthesize_research(goal, all_results)
    
    if not synthesized:
        return "Failed to synthesize research."
        
    print("Creating research page in Notion...")
    url = create_research_page(f"Research: {goal}", synthesized)
    return f"Research complete! View your page here: {url}"
