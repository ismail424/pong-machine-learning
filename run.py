from pong.view.PongGUI import PongGUI
from pong.AI.PongAI import PongAI
if __name__ == "__main__":
    # Run the game normally
    #PongGUI.run()
    
    # Train the AI
    #PongAI.run_neat( load_checkpoint = "neat-checkpoint-54" )

    # Test AI
    PongAI.test_ai()