
# 최종 보고서 및 기술 문서 제출

# Technical Document

1. How to use
    
    Follow the process shown below. 
    
    1. Choose the mode between ‘튜토리얼 연습하기’ and ‘노래 연습하기’
    2. Record the song, if you are not satisfying with the result you can record again.
    3. It takes little time to analyze the input file, wait for a second.
    4. User can check the result in next page. While pronunciation score is shown in percentage, the rate of correctness, the pitch score is shown is error score, the amount of distances between the input and answer.
    5. User can compare the differences. The user and answer pronunciation/pitch is shown through the UI.
    
2. Function details
    
    1) pcm2wav.py
    
    - make_wav_format(pcm_data:bytes, ch:int)
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled.png)
        
        Used for converting the audio file format from .pcm to .wav
        
        The initial recorded audio is saved as pcm file, but the neede file format for  wav. So we converted the pcm audio to wav audio using this function. 
        
        After changing some details and functions, the recorded audio is saved as both pcm and wav file, so no more needed. This function may be used in future processing.
        
    
    2) sp_recog.py
    
    - recognition(convert_path)
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled%201.png)
        
        The main function of the speech recognition.
        
        First we used the DeepSpeech2 model, but our preprocessing for noisy audio file’s was not enough to get the satisfactory accuracy. So, for the level of completion, we decided to use google STT api. 
        
        Also, this api provide the option for Korean, so we can both analyze the english song and korean song by changing language format.
        
    
    3) pitch_detection.py
    
    For pitch detection, we used the SPICE model supported by TensorFlow Hub.
    
    - convert_audio_for_model(user_file, output_file='converted_audio_file.wav')
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled%202.png)
        
        Convert audio file to the expected format, this format does mean the file format. In this phase, convert the original audio file the sampling rate of 16KHz with only one channel, the mono audio.
        
    - output2hz(pitch_output)
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled%203.png)
        
        The pitch value returned by SPICE model are in the range of 0 to 1. We need to convert these values into absolute pitch values represented with hz.
        
    - hz2offset(C0,freq)
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled%204.png)
        
        Our recording data include the individual’s sing, not an absolute value pitch value. So, the before converting the pitch values to notes, the correction for possible offset is needed. So we use this function to correct the possible offset.
        
    - quantize_predictions(group, ideal_offset, note_names, C0), get_quantization_and_error(pitch_outputs_and_rests, predictions_per_eighth, prediction_start_offset, ideal_offset, note_names, C0)
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled%205.png)
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled%206.png)
        
        Before use some heuristics to try and estimate the answer sequence of notes, We need to know the speed and the time offset of quantizing start point. So, we different the speeds and time offsets, and measure the qunatization error.
        
    
    4) metric.py
    
    - originer_note(lines)
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled%207.png)
        
        Used for pitch_metric_eval.
        
        Divide the input notes returned in string into seperated array form.
        
    - pitch_metric_eval(ori_note, detect_note)
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled%2015.png)
        
        Evaluation metrics for pitch accuracy score.
        
        Simply calculate the differences between the notes, this error depends on distances between the answer and input. We used mean squared error score.
        
    - pronoun_metric_eval(origin_txt, pronoun_text)
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled%208.png)
        
        Evaluation metrics for pronunciation accuracy score.
        
        Check the wrong input compared with the answer text, and calculate the accuracy. When all the input is correct the accuracy percentage will be 100%.
        
    
