from networkHandler import network_handler
import pyglet



def clientResponse(command, net_handler, player):

    #print("speaker got " + command)
    if (command == "upload"):
        file = net_handler.receiveMessage(True)
        print("got file")
        src = pyglet.media.load(file)
        player.queue(src)
        print("everything is uploaded")
    if(command == "play"):
        player.play()
    if(command == "pause"):
        player.pause()
    if(command == "raiseVolume"):
        player.volume += 0.1
    if(command == "lowerVolume"):
        player.volume -= 0.1
    if(command == "lowerVolumeToZero"):
        player.volume = 0
    if(command == "raiseVolumeToHalf"):
        player.volume = 0.5



def serverResponse(handler, command, speakerSockets, specific_speaker):
    if(command == "upload"):
        print("server got upload")

        file = handler.receiveMessage(True)
        print(file)
        for candidate_as_speaker in speakerSockets:

            speakerHandler = network_handler(candidate_as_speaker)
            speakerHandler.sendMessage(command, True)
            speakerHandler.sendMessage(file, True)

    elif (command == "settings"):
        print("got settings")
        stringSpeakers = ""
        for i in range(len(speakerSockets)):
            stringSpeakers += (str(speakerSockets[i]) + "*")

        print(stringSpeakers)
        handler.sendMessage(stringSpeakers, True)
        print("sent speakers")

    else:
        if(specific_speaker != None):
            for i in speakerSockets:
                if (specific_speaker == str(i)):
                    speakerHandler = network_handler(i)
                    speakerHandler.sendMessage(command, True)

        else:
            for candidate_as_speaker in speakerSockets:
                speakerHandler = network_handler(candidate_as_speaker)
                speakerHandler.sendMessage(command, True)

