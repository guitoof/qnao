qnao
====

Q-Learning experiment on Nao robot

Running the Experiment
======================

To acquire the code, simply run the command :

    git clone https://github.com/Guitoof/qnao
    cd qnao

After plugging in the robot to the computer, make sure that the IP and port match the robot's in `python/config.py`.

To get the list of parameters and the help, one can run the following command :

    python qnao.py --help
    
Finally, to run the experiment (for instance with a custom value of epsilon):

    python qnao.py --epsilon 0.8


Licence
=======
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
