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
         possibilities = num2cell(enumeration('ActionsStates'));
         vFilter = cellfun(@(x)ne(currentState.vertical, x.vertical), possibilities);
         hFilter = cellfun(@(x)ne(currentState.horizontal, x.horizontal), possibilities);
         possibilities = possibilities(vFilter & hFilter);
         action = possibilities{randi(size(possibilities, 1), 1, 1)};
      end
   end
end
