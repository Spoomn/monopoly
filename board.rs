use rand::Rng;

struct Player {
    position: usize,
    money: i32,
}

impl Player {
    fn new() -> Self {
        Player {
            position: 0,
            money: 1500,
        }
    }
}

struct MonopolyGame {
    player: Player,
    board: Vec<(&'static str, i32)>,
}

impl MonopolyGame {
    fn new() -> Self {
        let board = vec![
            ("Go", 0), ("Mediterranean Avenue", 0), ("Community Chest", 0), ("Baltic Avenue", 0),
            ("Income Tax", 0), ("Reading Railroad", 0), ("Oriental Avenue", 0), ("Chance", 0),
            ("Vermont Avenue", 0), ("Connecticut Avenue", 0), ("Jail", 0), ("St. Charles Place", 0),
            ("Electric Company", 0), ("States Avenue", 0), ("Virginia Avenue", 0), ("Pennsylvania Railroad", 0),
            ("St. James Place", 0), ("Community Chest", 0), ("Tennessee Avenue", 0), ("New York Avenue", 0),
            ("Free Parking", 0), ("Kentucky Avenue", 0), ("Chance", 0), ("Indiana Avenue", 0),
            ("Illinois Avenue", 0), ("B&O Railroad", 0), ("Atlantic Avenue", 0), ("Ventnor Avenue", 0),
            ("Water Works", 0), ("Marvin Gardens", 0), ("Go To Jail", 0), ("Pacific Avenue", 0),
            ("North Carolina Avenue", 0), ("Community Chest", 0), ("Pennsylvania Avenue", 0),
            ("Short Line", 0), ("Chance", 0), ("Park Place", 0), ("Luxury Tax", 0), ("Boardwalk", 0),
        ];
        MonopolyGame {
            player: Player::new(),
            board,
        }
    }

    fn play(&mut self) {
        let mut moves = 0;
        let mut doubles_count = 0;

        loop {
            println!("Player is at {}", self.board[self.player.position].0);

            let dice_roll = roll_dice();
            println!("rolled a {}", dice_roll.0);

            self.player.position += dice_roll.0;

            if dice_roll.1 {
                doubles_count += 1;
            } else {
                doubles_count = 0;
            }

            if doubles_count == 3 {
                self.player.position = 10;
                println!("\nPlayer rolled three doubles in a row and is now in Jail\n");
                doubles_count = 0;
            }

            moves += 1;

            if self.player.position == 30 {
                self.player.position = 10;
                println!("\nPlayer landed on Go To Jail and is now in Jail\n");
            }

            if self.player.position >= 40 {
                self.player.position -= 40;
                self.player.money += 200;
                println!("Player passed Go and collected $200");
            }

            println!("Player is now at {}", self.board[self.player.position].0);

            println!("Player has made {} moves", moves);

            let landing = self.board[self.player.position];
            self.board[self.player.position] = (landing.0, landing.1 + 1);
            println!("Player has landed on {} {} times", self.board[self.player.position].0, self.board[self.player.position].1);

            if self.is_game_over() {
                println!("Player has ${}", self.player.money);
                println!("Game Over");
                break;
            }
        }
    }

    fn is_game_over(&self) -> bool {
        self.player.money >= 21000
    }
}

fn roll_dice() -> (usize, bool) {
    let mut rng = rand::thread_rng();
    let die1 = rng.gen_range(1..=6);
    let die2 = rng.gen_range(1..=6);
    let sum = die1 + die2;
    let doubles = die1 == die2;
    (sum, doubles)
}

fn main() {
    let mut game = MonopolyGame::new();
    game.play();
}
