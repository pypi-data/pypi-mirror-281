import random
from text_adventure_game.characters.character import Character
from text_adventure_game.gameplay.relationship import Relationship
from text_adventure_game.gameplay.quest import QuestManager
from text_adventure_game.gameplay.explore import Explore
from text_adventure_game.characters.status import Status
from text_adventure_game.inventory.inventory import Inventory
from text_adventure_game.inventory.equipment_view import EquipmentView
from text_adventure_game.gameplay.relationship_manager import RelationshipManager
from text_adventure_game.core.code import game_init
from text_adventure_game.core.constants import SCENES

class Game:
    def __init__(self, player_name="龙傲天"):
        from text_adventure_game.battle.battle import Battle  # 延迟导入
        self.player = Character(player_name, 100, 10, 5, 5, 5)
        self.love_interests = []
        self.quest_manager = QuestManager()
        self.scenes = SCENES
        self.current_scene = random.choice(self.scenes)
        self.completed_quests = []
        self.current_enemy = None
        self.battle = Battle(self)
        self.explore = Explore(self)
        self.status = Status(self)
        self.inventory = Inventory(self)
        self.equipment_view = EquipmentView(self)
        self.relationship_manager = RelationshipManager(self)

    def play(self):
        print("欢迎来到冒险与爱情的世界！")
        while self.player.health > 0:
            self.describe_scene()
            print("你想做什么？")
            print("1. 探索")
            print("2. 战斗")
            print("3. 任务")
            print("4. 查看状态")
            print("5. 查看物品栏")
            print("6. 查看装备栏")
            print("7. 住旅馆")
            print("8. 查看关系栏")
            print("9. 保存")
            print("10. 退出")

            action = input("请输入选项（1-10）：")
            if action == "1":
                self.explore.explore()
            elif action == "2":
                self.battle.choose_enemy()
            elif action == "3":
                self.quest_manager.manage_quests()
            elif action == "4":
                self.status.check_status()
            elif action == "5":
                self.inventory.check_inventory()
            elif action == "6":
                self.equipment_view.show_equipment()
            elif action == "7":
                self.visit_inn()
            elif action == "8":
                self.relationship_manager.check_relationships()
            elif action == "9":
                from text_adventure_game.save.save_load import save_game  # 延迟导入
                save_game(self)
                print("游戏已保存。")
            elif action == "10":
                print("游戏结束，再见！")
                break
            else:
                print("无效的选择，请重新输入。")

    def describe_scene(self):
        print(f"你现在在{self.current_scene}。")

    def visit_inn(self):
        gold_count = self.inventory.count_gold()
        if gold_count >= 1:
            self.inventory.remove_gold(1)
            print("你住进了旅馆，所有状态已恢复。")
            self.player.health = self.player.max_health
            self.player.mana = self.player.max_mana
            print(f"你花费了1金币，现在你还有 {self.inventory.count_gold()} 金币。")
        else:
            print("你没有足够的金币住旅馆。")

def new_game():
    game_init()
    player_name = input("请输入你的名字：")
    game = Game(player_name)
    game.play()

def continue_game():
    from text_adventure_game.save.save_load import load_game  # 延迟导入
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
