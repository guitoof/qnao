classdef States
   properties
      vertical
      horizontal
   end
   methods
      function c = States(v, h)
         c.vertical = v; c.horizontal = h;
      end
   end
   enumeration
      UpLeft (1, -1)
      Up (1, 0)
      UpRight (1, 1)
      Left (0, -1)
      Center (0, 0)
      Right (0, 1)
      DownLeft (-1, -1)
      Down (-1, 0)
      DownRight (-1, 1)
   end
end
