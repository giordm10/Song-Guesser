def CoversByArtist(artist_name, songTitle):
    print(artist_name)
    album_cover = "spotifyImage.png"
    if(artist_name == "Billy Joel"):
        if(songTitle == "Uptown Girl"):
            album_cover = "billyjoel3.jfif"
        elif(songTitle == "Vienna"):
            album_cover = "billyjoel1.jfif"
        elif(songTitle == "Piano Man"):
            album_cover = "billyjoel4.jfif"
        elif(songTitle == "We Didn't Start the Fire"):
            album_cover = "billyjoel5.jfif"
        elif(songTitle == "She's Always a Woman"):
            album_cover = "billyjoel1.jfif"
        elif(songTitle == "Just the Way You Are"):
            album_cover = "billyjoel1.jfif"
        elif(songTitle == "My Life"):
            album_cover = "billyjoel2.jfif"
        elif(songTitle == "It's Still Rock and Roll to Me"):
            album_cover = "billyjoel6.jfif"
        elif(songTitle == "Only the Good Die Young"):
            album_cover = "billyjoel1.jfif"
        elif(songTitle == "Movin' Out (Anthony's Song)"):
            album_cover = "billyjoel1.jfif"
        else:
            album_cover = "billyjoel1.jfif"

        if(artist_name == "Nothing But Thieves"):
            if(songTitle == "Amsterdam"):
                album_cover = "nbt1.jfif"
            elif(songTitle == "Soda"):
                album_cover = "nbt1.jfif"
            elif(songTitle == "Sorry"):
                album_cover = "nbt1.jfif"
            elif(songTitle == "Life's Coming in Slow - from GRAN TURISMO 7"):
                album_cover = "nbt2.jfif"
            elif(songTitle == "You Know Me Too Well"):
                album_cover = "nbt3.jfif"
            elif(songTitle == "Is Everybody Going Cazy?"):
                album_cover = "nbt4.jfif"
            elif(songTitle == "Impossible"):
                album_cover = "nbt4.jfif"
            elif(songTitle == "Particles"):
                album_cover = "nbt1.jfif"
            elif(songTitle == "Trip Switch"):
                album_cover = "nbt5.jfif"
            elif(songTitle == "I Was Just a Kid"):
                album_cover = "nbt1.jfif"
            else:
                album_cover = "nbt1.jfif"

    return album_cover