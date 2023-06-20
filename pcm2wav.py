import os
import struct
from pathlib import Path

class Pcm2Wav:
    def make_wav_format(pcm_data:bytes, ch:int) -> bytes:
        """ 
        pcm_data를 통해서 wav 헤더를 만들고 wav 형식으로 저장한다.
        :param pcm_data: pcm bytes
        :param ch: 채널 수
        :return wav: wave bytes
        """
        waves = []
        waves.append(struct.pack('<4s', b'RIFF'))
        waves.append(struct.pack('I', 1))  
        waves.append(struct.pack('4s', b'WAVE'))
        waves.append(struct.pack('4s', b'fmt '))
        waves.append(struct.pack('I', 16))
        # audio_format, channel_cnt, sample_rate, bytes_rate(sr*blockalign:초당 바이츠수), block_align, bps
        if ch == 2:
            waves.append(struct.pack('HHIIHH', 1, 2, 16000, 64000, 4, 16))  
        else:
            waves.append(struct.pack('HHIIHH', 1, 1, 16000, 32000, 2, 16))
        waves.append(struct.pack('<4s', b'data'))
        waves.append(struct.pack('I', len(pcm_data)))
        waves.append(pcm_data)
        waves[1] = struct.pack('I', sum(len(w) for w in waves[2:]))
        return b''.join(waves)