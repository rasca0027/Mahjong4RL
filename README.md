# Mahjong4RL

名詞對照表：http://arcturus.su/wiki/List_of_terminology_by_usage_category

回合 flowchart https://app.lucidchart.com/documents/view/1dea0807-cc12-4456-85c1-fd118aa442ba


玩家
- 名字
- 座位（風）
- ~~點棒~~
- 是否立直
- 手牌 list of Tiles
- 副露 list of list of Tiles
- 打出來的牌

牌
- suit
- Value
- 寶牌

回合
- 以其中一個打出排為開始，到下一個人打出牌瞬間結束
- 如果有人和牌就結束局
- 規則

局
- 洗牌結果
- 寶牌
- 發到第幾張牌了
- ~~誰是莊家~~
- ~~幾本場~~


TODO:
[ ] dora記在Kyoku裡面 把Tile的is_dora拿掉
[ ] set_dora() 移到Kyoku (dora可能會增加)
[ ] naki_and_actions 新增check_tsumo() 跟check_ron() call同一個helper function
[ ] 7/30 先寫player 再寫吃碰槓
