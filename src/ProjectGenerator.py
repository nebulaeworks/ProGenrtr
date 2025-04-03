from ConfigManager import ConfMgr as Conf
import sys, os, shutil
from git import Repo

class ProjectGenerator:
    """!
    This class handles the process of creating new projects by:
        - Cloning a template repository to a specified directory
        - Removing the original repository information
        - Re-initializing it as a fresh Git repository
    """

    def run(self, args: dict):
        """!
        Processes command line arguments to generate a new project based on
        specified language and project type templates.
        
        @param args Dictionary containing command line arguments
                    Expected keys:
                    - <LANGUAGE>: Programming language of the template
                    - <PROJECT_TYPE>: Type of project to generate
                    - <PROJECT_PATH>: Target directory for the new project
        """
        langArg = args["<LANGUAGE>"]
        projectArg = args["<PROJECT_TYPE>"]
        path = args["<PROJECT_PATH>"]
        project = Conf().projects.get(langArg).get(projectArg)

        self.__cloneRepo(project, path)
        self.__cleanProject(path)
        self.__reinitialiseProject(path)

    def __cloneRepo(self, project: str, path: str):
        """!
        Clones the template repository to the target path
        
        @param project string URL or path of the template repository to clone
        @param path string target directory where the repository will be cloned
        
        @exception Exits the program if cloning fails
        """
        try:
            Repo.clone_from(project, path)
        except Exception as e:
            print("ERROR: could not clone project repo...")
            sys.exit(e)

    def __cleanProject(self, path: str):
        """!
        Removes all Git-related files and directories from the cloned project
        
        This ensures the generated project doesn't contain any Git history
        or configuration from the template repository.
        
        @param path string representing path to the project directory to clean
        """
        git_path = os.path.join(path, ".git")
        
        # Remove the .git directory
#        if os.path.exists(git_path):
        if os.path.exists(os.path.join(path, ".git")):
            shutil.rmtree(git_path)
            print(f"Removed: {git_path}")

        # Remove other Git-related files
        git_files = [".gitignore", ".gitattributes", ".gitmodules"]
        for file in git_files:
            file_path = os.path.join(path, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Removed: {file_path}")
        print("project templated cleaned")

    def __reinitialiseProject(self, path: str):
        """!
        Initialize a fresh Git repository in the project directory
        
        Creates a new Git repository with an initial empty commit to mark
        the beginning of the project history.
        
        @param path string representing the path to the project directory to
                    initialize
        
        @note The repository is initialized with a 'master' branch and an empty commit
              with the message "#===>[BEGIN]<===#"
        """
        repo = Repo.init(path)
        print("Project Initialised")
        # Ensure HEAD is on 'master' (Git 2.28+ uses 'main' by default)
        if repo.head.is_detached or "master" not in repo.heads:
            repo.git.checkout("-b", "master")

        # Make an empty commit
        repo.git.commit("--allow-empty", "-m", "#===>[BEGIN]<===#")
