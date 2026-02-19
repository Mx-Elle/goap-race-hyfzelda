import random
from game_world.racetrack import RaceTrack
from queue import PriorityQueue
import math
Point = tuple[int, int]
class RandomBot:
    def __init__(self):
        self.route = []
        self.button = {}
        self.can_pass = {}
        self.target = None
        self.button_connect = {}
        self.key_buttons = []

    def __call__(
        self,
    ):
        pass

    def button_connection(self, track: RaceTrack):
        track.target = (int(track.target[0]), int(track.target[1]))
        buttons = track.find_buttons()
        for col in track.button_colors:

            button = track.find_buttons(col)
            # print(button)
            for itm in button:

                # print(itm)
                x = int(itm[0])
                y = int(itm[1])
                itm = (x, y)
                self.button_connect[itm] = []
                visited = {}
                visited[(x, y)] = True
                # print('zelda', itm)
                initial = itm
                temp_can_pass = track.find_wall_locations(
                    col
                )  # find the walls that the button unlocks
                # print(temp_can_pass)
                frontier = []
                frontier.append((itm, 0))
                while len(frontier) > 0:

                    now, depth = frontier.pop(0)
                    if (
                        now in buttons or now == track.target
                    ) and now not in self.button_connect[itm]:
                        if now == track.target:
                            print("yayyyyyyyy", itm)
                        self.button_connect[itm].append((now, depth))
                    # print(now)

                    options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    neighbors = []
                    for opt in options:
                        neighbors.append((now[0] + opt[0], now[1] + opt[1]))
                    for addfrontier in neighbors:  # add all the frontiers
                        # print(addfrontier,"frontier")

                        if (
                            addfrontier not in track.find_traversable_cells()
                            and addfrontier not in temp_can_pass
                        ):
                            continue

                        if addfrontier not in visited:
                            visited[addfrontier] = True
                            frontier.append((addfrontier, depth + 1))

    def neighbor(self, loc: Point, phase, track: RaceTrack):
        x, y = loc
        maxrow, maxcol = track.shape
        options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []

        for opt in options:
            next_x = x + opt[0]
            next_y = y + opt[1]

            if not (0 <= next_x < maxrow and 0 <= next_y < maxcol):
                continue
            if track.wall_colors[next_x, next_y] != 0:
                tmp = int(track.wall_colors[next_x, next_y])
                if (track.active[next_x, next_y] == 1) ^ (phase[tmp] == 1):
                    continue

            if (
                next_x,
                next_y,
            ) not in track.find_traversable_cells() and track.wall_colors[
                next_x, next_y
            ] == 0:
                continue

            next_phase = phase[:]
            if track.buttons[next_x, next_y]:
                button_color = int(track.button_colors[next_x, next_y])
                next_phase = phase[:]
                next_phase[button_color] ^= 1

            neighbors.append(((next_x, next_y), next_phase, opt))

        return neighbors

    def Astar(
        self, start, target, track
    ):  # list can not be a list in frontier, need to be a tuple, but we want to keep the phase as a list for easy manipulation, so we will convert it to a tuple when we put it in the frontier and convert it back to a list when we pop it from the frontier
        start = (int(start[0]), int(start[1]))
        target = (int(target[0]), int(target[1]))

        frontier = PriorityQueue()
        initial_phase = [0] * 10

        # priority, tie breaker, location and phase
        frontier.put((0, 0, (start, initial_phase)))

        camefrom = {}
        cost = {}
        start_state = (start, tuple(initial_phase))
        camefrom[start_state] = None
        cost[start_state] = 0

        while not frontier.empty():
            _, __, now = frontier.get()
            now, current_phase = now

            current_state = (now, tuple(current_phase))

            if now == target:
                route = []
                tmp = current_state
                while tmp is not None:
                    route.append(tmp[0])
                    tmp = camefrom[tmp]
                route.reverse()
                return route[1:]

            for addfrontier, add_phase, add_opt in self.neighbor(
                now, current_phase, track
            ):
                add_state = (addfrontier, tuple(add_phase))
                current_cost = cost[current_state] + 1

                if add_state not in cost or current_cost < cost[add_state]:
                    cost[add_state] = current_cost
                    dist = abs(target[1] - addfrontier[1]) + abs(
                        target[0] - addfrontier[0]
                    )

                    frontier.put(
                        (
                            current_cost + dist,
                            random.randint(0, 2147483647),
                            (addfrontier, add_phase),
                        )
                    )  # keep add_phase as list in frontier

                    camefrom[add_state] = current_state

        return None

    # write a function that finds the necessary buttons to press to get to the target, and return a list in order of the buttons to press

    def __call__(self, loc: Point, track: RaceTrack) -> Point:
        #     print(track.shape,'shape')
        #    #print(self.button_connect)
        #     self.can_pass=track.find_traversable_cells()
        #     if self.button_connect=={}:
        #         self.button_connection(track)
        #         if self.Astar(loc, track.target) is not None:
        #             self.route=self.Astar(loc, track.target)
        #             self.target=track.target
        #         else:
        #             connected=[]
        #             for button in self.button_connect:
        #                 button=(int(button[0]),int(button[1]))
        #                 #print('button',loc, button)
        #                 if self.Astar(loc, button) is not None:#fix astar
        #                     connected.append(button)
        #             #print('connected',connected)
        #             tmp=self.button_route(connected[0], track.target)
        #             if tmp == None:
        #                 self.button_connect={}
        #                 safe = track.find_traversable_cells()
        #                 options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        #                 neighbors = {opt: (loc[0] + opt[0], loc[1] + opt[1]) for opt in options}
        #                 safe_options = [opt for opt in neighbors if neighbors[opt] in safe]
        #                 return random.choice(safe_options)
        #             self.key_buttons=self.button_route(connected[0], track.target)# problem: if there are multiple buttons that can unlock the target, it will only consider one of them
        #     if self.route==[] and self.key_buttons!=[]:
        #         #print('boom')
        #         button=self.key_buttons[0]
        #         if self.Astar(loc, button) is not None:
        #             self.route=self.Astar(loc, button)
        #             self.target=button
        #         else:
        #             self.key_buttons.pop(0)
        #     if loc==self.target:
        #         print('reached target', self.target)
        #         self.can_pass=track.find_traversable_cells()
        #         if self.Astar(loc, track.target) is not None:
        #             print('target')
        #             self.route=self.Astar(loc, track.target)
        #             self.target=track.target
        #         else:
        #             print('button')
        #             self.key_buttons.pop(0)
        #             print('key_buttons', self.key_buttons[0])
        #             self.target=self.key_buttons[0]
        #             self.route=self.Astar(loc, self.target)
        if self.route == []:
            self.route = self.Astar(loc, track.target, track)
        options = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
        if self.route[0] not in track.find_traversable_cells():
            return (0, 0)
        if self.route != [] and self.route[0] in track.find_traversable_cells():
            # print(track.find_traversable_cells()   )
            for opt in options:
                # print('opt',opt)
                if (loc[0] + opt[0], loc[1] + opt[1]) == self.route[0] and (
                    loc[0] + opt[0],
                    loc[1] + opt[1],
                ) in track.find_traversable_cells():
                    self.route.pop(0)
                    # print('opt',opt)
                    return opt
            self.route.pop(0)
            return (0, 0)
