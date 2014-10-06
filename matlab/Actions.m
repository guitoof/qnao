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
         allPossibilities = num2cell(enumeration('ActionsStates'));
         possibilities = Actions.pickPossibleActions(currentState);
         [Y, bestActionIndexes] = sort(QRow, 'descend');

         if (rand < epsilon)
             action = possibilities{randi(size(possibilities, 1), 1, 1)};
         else
             i = 1;
            while(~any(cellfun(@(x) x==allPossibilities{bestActionIndexes(i)}, possibilities, 'UniformOutput', 1)))
                i = i +1;
            end
            action = allPossibilities{bestActionIndexes(i)};
         end
      end
      function possibilities = pickPossibleActions(currentState);
         possibilities = num2cell(enumeration('ActionsStates'));
         vFilter = cellfun(@(x)ne(currentState.vertical, x.vertical)||eq(currentState.vertical, 0), possibilities);
         hFilter = cellfun(@(x)ne(currentState.horizontal, x.horizontal)||eq(currentState.horizontal, 0), possibilities);
         possibilities = possibilities(vFilter & hFilter);
      end
   end
end
