classdef Actions
   properties
      vertical = 0;
      horizontal = 0;
   end
   methods
      function obj = Actions(v, h)
         obj.vertical = v; obj.horizontal = h;
      end
   end
   methods (Static)
      function action = pickRandomAction(currentState)
         possibilities = Actions.pickPossibleActions(currentState);
         action = possibilities{randi(size(possibilities, 1), 1, 1)};
      end
      function action = pickGreedyAction(currentState, QRow, epsilon)
          action = 1
      end
      function possibilities = pickPossibleActions(currentState);
         possibilities = num2cell(enumeration('ActionsStates'));
         vFilter = cellfun(@(x)ne(currentState.vertical, x.vertical)||eq(currentState.vertical, 0), possibilities);
         hFilter = cellfun(@(x)ne(currentState.horizontal, x.horizontal)||eq(currentState.horizontal, 0), possibilities);
         possibilities = possibilities(vFilter & hFilter);
      end
   end
end
