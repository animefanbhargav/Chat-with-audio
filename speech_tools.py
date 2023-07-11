from constants import FileType,Language

import streamlit as st

from audio_processing import AudioProcessor,format_time


audio_processor = AudioProcessor()





class Transcriber:
    '''
        Transcribes speech to text , either using the GoogleSpeechRecognitionAPI or Whisper API
    '''
    def __init__(self,container,type='free'):
        self.type = type
        self.container = container
        self.got_input = False
        self.processing = False

    @st.cache_data(hash_funcs={st.delta_generator.DeltaGenerator: lambda x: None},show_spinner='Transcribing Audio...')
    def get_generator(_self,data,file_name,input_type,language):
        audio = audio_processor.convert_audio(data,file_name,input_type)
        text_generator = audio_processor.transcribe_free(audio,language)
        return tuple(text_generator)

        
    
    def transcribe_free(_self,data,file_name,input_type=FileType.FILE,language=Language.USENGLISH):
        '''
        Displays the Transcribed text using GoogleSpeechRecognitionAPI , results may be inaccurate.

        Args:
            data(streamlit.runtime.uploaded_file_manager.UploadedFile or bytes): The audio data from the uploaded file or recorded bytes
            file_name(str): The audio file path (is one of 'audio.wav','audio.mp3','audio.ogg')
            input_type(FileType,optional): Whether the audio is from a file or from the microphone. Deafaults to File Input.
            language(Language,optional): The language the transcribed text should be in. Defaults to US English.
        '''
        _self.loading_text = _self.container.empty()
        _self.full_text = ""
        try:
            with _self.loading_text.container():
                st.markdown(f':blue[Speech Processing In Progress...Please Wait...]')
                    
            _self.got_input  = True
            _self.processing = True
            
            _self.container.markdown(f':blue[Transcribed Text:]')
            text_generator = _self.get_generator(data,file_name,input_type,language)
            with open('text.txt','w') as f:
                for result in text_generator:
                    _self.loading_text.empty()
                    with _self.loading_text.container():
                        chunk = format_time(result["start_time"]) + ' to ' + format_time(result["end_time"])
                        st.markdown(f':blue[Processing {chunk}]')

                    text = result['text']
                    if text:
                        _self.container.markdown(f':green[**{text}**]')
                        _self.full_text+=text
                        f.write(text)
                    else:
                        _self.container.markdown(f':red[**Could not transcribe audio from {chunk}**]')
            
        except ValueError as e:
            _self.container.markdown(f':red[{e}]')
        except ConnectionError as e:
            _self.container.markdown(f':red[{e}]')
        finally:
            _self.loading_text.empty()
            _self.processing = False








