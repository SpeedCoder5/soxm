from pathlib import Path
import os
import shutil

class Paths:
    ''' Resolve project folder paths paths.
    '''
    def __init__():
        super().__init__()

    @staticmethod
    def project(key_root_filename = 'requirements.txt') -> Path:
        ''' returns root folder of project
        :return Path: root folder of project
        :raises OSError: if root folder of project not found 
        '''
        user_path = Path.cwd()
        
        while user_path != Path('/') and not (user_path / key_root_filename).is_file():
            user_path = user_path.parent
        
        if user_path == Path('/'):
            raise OSError(f"{Path.cwd()} has no project root folder found that contains {key_root_filename}")
        
        return Path(user_path).resolve()

    @staticmethod
    def data() -> Path:
        ''' returns path to data folder for project
        :return Path: data folder path for project
        :raises OSError: if root folder of project not found 
        '''
        root_dir = Paths.project()
        data_dir = root_dir / 'data/'
        return Path(data_dir).resolve()

if __name__ == '__main__':
    ### Test Paths.project() 
    # Create a temporary directory structure for testing.
    cur_dir = Path.cwd().resolve()
    print('working from ' + str(cur_dir))
    test_dir = Path("test_project")
    expected_result = test_dir.resolve()
    test_dir.mkdir(exist_ok=True)
    (test_dir / "requirements.txt").touch()

    try:
        # Change the current working directory to the temporary directory.
        os.chdir(test_dir)

        # Call the Paths.project function.
        result = Paths.project()

        # Check if the result is the expected project root directory.
        if result == expected_result:
            print("Paths.project() works as expected.")
        else:
            print("Paths.project() did not return the expected result.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Change back to the original working directory and clean up.
        os.chdir(cur_dir)
        if test_dir.exists():
            shutil.rmtree(test_dir)
