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

    def equip_weapon(self, weapon, slot=-1):
        if 0 <= slot < 4:
            self.weapon_slots[slot] = weapon
        else:
            self.equip_random_weapon(weapon)
             
    def equip_random_weapon(self,weapon):
        for slot in range(4):
            if self.weapon_slots[slot] is None:
                self.weapon_slots[slot] = weapon
                return

    def unequip_weapon(self, slot):
        if 0 <= slot < 4:
            weapon = self.weapon_slots[slot]
            self.weapon_slots[slot] = None
            return weapon
        else:
            return None

    def get_equipped_weapon(self):
        for weapon in self.weapon_slots:
            if weapon:
                return weapon
        return None

    def equip_armor(self, armor, slot):
        if slot in self.armor_slots:
            self.armor_slots[slot] = armor

    def unequip_armor(self, slot):
        if slot in self.armor_slots:
            armor = self.armor_slots[slot]
            self.armor_slots[slot] = None
            return armor
        else:
            return None

    def get_defense(self):
        total_defense = 0
        for armor in self.armor_slots.values():
            if armor:
                total_defense += armor.defense
        return total_defense

    def equip_mount(self, mount):
        self.mount = mount

    def unequip_mount(self):
        mount = self.mount
        self.mount = None
        return mount

    def equip_mount_armor(self, mount_armor):
        self.mount_armor = mount_armor

    def unequip_mount_armor(self):
        mount_armor = self.mount_armor
        self.mount_armor = None
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
    def __init__(self, name, defense, description, slot, resistance=0):
        self.name = name
        self.defense = defense
        self.description = description
        self.slot = slot
        self.resistance = resistance

    def __str__(self):
        return f"{self.name} - 防御: {self.defense} - 抗性: {self.resistance} - 槽位: {self.slot} - {self.description}"
    
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



