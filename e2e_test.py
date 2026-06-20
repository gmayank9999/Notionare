import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

# We will test all four features one by one and collect results
results = []

def test_feature1():
    print("\n--- Testing Feature 1 (Task Creator) ---")
    try:
        from feature1_task_creator import process_user_input
        # "Finish the biology lab report by tomorrow, low priority"
        res = process_user_input("Finish the biology lab report by tomorrow, low priority")
        print("Feature 1 Success:", res)
        results.append(("Feature 1: Task Creator", True, res))
    except Exception as e:
        print("Feature 1 Failed:", e)
        results.append(("Feature 1: Task Creator", False, str(e)))

def test_feature2():
    print("\n--- Testing Feature 2 (Research Agent) ---")
    try:
        from feature2_research_agent import process_research_goal
        res = process_research_goal("compare top 3 mechanical keyboards for programming")
        print("Feature 2 Success:", res)
        results.append(("Feature 2: Research Agent", True, res))
    except Exception as e:
        print("Feature 2 Failed:", e)
        results.append(("Feature 2: Research Agent", False, str(e)))

def test_feature3():
    print("\n--- Testing Feature 3 (Monitor) ---")
    try:
        # run monitor as a script or import check_conflicts
        from feature3_monitor import main as check_conflicts
        check_conflicts()
        results.append(("Feature 3: Monitor", True, "Ran successfully (check logs for conflicts)"))
    except Exception as e:
        print("Feature 3 Failed:", e)
        results.append(("Feature 3: Monitor", False, str(e)))

def test_feature4():
    print("\n--- Testing Feature 4 (Workspace Generator) ---")
    try:
        from feature4_workspace_generator import process_workspace_idea
        res = process_workspace_idea("Build a real-time multiplayer chess game in React")
        print("Feature 4 Success:", res)
        results.append(("Feature 4: Workspace Generator", True, res))
    except Exception as e:
        print("Feature 4 Failed:", e)
        results.append(("Feature 4: Workspace Generator", False, str(e)))

def test_feature5():
    print("\n--- Testing Feature 5 (RAG Chat) ---")
    try:
        from feature5_rag_chat import process_rag_chat
        res = process_rag_chat("What is the goal of the multiplayer chess game?")
        print("Feature 5 Success:", res)
        results.append(("Feature 5: RAG Chat", True, "Answered query successfully"))
    except Exception as e:
        print("Feature 5 Failed:", e)
        results.append(("Feature 5: RAG Chat", False, str(e)))

if __name__ == "__main__":
    test_feature1()
    test_feature2()
    test_feature3()
    test_feature4()
    test_feature5()
    
    print("\n\n=== E2E Test Summary ===")
    all_passed = True
    for name, passed, info in results:
        status = "PASSED" if passed else "FAILED"
        if not passed: all_passed = False
        print(f"[{status}] {name}: {info}")
        
    if all_passed:
        print("\nALL FEATURES PASSED END-TO-END!")
        sys.exit(0)
    else:
        print("\nSOME FEATURES FAILED.")
        sys.exit(1)
