Q = zeros(9, 4);
alpha = 0.2;
gamma = 0.9;
epsilon = 0.1;
possibleStates = enumeration('States');
state = possibleStates(randi(size(possibleStates, 1), 1, 1));
goalState = possibleStates(randi(size(possibleStates, 1), 1, 1));
possibleActions = enumeration('ActionsStates');

for i=1:10,
    fprintf('Initial state : %s \nGoal state: %s\n===============\n\n', char(state), char(goalState));
    while(ne(state, goalState))
        currentPosition  = 3*(-state.vertical+1)+state.horizontal+2;
        %action = Actions.pickRandomAction(state);
        action = Actions.pickGreedyAction(state, Q(currentPosition,:), epsilon);
        fprintf('Current state was %s and the robot will go %s (Goal : %s)\n', char(state), char(action), char(goalState));
        reward = input('> Input the reward\n');
        nextPosition  = currentPosition-3*action.vertical+action.horizontal;
        actionIndex = find(possibleActions == action, 1);
        maxQ=max(Q(nextPosition,:));
        currentQ=Q(currentPosition, actionIndex);
        Q(currentPosition, actionIndex)=currentQ+alpha*(reward+gamma*maxQ-currentQ);
        state=possibleStates(nextPosition);
    end
    fprintf('Next round !!!\n');
    state = possibleStates(randi(size(possibleStates, 1), 1, 1));
end