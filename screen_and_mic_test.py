import pyaudio
from PIL import Image, ImageDraw
import st7735

# Setari Audio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 
RATE = 48000
MIC_INDEX = 1

APPLE_ASCII = """
   .:'
__ :'__
.'`__`-'__``.
:__________.-'
:_________:
 :_________`-;
  `.__.-.__.'
"""

def setup_display():
    disp = st7735.ST7735(
        port=0, cs=0, dc=17, rst=4, backlight=22, 
        width=128, height=160, rotation=90, spi_speed_hz=4000000
    )
    disp.begin()
    
    img = Image.new('RGB', (disp.width, disp.height), color=(0, 0, 0))
    ImageDraw.Draw(img).text((10, 20), APPLE_ASCII, fill=(255, 255, 255))
    disp.display(img)
    print("Display initializat.")

def main():
    print("Initializare Hello Pi...")
    setup_display()
    
    p = pyaudio.PyAudio()
    
    stream_in = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                       input=True, input_device_index=MIC_INDEX, frames_per_buffer=CHUNK)
                       
    stream_out = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                        output=True, frames_per_buffer=CHUNK)

    print("Audio pornit. Microfonul transmite direct in casti.")
    
    try:
        # Bucla infinita ultra-rapida doar pentru transfer audio
        while True:
            data = stream_in.read(CHUNK, exception_on_overflow=False)
            stream_out.write(data)

    except KeyboardInterrupt:
        print("\nOprire Hello Pi...")
        
    finally:
        stream_in.stop_stream()
        stream_in.close()
        stream_out.stop_stream()
        stream_out.close()
        p.terminate()
        print("Sistem oprit in siguranta.")

if __name__ == "__main__":
    main()