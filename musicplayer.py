#CREDIT TO Stephen Harding AKA originalsteve51
#https://github.com/originalsteve51

"""
This module contains a reusable MusicPlayer class that is based
on an audio player application named mpg123.
"""

import subprocess
import time
from threading import Thread

#-------------------------------------------------------------------
# AudioEngineUnavailableError class
#-------------------------------------------------------------------
class AudioEngineUnavailableError(Exception):
    """
    When the required player application (mpg123) is not available
    this Exception is raised.
    """
    pass 

#-------------------------------------------------------------------
# NoPlaybackError class
#-------------------------------------------------------------------
class NoPlaybackError(Exception):
    """
    When an attempt is made to control playback but nothing is
    being played, this Exception is raised.
    """
    pass 


#-------------------------------------------------------------------
# PlaybackInProgressError class
#-------------------------------------------------------------------
class PlaybackInProgressError(Exception):
    """
    When an attempt is made to begin playback while something
    is already playing, this Exception is raised.
    """
    pass 

#-------------------------------------------------------------------
# MusicPlayer class
#-------------------------------------------------------------------
class MusicPlayer():
    """
    Start a subprocess running audio player mpg123 to play a specified
    mp3 file. Provide controls to stop/start and quit playback.
    """
    def __init__(self):
        self._audioengine = 'mpg123' # Only supported player is mpg123
        self._p = None
        self._is_paused = False

        # The following instance variables are affected by the process_monitor
        # thread. 
        self._process_running = False
        self._return_code = None


    def play(self, sound_file):
        if not self._process_running:
            try:
                # Open a subprocess that runs mpg123 to play an mp3 file
                self._p = subprocess.Popen([self._audioengine, 
                                      '-C',     # Enable commands to be read from stdin
                                      '-q',     # Be quiet
                                      sound_file],
                                      stdin=subprocess.PIPE, # Pipe input via bytes
                                      stdout=None,   
                                      stderr=None)

                # Since we are using stdin for commands, we have to send something
                # to keep mpg123 from complaining when we exit. The complaint is
                # not a serious one, but it is annoying. If stdin is not used the
                # terminal is posted with "Can't set terminal attributes" at exit.
                # I send an empty string below to keep mpg123 happy.
                self._p.stdin.write(b'')
                self._p.stdin.flush()

                # start a monitor thread that sets instance variables with the
                # status of the subprocess. 
                monitor_thread = Thread(target=self.process_monitor,args=()) 
                monitor_thread.start()

            except FileNotFoundError as e:
                raise AudioEngineUnavailableError(f'AudioEngineUnavailableError: {e}')
        else:
            raise PlaybackInProgressError('You cannot play while something else is already playing.')

    def quit_playing(self):
        if self._process_running:
            self._p.terminate()

            # Wait for process to end
            while self._process_running:
                time.sleep(0.1)
        else:
            raise NoPlaybackError('Cannot quit playback because nothing is playing.')



    def pause(self):
        if self._process_running:
            if self._is_paused:
                # Already paused, do nothing
                pass
            else:
                self._p.stdin.write(b's')
                self._p.stdin.flush()
                self._is_paused = True
        else:
            raise NoPlaybackError('Cannot pause playback because nothing is playing.')
                    

    def resume(self):
        if self._process_running:
            if not self._is_paused:
                # Already playing, do nothing
                pass
            else:
                self._p.stdin.write(b's')
                self._p.stdin.flush()
                self._is_paused = False
        else:
            raise NoPlaybackError('Cannot resume playback because nothing is playing.')

    def is_playing(self):
        return self._process_running

    def return_code(self):
        return self._return_code

    def process_monitor(self):
        """
        This code runs in its own thread to monitor the state of our
        external subprocess. Instance variables _process_running and
        _return_code are used to show the process status.
        """
        # Indicate that the process is running at the start, it
        # should be
        self._process_running = True

        # When a process exits, p.poll() returns the code it set upon
        # completion
        self._return_code = self._p.poll()

        # See whether the process has already exited. This will cause a
        # value (i.e. not None) to return from p.poll()
        if self._return_code == None:
            # Wait for the process to complete, get its return code directly
            # from the wait() call (i.e. do not use p.poll())
            self._return_code = self._p.wait()

        # When we get here, the process has exited and set a return code
        self._process_running = False
