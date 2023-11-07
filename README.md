# Czech Quest: Master 1000 Words


Czech Quest is a terminal based, immersive language learning application designed to help users master 1000 common Czech words through an engaging, adaptive, and fun learning process. Utilizing the Leitner system and focused repetition, the app ensures effective vocabulary retention and learning.

![image](https://github.com/diamond-one/Czech_Quest/assets/45215287/d5e9082b-5d55-45df-98d5-1e6e224e41f9)


## Features
- **Interactive Learning**: Users interactively learn new Czech words and their usage in sentences.
- **Adaptive Learning**: The app adapts to the user's progress using the Leitner system, ensuring efficient learning.
- **Audio Integration**: Integration with `gtts` and `pygame` for auditory learning.
- **Progress Tracking**: User progress is saved and loaded from JSON files, allowing for continuity in learning.
- **Scoreboard**: Keep track of your learning streaks and scores.
- **Interface**: By choice the UI is purely terminal based, no colour, not distractions, minimal frills.. just learning

## Installation

To get started with Czech Quest, you need to have Python installed on your system. Then, you can clone the repository and install the required dependencies.

```bash
git clone https://github.com/your-username/Czech-Quest.git
cd Czech-Quest
pip install -r requirements.txt
```

## Usage

Run the main script to start the application:

```bash
python main.py
```

1. **Enter your username**: This allows the app to track your individual progress.
2. **Engage with the session**: The app will present you with words and sentences. Your task is to guess the English translation.
3. **Learn and Repeat**: Based on your answers, the app will adapt and present new words or repeat ones you're struggling with.
4. **Track Your Progress**: Your progress is saved after each session.

## File Structure

- `utilities/`: Contains utility scripts for score management and progress tracking.
- `content/common_1000/`: The dataset of 1000 common Czech words.
- `main.py`: Main script to run the application.
- `requirements.txt`: Required Python packages.

## Contributing

Contributions to Czech Quest are welcome! Whether it's bug fixes, feature additions, or improvements in documentation, your help is appreciated.

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- [gtts (Google Text-to-Speech)](https://pypi.org/project/gTTS/)
- [pygame](https://www.pygame.org/news)
- [Pandas](https://pandas.pydata.org/)

---

Start your journey to Czech mastery with Czech Quest today! 🚀🇨🇿

