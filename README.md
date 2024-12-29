# Sea of Thieves Server Finder
This program requires [npcap](https://npcap.com/dist/npcap-1.80.exe) to work. During **npcap** installation, select **WinPCap compatibility mode**.
If you want to build it urself, I personally used [pyinstaller](https://pyinstaller.org/en/stable/). The version v4.0 and above uses [https://ip-api.com](https://ip-api.com) to get the [stamp](https://www.seaofthieves.com/community/forums/topic/155277/stamps-servers-regions-everything-i-have-figured-out) of the player.
This program does not read, modifies or interacts with the gamefiles in any way. Also does not inject or interact with the game's memory. It uses simple cmd commands and functions to listen, and displays the ip of incoming internet traffic of the game, and displays it's source ip and port.
Works in Insider too! 
