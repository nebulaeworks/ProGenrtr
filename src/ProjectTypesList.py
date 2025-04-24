import pprint, sys
from ConfigManager import ConfMgr as Config
from Config import DataStruct

class ProjectTypesList:
    """!
    handle the listing of project types defined in the application config
    """

    NO_LANG = DataStruct(ERROR = "No projects found for language")

    def run(self, args: dict):
        """!
        entry point to this command
        @param args the dictionary of command line arguments provided at the
               command line.
        """
        if args["--lang"] is None:
            print("Listing all known projects for all known languages")
            self.__print()
        else:
            self.__print(args["--lang"])

    def __print(self, lang: str = None):
        """!
        if a language is provided handle the printing of all the projects
        associated with that language. If no language is provided and this is
        called with default arguments, list all projects for every language
        that the application knows about.
        @param lang a string representing the language to be listed. defaults to
               None.
        """
        if lang is None:
            for language,entries in vars(Config().projects).items():
                print(f"- {language}")
                self.__printProjects(entries)
        else:
            try:
                self.__printProjects(Config().projects.get(lang))
            except AttributeError as e:
                sys.exit("ERROR: Language " + str(e))

    def __printProjects(self, language: DataStruct):
        """!
        print all the projects for a given language
        @param language a DataStruct made up of the projects that are
               applicable for a particular programming language.
        """
        for index, (project,source) in enumerate(vars(language).items()):
            print(f"   {index+1}. {project} ({source})")
