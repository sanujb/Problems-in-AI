with open('gw1.txt', 'r') as f:
    n_states = int(f.readline())
    reward = {}
    actions = [0, 1, 2, 3]
    T = {}
    for i in range(n_states):
        reward[i] = float(f.readline())

    for action in actions:
        T[action] = []
        for i in range(n_states):
            T[action].append([float(x) for x in f.readline().split(',')])

U = [0 for x in range(n_states)]
U_next = [0 for x in range(n_states)]
delta = 1
best_actions = [0 for x in range(n_states)]
while delta > 0:
    U = U_next.copy()
    delta = 0
    for cur_state in range(n_states):
        best_action = [[0], -float('inf')]
        for action in actions:
            total = 0
            for next_state in range(n_states):
                total += T[action][cur_state][next_state]*U[next_state]
            if total >= best_action[1]:
                if total == best_action[1]:
                    best_action[0].append(action)
                else:
                    best_action = [[action], total]
        best_actions[cur_state] = best_action[0]
        U_next[cur_state] = reward[cur_state] + best_action[1]
        delta = max(delta, abs(U_next[cur_state] - U[cur_state]))
        # if cur_state == 4:
        #     print(U[cur_state], best_action)

print(U)
print(best_actions)