3. Parameter/variable -> what is function for, how to adjust parameter/variables, and the resuslt of adjustment
    1. Model Parameter
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled%209.png)
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled%2010.png)
        
        Loss function : CTCLoss
        
        main evaluation metric
        
        - WER (WordErrorRate) VS CER (Charactor Error Rate)
            
            using CER (For detect user pronunciation)
            
        - Performance : CER 0.254
        
        Determining minibatch Ordering using SortaGrad Approach for CTC Loss
        
        In the context of CTC (Connectionist Temporal Classification) loss, the loss and gradients tend to increase as the length of the speech frame sequence increases. This poses a challenge in maintaining balanced gradient updates when the lengths of speech sequences vary across mini-batches, even with a fixed learning rate. To address this issue, we propose a method for determining the ordering of mini-batches based on the length of the speech frame sequences. This ensures that the maximum length of speech sequences gradually increases within each mini-batch, promoting more balanced gradient propagation during training.
        
    2. Hyper Parameter Tuning
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled%2011.png)
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled%2012.png)
        
        ![Untitled](%E1%84%8E%E1%85%AC%E1%84%8C%E1%85%A9%E1%86%BC%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%E1%84%89%E1%85%A5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%80%E1%85%B5%E1%84%89%E1%85%AE%E1%86%AF%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%20%E1%84%8C%E1%85%A6%E1%84%8E%E1%85%AE%E1%86%AF%206af5bb5073f541a0b477573c0e42f2fe/Untitled%2013.png)
        
    3. Data Preprocessing Function
        - Base Function
            
            ****filenum_padding()****
            
            To Ensure that files in the Ksponspeech dataset from AI Hub can be accessed using only the file number, we take into consideration that the file names follow a numerical format. This allows for accessing the files based on the file number alone.
            
            input : file number
            
            output : File name in the specified format (str + str(filenum))
            
            ****get_path()****
            
            Plays a role in determining the path of the text file.
            
            input: Path, filename, filenum, format
            
            output: Text file path
            
        - Data Preprocessing
            
            ****bracket_filter()****
            
            In order to select only the pronunciation transcription among the transcription methods of the data, such as spelling transcription and pronunciation transcription.
            
            Input: Text containing candidate text based on transcription methods (e.g., strA/strB)
            
            Output: Text containing only the pronunciation transcription
            
            ****special_filter()****
            
            Filters out special characters and noise notations.
            
            input: Text containing <.>, <, >, #, %, etc.
            
            output: Filtered text
            
            ****sentence_filter()****
            
            Preprocessing function that includes both braket_filter() and special_filter.
            
        - Create Character Labels
            
            Create Character labels.
            
            Convert the data to numerical form so that it can be used for training.
            
            Check all the characters that appear in the dataset.
            
            Create 2,337 character labels - Only 2,040 characters are used for training.
            
        - Create Target Text
            
            ****sentence_to_target()****
            
            Convert Korean text to numerical labels.
            
            input: Korean text
            
            output: Numerical labels
            
            ****target_to_sentence()****
            
            Convert numerical labels to Korean text.
            
            input: Numerical labels
            
            output: Korean text
            

# Source Code / Build

1. **buildable source code**
    
    buildable source code - github [https://github.com/HYUSpeech/PitchAndPronounceTuner](https://github.com/HYUSpeech/PitchAndPronounceTuner)
    
2. **documentation for “how to build”**
    
    Setup environment for flask - install flask
    
    Download libraries used in project using ‘requirements.txt’ file in the project folder
    
    Before running project, we need answer label for pitch and pronunciation 
    
    First, prepare the answer label of pitch recognition data in ‘pitch_data’ folder. 
    
    And then for speech recognition write the answer label at [app.py](http://app.py) 147th line, origin text variable.
    
    After the answer label is prepared, we need to setup the information of the songs.
    
    Change the directory path of data and pitch. These path parameter is at setup phase of [app.py](http://app.py)
    
    Change the song name(song) and audio data file name(data_name) below the directory path in the setup phase.
    
    Run the project folder with local connection
    
3. **About training data**
    
    We’ve used the ‘한국어 음성’ data from AI hub.
    
    [https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=123](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=123)
    
    Actually this dataset was created by the kospeech team, the toolkit we used. They build this dataset for the purpose of training the communicative speech recognition AI technology. Kospeech supports the preprocessing rules for this dataset, and this helps to save time in preprocessing session.
