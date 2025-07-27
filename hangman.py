import random
import os
import sys
import requests
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class HangmanGame:
    def __init__(self):
        self.words = self.fetch_words_from_api()
        self.hangman_stages = self.create_hangman_stages()
        self.score = {"wins": 0, "losses": 0}
        self.difficulty_levels = {
            "easy": {"max_wrong": 8, "min_length": 4},
            "medium": {"max_wrong": 6, "min_length": 6},
            "hard": {"max_wrong": 4, "min_length": 8}
        }
        self.reset_game()
    
    def fetch_words_from_api(self):
        """Fetch words from Datamuse API with fallback to local list"""
        try:
            response = requests.get(
                "https://api.datamuse.com/words?sp=??????&max=50",
                timeout=3
            )
            if response.status_code == 200:
                return [item["word"] for item in response.json() 
                        if item.get("word") and 4 <= len(item["word"]) <= 10]
        except:
            pass
        
        # Fallback words if API fails
        return [
            "python", "programming", "computer", "algorithm", "function",
            "variable", "debugging", "software", "keyboard", "monitor",
            "internet", "website", "database", "server", "network",
            "creative", "challenge", "mystery", "adventure", "journey"
        ]
    
    def create_hangman_stages(self):
        """Create colorized hangman stages"""
        stages = []
        colors = [Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.RED, 
                 Fore.LIGHTRED_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX]
        
        stage_designs = [
            ["  ╔═════╗", "  ║     │", "      │", "      │", "      │", "      │", " ═══════"],
            ["  ╔═════╗", "  ║     │", f"{colors[0]}  O    │", "      │", "      │", "      │", " ═══════"],
            ["  ╔═════╗", "  ║     │", f"{colors[1]}  O    │", f"{colors[1]}  |    │", "      │", "      │", " ═══════"],
            ["  ╔═════╗", "  ║     │", f"{colors[2]}  O    │", f"{colors[2]} /|    │", "      │", "      │", " ═══════"],
            ["  ╔═════╗", "  ║     │", f"{colors[3]}  O    │", f"{colors[3]} /|\\   │", "      │", "      │", " ═══════"],
            ["  ╔═════╗", "  ║     │", f"{colors[4]}  O    │", f"{colors[4]} /|\\   │", f"{colors[4]} /     │", "      │", " ═══════"],
            ["  ╔═════╗", "  ║     │", f"{colors[5]}  O    │", f"{colors[5]} /|\\   │", f"{colors[5]} / \\   │", "      │", " ═══════"]
        ]
        
        return ["\n".join(stage) for stage in stage_designs]
    
    def reset_game(self):
        """Reset game state with new word based on difficulty"""
        self.word = self.select_word()
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong_guesses = self.difficulty_levels[self.difficulty]["max_wrong"]
        self.game_over = False
        self.won = False
        self.hint_used = False
    
    def select_word(self):
        """Select appropriate word based on difficulty"""
        min_length = self.difficulty_levels[self.difficulty]["min_length"]
        eligible_words = [w for w in self.words if len(w) >= min_length]
        return random.choice(eligible_words).upper()
    
    def display_hangman(self):
        """Display current hangman stage with colors"""
        stage_index = min(self.wrong_guesses, len(self.hangman_stages) - 1
        print(self.hangman_stages[stage_index])
    
    def display_word(self):
        """Display word with guessed letters revealed"""
        display = []
        for letter in self.word:
            if letter in self.guessed_letters:
                display.append(Fore.GREEN + letter + Style.RESET_ALL)
            else:
                display.append("_")
        return " ".join(display)
    
    def display_game_state(self):
        """Display full game state"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(Fore.CYAN + "=" * 50)
        print(Fore.YELLOW + "🎯 HANGMAN GAME" + Fore.MAGENTA + f" [Mode: {self.difficulty.upper()}]")
        print(Fore.CYAN + "=" * 50)
        
        self.display_hangman()
        
        print(f"\n{Fore.LIGHTBLUE_EX}Word: {self.display_word()}")
        
        remaining = self.max_wrong_guesses - self.wrong_guesses
        color = Fore.GREEN if remaining > 3 else Fore.YELLOW if remaining > 1 else Fore.RED
        print(f"{color}Wrong guesses remaining: {remaining}{Style.RESET_ALL}")
        
        if self.guessed_letters:
            sorted_guesses = sorted(self.guessed_letters)
            print(f"{Fore.LIGHTMAGENTA_EX}Guessed letters: {', '.join(sorted_guesses)}")
        
        print(Fore.CYAN + "-" * 50)
        print(f"{Fore.LIGHTYELLOW_EX}Score: {self.score['wins']} wins, {self.score['losses']} losses")
        
        if not self.hint_used:
            print(f"\n{Fore.LIGHTGREEN_EX}Type 'hint' for a free letter (one-time use)")
    
    def get_hint(self):
        """Provide a hint by revealing a random unguessed letter"""
        unguessed = [l for l in self.word if l not in self.guessed_letters]
        if unguessed and not self.hint_used:
            hint = random.choice(unguessed)
            self.guessed_letters.add(hint)
            self.hint_used = True
            return hint
        return None
    
    def is_valid_guess(self, guess):
        """Validate player input"""
        if guess.lower() in ['quit', 'exit']:
            print(f"{Fore.YELLOW}\nThanks for playing! 👋")
            sys.exit()
            
        if guess.lower() == 'hint':
            return True
        
        if len(guess) != 1:
            print(f"{Fore.RED}❌ Please enter only one letter!")
            return False
        
        if not guess.isalpha():
            print(f"{Fore.RED}❌ Please enter a valid letter!")
            return False
        
        if guess.upper() in self.guessed_letters:
            print(f"{Fore.YELLOW}❌ You already guessed that letter!")
            return False
        
        return True
    
    def make_guess(self, guess):
        """Process player guess"""
        if guess.lower() == 'hint':
            hint = self.get_hint()
            if hint:
                print(f"\n{Fore.GREEN}💡 HINT: The letter '{hint}' is in the word!")
                # Check if hint completed the word
                if all(l in self.guessed_letters for l in self.word):
                    self.won = True
                    self.game_over = True
            else:
                print(f"{Fore.RED}❌ No hints available!")
            return
        
        guess = guess.upper()
        self.guessed_letters.add(guess)
        
        if guess in self.word:
            print(f"\n{Fore.GREEN}✅ Good guess! '{guess}' is in the word!")
            # Check if word is complete
            if all(l in self.guessed_letters for l in self.word):
                self.won = True
                self.game_over = True
        else:
            self.wrong_guesses += 1
            print(f"\n{Fore.RED}❌ Sorry, '{guess}' is not in the word.")
            # Check if game is lost
            if self.wrong_guesses >= self.max_wrong_guesses:
                self.game_over = True
    
    def select_difficulty(self):
        """Let player select difficulty level"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + "=" * 50)
        print(Fore.YELLOW + "🎯 SELECT DIFFICULTY LEVEL 🎯")
        print(Fore.CYAN + "=" * 50)
        
        print(f"\n{Fore.LIGHTBLUE_EX}1. Easy   {Fore.GREEN}(8 guesses, simple words)")
        print(f"{Fore.LIGHTBLUE_EX}2. Medium {Fore.YELLOW}(6 guesses, medium words)")
        print(f"{Fore.LIGHTBLUE_EX}3. Hard   {Fore.RED}(4 guesses, complex words)")
        
        while True:
            choice = input(f"\n{Fore.MAGENTA}Enter choice (1-3): ").strip()
            if choice == '1': return "easy"
            elif choice == '2': return "medium"
            elif choice == '3': return "hard"
            print(f"{Fore.RED}❌ Invalid choice. Please enter 1, 2, or 3")
    
    def play_round(self):
        """Play a single round of the game"""
        while not self.game_over:
            self.display_game_state()
            
            try:
                guess = input(f"\n{Fore.LIGHTCYAN_EX}Enter your guess: ").strip()
                
                if self.is_valid_guess(guess):
                    self.make_guess(guess)
                    
                    if not self.game_over:
                        input(f"\n{Fore.LIGHTBLACK_EX}Press Enter to continue...")
                
            except KeyboardInterrupt:
                print(f"{Fore.YELLOW}\n\nGame interrupted. Thanks for playing! 👋")
                sys.exit()
        
        # Update score
        if self.won:
            self.score["wins"] += 1
        else:
            self.score["losses"] += 1
        
        # Show final state
        self.display_game_state()
        
        if self.won:
            print(f"{Fore.GREEN}🎉 CONGRATULATIONS! 🎉")
            print(f"You guessed the word: {Fore.LIGHTGREEN_EX}{self.word}")
            print(f"You won with {self.max_wrong_guesses - self.wrong_guesses} guesses remaining!")
        else:
            print(f"{Fore.RED}💀 GAME OVER! 💀")
            print(f"The word was: {Fore.LIGHTRED_EX}{self.word}")
            print("Better luck next time!")
        
        return True
    
    def play(self):
        """Main game loop"""
        print(f"{Fore.YELLOW}\n🎯 Welcome to Hangman! 🎯")
        print(f"{Fore.LIGHTCYAN_EX}Guess the hidden word one letter at a time.")
        print(f"Type 'hint' for a one-time free letter reveal.")
        print(f"Type 'quit' anytime to exit the game.")
        input(f"\n{Fore.LIGHTGREEN_EX}Press Enter to start...")
        
        self.difficulty = self.select_difficulty()
        
        while True:
            game_completed = self.play_round()
            
            if not game_completed:
                break
            
            print("\n" + Fore.CYAN + "=" * 50)
            play_again = input(f"{Fore.MAGENTA}Would you like to play again? (y/n): ").strip().lower()
            
            if play_again in ['y', 'yes']:
                self.reset_game()
                print(f"{Fore.GREEN}Starting new game...")
                input(f"{Fore.LIGHTBLACK_EX}Press Enter to continue...")
            else:
                print(f"{Fore.YELLOW}\nThanks for playing Hangman! Final score: ")
                print(f"{Fore.GREEN}Wins: {self.score['wins']} {Fore.LIGHTRED_EX}Losses: {self.score['losses']}")
                print(f"{Fore.LIGHTMAGENTA_EX}👋 Goodbye!")
                break

def main():
    game = HangmanGame()
    game.play()

if __name__ == "__main__":
    main()