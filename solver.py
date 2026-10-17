import numpy as np
from scipy.optimize import linear_sum_assignment

# --- TRANSPORTATION METHODS ---

def northwest_corner(supply, demand, cost_matrix):
    s = supply.copy()
    d = demand.copy()
    rows, cols = cost_matrix.shape
    allocation = np.zeros((rows, cols))
    i = 0
    j = 0
    while i < rows and j < cols:
        qty = min(s[i], d[j])
        allocation[i, j] = qty
        s[i] -= qty
        d[j] -= qty
        if s[i] == 0: i += 1
        elif d[j] == 0: j += 1
    return allocation, np.sum(allocation * cost_matrix)

def least_cost(supply, demand, cost_matrix):
    s = supply.copy()
    d = demand.copy()
    rows, cols = cost_matrix.shape
    allocation = np.zeros((rows, cols))
    cost = cost_matrix.copy()
    while np.sum(s) > 0 and np.sum(d) > 0:
        min_val = np.inf
        min_idx = (0, 0)
        for i in range(rows):
            for j in range(cols):
                if s[i] > 0 and d[j] > 0 and cost[i, j] < min_val:
                    min_val = cost[i, j]
                    min_idx = (i, j)
        i, j = min_idx
        qty = min(s[i], d[j])
        allocation[i, j] = qty
        s[i] -= qty
        d[j] -= qty
        if s[i] == 0: cost[i, :] = np.inf
        if d[j] == 0: cost[:, j] = np.inf
    return allocation, np.sum(allocation * cost_matrix)

def vogels_approximation(supply, demand, cost_matrix):
    s = supply.copy()
    d = demand.copy()
    cost = cost_matrix.copy().astype(float)
    rows, cols = cost.shape
    allocation = np.zeros((rows, cols))
    while np.sum(s) > 0 and np.sum(d) > 0:
        row_penalties = []
        for i in range(rows):
            if s[i] > 0:
                valid = sorted([cost[i, j] for j in range(cols) if d[j] > 0 and not np.isinf(cost[i, j])])
                if len(valid) >= 2: row_penalties.append((valid[1] - valid[0], i, 'row'))
                elif len(valid) == 1: row_penalties.append((valid[0], i, 'row'))
                else: row_penalties.append((-1, i, 'row'))
            else: row_penalties.append((-1, i, 'row'))
        
        col_penalties = []
        for j in range(cols):
            if d[j] > 0:
                valid = sorted([cost[i, j] for i in range(rows) if s[i] > 0 and not np.isinf(cost[i, j])])
                if len(valid) >= 2: col_penalties.append((valid[1] - valid[0], j, 'col'))
                elif len(valid) == 1: col_penalties.append((valid[0], j, 'col'))
                else: col_penalties.append((-1, j, 'col'))
            else: col_penalties.append((-1, j, 'col'))
                
        all_penalties = row_penalties + col_penalties
        all_penalties.sort(key=lambda x: x[0], reverse=True)
        if not all_penalties or all_penalties[0][0] == -1: break
            
        max_pen, idx, p_type = all_penalties[0]
        if p_type == 'row':
            i = idx
            j = min((j for j in range(cols) if d[j] > 0), key=lambda x: cost[i, x])
        else:
            j = idx
            i = min((i for i in range(rows) if s[i] > 0), key=lambda x: cost[x, j])
            
        qty = min(s[i], d[j])
        allocation[i, j] = qty
        s[i] -= qty
        d[j] -= qty
        if s[i] == 0: cost[i, :] = np.inf
        if d[j] == 0: cost[:, j] = np.inf
    return allocation, np.sum(allocation * cost_matrix)

# --- ASSIGNMENT METHOD ---

def solve_assignment(cost_matrix):
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    return cost_matrix[row_ind, col_ind].sum()

# --- SCHEDULING METHOD (Johnson's Rule: n Jobs on 2 Machines) ---

def solve_scheduling(machine1_times, machine2_times):
    """
    Johnson's Rule for n jobs on 2 machines.
    Takes arrays/lists of times for Machine 1 and Machine 2.
    """
    n = len(machine1_times)
    jobs = [{'id': i+1, 'm1': machine1_times[i], 'm2': machine2_times[i]} for i in range(n)]
    
    left = 0
    right = n - 1
    optimal_sequence = [0] * n
    
    # Sort jobs or iteratively pick minimum
    job_pool = jobs.copy()
    while job_pool:
        # Find minimum time across all remaining jobs and machines
        min_val = float('inf')
        best_job = None
        best_machine = None
        
        for job in job_pool:
            if job['m1'] < min_val:
                min_val = job['m1']
                best_job = job
                best_machine = 1
            if job['m2'] < min_val:
                min_val = job['m2']
                best_job = job
                best_machine = 2
                
        if best_machine == 1:
            optimal_sequence[left] = best_job['id']
            left += 1
        else:
            optimal_sequence[right] = best_job['id']
            right -= 1
            
        job_pool.remove(best_job)
        
    # Calculate total elapsed time / makespan
    m1_time = 0
    m2_time = 0
    for job_id in optimal_sequence:
        j_data = next(j for j in jobs if j['id'] == job_id)
        m1_time += j_data['m1']
        if m2_time < m1_time:
            m2_time = m1_time
        m2_time += j_data['m2']
        
    return optimal_sequence, m2_time