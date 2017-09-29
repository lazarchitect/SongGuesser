# SongGuesser
Name-That-Tune style trivia game written in Python's Pygame. My first foray into the module. 
Uses Billboard API to determine popular songs, and Spotify API to download freee 30-second snippets and artist data.

The game goes through three rounds, with each one getting progressively harder. 
In the beginning, you can hear the audio, see the artist's name, and see a picture of them.
In round two, you only have a picture and audio.
By the third round, you only have audio cues to work with.

Pygame has no built-in button library, so the buttons are just Pygame Rectangles with text overlayed on them.
In a third layer, matching Rectangles are set to certain actions on click, depending on if the Button represents the correct answer.

The Audio uses Spotify's unlimited free tier to access 30 second audio samples for the songs.
A premium tier exists to access full songs, but thankfully, the game doesn't require the full song.
In fact, the sample is superior, as it usually starts and ends at key points in the song.

All the graphics are just saved to variables and overwritten on the fly.
Pygame works by "blitting" new graphics to the screen, so its a simple matter to completely erase the screen and write in new values.
This is surprisingly fast and efficient.

The clock animation was a fun challenge: it made by overwriting certain arcs of the circular image using a built-in arc method.
