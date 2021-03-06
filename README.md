# Mahjong4RL 🀄

![Mahjong](https://img.shields.io/badge/awesome-mahjong-green)
![MIT license](https://img.shields.io/github/license/rasca0027/Mahjong4RL)
![PR closed](https://img.shields.io/github/issues-pr-closed/rasca0027/Mahjong4RL)
![hacktoberfest](https://img.shields.io/github/hacktoberfest/2020/rasca0027/Mahjong4RL)

Mahjong4RL is a project that recreates the game of Japanese Mahjong and use deep reinforcement learning to play it.

[Japanese Mahjong](https://en.wikipedia.org/wiki/Japanese_Mahjong), or Riichi Mahjong, is a variation of mahjong. While the basic rules to the game are retained, the variation emphasizes on player's menzenchin and features a unique set of rules such as riichi and doras.

We aim to create a game system of Japanese Mahjong from scratch. We will be implementing [this paper](https://arxiv.org/abs/2003.13590) afterwards.

## 🚀 Usage

```python
from mahjong.game import Game

names = ['Kelly', 'Leo', 'Ball', 'Hao']
game = Game(names)
game.start_game()
```

```
can add your own config json file to configs/
and change the following in python to use your config file

game = Game(names, YOUR_CONFIG_FILE_NAME)

available input: "inquirer" or "raw_input"
```

## 👀 Run Tests
```python
python -m unittest
```

## 📝 Documentation and TODOs
* [Notion Workspace](https://www.notion.so/mahjong4dl/)
* [English Terminology Reference](http://arcturus.su/wiki/List_of_terminology_by_usage_category)
* [Invitation to Notion Workspace](https://www.notion.so/mahjong4dl/invite/31fc3f4c23c97bff892986178b710ffa29f019b9)


## 👤 Author

* [Kelly Chang](https://github.com/rasca0027/)
* [K.T. Chang](https://github.com/ktc312)
* [Hao Shen](https://github.com/hoaaoh)
* [George Yang](https://github.com/HappyBall)
* [Yi-Hsuan Hsu](https://github.com/easonla)


## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)
