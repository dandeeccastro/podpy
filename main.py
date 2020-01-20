from pod import Main

file_name = input("Please name the filename you want the final audio to have (enter for podcast.mp3): ")
if file_name:
    print("You chose " + file_name)
else:
    file_name = None

folder_path = input("Please insert the folder that contains the needed files (enter for current directory): ")
if folder_path:
    folder_path = "./" + folder_path
else:
    folder_path = None
Main(path=folder_path,final_filename=file_name).main()