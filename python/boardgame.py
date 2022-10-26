import sys

class Boardgame:
    def __init__(self,path):
        self.board = self.get_orignal_matrix(path) # list of list which represente the grid as a matrix
        self.height, self.width = self.get_size()
        self.round = 0



    def find_soulution(self):
        specific_coords = self.get_specific_coords()

        round_max = self.get_round_max(specific_coords)

        if round_max == 0:
            message = "the character can't reach an exit before the fire"
            possible = False

        else:
            self.ongoing = {'F' : specific_coords['F']}
            self.ongoing['S'] = [(specific_coords['S'][0], '')]

            self.solution = ''

            while self.round < round_max and not self.solution:
                self.round += 1
                self.set_iteration()

            if self.solution:
                possible = True
                message = self.solution
            else:
                possible = False
                message = "the character can't reach an exit before the fire"

        return possible, message


    def get_orignal_matrix(self, path):
        try:
            file = open(path)
        except FileNotFoundError:
            sys.stdout.write("File not found")
            sys.exit(1)
        else:
            raw_data = file.readlines()
            data = []
            for element in raw_data:
                data.append([e for e in element if e!='\n'])
            if data:
                return data


    def get_size(self):
        height=len(self.board)
        width = len(self.board[0])
        for line in self.board:
            if len(line)!=width:
                sys.stdout.write("The grid is not a rectangle")
                sys.exit(1)
        return height, width


    def get_specific_coords(self):
        info = {'F':[],'E':[],'S':[]}
        for i in range(self.height):
            line = self.board[i]
            for j in range(self.width):
                element = line[j][0]
                if element == 'F':
                    info['F'].append((i,j))
                elif element == 'E':
                    info['E'].append((i,j))
                elif element == 'S':
                    info['S'].append((i,j))
        return info


    def get_round_max(self, specific_coords):
        """
        :param specific_coords: dict : contains list of fire coordinates, list of exit coordinates and the spawn coordinates. It's the result of get_specific_coords methods.
        :return: int : number of moves that can be done before fire(s) reach all exits
        """

        fire = specific_coords['F']
        exit = specific_coords['E']
        spawn = specific_coords['S'][0]
        itermax = 0

        for e in exit:
            distance_spawn_exit = abs(e[0]-spawn[0]) + abs(e[1] - spawn[1])
            distance_fire_exit = self.height + self.width

            for f in fire:
                distance = abs(e[0]-f[0]) + abs(e[1] - f[1])
                if distance < distance_fire_exit:
                    distance_fire_exit = distance

            if distance_spawn_exit < distance_fire_exit:
                itermax = max(itermax,distance_fire_exit)

        return itermax


    def set_iteration(self):
            next = {'F': [], 'S': []}

            # Propagation du feu
            for i,j in self.ongoing['F']:
                new_fire = [(i-1,j),(i,j-1),(i,j+1),(i+1,j)]
                for new_i, new_j in new_fire:
                    if new_i >= 0 and new_i < self.height and new_j >=0 and new_j < self.width:
                        if self.board[new_i][new_j] != 'F':
                            next['F'].append((new_i,new_j))
                            self.board[new_i][new_j] = 'F'

            # Par rapport aux positions possibles au précédent tour on regarde les cases atteignables par le personnage en se déplacant d'une case, si la prochaine case est vide.
            for (i,j),t in self.ongoing['S']:
                new_spawn = [((i - 1, j), t+'U'), ((i, j - 1), t+'L'), ((i, j + 1), t+'R'), ((i + 1, j), t+'D')]
                for (new_i, new_j), new_t in new_spawn:
                    if new_i >= 0 and new_i < self.height and new_j >= 0 and new_j < self.width:
                        if self.board[new_i][new_j] == '.':
                            next['S'].append(((new_i, new_j), new_t))
                            self.board[new_i][new_j] = str(self.round)
                        if self.board[new_i][new_j] == 'E':
                            self.solution = new_t
                            break

            # self.print_board()
            self.ongoing = next


    # def print_board(self): # Suivre l'évolution du plateau de jeu
    #     print('\n')
    #     print(f"Tour {self.round}")
    #     for element in self.board:
    #         print(element)
    #
