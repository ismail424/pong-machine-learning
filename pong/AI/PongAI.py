from pong.view.PongGUI import PongGUI
from pong.view.theme.Cool import Cool
from pong.view.theme.Duckie import Duckie
from pong.model.Pong import Pong
from pong.model.Config import *
import neat
import pickle
import os
import pygame

class PongAI(PongGUI):
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    @classmethod
    def run_neat(cls, load_checkpoint: str = None):
        if load_checkpoint is not None:
            # Load from checkpoint
            check_points_dir = os.path.join(cls.dir_path, "checkpoints")
            checkpoint = os.path.join(check_points_dir, load_checkpoint)
            p = neat.Checkpointer.restore_checkpoint(checkpoint)
        else:
            # Load from config file
            config = cls.__load_config()
            p = neat.Population(config)
        
        # Print Information
        p.add_reporter(neat.StdOutReporter(True))
        
        # Statistics Reporter 
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        
        # Save Checkpoints
        check_points_dir = os.path.join(cls.dir_path, "checkpoints")
        p.add_reporter(neat.Checkpointer(5, filename_prefix=check_points_dir + '/neat-checkpoint-')) # Save every 5 generations
        
        # Get the best genome
        winner = p.run(cls.__eval_genomes, 50)
        best_ai_object_path = os.path.join(cls.dir_path, "best_ai_object.pkl")
        print("Saving best AI object to: " + best_ai_object_path)
        with open(best_ai_object_path, 'wb') as output:
            pickle.dump(winner, output)         
    
    @classmethod
    def train_ai(cls, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
                
        # Load assets
        cls.running = True
        cls.assets = Cool()
        Pong.load_entities()
        Pong.reset_points()
        while cls.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                         
            output1 = net1.activate((Pong.left_paddle.y, Pong.ball.y, abs(Pong.ball.x - Pong.left_paddle.x)))
            decision1 = output1.index(max(output1))
            
            if decision1 == 0:
                pass
            elif decision1 == 1:
                cls.move_paddle(left=True, up=True)
            else:
                cls.move_paddle(left=True, up=False)
                
            
            output2 = net2.activate((Pong.right_paddle.y, Pong.ball.y, abs(Pong.ball.x - Pong.right_paddle.x)))
            decision2 = output2.index(max(output2))
            
            if decision2 == 0:
                pass
            elif decision2 == 1:
                cls.move_paddle(left=False, up=True)
            else:
                cls.move_paddle(left=False, up=False)
                
            
            Pong.update()
            cls.render()
            if Pong.points_left >= 1 or Pong.points_right >= 1 or Pong.left_hits > 50 or Pong.right_hits > 50:
                cls.calculate_fitness(genome1, genome2)
                break
            cls.clock.tick(120)
            
    @classmethod
    def get_best_ai(cls):
        best_ai_object_path = os.path.join(cls.dir_path, "best_ai_object.pkl")
        return pickle.load(open(best_ai_object_path, 'rb'))

    @classmethod
    def test_ai(cls):
        net = neat.nn.FeedForwardNetwork.create(cls.get_best_ai(), cls.__load_config())
        
        # Load assets
        cls.running = True
        cls.assets = Cool()
        cls.init_pygame()
        Pong.load_entities()
        Pong.reset_points()

        while cls.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                         
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_UP]:
                cls.move_paddle(left=False, up=True)
            elif key_pressed[pygame.K_DOWN]:
                cls.move_paddle(left=False, up=False)
            else:
                Pong.right_paddle.accelerate(0,0)

            
                
            output = net.activate((Pong.left_paddle.y, Pong.ball.y, abs(Pong.ball.x - Pong.left_paddle.x)))
            decision = output.index(max(output))
            
            if decision == 0:
                pass
            elif decision == 1:
                cls.move_paddle(left=True, up=True)
            else:
                cls.move_paddle(left=True, up=False)

            
            Pong.update()
            cls.render()

            cls.clock.tick(60)

    @classmethod
    def calculate_fitness(cls, genome1, genome2):
        genome1.fitness += Pong.points_left
        genome2.fitness += Pong.right_hits

    @classmethod
    def __eval_genomes(cls, genomes, config):
        """Evaluates the genomes."""
        cls.init_pygame()
        
        for i, (genome_id1 , genome1) in enumerate(genomes):
            if i == len(genomes) - 1:
                break
            genome1.fitness = 0
            
            for genome_id2, genome2 in genomes[i+1:]:
                genome2.fitness = 0 if genome2.fitness == None else genome2.fitness

                cls.train_ai(genome1, genome2, config)
            
    @classmethod
    def __load_config(cls):
        local_dir = os.path.dirname(__file__)
        config_pah = os.path.join(local_dir, 'config.ini')
        
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_pah
                            )
        return config
    

    