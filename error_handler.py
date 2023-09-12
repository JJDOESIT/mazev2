class Error_Handler:
    def __init__(self, state_manager, text):
        self.state_manager = state_manager
        self.text = text

    #Check for errors when maze page is open
    def check_for_errors(self):
        if not self.state_manager.draw_maze:
            self.text.handle_text('Error: Generate or Draw Maze', 'Error: Generate or Draw Maze (press g or d)', self.state_manager)
            return False
        elif self.state_manager.start==None or self.state_manager.stop==None:
            self.text.handle_text('Error: No Start or Stop', 'Error: No Start or Stop (start + end must be placed)', self.state_manager)
            return False
        elif not self.state_manager.solution_path and not self.state_manager.step_path:
            self.text.handle_text('Error: Recache', 'Error: Recache (select an algorithm)', self.state_manager)
            return False
        return True
    
    #Check to see if maze page is even open
    def check_algorithm_error(self):
        if not self.state_manager.draw_maze:
            self.text.handle_text('Error: Generate or Draw Maze', 'Error: Generate or Draw Maze (press g or d)', self.state_manager)
            return False
        elif self.state_manager.start==None or self.state_manager.stop==None:
            self.text.handle_text('Error: No Start or Stop', 'Error: No Start or Stop (start + end must be placed)', self.state_manager)
            return False
        return True