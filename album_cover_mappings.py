def CoversByArtist(artist_name, songTitle):
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

        if(artist_name == ""):
            if(songTitle == ""):
                album_cover = ""
            elif(songTitle == ""):
                album_cover = ""
            elif(songTitle == ""):
                album_cover = ""
            elif(songTitle == ""):
                album_cover = ""
            elif(songTitle == ""):
                album_cover = ""
            elif(songTitle == ""):
                album_cover = ""
            elif(songTitle == ""):
                album_cover = ""
            elif(songTitle == ""):
                album_cover = ""
            elif(songTitle == ""):
                album_cover = ""
            elif(songTitle == ""):
                album_cover = ""
            else:
                album_cover = ""

    return album_cover