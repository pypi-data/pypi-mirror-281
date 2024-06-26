class Item:
    def __init__(self, name, description, rarity, item_type, quantity=1, attributes=None):
        self.name = name
        self.description = description
        self.rarity = rarity
        self.item_type = item_type
        self.quantity = quantity
        self.attributes = attributes if attributes else {}

    def __str__(self):
        quantity_str = f" x{self.quantity}" if self.quantity > 1 else ""
        attributes_str = f" ({', '.join(f'{k}: {v}' for k, v in self.attributes.items())})"
        return f"{self.name} ({self.rarity}): {self.description}{quantity_str}{attributes_str}"

    def use(self, character):
        if self.item_type == "potion":
            self.apply_potion_effect(character)
        elif self.item_type == "weapon":
            print(f"{self.name} 是一种武器，可以装备在装备栏中。")
        elif self.item_type == "armor":
            print(f"{self.name} 是一种护甲，可以装备在装备栏中。")
        elif self.item_type == "skill_book":
            character.learn_skill(self)
        elif self.item_type == "mount":
            character.equipment.equip_mount(self)
        elif self.item_type == "mount_armor":
            character.equipment.equip_mount_armor(self)
        else:
            print(f"{self.name} 无法使用。")

    def apply_potion_effect(self, character):
        if self.name == "治疗药剂":
            character.health = min(character.max_health, character.health + 20)
            print(f"{character.name} 使用了 {self.name}，恢复了 20 点生命值。")
            self.quantity -= 1
        elif self.name == "力量药水":
            character.strength += 5
            print(f"{character.name} 使用了 {self.name}，力量增加了 5 点。")
            self.quantity -= 1
        # 添加更多药水的效果
        else:
            print(f"{self.name} 无法使用。")
