import os
class File_Service:
    @staticmethod
    def get_files(directory, search_name):
        matching_files = []
        for filename in os.listdir(directory):
            if filename.endswith(search_name):
                matching_files.append(os.path.join(directory, filename))

        print("Matching files:", matching_files)
        return matching_files