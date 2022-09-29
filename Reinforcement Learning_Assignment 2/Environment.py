class Env:
    City_matrix = []
    Blocks = []
    Stations = []
    Moving_actions = []
    Moving_toward = []
    Put_pick_actions = []
    Source_Destination_dict = {}
    #---------- For awaring Agent -----------
    Passenger_Position = ()
    Destination_Position = ()
    Agent_Position = ()
    Source_Destination = []

    def __init__(self):
        self.Defining_envirtonment(5)

        # self.Defining_Source_Destination_Agent_randomly()
        # state_now = [self.Agent_Position, self.Passenger_Position, self.Destination_Position]

        return

    def New_episod(self):
        self.Defining_Source_Destination_Agent_randomly()
        state_now = [self.Agent_Position, self.Passenger_Position, self.Destination_Position]

        return state_now


    def Defining_envirtonment(self, n=5):

        self.City_matrix = [['R', 'n', 'n', 'n', 'G'], ['n', 'n', 'n', 'n', 'n'], ['n', 'n', 'n', 'n', 'n'], ['n', 'n', 'n', 'n', 'n'], ['Y', 'n', 'n', 'B', 'n']]

        self.Stations = [(0, 0), (0, 4), (4, 0), (4, 3)]

        self.Blocks = [[(0, 1), (0, 2)], [(1, 1), (1, 2)], [(3, 0), (3, 1)], [(4, 0), (4, 1)], [(3, 2), (3, 3)],
                  [(4, 2), (4, 3)]]

        self.Moving_actions = ["Norht", "South", "East", "West"]
        self.Moving_toward = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        self.Put_pick_actions = ["Pickup", "Putdown"]


        return

    def Defining_Source_Destination_Agent_randomly(self):
        m = len(self.Stations)
        if(m == 0):
            print("Error in 'Defining_Source_Destination_randomly' function: station has no element.")
        else:
            import random
            index_source = int(random.uniform(0, m))
            index_destination = int(random.uniform(0, m))

            Source_Destination = [self.Stations[index_source], self.Stations[index_destination]]
            self.Source_Destination_dict = {"position_S_D": Source_Destination, "Status": [False, False]}
            self.Passenger_Position = Source_Destination[0]
            self.Destination_Position = Source_Destination[1]

            n = len(self.City_matrix)
            if (n == 0):
                print("Error in 'Defining_Source_Destination_randomly' function: City_matrix has no element.")
            else:
                self.Agent_Position = (int(random.uniform(0, n)) , int(random.uniform(0, n)))
                # False means that the passenger was not picked up or putdown
        return

    def Response_of_Environment(self, a):
        # a should be one entry in ["Norht", "South", "East", "West", "Pickup", "Putdown"]
        # S is [Agent_Position, Passenger_Position, Destination] in [(), (), ()] format
        Moving_actions = self.Moving_actions
        Moving_toward = self.Moving_toward
        Put_pick_actions = self.Put_pick_actions

        n = len(self.City_matrix)
        S = self.Agent_Position
        # S should be (r,c) form
        Reward = -1
        S_ = S
        # ----- if agent take moving actions-----

        if (a in Moving_actions):
            indx = Moving_actions.index(a)
            Through = Moving_toward[indx]
            S_ = (S[0] + Through[0], S[1] + Through[1])

            # ----- if agent near the block and out of matrix-----
            if (S_[0] == -1 or S_[0] == n):
                S_ = S
            if (S_[1] == -1 or S_[1] == n):
                S_ = S
            for pair in self.Blocks:
                if (pair[0] == S and pair[1] == S_):
                    S_ = S
                elif (pair[1] == S and pair[0] == S_):
                    S_ = S


            Status = self.Source_Destination_dict["Status"]
            if (Status[0] == True):
                # the passenger have taken from source:
                self.Passenger_Position = S_
        # ------------------------------------

        # ----- if agent take put_pick action

        elif (a in Put_pick_actions):
            Source_Destination = self.Source_Destination_dict["position_S_D"]
            Status = self.Source_Destination_dict["Status"]
            if (S == Source_Destination[0]):
                # Agent is in Source
                if (Status[0] == False and a == "Pickup"):
                    Reward += 20
                    Status[0] = True
                elif (S == Source_Destination[1] and Status[0] == True and Status[1] == False):
                    if (a == "Putdown"):
                        Reward += 20
                        Status[1] = True
                        S_ = (-1,-1) # as "Terminal"
                    else:
                        Reward -= 9
                else:
                    Reward -= 9

            elif (S == Source_Destination[1]):
                # Agent is in destination
                if (Status[0] == True and Status[1] == False):
                    if (a == "Putdown"):
                        Reward += 20
                        Status[1] = True
                        S_ = (-1,-1) # as "Terminal"
                    else:
                        Reward -= 9
                else:
                    Reward -= 9
            else:
                Reward -= 9
        # ------------------------------------

        else:
            print("Error: wrong action taken by Agent:", a)

        self.Agent_Position = S_
        self.Source_Destination_dict["Status"] = Status
        next_state = [self.Agent_Position, self.Passenger_Position, self.Destination_Position]


        return next_state, Reward
