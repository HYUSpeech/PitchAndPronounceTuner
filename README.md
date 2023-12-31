# PitchAndPronounceTuner
## 🎙️Introduction
Our project aims to increase accessibility to singing of hearing-impaired people using voice recognition. To achieve this goal, we made a web service with pronunciation recognition function, pitch detection function.

## 📽️Demo Video

## 🧑🏻‍💻People
Team. 구구빵빵
- [박성진](https://github.com/sjpark0070) | Data Preprocessing, Web Front-end
- [안세윤](https://github.com/yunniya097) | Pitch Detection, UI Design(App), Back-end
- [이동준](https://github.com/dongjun0207) | Data Preprocessing, Pronounciation
- [전민지](https://github.com/minji9924) | Team Leader, Web Front-end, Back-end

## 🗓️Schedule
### Duration
2023.04.01 - 2023.06.11

### Presentation Schedule
|날짜|일정|
|:-----:|:-----:|
|2023.04.04 (Tue) | Proposal Submission |
|2023.04.11 (Tue) | Proposal Presentation |
|2023.05.11 (Thu) | Interim Presentation |
|2023.06.13 (Tue) | Final Presentation |
|2023.06.15 (Thu) | Demo Day |

### WBS
Initial WBS
<img width="1002" alt="image" src="https://github.com/HYUSpeech/PitchAndPronounceTuner/assets/81553569/54fed1de-ed5f-4ab4-bc9e-e0935f763c6f">

Final WBS\
<img width="933" alt="wbs" src="https://github.com/HYUSpeech/PitchAndPronounceTuner/assets/58546758/b983416d-c95c-45f3-b2e3-64ddb3da05e0">


## 🔥How to Build
### Data
We’ve used the [‘한국어 음성’](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=123) data from AI hub.

Actually this dataset was created by the kospeech team, the toolkit we used. They build this dataset for the purpose of training the communicative speech recognition AI technology. Kospeech supports the preprocessing rules for this dataset, and this helps to save time in preprocessing session.

### SetUp
1) Setup environment for flask
   
   ```bash
   pip install flask
   ```
   
   if you use conda environment,
   
   ```bash
   conda install -c anaconda flask
   ```

3) Download libraries used in project using **‘requirements.txt’** file in the project folder

   ```bash
   pip install -r requirements.txt
   ```
   
4) Before running project, we need answer label for pitch and pronunciation 

   - First, prepare the answer label of pitch recognition data in ‘**pitch_data**’ folder. 

   - And then for speech recognition write the answer label at **app.py** 147th line, origin text variable.

5) After the answer label is prepared, we need to setup the information of the songs.

   - Change the directory path of data and pitch. These path parameter is at setup phase of **app.py**

   - Change the song **name(song)** and audio **data file name(data_name)** below the directory path in the setup phase.

6) Run the project folder with local connection
   ```bash
   python app.py
   ```

## 📬Contact
If you have any questions, please send an email to **pureb_9924@naver.com**
