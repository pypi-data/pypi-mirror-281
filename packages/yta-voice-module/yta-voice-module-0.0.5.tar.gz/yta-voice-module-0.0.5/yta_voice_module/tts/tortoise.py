from tortoise import api

def narrate(text, output_filename):
    tts = api.TextToSpeech()
    tts.tts_to_file(text = text,
        file_path = output_filename,
        voice_dir = 'tortoise/voices/',
        speaker = 'lj',
        num_autoregressive_samples = 1,
        diffusion_iterations = 10)

    #reference_clips = [utils.audio.load_audio(p, 22050) for p in clips_paths]
    
    #pcm_audio = tts.tts(text)
    #pcm_audio = tts.tts_with_preset("your text here", voice_samples=reference_clips, preset='fast')
    
    #from tortoise.utils.audio import load_audio, load_voice