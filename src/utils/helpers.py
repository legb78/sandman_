import os
import glob
import logging
from datetime import datetime, timedelta

def load_audio_file(file_path):
    # Function to load an audio file
    pass

def save_text_to_file(text, file_path):
    # Function to save text to a file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

def generate_image_from_text(text):
    # Function to generate an image from text
    pass

def clean_up_temp_files(directory=None, pattern='temp_*', max_age_hours=24):
    """
    Clean up temporary files in a directory based on pattern and age
    
    Args:
        directory (str): Directory to clean up. If None, uses the current directory.
        pattern (str): File pattern to match for deletion (glob syntax)
        max_age_hours (int): Maximum age of files to keep in hours
        
    Returns:
        tuple: (number of files deleted, total bytes freed)
    """
    try:
        if directory is None:
            directory = os.getcwd()
        
        # Calculate cutoff time
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        # Find files matching pattern
        files_to_check = glob.glob(os.path.join(directory, pattern))
        
        deleted_count = 0
        freed_bytes = 0
        
        for file_path in files_to_check:
            try:
                # Get file stats
                file_stats = os.stat(file_path)
                last_modified = datetime.fromtimestamp(file_stats.st_mtime)
                
                # Check if file is older than cutoff
                if last_modified < cutoff_time:
                    file_size = file_stats.st_size
                    os.remove(file_path)
                    deleted_count += 1
                    freed_bytes += file_size
                    logging.info(f"Deleted temporary file: {file_path}")
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {str(e)}")
        
        return deleted_count, freed_bytes
    except Exception as e:
        logging.error(f"Error cleaning up temporary files: {str(e)}")
        return 0, 0

def clean_temp_images(directory=None, max_age_hours=24):
    """
    Clean up temporary image files (png, jpg, jpeg)
    
    Args:
        directory (str): Directory to clean up. If None, uses the current directory.
        max_age_hours (int): Maximum age of files to keep in hours
        
    Returns:
        tuple: (number of files deleted, total bytes freed)
    """
    if directory is None:
        directory = os.getcwd()
    
    total_deleted = 0
    total_freed = 0
    
    # Clean up different image formats
    for pattern in ['temp_*.png', 'temp_*.jpg', 'temp_*.jpeg', 'temp_*.gif']:
        deleted, freed = clean_up_temp_files(directory, pattern, max_age_hours)
        total_deleted += deleted
        total_freed += freed
    
    return total_deleted, total_freed