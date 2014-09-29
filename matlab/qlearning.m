Q = zeros(9, 9);
alpha = 0;
gamma = 0;

possibleStates = enumeration('States');
state = possibleStates(randi(size(possibleStates, 1), 1, 1));
goalState = possibleStates(randi(size(possibleStates, 1), 1, 1));

fprintf('Initial state : %s \nGoal state: %s\n===============\n\n', char(state), char(goalState))

action = Actions.pickRandomAction(state);
fprintf('Current state was %s and the robot will go %s\n', char(state), char(action))
reward = input('> Input the reward\n');
