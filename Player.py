class player:
    # class attributes
    # we don't need any class attributes because each player is a different player, they don't share attributes
    
    
    # instance attributes
    # we want to use the data we collected to initialize all of the player's probabilities of say,
    # hitting a fairway in regulation or making a putt within 10 feet
    def __init__(self, name, year, df):
        self.name = name
        self.year = year
        self.fir = float(df.loc[(df['YEAR'] == str(self.year)) & (df['PLAYER NAME'] == str(self.name))]['DRIVING ACCURACY PERCENTAGE'].values[0])
        self.gir = float(df.loc[(df['YEAR'] == str(self.year)) & (df['PLAYER NAME'] == str(self.name))]['GREENS IN REGULATION PERCENTAGE'].values[0])
        self.drive_distance = float(df.loc[(df['YEAR'] == str(self.year)) & (df['PLAYER NAME'] == str(self.name))]['DRIVING DISTANCE'].values[0])
        self.sg_putt = float(df.loc[(df['YEAR'] == str(self.year)) & (df['PLAYER NAME'] == str(self.name))]['SG: PUTTING'].values[0])
        self.sg_ttg = float(df.loc[(df['YEAR'] == str(self.year)) & (df['PLAYER NAME'] == str(self.name))]['SG: TEE-TO-GREEN'].values[0])
        self.sg_apr = float(df.loc[(df['YEAR'] == str(self.year)) & (df['PLAYER NAME'] == str(self.name))]['SG:APR'].values[0])
        self.sg_arg = float(df.loc[(df['YEAR'] == str(self.year)) & (df['PLAYER NAME'] == str(self.name))]['SG:ARG'].values[0])
        self.sg_total = float(df.loc[(df['YEAR'] == str(self.year)) & (df['PLAYER NAME'] == str(self.name))]['SG: TOTAL'].values[0])
        self.putt_5 = float(df.loc[(df['YEAR'] == str(self.year)) & (df['PLAYER NAME'] == str(self.name))]["PUTTING FROM 5'"].values[0])/100
        self.putt_5_10 = float(df.loc[(df['YEAR'] == str(self.year)) & (df['PLAYER NAME'] == str(self.name))]["PUTTING - INSIDE 10'"].values[0])/100
        self.putt_10_15 = float(df.loc[(df['YEAR'] == str(self.year)) & (df['PLAYER NAME'] == str(self.name))]["PUTTING FROM - 10-15'"].values[0])/100
        self.putt_15_20 = float(df.loc[(df['YEAR'] == str(self.year)) & (df['PLAYER NAME'] == str(self.name))]["PUTTING FROM - 15-20'"].values[0])/100
        self.putt_20_25 = float(df.loc[(df['YEAR'] == str(self.year)) & (df['PLAYER NAME'] == str(self.name))]["PUTTING FROM - 20-25'"].values[0])/100
        self.putt_25 = float(df.loc[(df['YEAR'] == str(self.year)) & (df['PLAYER NAME'] == str(self.name))]["PUTTING FROM - &GT; 25'"].values[0])/100
        self.distance_from_hole = 400
        self.location = 'Tee box'
        self.par = 4
        self.in_hole = False
        self.is_in_play = True
        self.number_of_strokes = 0
        
        # Adding the data from the database to our player instance based on the player's name and the specific year.
        # Adding instance variables to track distance from the hole, where the ball is (ie tee box, bunker, fairway,
        # green, rough, hazard, out of bounds, etc), the par of the hole, if the ball is in the hole, if the ball is
        # in play
        

    # player methods
    def fairway_in_reg(self):
        """This method uses the player's fairway in regulation percentage as a weight 
        to compute the probability of hitting the fairway on a tee shot. Returns a list
        of probabilities, that sum to 1, of where the ball will end up."""
        
        fir_prob = self.fir / 100
        first_cut = fir_prob/15
        second_cut = 1 - fir_prob - first_cut
        fir = [fir_prob, first_cut, second_cut]
        return fir
    
    def green_in_reg(self):
        """This method uses the player's green in regulation percentage as a weight
        to compute the probability of hitting the green on an approach shot. Returns a list
        of probabilities, that sum to 1, of where the ball will end up."""
        # What I need to implement in the future with this method is more precise penalties
        # and bonuses for the lie of the ball. Also work with the stroke method
        # to take into account the distance from the green.
        # Then I can use parameters of strokes gained from specific distances.
        gir = []
        
        gir_prob = self.gir / 100
        fairway_prob = .1
        first_cut_prob = .15
        second_cut_prob = 1 - gir_prob - fairway_prob - first_cut_prob
        gir.append(gir_prob)
        gir.append(fairway_prob)
        gir.append(first_cut_prob)
        gir.append(second_cut_prob)
        
        # What I really need is a feature that I can use to determine how far from the hole
        # the approach shot will place me.
        
        return gir
    
    def putt(self):
        """This method uses the player's strokes gained putting as a weight to compute the
        probability of making a putt. Returns a list of probabilities, that sum to 1, of where
        the ball will end up."""
        # Eventually I will gather more parameters to make this function more specific. These can
        # include putt percentage from specific distances, 3 putt percentage, 2 putt percentage,
        # average number of putts per round, etc. But for now I am just going to use
        # simple strokes gained to give a rough estimate of the top and bottom 50%
        # of the Tour's performance.
        import numpy as np
        
        if self.distance_from_hole < (5/3):
            # Putting inside 5 feet
            putt = [self.putt_5, 1 - self.putt_5]
            #make_putt = np.mean(np.random.choice([1, 0], size = 10, p = make_putt_probs)).round()
                    
        elif (self.distance_from_hole < (10/3)) and (self.distance_from_hole >= (5/3)):
            # Putting from 5 to 10 feet
            putt = [self.putt_5_10, 1 - self.putt_5_10]
            #make_putt = np.mean(np.random.choice([1, 0], size = 10, p = make_putt_probs)).round()
                    
        elif (self.distance_from_hole < (15/3)) and (self.distance_from_hole >= (10/3)):
            # Puttin from 10 to 15 feet
            putt = [self.putt_10_15, 1 - self.putt_10_15]
            #make_putt = np.mean(np.random.choice([1, 0], size = 10, p = make_putt_probs)).round()
        elif (self.distance_from_hole < (20/3)) and (self.distance_from_hole >= (15/3)):
            # Putting from 15 to 20 feet
            putt = [self.putt_15_20, 1 - self.putt_15_20]
            #make_putt = np.mean(np.random.choice([1, 0], size = 10, p = make_putt_probs)).round()
        elif (self.distance_from_hole < (25/3)) and (self.distance_from_hole >= (20/3)):
            # Putting from 20 to 25 feet
            putt = [self.putt_20_25, 1 - self.putt_20_25]
            #make_putt = np.mean(np.random.choice([1, 0], size = 10, p = make_putt_probs)).round()
        else:
            # Putting outside 25 feet
            putt = [self.putt_25, 1 - self.putt_25]
            #make_putt = np.mean(np.random.choice([1, 0], size = 10, p = make_putt_probs)).round()
        
        
                
        return putt
    
    def chip(self):
        """This method uses the player's strokes gained around the green as a weight to compute the
        probability of making a chip. Returns a list of probabilities, that sum to 1, of where
        the ball will end up."""
        
        # I need to add a feature for the lie of the ball, i.e. bunker, thickness of the grass,
        # how tight the lie is. I need a feature to figure out how close the player can 
        # chip it to the pin rather than just "on the green" and "in the hole"
        # Note: strokes gained around the green uses sand recoveries and anything within 30 yards.
        # that means pitch shots within 60 yards for example are considered approach shots
        # and should be part of the green in regulation method or another method entirely.
        
        chip = []
        
        if self.sg_arg > 0:
            if self.distance_from_hole < 10:
                make_chip_prob = .15
                not_make = 1 - make_chip_prob
                chip.append(make_chip_prob)
                chip.append(not_make)
            else:
                make_chip_prob = .075
                not_make = 1 - make_chip_prob
                chip.append(make_chip_prob)
                chip.append(not_make)
            
        if self.sg_arg < 0:
            if self.distance_from_hole < 10:
                make_chip_prob = .1
                not_make = 1 - make_chip_prob
                chip.append(make_chip_prob)
                chip.append(not_make)
            else:
                make_chip_prob = .05
                not_make = 1 - make_chip_prob
                chip.append(make_chip_prob)
                chip.append(not_make)
        return chip
    
    def pitch(self):
        """This method uses the player's strokes gained approach the green as a weight to compute the
        probability of holing a pitch. Returns a list of probabilities, that sum to 1, of where
        the ball will end up."""
        # The idea is this method will cover all shots with a wedge not considered a chip.
        # This will make use of strokes gained approach the green and other parameters
        # with regards to short finesse shots into the green. 
        # I need to make some feature that helps me determine how close the player will hit the ball
        # to the hole
        
        import numpy as np
        
        pitch = []
        
        if self.sg_apr > 0:
            second_cut = .05
            first_cut = .1
            on_green = 1 - second_cut - first_cut
            pitch.append(on_green)
            pitch.append(first_cut)
            pitch.append(second_cut)
        elif self.sg_apr <= 0:
            second_cut = .025
            first_cut = .15
            on_green = 1 - second_cut - first_cut
            pitch.append(on_green)
            pitch.append(first_cut)
            pitch.append(second_cut)
        return pitch
    
    
    def stroke(self, shot):
        """This method performs a player's next stroke. Uses the other member functions to calculate
        the probability of specific outcomes for each shot then spits out the distance to the hole
        after the shot. The general idea is the stroke method use the resulting shot-type as chosen
        by the member functions, and the distance before the shot was taken, and advance the ball accordingly.
        The stroke method will just return self so that it can be chained to other methods if desired, 
        it will change instance variables."""
        
        import numpy as np
        
        if self.location == 'Tee box':
            # par 4 or par 5 tee shot
            if self.distance_from_hole >= 280:
                if shot == 'Fairway':
                    # can potentially add a random choice component to vary the driving distance
                    self.distance_from_hole -= self.drive_distance
                elif shot == 'First Cut':
                    self.distance_from_hole = self.distance_from_hole - self.drive_distance + 5
                elif shot == 'Second Cut':
                    self.distance_from_hole = self.distance_from_hole - self.drive_distance + 15
                    
            else:
                # par 3 tee shot
                if shot == 'Green':
                    # if the player is a great iron player then they hit it to within 21 feet
                    if self.sg_apr > .5:
                        self.distance_from_hole = np.mean(np.random.choice([7], size = 10))
                    # if the player is a decent iron player then they hit it to within 30 feet
                    elif self.sg_apr > 0:
                        self.distance_from_hole = np.mean(np.random.choice([10], size = 10))
                    else:
                    # if the player is a poor iron player then they hit it to within 45 feet
                        self.distance_from_hole = np.mean(np.random.choice([15], size = 10))
                        
                elif shot == 'Fairway':
                    self.distance_from_hole = 30
                    
                elif shot == 'First Cut':
                    # need to work out a way to have some fringe shots be close (pin locations)
                    # this will come when I have some course layout data to work with
                    # but this will be fine for now as shots on the green tend to be closer to the
                    # pin than shots on the fringe.
                    self.distance_from_hole = 20
                    
                elif shot == 'Second Cut':
                    self.distance_from_hole = 25
                    
                    
        elif self.location == 'Fairway':
            if (self.distance_from_hole > 220) and (self.distance_from_hole < 280):
                if shot == 'Green':
                    # if the player is a great approach player then they hit it to within 30 feet
                    if self.sg_apr > .5:
                        self.distance_from_hole = np.mean(np.random.choice([10], size = 10))
                    # if the player is a decent approach player then they hit it to within 60 feet
                    elif self.sg_apr > 0:
                        self.distance_from_hole = np.mean(np.random.choice([20], size = 10))
                    else:
                    # if the player is a poor approach player then they hit it to within 90 feet
                        self.distance_from_hole = np.mean(np.random.choice([30], size = 10))
                        
                elif shot == 'Fairway':
                    self.distance_from_hole = 30
                    
                elif shot == 'First Cut':
                    # need to work out a way to have some fringe shots be closer (pin locations)
                    # this will come when I have some course layout data to work with
                    # but this will be fine for now as shots on the green tend to be closer to the
                    # pin than shots on the fringe.
                    self.distance_from_hole = 20
                
                elif shot == 'Second Cut':
                    self.distance_from_hole = 25
                
            elif (self.distance_from_hole <= 220) and (self.distance_from_hole > 120):
                if shot == 'Green':
                    # if the player is a great iron player then they hit it to within 21 feet
                    if self.sg_apr > .5:
                        self.distance_from_hole = np.mean(np.random.choice([7], size = 10))
                    # if the player is a decent iron player then they hit it to within 30 feet
                    elif self.sg_apr > 0:
                        self.distance_from_hole = np.mean(np.random.choice([10], size = 10))
                    else:
                    # if the player is a poor iron player then they hit it to within 45 feet
                        self.distance_from_hole = np.mean(np.random.choice([15], size = 10))
                        
                elif shot == 'Fairway':
                    self.distance_from_hole = 30
                    
                elif shot == 'First Cut':
                    # need to work out a way to have some fringe shots be closer (pin locations)
                    # this will come when I have some course layout data to work with
                    # but this will be fine for now as shots on the green tend to be closer to the
                    # pin than shots on the fringe.
                    self.distance_from_hole = 20
                
                elif shot == 'Second Cut':
                    self.distance_from_hole = 25
            
            elif (self.distance_from_hole <= 120) and (self.distance_from_hole > 30):
                if shot == 'Green':
                    # if the player is a great iron player then they hit it to within 10 feet
                    if self.sg_apr > .5:
                        self.distance_from_hole = np.mean(np.random.choice([3.334], size = 10))
                    # if the player is a decent iron player then they hit it to within 20 feet
                    elif self.sg_apr > 0:
                        self.distance_from_hole = np.mean(np.random.choice([7], size = 10))
                    else:
                    # if the player is a poor iron player then they hit it to within 30 feet
                        self.distance_from_hole = np.mean(np.random.choice([10], size = 10))
                        
                elif shot == 'Fairway':
                    self.distance_from_hole = 30
                    
                elif shot == 'First Cut':
                    # need to work out a way to have some fringe shots be closer (pin locations)
                    # this will come when I have some course layout data to work with
                    # but this will be fine for now as shots on the green tend to be closer to the
                    # pin than shots on the fringe.
                    self.distance_from_hole = 20
                
                elif shot == 'Second Cut':
                    self.distance_from_hole = 25
                
            elif shot == 'Make Chip':
                self.distance_from_hole = 0
            elif shot == 'Miss Chip':
                self.distance_from_hole = 6
                    
        elif self.location == 'First Cut' or self.location == 'Second Cut':
            # for now I'm just going to group second and first cut together, I will
            # end up making helper functions to make this process easier to read and 
            # write out. Then I will separate these two cases.
            if (self.distance_from_hole > 220) and (self.distance_from_hole < 280):
                if shot == 'Green':
                    # if the player is a great approach player then they hit it to within 45 feet
                    if self.sg_apr > .5:
                        self.distance_from_hole = np.mean(np.random.choice([15], size = 10))
                    # if the player is a decent approach player then they hit it to within 75 feet
                    elif self.sg_apr > 0:
                        self.distance_from_hole = np.mean(np.random.choice([25], size = 10))
                    else:
                    # if the player is a poor approach player then they hit it to within 120 feet
                        self.distance_from_hole = np.mean(np.random.choice([40], size = 10))
                        
                elif shot == 'Fairway':
                    self.distance_from_hole = 30
                    
                elif shot == 'First Cut':
                    # need to work out a way to have some fringe shots be closer (pin locations)
                    # this will come when I have some course layout data to work with
                    # but this will be fine for now as shots on the green tend to be closer to the
                    # pin than shots on the fringe.
                    self.distance_from_hole = 20
                
                elif shot == 'Second Cut':
                    self.distance_from_hole = 25
                
            elif (self.distance_from_hole <= 220) and (self.distance_from_hole > 120):
                if shot == 'Green':
                    # if the player is a great iron player then they hit it to within 30 feet
                    if self.sg_apr > .5:
                        self.distance_from_hole = np.mean(np.random.choice([10], size = 10))
                    # if the player is a decent iron player then they hit it to within 45 feet
                    elif self.sg_apr > 0:
                        self.distance_from_hole = np.mean(np.random.choice([15], size = 10))
                    else:
                    # if the player is a poor iron player then they hit it to within 60 feet
                        self.distance_from_hole = np.mean(np.random.choice([20], size = 10))
                        
                elif shot == 'Fairway':
                    self.distance_from_hole = 30
                    
                elif shot == 'First Cut':
                    # need to work out a way to have some fringe shots be closer (pin locations)
                    # this will come when I have some course layout data to work with
                    # but this will be fine for now as shots on the green tend to be closer to the
                    # pin than shots on the fringe.
                    self.distance_from_hole = 20
                
                elif shot == 'Second Cut':
                    self.distance_from_hole = 25
            
            elif (self.distance_from_hole <= 120) and (self.distance_from_hole > 30):
                if shot == 'Green':
                    # if the player is a great iron player then they hit it to within 15 feet
                    if self.sg_apr > .5:
                        self.distance_from_hole = np.mean(np.random.choice([5], size = 10))
                    # if the player is a decent iron player then they hit it to within 25 feet
                    elif self.sg_apr > 0:
                        self.distance_from_hole = np.mean(np.random.choice([8.5], size = 10))
                    else:
                    # if the player is a poor iron player then they hit it to within 40 feet
                        self.distance_from_hole = np.mean(np.random.choice([13.5], size = 10))
                        
                elif shot == 'Fairway':
                    self.distance_from_hole = 30
                    
                elif shot == 'First Cut':
                    # need to work out a way to have some fringe shots be closer (pin locations)
                    # this will come when I have some course layout data to work with
                    # but this will be fine for now as shots on the green tend to be closer to the
                    # pin than shots on the fringe.
                    self.distance_from_hole = 20
                
                elif shot == 'Second Cut':
                    self.distance_from_hole = 25
                
            elif shot == 'Make Chip':
                self.distance_from_hole = 0
            elif shot == 'Miss Chip':
                self.distance_from_hole = 6
                
            
        #elif self.location == 'Second Cut':
        elif self.location == 'Green':
            # Need to set the distance form the hole after mssing a putt
            if self.distance_from_hole < (5/3):
                # Putting inside 5 feet
                remaining_distance = np.linspace(.1/3, 5/3)
                self.distance_from_hole = np.mean(np.random.choice(remaining_distance, size = 10))
                    
            elif (self.distance_from_hole < (10/3)) and (self.distance_from_hole >= (5/3)):
                # Putting from 5 to 10 feet
                remaining_distance = np.linspace(.1/3, 5/3)
                self.distance_from_hole = np.mean(np.random.choice(remaining_distance, size = 10))
                    
            elif (self.distance_from_hole < (15/3)) and (self.distance_from_hole >= (10/3)):
                # Puttin from 10 to 15 feet
                remaining_distance = np.linspace(.1/3, 5/3)
                self.distance_from_hole = np.mean(np.random.choice(remaining_distance, size = 10))
                
            elif (self.distance_from_hole < (20/3)) and (self.distance_from_hole >= (15/3)):
                # Putting from 15 to 20 feet
                remaining_distance = np.linspace(.1/3, 5/3)
                self.distance_from_hole = np.mean(np.random.choice(remaining_distance, size = 10))
                
            elif (self.distance_from_hole < (25/3)) and (self.distance_from_hole >= (20/3)):
                # Putting from 20 to 25 feet
                remaining_distance = np.linspace(.1/3, 6/3)
                self.distance_from_hole = np.mean(np.random.choice(remaining_distance, size = 10))
                
            else:
                # Putting outside 25 feet
                remaining_distance = np.linspace(.1/3, 7/3)
                self.distance_from_hole = np.mean(np.random.choice(remaining_distance, size = 10))
            
                
        return self.distance_from_hole
    
    def simulate_round(self, course_info):
        """
        This function simulates a round of golf using the other methods in the class
        and returns the number of strokes recorded by the player. This function takes
        in a player object and the course information stored as a dict with hole lengths
        as keys and their corresponding pars as values.
        """
        import numpy as np


        #McIlroy = Player.player(name = 'Rory McIlroy', year = 2020, df = df_total)
        total_strokes = 0
        course_lengths = list(course_info.keys())
        for i in range(len(course_info)):
            self.distance_from_hole = course_lengths[i]
            self.par = course_info[course_lengths[i]]
            self.location = 'Tee box'
            self.number_of_strokes = 0
            self.in_hole = False

            while self.in_hole == False:
                if self.location == 'Tee box':
                    print('1st')
                    if self.par == 4 or self.par == 5:
                        # use the fir method
                        tee_shot_probs = self.fairway_in_reg() # this is a list of probabilities
                        tee_shot_outcomes = ['Fairway', 'First Cut', 'Second Cut']
                        tee_shot = np.random.choice(tee_shot_outcomes, size = 1, p = tee_shot_probs)
                        self.distance_from_hole = self.stroke(tee_shot)
                        self.location = tee_shot
                    else:
                        approach_shot_probs = self.green_in_reg()
                        approach_shot_outcomes = ['Green', 'Fairway', 'First Cut', 'Second Cut']
                        approach_shot = np.random.choice(approach_shot_outcomes, size = 1, p = approach_shot_probs)
                        self.distance_from_hole = self.stroke(approach_shot)
                        self.location = approach_shot



                elif self.location == 'Fairway':
                    if (self.distance_from_hole <= 280) and (self.distance_from_hole > 120):
                        # use the gir method

                        print('2nd')
                        approach_shot_probs = self.green_in_reg()
                        approach_shot_outcomes = ['Green', 'Fairway', 'First Cut', 'Second Cut']
                        approach_shot = np.random.choice(approach_shot_outcomes, size = 1, p = approach_shot_probs)
                        self.distance_from_hole = self.stroke(approach_shot)
                        self.location = approach_shot

                    elif self.distance_from_hole > 280:
                        # use the fir method

                        print('3rd')
                        layup_probs = self.fairway_in_reg() # this is a list of probabilities
                        layup_outcomes = ['Fairway', 'First Cut', 'Second Cut']
                        layup = np.random.choice(layup_outcomes, size = 1, p = layup_probs)
                        self.distance_from_hole = self.stroke(layup)
                        self.location = layup

                    elif (self.distance_from_hole  >= 30) and (self.distance_from_hole <= 120):
                        # use the pitch method

                        print('4th')
                        pitch_probs = self.pitch() # this is a list of probabilities
                        pitch_outcomes = ['Green', 'First Cut', 'Second Cut']
                        pitch = np.random.choice(pitch_outcomes, size = 1, p = pitch_probs)
                        self.distance_from_hole = self.stroke(pitch)
                        self.location = pitch

                    else:
                        # use the chip method

                        print('5th')
                        chip_probs = self.chip() # this is a list of probabilities
                        chip_outcomes = ['Make Chip', 'Miss Chip']
                        chip = np.random.choice(chip_outcomes, size = 1, p = chip_probs)
                        self.distance_from_hole = self.stroke(chip)
                        self.location = 'Green'

                elif self.location == 'First Cut':
                    # The lie will adjust the maximum distance the player can reach the green in two.
                    # If poorer the lie is, the shorter the maximum distance becomes.
                    if (self.distance_from_hole <= 260) and (self.distance_from_hole > 120):

                        print('6th')
                        # use the gir method
                        approach_shot_probs = self.green_in_reg()
                        approach_shot_outcomes = ['Green', 'Fairway', 'First Cut', 'Second Cut']
                        approach_shot = np.random.choice(approach_shot_outcomes, size = 1, p = approach_shot_probs)
                        self.distance_from_hole = self.stroke(approach_shot)
                        self.location = approach_shot

                    elif self.distance_from_hole > 260:

                        print('7th')
                        # use the fir method
                        layup_probs = self.fairway_in_reg() # this is a list of probabilities
                        layup_outcomes = ['Fairway', 'First Cut', 'Second Cut']
                        layup = np.random.choice(layup_outcomes, size = 1, p = layup_probs)
                        self.distance_from_hole = self.stroke(layup)
                        self.location = layup

                    elif (self.distance_from_hole  >= 30) and (self.distance_from_hole <= 120):

                        print('8th')
                        # use the pitch method
                        pitch_probs = self.pitch() # this is a list of probabilities
                        pitch_outcomes = ['Green', 'First Cut', 'Second Cut']
                        pitch = np.random.choice(pitch_outcomes, size = 1, p = pitch_probs)
                        self.distance_from_hole = self.stroke(pitch)
                        self.location = pitch

                    else:
                        # use the chip method

                        print('9th')
                        chip_probs = self.chip() # this is a list of probabilities
                        chip_outcomes = ['Make Chip', 'Miss Chip']
                        chip = np.random.choice(chip_outcomes, size = 1, p = chip_probs)
                        self.distance_from_hole = self.stroke(chip)
                        self.location = 'Green'

                elif self.location == 'Second Cut':
                    # The lie will adjust the maximum distance the player can reach the green in two.
                    # If poorer the lie is, the shorter the maximum distance becomes.
                    if self.distance_from_hole <= 230 and self.distance_from_hole > 120:

                        print('10th')
                        # use the gir method
                        approach_shot_probs = self.green_in_reg()
                        approach_shot_outcomes = ['Green', 'Fairway', 'First Cut', 'Second Cut']
                        approach_shot = np.random.choice(approach_shot_outcomes, size = 1, p = approach_shot_probs)
                        self.distance_from_hole = self.stroke(approach_shot)
                        self.location = approach_shot

                    elif self.distance_from_hole > 230:

                        print('11th')
                        # use the fir method
                        layup_probs = self.fairway_in_reg() # this is a list of probabilities
                        layup_outcomes = ['Fairway', 'First Cut', 'Second Cut']
                        layup = np.random.choice(layup_outcomes, size = 1, p = layup_probs)
                        self.distance_from_hole = self.stroke(layup)
                        self.location = layup

                    elif (self.distance_from_hole  >= 30) and (self.distance_from_hole <= 120):

                        print('12th')
                        # use the pitch method
                        pitch_probs = self.pitch() # this is a list of probabilities
                        pitch_outcomes = ['Green', 'First Cut', 'Second Cut']
                        pitch = np.random.choice(pitch_outcomes, size = 1, p = pitch_probs)
                        self.distance_from_hole = self.stroke(pitch)
                        self.location = pitch

                    else:

                        print('13th')
                        # use the chip method
                        chip_probs = self.chip() # this is a list of probabilities
                        chip_outcomes = ['Make Chip', 'Miss Chip']
                        chip = np.random.choice(chip_outcomes, size = 1, p = chip_probs)
                        self.distance_from_hole = self.stroke(chip)
                        self.location = 'Green'

                elif self.location == 'Green':
                    # use the putt method

                    print('14th')
                    putt_probs = self.putt()
                    putt_outcomes = ['Make', 'Miss']
                    #putt = np.mean(np.random.choice([1, 0], size = 10, p = putt_probs)).round()
                    putt = np.random.choice(putt_outcomes, size = 1, p = putt_probs)
                    print(putt, putt_probs)
                    if putt == 'Make':
                        self.in_hole == True
                        self.number_of_strokes += 1
                        break
                    else:
                        self.distance_from_hole = self.stroke(putt)

                self.number_of_strokes += 1
            print('Number of strokes: ', self.number_of_strokes)
            total_strokes += self.number_of_strokes
        print('Total Number of Strokes', total_strokes)
        pass