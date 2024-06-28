import os

# This test file will create some audio files during the process
TEST_FOLDER = os.getcwd().replace('\\', '/') + '/yta_voice_module/test/'
TEST_TEXT = text = 'Esto es un test con el que quiero que se genere un audio narrado'

def test_coqui_tts():
    from yta_voice_module.tts.coqui import narrate
    
    narrate(TEST_TEXT, output_filename = TEST_FOLDER + 'test_coqui_tts.wav')

def test_google_tts():
    from yta_voice_module.tts.google import narrate

    narrate(TEST_TEXT, output_filename = TEST_FOLDER + 'test_google_tts.wav')

def test_microsoft_tts():
    from yta_voice_module.tts.microsoft import narrate

    narrate(TEST_TEXT, output_filename = TEST_FOLDER + 'test_microsoft_tts.wav')

def test_open_voice_tts():
    from yta_voice_module.tts.open_voice import narrate

    narrate(TEST_TEXT, output_filename = TEST_FOLDER + 'test_open_voice_tts.wav')

def test_imitate_open_voice_tts():
    from yta_voice_module.tts.open_voice import imitate_voice

    # This audio was extracted from the first 2:03 minutes of https://www.youtube.com/watch?v=ZD2h5-qAXww
    # video, that belongs to Irene Albacete's Youtube Channel (awesome voice)
    imitate_voice(TEST_TEXT, TEST_FOLDER + 'resources/narracion_irene_albacete_recortado.mp3', output_filename = TEST_FOLDER + 'test_imitate_open_voice_tts.wav')

def tests():
    import os, glob

    print('Executing all tests')

    # test_coqui_tts()
    # test_google_tts()
    # test_microsoft_tts()
    # test_open_voice_tts()
    test_imitate_open_voice_tts()

    print('Tests executed')
    
    # Set this to False to preserve test files to be able to manually check them
    do_remove = False
    if do_remove:
        for filename in glob.glob(TEST_FOLDER + '*.wav'):
            os.remove(filename)

tests()