import pyaudio
import RPi.GPIO as GPIO
import time
from PIL import Image, ImageDraw, ImageFont
import st7735
# --- Hardware Configuration ---
BUTTON_PIN = 26 # I/O pin for TTP223 button

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    # Pull DOWN the pin, wait for the sensor to drive it HIGH
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# --- Audio Configuration ---
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 
RATE = 48000 # <-- Change this from 44100 to 48000

# --- ASCII Art ---
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
    # Initialize the 1.8" TFT SPI Display
    # Using the standard ST7735 library which defaults to SPI bus 0
    disp = st7735.ST7735(
        port=0,
        cs=0,  # <-- Changed from 27 to 0 (Maps to native CE0 / GPIO8)
        dc=17, 
        rst=4,  
        backlight=22,  
        width=128,
        height=160,
        rotation=90,
        spi_speed_hz=4000000
    )
    disp.begin()
    
    # Create blank image for drawing
    img = Image.new('RGB', (disp.width, disp.height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw the Apple ASCII art
    draw.text((10, 20), APPLE_ASCII, fill=(255, 255, 255))
    disp.display(img)
    print("Display initialized with Apple ASCII art.")

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    # The TTP223 drives the line HIGH when pressed.
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def main():
    print("Initializing Hello Pi System...")
    
    # 1. Setup Display
    setup_display()
    
    # 2. Setup Button
    setup_gpio()
    
    # 3. Setup Audio
    p = pyaudio.PyAudio()
    

    # Open Input Stream (I2S Mic)
    stream_in = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       input_device_index=1,  # <-- Set this to 1!
                       frames_per_buffer=CHUNK)
                       
    # Open Output Stream (Headphone Jack)
    stream_out = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)

    print("Audio routing started. Press the TTP223 button to mute.")
    
    try:
        while True:
            # Read chunk from microphone
            data = stream_in.read(CHUNK, exception_on_overflow=False)
            

            is_pressed = GPIO.input(BUTTON_PIN)
            
            if is_pressed:
                # Button is pressed -> MUTE
                print("Button Pressed! Muting audio...")
                silence = b'\x00' * len(data)
                stream_out.write(silence)
            else:
                # Button is NOT pressed -> Play Mic Audio
                stream_out.write(data)

    except KeyboardInterrupt:
        print("\nStopping Hello Pi...")
    
    finally:
        # Clean up resources
        stream_in.stop_stream()
        stream_in.close()
        stream_out.stop_stream()
        stream_out.close()
        p.terminate()
        GPIO.cleanup()
        print("System safely shut down.")

if __name__ == "__main__":
    main()