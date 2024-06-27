from setuptools import setup, find_packages

setup(
    name='Bilingual-conversational-bot',  
    version='0.1',
    author='Palash Dandge',
    # author_email='palashdandge9@gmail.com',
    description='A Real-Time Live Bilingual Conversation bot for English to Spanish and Spanish to English using Streamlit',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/bilingual-bot',  
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'googletrans==4.0.0-rc1',
        'SpeechRecognition',
        'gtts',
        'pydub',
        'pyaudio',
    ],
    entry_points={
        'console_scripts': [
            'bilingual-bot=bilingual_bot.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
