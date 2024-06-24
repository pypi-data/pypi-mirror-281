import random
from .character import Character
from .constants import SCENES, ENEMIES_BY_SCENE, BOSSES, LOVE_INTERESTS
from .relationship import Relationship
from .quest import QuestManager
from .skill import SKILL_BOOKS
from .battle import Battle
from .explore import Explore
from .status import Status
from .inventory import Inventory
from .relationship_manager import RelationshipManager
from .save_load import save_game, load_game
from .code import game_init

class Game:
    def __init__(self, player_name="龙傲天"):
        self.player = Character(player_name, 100, 10, 5, 5, 5)
        self.love_interests = [Relationship(self.player, love_interest) for love_interest in LOVE_INTERESTS]
        self.quest_manager = QuestManager()
        self.scenes = SCENES
        self.current_scene = random.choice(self.scenes)
        self.completed_quests = []
        self.current_enemy = None
        self.battle = Battle(self)
        self.explore = Explore(self)
        self.status = Status(self)
        self.inventory = Inventory(self)
        self.relationship_manager = RelationshipManager(self)

    def play(self):
        print("欢迎来到冒险与爱情的世界！")
        while self.player.health > 0:
            self.describe_scene()
            print("你想做什么？")
            print("1. 探索")
            print("2. 战斗")
            print("3. 谈恋爱")
            print("4. 任务")
            print("5. 查看状态")
            print("6. 查看物品栏")
            print("7. 查看关系栏")
            print("8. 保存")
            print("9. 退出")
            action = input("请输入选项（1-9）：")
            if action == "1":
                self.explore.explore()
            elif action == "2":
                self.battle.choose_enemy()
            elif action == "3":
                self.relationship_manager.choose_love_interest()
            elif action == "4":
                self.quest_manager.manage_quests()
            elif action == "5":
                self.status.check_status()
            elif action == "6":
                self.inventory.check_inventory()
            elif action == "7":
                self.relationship_manager.check_relationships()
            elif action == "8":
                save_game(self)
                print("游戏已保存。")
            elif action == "9":
                print("游戏结束，再见！")
                break
            else:
                print("无效的选择，请重新输入。")

    def describe_scene(self):
        print(f"你现在在{self.current_scene}。")

def new_game():
    game_init()
    player_name = input("请输入你的名字：")
    game = Game(player_name)
    game.play()

def continue_game():
    game = load_game()
    if game:
        game.play()
    else:
        print("没有找到保存的游戏，开始新游戏。")
        new_game()

def game_run():
    print("你想要做什么？")
    print("1. 新游戏")
    print("2. 继续游戏")
    choice = input("请输入选项（1或2）：")
    if choice == "1":
        new_game()
    elif choice == "2":
        continue_game()
    else:
        print("无效的选择，请重新运行程序。")
