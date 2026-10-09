import os
import zipfile

def zip_project(output_filename, source_dir):
    exclusions = ['venv', '__pycache__', '.env', '.git', 'node_modules', output_filename]
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Exclude directories
            dirs[:] = [d for d in dirs if d not in exclusions]
            
            for file in files:
                if file in exclusions or file.endswith('.pyc'):
                    continue
                    
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)

zip_project('TrustDoc-AI-Final.zip', '.')
print('Zipped successfully')
