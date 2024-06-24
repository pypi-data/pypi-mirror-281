class Status:
    def __init__(self, game):
        self.game = game

    def check_status(self):
        player = self.game.player
        print(f"玩家状态：")
        print(f"等级：{player.level}")
        print(f"经验值：{player.experience}/{player.level * 10}")
        print(f"生命值：{player.health}/{player.max_health}")
        print(f"力量：{player.strength}")
        print(f"魅力：{player.charm}")
        print(f"智力：{player.intelligence}")
        print(f"敏捷：{player.agility}")

