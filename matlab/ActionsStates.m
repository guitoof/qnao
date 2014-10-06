classdef ActionsStates
   properties
      vertical
      horizontal
   end
   methods
      function c = ActionsStates(v, h)
         c.vertical = v; c.horizontal = h;
      end
   end
   enumeration
      %UpLeft (1, -1)
      Up (1, 0)
      Down(-1, 0)
      %UpRight (1, 1)
      Left (0, -1)
      Right (0, 1)
      %DownLeft (-1, -1)
      %DownRight (-1, 1)
   end
end
