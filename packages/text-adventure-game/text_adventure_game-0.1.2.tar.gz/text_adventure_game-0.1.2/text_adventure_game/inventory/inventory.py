from text_adventure_game.characters.skill import SkillBook
from text_adventure_game.inventory.equipment import Weapon, Armor
from text_adventure_game.inventory.items import LootItem

class Inventory:
    def __init__(self, game):
        self.game = game

    def check_inventory(self):
        print("物品栏：")
        for i, item in enumerate(self.game.player.inventory, 1):
            print(f"{i}. {item}")
        self.use_item()

    def use_item(self):
        choice = input("请输入要使用的物品编号（或按Enter跳过）：")
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(self.game.player.inventory):
                item = self.game.player.inventory[index]
                print(type(item))
                if isinstance(item, SkillBook):
                    self.learn_skill(item)
                elif isinstance(item, Weapon):
                    slot = int(input("请输入要装备的槽位编号（1-4）：")) - 1
                    self.game.player.equipment.equip_weapon(item, slot)
                elif isinstance(item, Armor):
                    print("可用的盔甲槽位：头，身，手腕，手套，腿，脚")
                    slot = input("请输入要装备的盔甲槽位：")
                    self.game.player.equipment.equip_armor(item, slot)
                elif isinstance(item, LootItem) and item.item_type == "potion":
                    item.use(self.game.player)
                    if item.quantity <= 0:
                        self.game.player.inventory.pop(index)
                else:
                    print("该物品不能使用。")
            else:
                print("无效的选择。")
        else:
            print("跳过使用物品。")

    def learn_skill(self, skill_book):
        if skill_book.requirement(self.game.player):
            self.game.player.skills.append(skill_book.skill)
            self.game.player.inventory.remove(skill_book)
            print(f"你学习了技能：{skill_book.skill['name']} - {skill_book.skill['description']}")
        else:
            print(f"你的属性未达到学习 {skill_book.name} 的要求。")