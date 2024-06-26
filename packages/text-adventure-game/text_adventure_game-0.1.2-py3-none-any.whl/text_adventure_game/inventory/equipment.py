class Equipment:
    def __init__(self):
        self.weapon_slots = [None, None, None, None]  # 四个武器栏
        self.armor_slots = {
            "头": None,
            "身": None,
            "手腕": None,
            "手套": None,
            "腿": None,
            "脚": None
        }
        self.mount = None
        self.mount_armor = None

    def equip_weapon(self, weapon, slot):
        if 0 <= slot < 4:
            self.weapon_slots[slot] = weapon
            print(f"装备 {weapon.name} 在槽位 {slot + 1}")
        else:
            print("无效的槽位。")

    def unequip_weapon(self, slot):
        if 0 <= slot < 4:
            weapon = self.weapon_slots[slot]
            self.weapon_slots[slot] = None
            print(f"卸下 {weapon.name} 从槽位 {slot + 1}")
            return weapon
        else:
            print("无效的槽位。")
            return None

    def get_equipped_weapon(self):
        for weapon in self.weapon_slots:
            if weapon:
                return weapon
        return None

    def equip_armor(self, armor, slot):
        if slot in self.armor_slots:
            self.armor_slots[slot] = armor
            print(f"装备 {armor.name} 在 {slot} 部位")
        else:
            print("无效的槽位。")

    def unequip_armor(self, slot):
        if slot in self.armor_slots:
            armor = self.armor_slots[slot]
            self.armor_slots[slot] = None
            print(f"卸下 {armor.name} 从 {slot} 部位")
            return armor
        else:
            print("无效的槽位。")
            return None

    def get_defense(self):
        total_defense = 0
        for armor in self.armor_slots.values():
            if armor:
                total_defense += armor.attributes.get("defense", 0)
        return total_defense

    def equip_mount(self, mount):
        self.mount = mount
        print(f"装备 {mount.name} 作为坐骑")

    def unequip_mount(self):
        mount = self.mount
        self.mount = None
        print(f"卸下 {mount.name} 作为坐骑")
        return mount

    def equip_mount_armor(self, mount_armor):
        self.mount_armor = mount_armor
        print(f"装备 {mount_armor.name} 作为坐骑护甲")

    def unequip_mount_armor(self):
        mount_armor = self.mount_armor
        self.mount_armor = None
        print(f"卸下 {mount_armor.name} 作为坐骑护甲")
        return mount_armor


class Weapon:
    def __init__(self, name, damage, description, armor_penetration=0, quantity=None):
        self.name = name
        self.damage = damage
        self.description = description
        self.armor_penetration = armor_penetration
        self.quantity = quantity  # 数量仅适用于远程武器

    def __str__(self):
        quantity_str = f" - 数量: {self.quantity}" if self.quantity is not None else ""
        return f"{self.name} - 伤害: {self.damage} - 护甲穿透: {self.armor_penetration}{quantity_str} - {self.description}"

class Armor:
    def __init__(self, name, defense, description, resistance=0):
        self.name = name
        self.defense = defense
        self.description = description
        self.resistance = resistance

    def __str__(self):
        return f"{self.name} - 防御: {self.defense} - 抗性: {self.resistance} - {self.description}"

class Mount:
    def __init__(self, name, speed, health, description):
        self.name = name
        self.speed = speed
        self.health = health
        self.description = description

    def __str__(self):
        return f"{self.name} - 速度: {self.speed} - 生命值: {self.health} - {self.description}"

class MountArmor:
    def __init__(self, name, defense, description):
        self.name = name
        self.defense = defense
        self.description = description

    def __str__(self):
        return f"{self.name} - 坐骑防御: {self.defense} - {self.description}"



