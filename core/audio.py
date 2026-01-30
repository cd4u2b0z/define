"""
Audio playback for pronunciations.
"""

import subprocess
import tempfile
import urllib.request
from typing import Optional


class AudioPlayer:
    """Cross-platform audio playback for pronunciations."""
    
    def __init__(self):
        self.player = self._detect_player()
    
    def _detect_player(self) -> Optional[str]:
        """Detect available audio player."""
        players = ["mpv", "ffplay", "cvlc", "afplay", "paplay"]
        
        for player in players:
            try:
                subprocess.run(
                    ["which", player],
                    capture_output=True,
                    check=True
                )
                return player
            except subprocess.CalledProcessError:
                continue
        
        return None
    
    def play(self, url: str) -> bool:
        """
        Play audio from URL.
        
        Args:
            url: URL to audio file
            
        Returns:
            True if playback succeeded
        """
        if not self.player:
            print("No audio player found. Install mpv, ffplay, or vlc.")
            print(f"Audio URL: {url}")
            return False
        
        try:
            if self.player == "mpv":
                subprocess.Popen(
                    ["mpv", "--no-video", "--really-quiet", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            elif self.player == "ffplay":
                subprocess.Popen(
                    ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            elif self.player == "cvlc":
                subprocess.Popen(
                    ["cvlc", "--play-and-exit", "--quiet", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            elif self.player in ("afplay", "paplay"):
                # These need a local file
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                    temp_path = f.name
                    urllib.request.urlretrieve(url, temp_path)
                    subprocess.Popen(
                        [self.player, temp_path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
            
            return True
            
        except Exception as e:
            print(f"Audio playback failed: {e}")
            return False
