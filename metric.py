import math

class PitchMetric:
    def originer_note(lines):
        ori = []
        ori_note = []

        for line in lines:
            ori.append(list(line))

        for o in range(len(ori)):
            if ori[o] != len(ori)-1:
                if ori[o+1] == '#' or ori[o+1] == 'b':
                    ori_note.append(ori[o]+ori[o+1])
                else:
                    ori_note.append(ori[o])
            else:
                if ori[o] == '#' or ori[o] == 'b':
                    pass
                else:
                    ori_note.append(ori[o])

        return ori_note

    def pitch_metric_eval(ori_note, detect_note):

        score = 0.0
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        l = len(ori_note)

        for i in range(l):
            if ori_note[i] == detect_note[i]:
                score += 0.0
            else:
                if ori_note[i][0] == detect_note[i][0]:
                    score += 0.25
                else:
                    o_i = notes.index(ori_note[i])
                    d_i = notes.index(detect_note[i])

                    if abs(o_i-d_i) == 1:
                        if ori_note[i] == 'E' and d_i-o_i == 1:
                            score += 1.0
                        elif ori_note[i] == 'F' and d_i-o_i == -1:
                            score += 1.0
                        elif ori_note[i] == 'B' and d_i-o_i == 1:
                            score += 1.0
                        else:
                            score += 0.25

                    elif abs(o_i-d_i) == 2:
                        if ori_note[i] == 'D#' and d_i-o_i == 2:
                            score += 2.25
                        elif ori_note[i] == 'E' and d_i-o_i == 2:
                            score += 2.25
                        elif ori_note[i] == 'F' and d_i-o_i == -2:
                            score += 2.25
                        elif ori_note[i] == 'F#' and d_i-o_i == -2:
                            score += 2.25
                        else:
                            score += 1.0

                    elif abs(o_i-d_i) == 3:
                        if ori_note[i] == 'D' and d_i-o_i == 3:
                            score += 4.0
                        elif ori_note[i] == 'D#' and d_i-o_i == 3:
                            score += 4.0
                        elif ori_note[i] == 'E' and d_i-o_i == 3:
                            score += 4.0
                        elif ori_note[i] == 'F' and d_i-o_i == -3:
                            score += 4.0
                        elif ori_note[i] == 'F#' and d_i-o_i == -3:
                            score += 4.0
                        elif ori_note[i] == 'G' and d_i-o_i == -3:
                            score += 4.0
                        else:
                            score += 2.25

                    elif abs(o_i-d_i) == 4:
                        if ori_note[i] == 'C#' and d_i-o_i == 4:
                            score += 6.25
                        elif ori_note[i] == 'D' and d_i-o_i == 4:
                            score += 6.25
                        elif ori_note[i] == 'D#' and d_i-o_i == 4:
                            score += 6.25
                        elif ori_note[i] == 'E' and d_i-o_i == 4:
                            score += 6.25
                        elif ori_note[i] == 'F' and d_i-o_i == -4:
                            score += 6.25
                        elif ori_note[i] == 'F#' and d_i-o_i == -4:
                            score += 6.25
                        elif ori_note[i] == 'G' and d_i-o_i == -4:
                            score += 6.25
                        elif ori_note[i] == 'G#' and d_i-o_i == -4:
                            score += 6.25
                        else:
                            score += 4.0

                    elif abs(o_i-d_i) == 5:
                        if ori_note[i] == 'B' and d_i-o_i == -5:
                            score += 6.25
                        elif ori_note[i] == 'Bb' and d_i-o_i == -5:
                            score += 6.25
                        elif ori_note[i] == 'F' and d_i-o_i == 5:
                            score += 6.25
                        elif ori_note[i] == 'F#' and d_i-o_i == 5:
                            score += 6.25
                        else:
                            score += 9.0

                    elif abs(o_i-d_i) == 6:
                        score += 12.25

                    elif abs(o_i-d_i) == 7:
                        score += 16.0

                    elif abs(o_i-d_i) == 8:
                        score += 20.25

                    elif abs(o_i-d_i) == 9:
                        score += 25.0

                    elif abs(o_i-d_i) == 10:
                        score += 30.25

                    elif abs(o_i-d_i) == 11:
                        score += 1.0

        pitch_score = (math.sqrt(score)/l)

        return "%.2f"%pitch_score
    
class PronounMetric:
    def pronoun_metric_eval(origin_txt, pronoun_text):
        pronoun_score = 0
        for i in range(len(origin_txt)):
            if origin_txt[i] == pronoun_text[i]:
                pronoun_score += 1
            else:
                pronoun_score += 0

        return "%.2f"%((pronoun_score/len(origin_txt))*100)