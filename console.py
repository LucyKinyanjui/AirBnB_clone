#!/usr/bin/python3
"""The console that contains the entry point of the command interpreter"""

import cmd
from datetime import datetime
import models
from models.amenity import Amenity
from models.base_model import BaseModel
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
    prompt = "(hbnb) "

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
                    except ValueError:
                        try:
                            val = float(val)
                        except ValueError:
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

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and ID"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints all string representation of all instances based
        or not on the class name"""
        args = shlex.split(arg)
        instance_list = []
        if len(args) == 0:
            instance_dict = models.storage.all()
        elif args[0] in classes:
            instance_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in instance_dict:
            instance_dict.append(str(instance_dict[key]))
        print("[", end="")
        print(", ".join(instance_list), end="")
        print("]")

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding
        or updating attribute"""
        args = shlex.split(arg)
        int_attributes = ["number_rooms", "number_bathrooms",
                          "max_guest", "price_by_night"]
        float_attributes = ["latitude", "longitude"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                all_instances = storage.all()
                if key in all_instances:
                    if len(args) > 2:
                        if len(args) > 3:
                            if args[0] == "Place":
                                if args[2] in int_attributes:
                                    try:
                                        args[3] = int(args[3])
                                    except ValueError:
                                        args[3] = 0
                                elif args[2] in float_attributes:
                                    try:
                                        args[3] = float(args[3])
                                    except ValueError:
                                        args[3] = 0.0
                            setattr(all_instances[key], args[2],
                                    args[3])
                            all_instances[key].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
