from game_controller import GameController


# Main game loop
if __name__ == "__main__":
    game = GameController()
    game.start_game()
    
    while game.play:
        game.handle_action()