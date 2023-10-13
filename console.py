#!/usr/bin/python3
"""The console that contains the entry point of the command interpreter"""

import cmd
from datetime import datetime
import models
from models.amenity import Amenity
from models.base_models import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import shlex

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class HBNBCommand(cmd.Cmd):
    """Implement a custom prompt"""
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Implement (Ctrl+D) to exit the program"""
        return True

    def emptyline(self):
        """An empty line + ENTER shouldn’t execute anything"""
        return False

    def do_quit(self, args):
        """Implement quit command to exit the program"""
        return True

    def _key_value_parser(self, args):
        """Parses a list of strings into a dictionary"""
        NewDict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                val = kvp[1]
                if val[0] == val[-1] == '"':
                    val = shlex.split(val)[0].replace('_', ' ')
                else:
                    try:
                        val = int(val)
                    except:
                        try:
                            val = float(val)
                        except:
                            continue
                NewDict[key] = val
        return NewDict

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it and prints the ID"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            NewDict = self._key_value_parser(args[1:])
            new_instance = classes[args[0]](**NewDict)
        else:
            print("** class doesn't exist **")
            return False
        print(new_instance.id)
        new_instance.save()

        def do_show(self, arg):
            """Prints the string representation of an instance
            based on the class name and ID"""
            args = shlex.split(arg)
            if len(args) == 0:
                print("** class name missing **")
                return False
            if args[0] in classes:
                if len(args) > 1:
                    key = args[0] + "." + args[1]
                    if key in models.storage.all():
                        print(models.storage.all()[key])
                    else:
                        print("** no instance found **")
                else:
                    print("** instance id missing **")
            else:
                print("** class doesn't exist **")

