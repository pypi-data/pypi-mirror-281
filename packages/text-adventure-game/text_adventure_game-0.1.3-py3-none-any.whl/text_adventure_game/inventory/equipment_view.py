class EquipmentView:
    def __init__(self, game):
        self.game = game

    def show_equipment(self):
        player = self.game.player
        print("装备栏：")

        for slot, armor in player.equipment.armor_slots.items():
            if armor:
                print(f"{slot}: {armor.name} - 防御: {armor.defense}")
            else:
                print(f"{slot}: 空")

        for i, weapon in enumerate(player.equipment.weapon_slots):
            if weapon:
                print(f"武器槽 {i + 1}: {weapon.name} - 伤害: {weapon.damage}")
            else:
                print(f"武器槽 {i + 1}: 空")

        mount = player.equipment.mount
        if mount:
            print(f"坐骑: {mount.name} - 速度: {mount.speed} - 生命值: {mount.health}")
        else:
            print("坐骑: 空")

        mount_armor = player.equipment.mount_armor
        if mount_armor:
            print(f"坐骑护甲: {mount_armor.name} - 防御: {mount_armor.defense}")
        else:
            print("坐骑护甲: 空")
