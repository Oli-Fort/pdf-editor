TEXT_FILE_EXTENSIONS = ('.txt', '.md', '.csv', '.json', '.xml', '.yaml', '.yml', '.py', '.html', '.js', '.css',
                        '.ts', '.jsx', '.tsx', '.php', '.java', '.c', '.cpp', '.h', '.hpp', '.go', '.rb', '.rs',
                        '.swift', '.kt', '.dart', '.lua', '.sh', '.bash', '.zsh', '.pl', '.perl', '.r', '.sql',)

IMAGE_FILE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico')

def is_text_file(extension):
        return extension in TEXT_FILE_EXTENSIONS
    
def is_image_file(extension):
    return extension in IMAGE_FILE_EXTENSIONS