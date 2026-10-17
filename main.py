import numpy as np
import ollama
from solver import northwest_corner, least_cost, vogels_approximation, solve_assignment, solve_scheduling

def print_banner():
    print("=" * 40)
    print("Opti AI Agent")
    print("=" * 40)

def get_matrix_input():
    print("\nEnter your 4x4 Matrix row by row (space-separated values):")
    matrix = []
    for i in range(4):
        while True:
            try:
                row = list(map(float, input(f"Row {i+1} (4 numbers): ").strip().split()))
                if len(row) == 4:
                    matrix.append(row)
                    break
                print("Error: Please enter exactly 4 numbers.")
            except ValueError:
                print("Error: Invalid input. Enter numbers only.")
    return np.array(matrix)

def get_vector_input(name):
    while True:
        try:
            vec = list(map(float, input(f"Enter {name} vector (4 numbers): ").replace(',', ' ').split()))
            if len(vec) == 4:
                return np.array(vec)
            print("Error: Please enter exactly 4 values.")
        except ValueError:
            print("Error: Invalid input.")

def ask_ollama_consultant(results, prob_type):
    prompt = f"""
    You are an expert Operations Research AI Consultant. 
    Problem Type: {prob_type}
    Results computed:
    {results}
    
    Provide a brief, professional terminal summary declaring the results. Keep it under 4 crisp lines. Do not use dollar signs.
    """
    print("\n🤖 [Opti AI Agent is evaluating locally via Qwen2.5:3b...]\n")
    try:
        response = ollama.chat(
            model='qwen2.5:3b',
            messages=[{'role': 'user', 'content': prompt}]
        )
        print(response['message']['content'])
    except Exception as e:
        print(f"Ollama note: Ensure Ollama is running (`ollama serve`). Error: {e}")

def main():
    print_banner()
    
    print("\nSelect Problem Type:")
    print("1. Transportation Problem (Northwest, Least Cost, & VAM)")
    print("2. Assignment Problem (Hungarian Method)")
    print("3. Scheduling / Sequencing Problem (Johnson's Rule: n Jobs on 2 Machines)")
    
    choice = input("\nEnter choice (1, 2, or 3): ").strip()
    
    if choice == '1':
        cost_matrix = get_matrix_input()
        supply = get_vector_input("Supply")
        demand = get_vector_input("Demand")
        
        print("\n⏳ Running Transportation Heuristics...")
        _, cost_nw = northwest_corner(supply, demand, cost_matrix)
        _, cost_lc = least_cost(supply, demand, cost_matrix)
        _, cost_vam = vogels_approximation(supply, demand, cost_matrix)
        
        results = {
            "Northwest Corner": cost_nw,
            "Least Cost Method": cost_lc,
            "Vogel's Approximation (VAM)": cost_vam
        }
        
        print("\n" + "-" * 50)
        print(f"📊 TRANSPORTATION RESULTS SUMMARY")
        print("-" * 50)
        for method, cost in results.items():
            print(f"-> {method:<30}: {cost:,.2f}")
        print("-" * 50)
        
        ask_ollama_consultant(results, "Transportation Problem")
        
    elif choice == '2':
        cost_matrix = get_matrix_input()
        print("\n⏳ Running Hungarian Assignment Algorithm...")
        cost_asg = solve_assignment(cost_matrix)
        
        results = {"Hungarian Assignment Method": cost_asg}
        
        print("\n" + "-" * 50)
        print(f"📊 ASSIGNMENT RESULTS SUMMARY")
        print("-" * 50)
        print(f"-> Optimal Assignment Cost    : {cost_asg:,.2f}")
        print("-" * 50)
        
        ask_ollama_consultant(results, "Assignment Problem")
        
    elif choice == '3':
        print("\n--- Scheduling / Job Sequencing (Johnson's Rule) ---")
        try:
            m1 = list(map(float, input("Enter processing times for Machine 1 (space-separated): ").strip().split()))
            m2 = list(map(float, input("Enter processing times for Machine 2 (space-separated): ").strip().split()))
            
            if len(m1) != len(m2):
                print("Error: Both machines must have the same number of jobs.")
                return
                
            print("\n⏳ Optimizing Job Sequence...")
            sequence, makespan = solve_scheduling(m1, m2)
            
            results = {
                "Optimal Job Sequence": f"Job {sequence}",
                "Total Total Elapsed Time (Makespan)": makespan
            }
            
            print("\n" + "-" * 50)
            print(f"📊 SCHEDULING RESULTS SUMMARY")
            print("-" * 50)
            print(f"-> Optimal Sequence           : Job {' -> '.join(map(str, sequence))}")
            print(f"-> Total Elapsed Time         : {makespan:,.2f}")
            print("-" * 50)
            
            ask_ollama_consultant(results, "Job Sequencing Scheduling Problem")
        except ValueError:
            print("Error: Please enter valid numbers.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()