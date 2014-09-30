Q = zeros(9, 9);
alpha = 0.2;
gamma = 0.9;

possibleStates = enumeration('States');
state = possibleStates(randi(size(possibleStates, 1), 1, 1));
goalState = possibleStates(randi(size(possibleStates, 1), 1, 1));

fprintf('Initial state : %s \nGoal state: %s\n===============\n\n', char(state), char(goalState))

for i=1:10,
    while(ne(state, goalState))
        action = Actions.pickRandomAction(state);
        fprintf('Current state was %s and the robot will go %s (Goal : %s)\n', char(state), char(action), char(goalState));
        reward = input('> Input the reward\n');
        currentPosition  = 3*(-state.vertical+1)+state.horizontal+2;
        nextPosition  = currentPosition-3*action.vertical+action.horizontal;
        maxQ=max(Q(nextPosition,:));
        currentQ=Q(currentPosition, nextPosition);
        Q(currentPosition, nextPosition)=currentQ+alpha*(reward+gamma*maxQ-currentQ);
        state=possibleStates(nextPosition);
    end
    state = possibleStates(randi(size(possibleStates, 1), 1, 1));
end