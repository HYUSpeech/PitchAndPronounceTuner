# PitchAndPronounceTuner
## 🎙️Introduction

## Demo Video

## 🧑🏻‍💻People
Team. 구구빵빵
- [박성진](https://github.com/sjpark0070) | Data Preprocessing, Web Front-end
- [안세윤](https://github.com/yunniya097) | Pitch Detection, UI Design(App), Back-end
- [이동준](https://github.com/dongjun0207) | Data Preprocessing, Pronounciation
- [전민지](https://github.com/minji9924) | Team Leader, Web Front-end, Back-end

## Duration
2023.04.01 - 2023.06.11

## Schedule
|날짜|일정|
|:-----:|:-----:|
|2023.04.04 (Tue) | Proposal Submission |
|2023.04.11 (Tue) | Proposal Presentation |
|2023.05.11 (Thu) | Interim Presentation |
|2023.06.13 (Tue) | Final Presentation |
|2023.06.15 (Thu) | Demo Day |

## How to Build
1) Setup environment for flask
   
   ```bash
   pip install flask
   ```
   
   if you use conda environment,
   
   ```bash
   conda install -c anaconda flask
   ```

3) Download libraries used in project using ‘requirements.txt’ file in the project folder
   

4) Before running project, we need answer label for pitch and pronunciation 

   First, prepare the answer label of pitch recognition data in ‘**pitch_data**’ folder. 

   And then for speech recognition write the answer label at [app.py](http://app.py) 147th line, origin text variable.

5) After the answer label is prepared, we need to setup the information of the songs.

   Change the directory path of data and pitch. These path parameter is at setup phase of [app.py](http://app.py)

   Change the song name(song) and audio data file name(data_name) below the directory path in the setup phase.

6) Run the project folder with local connection

### Set Up

### Data

