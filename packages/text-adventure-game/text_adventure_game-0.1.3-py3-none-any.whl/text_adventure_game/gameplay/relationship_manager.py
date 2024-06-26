class RelationshipManager:
    def __init__(self, game):
        self.game = game

    def choose_love_interest(self):
        print("请选择一个角色进行互动：")
        for i, relationship in enumerate(self.game.love_interests):
            print(f"{i + 1}. {relationship.character.name} - {relationship.relationship_type}")
        choice = int(input("输入角色的编号：")) - 1
        if 0 <= choice < len(self.game.love_interests):
            self.game.love_interests[choice].interact()
        else:
            print("无效的选择，请重新输入。")

    def check_relationships(self):
        for relationship in self.game.love_interests:
            relationship.check_affection()
